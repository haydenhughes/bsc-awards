# bsc-awards
A flask website for displaying award data.

# Usage

## Docker

```
docker pull registry.gitlab.com/haydenhughes/bsc-awards:latest
docker run -p 80:5000 \
  -e DATABASE_URI=sqlite:///data.db \
  -v /path/on/host/to/somewhere/:/usr/src/app/ \
  bsc-awards:latest
```

`DATABASE_URI` must be a valid [sqlalchemy database URL](http://docs.sqlalchemy.org/en/latest/core/engines.html).
`FLASK_APP` needs to be set to awards.

## Not Docker

### Requirements

*  python3
*  python3-pip
*  nodejs

### Installation

First clone this repo (or download the zip) and change your directory to it.

`git clone https://gitlab.com/haydenhughes/bsc-awards.git && cd bsc-awards`

Next install python packages with pip.

`pip install -r requirements.txt`

Then install the required node packages with npm.

`npm install -g gulp-cli`
`npm install`

And compile the scss files and setup the javascripts with gulp.

`gulp clean`
`gulp scss`
`gulp js`

Lastly run the flask server.

```
export FLASK_APP=awards
export DATABASE_URI=sqlite:///data.db

flask run
```

The `DATABASE_URI` enviroment variable must be a valid [sqlalchemy database URL](http://docs.sqlalchemy.org/en/latest/core/engines.html).


# Running unittests

`python3 -m unittest discover -s test`
