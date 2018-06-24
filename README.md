# bsc-awards
A flask website for displaying award data.

## Usage

Can be ran using [flask's built-in run command](http://flask.pocoo.org/docs/1.0/cli/) or using the provided [docker](https://www.docker.com/) image. There is also a `docker-compose.yml` for [docker-compose](https://github.com/docker/compose) which sets up the application and a postgresql database. 

The required enviroment variables are `DATABASE_URI` and `FLASK_APP`. `DATABASE_URI` must be a valid [sqlalchemy database URL](http://docs.sqlalchemy.org/en/latest/core/engines.html). `FLASK_APP` needs to be set to the path to the awards package.

Example:

```
export FLASK_APP=awards
export DATABASE_URI=sqlite:///data.db

flask run
```

