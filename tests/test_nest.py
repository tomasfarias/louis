import json

import pytest

from louis.nest import parse_args, process_json_array

CONTENT = """
[
  {
    "country": "US",
    "city": "Boston",
    "currency": "USD",
    "amount": 100
  },
  {
    "country": "FR",
    "city": "Paris",
    "currency": "EUR",
    "amount": 20
  },
  {
    "country": "FR",
    "city": "Lyon",
    "currency": "EUR",
    "amount": 11.4
  },
  {
    "country": "ES",
    "city": "Madrid",
    "currency": "EUR",
    "amount": 8.9
  },
  {
    "country": "UK",
    "city": "London",
    "currency": "GBP",
    "amount": 12.2
  },
  {
    "country": "UK",
    "city": "London",
    "currency": "FBP",
    "amount": 10.9
  }
]
"""


@pytest.fixture(scope="session")
def sample_json(tmp_path_factory):
    d = tmp_path_factory.mktemp("sample")
    p = d / "sample.json"
    p.write_text(CONTENT)
    return p


def test_parse_args(sample_json):
    sample_args = ["key1", "key2", "key3", "--json", str(sample_json)]
    parsed = parse_args(sample_args)

    assert parsed.keys == ["key1", "key2", "key3"]
    assert parsed.json.name == str(sample_json)
    assert parsed.debug is False


def test_process_json_array(sample_json):
    keys = ["currency", "country", "city"]
    with open(sample_json) as f:
        json_array = json.load(f)
    nested = process_json_array(json_array, *keys)

    expected = {
        "USD": {"US": {"Boston": [{"amount": 100}]}},
        "EUR": {
            "FR": {"Paris": [{"amount": 20}], "Lyon": [{"amount": 11.4}]},
            "ES": {"Madrid": [{"amount": 8.9}]},
        },
        "GBP": {"UK": {"London": [{"amount": 12.2}]}},
        "FBP": {"UK": {"London": [{"amount": 10.9}]}},
    }

    assert nested == expected
