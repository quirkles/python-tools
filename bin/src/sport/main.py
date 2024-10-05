import argparse
from pydantic import BaseModel


class Args(BaseModel):
    verbose: bool = False


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="sport")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    try:
        args = Args(**vars(parser.parse_args()))
    except Exception as e:
        parser.print_help()
        print(f"\nError: {e}")
        exit(1)

    # Print the version
    if args.verbose:
        print("Executing sport")

    # Run the main function
    print("Hello, world! from sport")
