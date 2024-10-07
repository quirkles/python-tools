from argparse import ArgumentParser

from typing import Tuple, List

from src.newtest.arg_parser.args_models import CommandArgs

parser = ArgumentParser(prog='newtest')

sub_parser = parser.add_subparsers(
    title="commands",
    description="Valid commands for newtest",
    dest="command"
)


def arg_parser() -> Tuple[CommandArgs, List[str]]:
    init_config_parser()

    init_newtest_parser()

    args, known_args = parser.parse_known_args()

    arg_dict = vars(args)

    command = arg_dict.get("command", None)
    sub_command = arg_dict.get("sub_command", None)

    if command != "config":
        sub_command = command
        command = "newtest"

    command_dict = {
        "args": {
            "command": command,
            "args": {
                "command": sub_command,
                **{k: v for k, v in arg_dict.items() if k not in ["command", "sub_command"]}
            }
        }
    }

    return CommandArgs(**command_dict), known_args

def init_config_parser():
    config_parser = sub_parser.add_parser(
        "config",
        help="Commands for managing the configuration for newtest"
    )

    config_sub_parsers = config_parser.add_subparsers(
        dest="sub_command",
        required=True,
        title="config sub commands",
        description="Valid sub commands for config"
    )

    config_set_parser = config_sub_parsers.add_parser(
        "set",
        help="Set a configuration value"
    )

    config_set_parser.add_argument(
        "key_path",
        type=str,
        help="A dot separated path to the configuration value to be set",
    )
    config_set_parser.add_argument(
        "value",
        type=str,
        help="The value to set the configuration value to"
    )

    config_get_parser = config_sub_parsers.add_parser(
        "get",
        help="Get a configuration value"
    )
    config_get_parser.add_argument(
        "key_path",
        type=str,
        help="A dot separated path to the configuration value to be retrieved"
    )

    config_sub_parsers.add_parser(
        "list",
        help="List all configuration values"
    )


def init_newtest_parser():
    newtest_add_parser = sub_parser.add_parser(
        "say",
        help="Say a message"
    )

    newtest_add_parser.add_argument(
        "msg",
        type=str,
        help="The message to say"
    )

    newtest_save_parser = sub_parser.add_parser(
        "save",
        help="Persist an item to the sqlite db"
    )

    newtest_save_parser.add_argument(
        "item",
        type=str,
        help="save an item"
    )

    newtest_list_parser = sub_parser.add_parser(
        "list",
        help="List the items"
    )
