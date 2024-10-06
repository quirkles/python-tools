import argparse
from typing import Literal, Optional, get_args

from pydantic import BaseModel

action_choices = Literal["put", "get"]


class Args(BaseModel):
    key_name: str
    action: action_choices
    valueOrVersion: Optional[str]


def arg_parser() -> Args:
    parser = argparse.ArgumentParser(description="A simple CLI to store user data")
    parser.add_argument(
        "action",
        metavar="action",
        type=str,
        choices=["put", "get"],
        help=f"Top level command. One of: {", ".join(get_args(action_choices))}",
    )

    parser.add_argument("key_name", metavar="keyname", type=str, help="The key name")

    parser.add_argument(
        "valueOrVersion",
        metavar="valueOrVersion",
        type=str,
        help="The value to store or version to display",
        nargs="?",
        default=None,
    )
    args = parser.parse_args()
    return Args(**vars(args))
