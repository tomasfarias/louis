# Louis

Louis is a challenge project consisting of two parts:
* A PostgreSQL database with a few analysis queries.
* A REST API with an endpoint to provide JSON nesting services.

# Requirements

Deploying Louis requires only installing `docker-compose` and `docker`. The following services will be deployed:
* A PostgreSQL database containing the result of the analysis queries.

# Usage

Before running, you may want to look at the ports we are exposing in `docker-compose.yml`:
* Port 5432 is used for the PostgreSQL database. If it's already in use (by another PostgreSQL database maybe?) then a different port number must be chosen.

Running the deployment is as simple as:

``` sh
docker-compose up -d
```

# Database and analysis queries

The PostgreSQL database deployed contains tables with the results of the analysis queries. See the database ![README](db/README.md) for more information.

# License

This project, like most of the challenge projects I do, is licensed under MIT. See ![LICENSE](LICENSE).
