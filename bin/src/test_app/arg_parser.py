import argparse
from pydantic import BaseModel, Field
from typing import Literal, Optional, get_args, Tuple, List

commands = Literal["config"]

class Args(BaseModel):
    command: Optional[commands] = Field(default=None)
    sub_command: Optional[str] = Field(default=None)
    verbose: Optional[bool] = Field(default=False)


def arg_parser() -> Tuple[Args, List[str]]:
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='test_app')
    parser.add_argument(
        'command',
        metavar="action",
        type=str,
        nargs="?",
        choices=get_args(commands),
        help=f"The action to take. One of: {", ".join(get_args(commands))}",
    )

    parser.add_argument(
        "sub_command",
        metavar="sub_command",
        type=str,
        nargs="?",
        default=None,
    )

    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Verbose output',
    )

    args, unknown_args = parser.parse_known_args()

    try:
        return Args(**vars(args)), unknown_args
    except Exception as e:
        parser.print_help()
        print(f'\nError: {e}')
        exit(1)