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

    command_args = {
        "args": {
            "command": command,
        }
    }

    if sub_command:
        command_args["args"]["sub_command"] = {
            "command": sub_command
        }

    for key, value in arg_dict.items():
        if key in ["command", "sub_command"]:
            continue
        if sub_command:
            command_args["args"]["sub_command"][key] = value
        else:
            command_args["args"][key] = value

    return CommandArgs(**command_args), known_args


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
    todos_say_parser = sub_parser.add_parser(
        "say",
        help="Say a message"
    )

    todos_say_sub_parser = todos_say_parser.add_subparsers(
        dest="sub_command",
        required=False,
        title="Sub-commands for say",
        description="Valid sub-commands for say, supported sub-commands are bear and fight"
    )

    # Add the message argument to the say subcommand
    todos_say_parser.add_argument(
        "-m",
        "--msg",
        type=str,
        help="The message to say"
    )

    my_colors_say_bear_parser = todos_say_sub_parser.add_parser(
        "bear",
        help="Say a bear message"
    )

    todos_say_bear_parser.add_argument(
        "-m",
        "--msg",
        type=str,
        required=True,
        help="The message to say"
    )

    todos_say_fight_parser = todos_say_sub_parser.add_parser(
        "fight",
        help="Say a fight message"
    )

    todos_say_fight_parser.add_argument(
        "-m",
        "--msg",
        type=str,
        required=True,
        help="The message to say"
    )

    # Add the parser for the save subcommand
    todos_save_parser = sub_parser.add_parser(
        "save",
        help="Persist an item to the sqlite db"
    )

    # Add the item argument to the save subcommand
    todos_save_parser.add_argument(
        "--item",
        "-i",
        required=True,
        type=str,
        help="save an item"
    )

    # Add the parser for the list subcommand
    sub_parser.add_parser(
        "list",
        help="List the items"
    )
