import argparse
import copy
import json
import logging
import sys
import typing


def configure_logging(debug: bool):
    """Configure root logger with stderr output"""
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(level=logging.DEBUG if debug is True else logging.INFO)
    logger.addHandler(handler)


def run():
    """Run the main CLI to nest JSON values"""
    parsed = parse_args(sys.argv[1:])
    json_array = json.load(parsed.json)
    configure_logging(parsed.debug)
    logging.debug("Read JSON array: %s", json_array)
    sys.stdout.write(json.dumps(process_json_array(json_array, *parsed.keys), indent=4))
    sys.stdout.flush()


def process_json_array(
    json_array: typing.List[typing.Dict[typing.Any, typing.Any]], *keys: str
) -> typing.Dict[typing.Any, typing.Any]:
    """
    Process a list of JSON-like dictionaries and recursively nest them according
    to the given keys.

    Args:
    json_array: A list of JSON-like dictionaries.
    keys: Variable number of keys to nest dictionaries. Dictionaries will be nested
        in the same order as the keys.

    Returns:
    JSON-like dictionary nested by keys
    """
    results: typing.Dict[typing.Any, typing.Any] = {}
    for json_dict in json_array:
        logging.debug("Processing JSON dictionary: %s", json_dict)
        nest_json(json_dict, [k for k in keys], results)
    return results


def nest_json(
    json_dict: typing.Dict[typing.Any, typing.Any],
    keys: typing.List[str],
    results: typing.Dict[typing.Any, typing.Any],
):
    """
    Recursively nest a single JSON-like dictionary in results according to all
    given keys.

    Args:
    json_dict: A JSON-like dictionary.
    keys: Variable number of keys to nest the dictionary. Dictionary will be nested
        in the same order as the keys.
    results: A dictionary that will contain the nested structure.
    """
    keys_copy = copy.deepcopy(keys)
    key = keys_copy.pop(0)
    value = json_dict.pop(key)
    if len(keys_copy) == 0:
        if value in results.keys():
            results[value].append(json_dict)
        else:
            results[value] = [json_dict]
    else:
        if value not in results.keys():
            results[value] = {}
        nest_json(json_dict, keys_copy, results[value])


def parse_args(args: typing.List[str]):
    """CLI argument parser"""
    parser = argparse.ArgumentParser(
        description="Group a JSON array by an arbitrary number of keys"
    )
    parser.add_argument(
        "--json",
        nargs="?",
        type=argparse.FileType("r"),
        help="JSON file to read, if empty, input is read from stdin",
        default=sys.stdin,
    )
    parser.add_argument(
        "--debug",
        help="Set logging level to DEBUG",
        action="store_true",
        default=False,
        required=False,
    )
    parser.add_argument(
        "keys",
        nargs="*",
        help="Arbitrary number of grouping keys. JSON dictionaries"
        "will be nested as deep as possible",
    )

    return parser.parse_args(args)


def main():
    run()


if __name__ == "__main__":
    sys.exit(main())
