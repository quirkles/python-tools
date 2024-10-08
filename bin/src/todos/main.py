from typing import Optional, List, cast

from src.todos.arg_parser.arg_parser import arg_parser
from src.todos.arg_parser.args_models import (
        ConfigCommandArgs,
        ConfigSetCommandArgs,
    TodosCommandArgs,
    TodosSayCommandArgs,
)

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

    # If the command is config, handle it
    if parsed.args.command == "config":
        handle_config(cast(ConfigCommandArgs, parsed.args))
        exit(0)

    run_todos(
        cast(
            TodosCommandArgs,
            parsed.args
        ),
        extra
    )
    exit(0)



def run_todos(
    args: Optional[TodosCommandArgs] = None,
    extra: Optional[List[str]] = None,
):
    if not args or not args.command:
        print("handle the base case for my_colors")
        exit(0)

    args = cast(TodosCommandArgs, args)

    match args.command:
        case "say":
            args = cast(TodosSayCommandArgs, args)
            msg = args.msg or args.sub_command.msg
            if not msg:
                print("arg \"msg\" provided")
                exit(1)
            if not args.sub_command:
                print(f"""
{"#" * (len(msg) + 4)}
# {msg} #
{"#" * (len(msg) + 4)}""")
                exit(0)
            match args.sub_command.command:
                case None:
                    print(f"{msg}")
                case "bear":
                    print(f"""
               {"_" * (len(msg))}
ʕっ•ᴥ•ʔっ ----({msg})
               {"‾" * (len(msg))}
""")
                case "fight":
                    print(f"""
              {"_" * (len(msg))}
(ง •̀_•́)ง ----({msg})
              {"‾" * (len(msg))}
""")
                case _:
                    print(f"Unknown say command: {args.sub_command.command}")
                    exit(1)
            exit(0)
        case "save":
            db.insert("items", {
                "item": args.item
            })
        case "list":
            for item in db.list_all("items"):
                print(item)
        case _:
            print("Unknown command")
            exit(1)


def handle_config(args: ConfigCommandArgs):
    if not args.sub_command.command:
        print("config command requires a sub-command, one of get, set, delete")
        exit(1)
    match args.sub_command.command:
        case "get":
            print(config.get(args.sub_command.key_path))
        case "set":
            args = cast(ConfigSetCommandArgs, args.sub_command)
            config.update(
                args.key_path,
                args.value
            )
        case "list":
            print(config.model_dump())
        case _:
            print(
                f"Unknown config command: {args.sub_command.command}. Must be one of get, set, delete")
            exit(1)
