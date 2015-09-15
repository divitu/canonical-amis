Canonical AMIs
==============

Find AWS EC2 AMIs for Canonical Ubuntu images.  The code in this repository powers [this AMI database](http://edge.divitu.com/canonical-amis.json).

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

Usage
-----

We recommend using the `canonical-amis` CLI to cache the current set of
available AMIs.  Then [jq](https://stedolan.github.io/jq/) can be used to query
that information and provide AMI IDs for your current needs.  E.g.:

    $ jq -r '
    >     .images[] |
    >     select(
    >         .architecture == "x86_64" and
    >         .ubuntu.version == "12.04" and
    >         .ebs == "standard" and
    >         .hvm == false and
    >         .region == "us-east-1"
    >     ) |
    >     .id
    > ' canonical-amis.json
    ami-ef6cdc84

You can also use the cached copy on our CDN:

    $ curl -sS edge.divitu.com/canonical-amis.json |
    > jq -r '
    >     .images[] |
    >     select(
    >         .architecture == "x86_64" and
    >         .ubuntu.version == "12.04" and
    >         .ebs == "standard" and
    >         .hvm == false and
    >         .region == "us-east-1"
    >     ) |
    >     .id
    > '
    ami-ef6cdc84
