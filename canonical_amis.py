"""
Find AWS EC2 AMIs for Canonical Ubuntu images
"""

import json
import sys

import boto.ec2

UBUNTU_OWNER = '099720109477'

ALL_REGIONS = [region.name for region in boto.ec2.regions()]

DEFAULT_FILE_TEMPLATE = "canonical-amis_{}.json"
DEFAULT_MULTI_REGION_FILE = "canonical-amis.json"
DEFAULT_FILE_MESSAGE = DEFAULT_FILE_TEMPLATE.format('REGION')

def main(regions=None, output=None, owner=None):
    if regions is None:
        regions = [None]
    if output is None:
        output = sys.stdout
    images = []
    for region in regions:
        images += get_amis(region, owner)
    json_images = json.dumps(images, ensure_ascii=False, sort_keys=True,
                             indent=4, separators=(',', ': ')) + "\n"
    try:
        output.write(json_images)
    except IOError:
        pass

def get_amis(region=None, owner=None):
    if owner is None:
        owner = UBUNTU_OWNER
    if region is None:
        region = 'us-east-1'
    conn = boto.ec2.connect_to_region(region)
    images = conn.get_all_images(owners=[owner],
                                 filters={'state': 'available'})
    filtered_images = {}
    for image in images:
        if (image.state == 'available' and
            image.id.startswith('ami-') and
            image.name and
            image.name.startswith('ubuntu/images/')):
                image.name_parts, key = process_name(image.name, region)
                replace_if_newer(filtered_images, key, image)
    return [adjust_ami(image) for image in filtered_images.values()]

def process_name(name, region):
    path_parts = name.split('/')
    sections = path_parts[-1].split('-')
    path_parts = path_parts[2:-1]

    key = region + "/"
    key += "/".join(path_parts)
    key += "-".join(sections[:-1])

    return path_parts + sections, key


def replace_if_newer(d, key, item):
    if key not in d or d[key].creationDate <= item.creationDate:
        d[key] = item

def adjust_ami(image):
    image = image.__dict__.copy()
    del image['connection']
    image['region'] = image['region'].name

    devices = {}
    for path, device in image['block_device_mapping'].items():
        devices[path] = device.__dict__.copy()
        devices[path]['connection'] = devices[path]['connection'].keys()
    image['block_device_mapping'] = devices

    type = ''
    if image['name_parts'][0] != 'ubuntu':
        type = image['name_parts'].pop(0)
    if type.startswith('hvm'):
        hvm = True
        ebs = 'standard'
        type = type[4:]
    else:
        hvm = False
        ebs = None
    if type.startswith('ebs'):
        ebs = 'standard'
        type = type[4:]
    if type == 'instance':
        ebs = None
    elif type == 'ssd':
        ebs = 'gp2'
    elif type:
        ebs = type

    image['hvm'] = hvm
    image['ebs'] = ebs
    image['ubuntu'] = {
        'name': image['name_parts'][1],
        'version': image['name_parts'][2],
        'release': image['name_parts'][5],
    }

    del image['name_parts']
    return image

def parse_args(args=None):
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    regions_group = parser.add_mutually_exclusive_group()
    regions_group.add_argument("region", choices=sorted(ALL_REGIONS), nargs='?',
                               help="The region that should be queried for AMIs")
    regions_group.add_argument("--all", action='store_true',
                               help="Query all regions")
    regions_group.add_argument("-m", "--most", action='store_true',
                               help="Query all regions except cn-* and us-gov-*")
    parser.add_argument("-o", "--output", type=argparse.FileType('w'), nargs=1,
                        help="The file to output to (defaults to {}; use - for stdout)".format(DEFAULT_FILE_MESSAGE))
    parser.add_argument("--owner", default=UBUNTU_OWNER,
                        help=argparse.SUPPRESS)
    args = parser.parse_args(args)
    if args.region:
        regions = [args.region]
    elif args.all:
        regions = sorted(ALL_REGIONS)
    elif args.most:
        regions = sorted(set(ALL_REGIONS) - set(['us-gov-west-1', 'cn-north-1']))
    else:
        regions = ['us-east-1']
    setattr(args, 'regions', regions)
    for attr in 'region', 'all', 'most':
        delattr(args, attr)
    if args.output is None:
        if len(args.regions) > 1:
            args.output = argparse.FileType('w')(DEFAULT_MULTI_REGION_FILE)
        else:
            args.output = argparse.FileType('w')(DEFAULT_FILE_TEMPLATE.format(args.regions[0]))
    return args

if __name__ == '__main__':
    args = parse_args()
    main(**args.__dict__)
