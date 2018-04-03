yafas server
===
[![Build Status](https://travis-ci.org/yafas/yafas-server.svg?branch=master)](https://travis-ci.org/yafas/yafas-server)
[![Coverage Status](https://coveralls.io/repos/github/yafas/yafas-server/badge.svg?branch=master)](https://coveralls.io/github/yafas/yafas-server?branch=master)
[![Docker hub](https://img.shields.io/badge/docker%20hub-latest-blue.svg)](https://hub.docker.com/r/yafas/yafas-server/)

Installation
===

``` shell
# install dependencies
pip install -r requirements.txt

# create `.env` file in project root
cp .env.ci .env

# migrate database
alembic upgrade head

# run
fab dev
```

Testing
===

``` shell
pytest
```

