# bsc-awards
A flask website for displaying award data.

# Usage

## Docker

```
$ docker run -p 80:5000 \
   -e DATABASE_URI=sqlite:///data.db \
   -e USERNAME=admin \
   -e PASSWORD=admin \
   -v /path/on/host/to/somewhere/:/usr/src/app/ \
   registry.gitlab.com/haydenhughes/bsc-awards:latest
```

`DATABASE_URI` must be a valid [sqlalchemy database URL](http://docs.sqlalchemy.org/en/latest/core/engines.html).
`USERNAME` and `PASSWORD` are exactly what you expect them to be. So set them to something secure.

## Not Docker

### Requirements

*  python3
*  python3-pip
*  nodejs

### Installation

First clone this repo (or download the zip) and change your directory to it.

`$ git clone https://gitlab.com/haydenhughes/bsc-awards.git && cd bsc-awards`

Next install python packages with pip.

`$ pip3 install -r requirements.txt`

Then install the required node packages with npm.

`$ npm install -g gulp-cli`
`$ npm install`

And compile the scss files and setup the javascripts with gulp.

`$ gulp clean`

`$ gulp scss`

`$ gulp js`

Lastly run the flask server.

```
$ export FLASK_APP=awards
$ export DATABASE_URI=sqlite:///data.db
$ export USERNAME=admin
$ export PASSWORD=admin

$ flask run
```

The `DATABASE_URI` environment variable must be a valid [sqlalchemy database URL](http://docs.sqlalchemy.org/en/latest/core/engines.html).
The `USERNAME` and `PASSWORD` environment variables are exactly what you expect them to be. So set them to something secure.


# Running unittests

`$ python3 -m unittest discover -s test`
