from typing import Optional, List, cast

from src.todos.arg_parser.arg_parser import arg_parser
from src.todos.arg_parser.args_models import ConfigCommandArgs, TodosCommandArgs

from src.shared.Config import Config
from src.shared.Database import Database

config = Config("todos")

db = Database("todos")


def main():
    # Parse command line arguments
    parsed, extra = arg_parser()

    if not parsed.args:
        # If the command is not set, run the default command
        run_todos()
        exit(0)

    if parsed.args.command == "todos":
        run_todos(
            cast(
                TodosCommandArgs,
                parsed.args.args
            ),
            extra
        )
        exit(0)

    # If the command is config, handle it
    if parsed.args.command == "config":
        handle_config(cast(ConfigCommandArgs, parsed.args.args))
        exit(0)


def run_todos(
    args: Optional[TodosCommandArgs] = None,
    extra: Optional[List[str]] = None,
):
    match args.command:
        case None:
            print("handle the base case for todos")
            exit(0)
        case "say":
            msg = args.msg
            if not msg:
                print("arg \"msg\" provided")
                exit(1)
        case "save":
            db.insert("items", {
                "item": args.item
            })
        case "list":
            db.list_all("items")
        case _:
            print("Unknown command")
            exit(1)


def handle_config(args: ConfigCommandArgs):
    if not args.args.command:
        print("config command requires a sub-command, one of get, set, delete")
        exit(1)
    match args.args.command:
        case "get":
            print(config.get(args.args.key_path))
        case "set":
            config.update(
                args.args.key_path,
                args.args.value
            )
        case "list":
            print(config.model_dump())
        case _:
            print(f"Unknown config command: {args.args.command}. Must be one of get, set, delete")
            exit(1)
