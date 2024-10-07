from argparse import ArgumentParser

from typing import Tuple, List

from src.todos.arg_parser.args_models import CommandArgs

parser = ArgumentParser(prog='todos')

sub_parser = parser.add_subparsers(
    title="commands",
    description="Valid commands for todos",
    dest="command"
)


def arg_parser() -> Tuple[CommandArgs, List[str]]:
    init_config_parser()

    init_todos_parser()

    args, known_args = parser.parse_known_args()

    arg_dict = vars(args)

    command = arg_dict.get("command", None)
    sub_command = arg_dict.get("sub_command", None)

    if command != "config":
        sub_command = command
        command = "todos"

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
    # Create the parser for the config subcommand
    config_parser = sub_parser.add_parser(
        "config",
        help="Commands for managing the configuration for todos"
    )

    # Create the subparsers for the config subcommand
    config_sub_parsers = config_parser.add_subparsers(
        dest="sub_command",
        required=True,
        title="config sub commands",
        description="Valid sub commands for config"
    )

    # Create the parser for the set subcommand
    config_set_parser = config_sub_parsers.add_parser(
        "set",
        help="Set a configuration value"
    )

    # Add the key_path argument to the set subcommand
    config_set_parser.add_argument(
        "key_path",
        type=str,
        help="A dot separated path to the configuration value to be set",
    )

    # Add the value argument to the set subcommand
    config_set_parser.add_argument(
        "value",
        type=str,
        help="The value to set the configuration value to"
    )

    # Create the parser for the get subcommand
    config_get_parser = config_sub_parsers.add_parser(
        "get",
        help="Get a configuration value"
    )

    # Add the key_path argument to the get subcommand
    config_get_parser.add_argument(
        "key_path",
        type=str,
        help="A dot separated path to the configuration value to be retrieved"
    )

    # Create the parser for the list subcommand
    config_sub_parsers.add_parser(
        "list",
        help="List all configuration values"
    )


def init_todos_parser():
    # Add the parser for the say subcommand
    todos_add_parser = sub_parser.add_parser(
        "say",
        help="Say a message"
    )

    # Add the message argument to the say subcommand
    todos_add_parser.add_argument(
        "msg",
        type=str,
        help="The message to say"
    )

    # Add the parser for the save subcommand
    todos_save_parser = sub_parser.add_parser(
        "save",
        help="Persist an item to the sqlite db"
    )

    # Add the item argument to the save subcommand
    todos_save_parser.add_argument(
        "item",
        type=str,
        help="save an item"
    )

    # Add the parser for the list subcommand
    sub_parser.add_parser(
        "list",
        help="List the items"
    )
