"""
Find AWS EC2 AMIs for Canonical Ubuntu images
"""

import json
import sys

import boto.ec2

from pkg_version import get_version

UBUNTU_OWNER = '099720109477'

ALL_REGIONS = [region.name for region in boto.ec2.regions()]

DEFAULT_FILE_TEMPLATE = "canonical-amis_{}.json"
DEFAULT_FILE_MESSAGE = DEFAULT_FILE_TEMPLATE.format('REGION')

def main(region=None, output=None, owner=None):
    if output is None:
        output = sys.stdout
    images = json.dumps(get_amis(region, owner), ensure_ascii=False,
                        sort_keys=True, indent=4, separators=(',', ': '))
    try:
        output.write(images + "\n")
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
    parser.add_argument("region", choices=sorted(ALL_REGIONS), nargs='?',
                        default='us-east-1',
                        help="The region that should be queried for AMIs")
    parser.add_argument("output", type=argparse.FileType('w'), nargs='?',
                        help="The file to output to (defaults to {}; use - for stdout)".format(DEFAULT_FILE_MESSAGE))
    parser.add_argument("-o", "--owner", default=UBUNTU_OWNER,
                        help=argparse.SUPPRESS)
    args = parser.parse_args(args)
    if args.output is None:
        args.output = argparse.FileType('w')(DEFAULT_FILE_TEMPLATE.format(args.region))
    return args

if __name__ == '__main__':
    args = parse_args()
    main(**args.__dict__)
