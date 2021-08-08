# Louis

Louis is a challenge project consisting of two parts:
* Some analysis queries done in PostgreSQL.
* A tool to provide JSON nesting services.

# Requirements

Deploying Louis requires only installing `docker-compose` and `docker`. The following services will be deployed:
* A PostgreSQL database containing the result of the analysis queries.
* A REST API with a `nestme` endpoint that provides JSON nesting services.

If choosing not to deploy with `docker` and `docker-compose`, the REST API does have some extra requirements as discussed in ![Deploying the REST API without docker](#deploying-the-rest-api-without-docker).

Interfacing with the database may require a front-end tool to interact with the PostgreSQL database, like `psql`.

# Database and analysis queries

The PostgreSQL database deployed contains tables with the results of the analysis queries. See the database ![README](db/README.md) for more information.

## Database deployment

Before running, you may want to look at the ports we are exposing in `docker-compose.yml`:
* Port 5432 is used for the PostgreSQL database. If it's already in use (by another PostgreSQL database maybe?) then a different port number must be chosen.

Running the deployment is as simple as:

``` sh
docker-compose up -d database
```

The database may then be accessed with (for example) `psql`:

``` sh
psql -h localhost -p 5432 -U test -d test
```

The test password is also `"test"`.

# JSON Nesting

The JSON Nesting service is offered in two ways: a CLI tool and a REST API.

## JSON Nesting via CLI

The Louis CLI tool only requires the Python standard library, so it may be run directly as:

``` sh
# Assuming we have a JSON file in sample.json
python louis city country --json sample.json
```

To conform with the task requirements, the `nest.py` file may be invoked directly and the JSON file may be piped into the script:

``` sh
cat sample.json | python louis/nest.py currency country city
```

The CLI supports a `--debug` flag to enable DEBUG logging.

The output of the CLI may be further piped into other tools, like `jq`:

``` sh
cat sample.json | python louis city | jq -r '.["Boston"]'
```

Which outputs:

``` json
[
  {
    "country": "US",
    "currency": "USD",
    "amount": 100
  }
]
```

## JSON Nesting via REST API

A REST API has been developed with `FastAPI` and it may be run with `docker-compose`:

``` sh
docker-compose up -d rest_api
```

Keep in mind that the API will attempt to use local port 8080. If we already have something running on 8080, we will need to edit the `docker-compose.yml` file to use some other free port.

Alternatively, just `docker` would work fine too:

``` sh
docker build -t tomasfarias/louis:latest .
docker run --env-file rest_api.env -p 8080:8080 tomasfarias/louis:latest
```

A `uvicorn` server will now be listening for requests at `127.0.0.1:8080` (by default). The current implementation has two endpoints, both of them protected by basic-auth:
* `/health`: A simple health-check.
* `/nestme`: Accepts JSONs and keys to offer the JSON nesting service.

We may interact with the API using `curl`:

``` sh
curl -u louis:test --request GET  http://127.0.0.1:8080/health
{"message":"10-4 all systems green"}
```

And make POST requests to get nested JSONs like (with some `jq` for pretty-printing):

``` sh
curl --header "Content-Type: application/json" \
  -u louis:test \
  --request POST \
  --data "{\"keys\": [\"country\", \"city\"], \"json_array\": $(cat sample.json)}" \
  http://127.0.0.1:8080/nestme | jq
{
  "US": {
    "Boston": [
      {
        "currency": "USD",
        "amount": 100
      }
    ]
  },
  "FR": {
    "Paris": [
      {
        "currency": "EUR",
        "amount": 20
      }
    ],
    "Lyon": [
      {
        "currency": "EUR",
        "amount": 11.4
      }
    ]
  },
  "ES": {
    "Madrid": [
      {
        "currency": "EUR",
        "amount": 8.9
      }
    ]
  },
  "UK": {
    "London": [
      {
        "currency": "GBP",
        "amount": 12.2
      },
      {
        "currency": "FBP",
        "amount": 10.9
      }
    ]
  }
}
```

### Deploying the REST API without docker

If wishing to run the REST API server without docker, a couple of dependencies need to be installed, as described in ![`requirements.txt`](requirements.txt).

Once installed the server may be run as:

``` sh
uvicorn louis.rest_api:app --host 0.0.0.0 --port 8080
```

# Development

This section describes development tools used for testing, linting, and static type checking. All tools are described in ![`requirements_dev.txt`](`requirements_dev.txt`).

## Linting

We use `black` for automated code formatting, `flake8` for PEP8 validation, and `isort` for import statement sorting. These tools may be run as:

``` sh
flake8 tests/ louis/
black tests/ louis/
isort tests/ louis/
```

## Testing

Python unit tests have been written in `pytest`, and may be run as:

``` sh
pytest tests/
```

## Static type checking

To validate the type hints available in Louis, we can run `mypy`:

``` sh
mypy louis/ tests/
```

## Limitations

In its current state the REST API is to be considered not more than a prototype, and much more work would be required before shipping to production, a few ideas:
* It should go without saying that basic authentication is not enough in terms of security.
* On the topic of security, credentials are being fed from the environment. A proper secrets backend should be setup instead. Especially considering the secrets are exposed via `docker inspect <container id>`.
* The API has no caching feature, which means that sending requests with the same inputs will trigger (perhaps unnecessary) re-computations.
* Error handling on the API is bare-bones and should be extended.

# License

This project, like most of the challenge projects I do, is licensed under MIT. See ![LICENSE](LICENSE).
