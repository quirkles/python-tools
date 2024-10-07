from typing import Optional, List, cast

from src.newtest.arg_parser.arg_parser import arg_parser
from src.newtest.arg_parser.args_models import ConfigCommandArgs, NewtestCommandArgs

from src.shared.Config import Config
from src.shared.Database import Database

config = Config("newtest")

db = Database("newtest")


def main():
    # Parse command line arguments
    parsed, extra = arg_parser()

    if not parsed.args:
        # If the command is not set, run the default command
        run_newtest()
        exit(0)

    if parsed.args.command == "newtest":
        run_newtest(
            cast(
                NewtestCommandArgs,
                parsed.args.args
            ),
            extra
        )
        exit(0)

    # If the command is config, handle it
    if parsed.args.command == "config":
        handle_config(cast(ConfigCommandArgs, parsed.args.args))
        exit(0)


def run_newtest(
    args: Optional[NewtestCommandArgs] = None,
    extra: Optional[List[str]] = None,
):
    match args.command:
        case None:
            print("handle the base case for newtest")
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
            print("Listing all items")
            for item in db.list_all("items"):
                print(item)
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
