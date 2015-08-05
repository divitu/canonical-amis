canonical-amis
==============

Install
-------

    git clone git@github.com:divitu/canonical-amis.git
    cd canonical-amis
    sudo ./setup.py install


Test
----

    ./setup.py test


Distribute
----------

    pip install twine
    ./setup.py sdist
    twine upload dist/*
