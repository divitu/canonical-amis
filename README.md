Canonical AMIs
==============

Find AWS EC2 AMIs for Canonical Ubuntu images.

Overview
--------

    import canonical_amis
    amis = canonical_amis.get_amis()

`get_amis()` returns a List of Dictionaries describing production-ready Ubuntu
AMIs provided by Canonical.

    $ canonical-amis

`canonical-amis` produces a JSON file containing the information from
`get_amis()`.  This command will get all the image information in parallel:

    $ for r in ap-northeast-1 ap-southeast-1 eu-central-1 eu-west-1 sa-east-1 \
    > us-east-1 us-west-1 ap-southeast-2 us-west-2 ; do canonical-amis $r &
    > done ; wait

Install
-------

    pip install --pre canonical-amis
