# bsc-awards [![Build Status](https://travis-ci.org/haydenhughes/bsc-awards.svg?branch=master)](https://travis-ci.org/haydenhughes/bsc-awards)
A flask website for displaying award data.


## Features
* Supports any SQL database for student and award data thanks to SQLAlchemy.
* Groups students so not too many students are on stage at once.
* Simple attendance management to ensure that only students attending have their name called out.
* Printable attendance sheets that also contain the awards of every attending student for each year level.
* A intuitive web based GUI built using [Bootstrap 4](getbootstrap.com) and [Flask](http://flask.pocoo.org/).
* User authentication.
* Awards marked as special are not displayed.


## Installation

### Docker

```
$ docker run -p 80:5000 \
   -e DATABASE_URI=sqlite:///data.db \
   -e USERNAME=admin \
   -e PASSWORD=admin \
   -v /path/on/host/to/somewhere/:/usr/src/app/ \
   haydenhughes/bsc-awards:latest
```

`DATABASE_URI` must be a valid [sqlalchemy database URL](http://docs.sqlalchemy.org/en/latest/core/engines.html).

`USERNAME` and `PASSWORD` are exactly what you expect them to be so set them to something secure.

### Not Docker

##### Requirements

*  python3
*  python3-pip
*  nodejs


First clone this repo (or download the zip) and change your directory to it.

`$ git clone https://gitlab.com/haydenhughes/bsc-awards.git && cd bsc-awards`

Next install python packages with pip.

`$ pip3 install -r requirements.txt`

Then install the required node packages with npm.

`$ npm install -g gulp-cli`
`$ npm install`

And compile the scss files and setup the javascripts with gulp.

```
$ gulp clean
$ gulp scss`
$ gulp js`
```

Lastly run the flask server.

```
$ export FLASK_APP=awards
$ export DATABASE_URI=sqlite:///data.db
$ export USERNAME=admin
$ export PASSWORD=admin
$ flask run
```

The `DATABASE_URI` environment variable must be a valid [sqlalchemy database URL](http://docs.sqlalchemy.org/en/latest/core/engines.html).

The `USERNAME` and `PASSWORD` environment variables are exactly what you expect them to be so set them to something secure.


## Contributing

### Running unittests locally

`$ python3 -m unittest discover -s test`

### Generating `requirements.txt`

For development I use `pipenv` to manage dependencies but Docker requires a `requirements.txt` which must be generated after every dependency change by running:

`$ pipenv lock --requirements > requirements.txt`
