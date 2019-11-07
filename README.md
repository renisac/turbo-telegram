# Getting Started
Required Environment variables:

REN_TOKEN = `token`

Optional Environment Variables, used for testing non-production as r.ren is hardcoded:

REN_REMOTE=https://test-env.domain.com

REN_VERIFY_SSL=False

## Ubuntu1404
```bash
$ export REN_TOKEN=1234
$ git clone https://github.com/renisac/turbo-telegram.git
$ pip install -e turbo-telegram
```

## Client Examples

```bash
$ ren --users sfinlon
$ ren --members 'Indiana University'
```

# Getting Involved
There are many ways to get involved with the project. If you have a new and exciting feature, or even a simple bugfix, simply [fork the repo](https://help.github.com/articles/fork-a-repo), create some simple test cases, [generate a pull-request](https://help.github.com/articles/using-pull-requests) and give yourself credit!

If you've never worked on a GitHub project, [this is a good piece](https://guides.github.com/activities/contributing-to-open-source) for getting started.

* [How To Contribute](contributing.md)  
* [Mailing List](https://groups.google.com/forum/#!forum/ci-framework)  
* [Project Page](http://csirtgadgets.org/collective-intelligence-framework/)

# Development
## Some of the tools we use:

* [PyCharm](https://www.jetbrains.com/pycharm/)
* [VirtualenvWrapper](https://virtualenvwrapper.readthedocs.org/en/latest/)
* [Vagrant](https://www.vagrantup.com/)

## Some useful books:

* [Vagrant Up & Running](http://www.amazon.com/Vagrant-Up-Running-Mitchell-Hashimoto/dp/1449335837/ref=sr_1_3?ie=UTF8&qid=1450109562&sr=8-3&keywords=ansible+up+and+running)
* [Docker Up & Running](http://www.amazon.com/Docker-Up-Running-Karl-Matthias/dp/1491917571/ref=sr_1_2?ie=UTF8&qid=1450109562&sr=8-2&keywords=ansible+up+and+running)


# COPYRIGHT AND LICENCE

Copyright (C) 2016 [the REN-ISAC](http://ren-isac.net)

Free use of this software is granted under the terms of the GNU Lesser General Public License (LGPLv3). For details see the files `COPYING` included with the distribution.
