Badger
======

Badger is a small set of scripts to mine [association rules](http://en.wikipedia.org/wiki/Association_rule_learning) of [Fedora Badges](https://badges.fedoraproject.org/). *Crawler* downloads the data from Badges API, *Miner* generates the rules.

Usage
-----

At least for *Miner* it is recommended to use [PyPy](http://pypy.org/) to get the results faster. For *Crawler* you can use any Python implementation you like, using PyPy brings no improvement here.

Here is an example of how to run this on Fedora supposing `pypy` and `python-virtualenv` packages are installed:

    virtualenv -p /usr/bin/pypy venv
    . venv/bin/activate
    pip install -r requirements.txt
    pypy crawler.py
    pypy miner.py 9 0.9 10 15

Note that downloading the data from Badges API will take it's time. Therefore `data.json` is already provided with data from 07-05-2015 (just skip `pypy crawler.py` and go straight to `pypy miner.py ...` to use it)

*Miner* requires some arguments:

    pypy miner.py <min_support> <min_confidence> [<user_limit> <badge_limit>]

 * `min_support` is the minimal support of the rules to be mined. You can experiment with it. The higher the number, the fewer the rules.
 * `min_confidence` is the minimal confidence of the rules to be mined. It's float between 0 and 1. The higher the number, the fewer the rules.
 * `user_limit` is a limit of users to use for mining. If you use it, you will get the top X user of Fedora Badges. You can omit the limits to use all the users, i.e. little less than 1500 now. (This would most certainly eat all your RAM.)
 * `badge_limit` is a limit of badges to use for mining. If you use it, the *Miner* will only see the first X badges in the order the *Crawler* downloaded the data (and although the order is deterministic, you can think of it as it would be random). You can omit the limits to use all the badges users get, i.e. little more than 250 now. (This would most certainly eat all your RAM.)

The idea
--------

The original idea was to get all the results, look at them and either filter them manually or by some other scripted logic, to avoid Cpt. Obvious rules, such as:

    if-you-build-it...-koji-success-ii -> if-you-build-it...-koji-success-i with support XXX and confidence 1.0

Meaning if user has [If you build it... (Koji Success II)](https://badges.fedoraproject.org/badge/if-you-build-it...-koji-success-ii) they will most certainly get [If you build it... (Koji Success I)](https://badges.fedoraproject.org/badge/if-you-build-it...-koji-success-i). This information is useless, because users allways get those badges in order that makes *Koji Success I* actually a dependency of *Koji Success II*.

The problem
-----------

Unfortunately, this is quite useless, because running the *Miner* with 20 users and 20 badges eats all my RAM and swap. So running it unlimited would probably require a large SSD powered swap. Also, running with 12 users and 15 badges (which is quite OK for my RAM), generates more than 100 000 rules. So any manual filtering is off the table. I'm also certainly sure that even if the filtering is scripted, the filtered results would be so large none would ever want to read them :(
