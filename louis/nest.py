import argparse
import copy
import json
import logging
import sys
import typing


def configure_logging(debug: bool):
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
    parsed = parse_args(sys.argv[1:])
    json_array = json.load(parsed.json)
    configure_logging(parsed.debug)
    logging.debug("Read JSON array: %s", json_array)
    sys.stdout.write(json.dumps(process_json_array(json_array, *parsed.keys)))
    sys.stdout.flush()


def process_json_array(
    json_array: typing.List[typing.Dict[typing.Any, typing.Any]], *keys: str
):
    results: typing.Dict[typing.Any, typing.Any] = {}
    for json_dict in json_array:
        logging.debug("Processing JSON dictionary: %s", json_dict)
        nest_json(json_dict, [k for k in keys], results)
    return results


def nest_json(json_dict, keys, results):
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
