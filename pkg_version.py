def get_version():
    VERSION = (     # SEMANTIC
        0,          # major
        1,          # minor
        1,          # patch
        'beta.1',   # pre-release
        None        # build metadata
    )

    version = "%i.%i.%i" % (VERSION[0], VERSION[1], VERSION[2])
    if VERSION[3]:
        version += "-%s" % VERSION[3]
    if VERSION[4]:
        version += "+%s" % VERSION[4]
    return version
