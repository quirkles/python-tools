from src.test_app.arg_parser import arg_parser, Args
from src.shared.Config import Config
from src.shared.Database import Database

config = Config("test_app")

db = Database("test_app")


def main():
    # Parse command line arguments
    args, extra_args = arg_parser()

    # Print the version
    if args.verbose:
        print('Executing test_app')

    if not args.command:
        run(args, extra_args)
        exit(0)
    else:
        match args.command:
            case "config":
                handle_config(args, extra_args)
            case _:
                print("Unknown command")
                exit(1)
        exit(0)


def run(
        args: Args,
        extra_args: list[str],
):
    print("running test_app")


def handle_config(args: Args, extra_args: list[str]):
    if not args.sub_command:
        print("config command requires a sub-command, one of get, set, delete")
        exit(1)
    [key_path, value] = extra_args + [None] if len(extra_args) < 2 else extra_args
    match args.sub_command:
        case "get":
            print(config.get(key_path))
        case "set":
            config.update(key_path, value)
        case "delete":
            config.delete(key_path)
        case _:
            print(
                f"Unknown config command: {args.sub_command}. Must be one of get, set, delete")
            exit(1)
