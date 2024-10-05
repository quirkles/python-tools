import argparse
import os
import shutil
from typing import Optional

from pydantic import BaseModel, computed_field, Field
from jinja2 import Environment, FileSystemLoader


class Args(BaseModel):
    bin_name: str
    bin_description: Optional[str] = Field(default=None)

    @computed_field
    @property
    def bin_slug(self) -> str:
        return self.bin_name.replace(" ", "_").lower()


# first lets get the absolute path to the bin directory
bin_dir = os.path.abspath("bin")


def main(args: Args) -> None:
    print("Creating new binary:", args.bin_name)
    if args.bin_description:
        print("Description:", args.bin_description)
    # check that there is no directory with the bin_slug name in bin/src
    does_bin_dir_exist = args.bin_slug in [
        directory for directory
        in os.listdir("bin/src")
        if os.path.isdir(os.path.join("bin/src", directory))
    ]
    # check that the binary file is not in the bin directory
    does_bin_exist = args.bin_slug in [
        file for file
        in os.listdir("bin")
        if os.path.isfile(os.path.join("bin", file))
    ]

    # if either the binary dir or binary file already exist lets ask the user if they want to delete and replace them with the new binary
    if does_bin_dir_exist or does_bin_exist:
        print(f"Binary with name {args.bin_slug} already exists")
        response = input("Do you want to delete and replace it? (y/n): ")
        if response.lower() != "y":
            print("Exiting...")
            return
        if does_bin_dir_exist:
            shutil.rmtree(f"bin/src/{args.bin_slug}", ignore_errors=True)
        if does_bin_exist:
            os.remove(f"bin/{args.bin_slug}")

    os.mkdir(f"bin/src/{args.bin_slug}")

    filenames = ["main.py", "__main__.py", "__init__.py"]
    # Now we iterate over the filenames and render the templates
    environment = Environment(loader=FileSystemLoader("templates/binary/"))
    for filename in filenames:
        template = environment.get_template(f"{filename}.tmpl")
        with open(f"bin/src/{args.bin_slug}/{filename}", "w") as f:
            f.write(
                template.render(
                    binary_name=args.bin_name,
                    binary_description=args.bin_description,
                    binary_slug=args.bin_slug
                )
            )
    # now we write the binary to the bin directory

    # get the absolute path to the python executable running this script
    python_path = shutil.which("python")

    with open(f"bin/{args.bin_slug}", "w") as f:
        template = environment.get_template("binary.tmpl")
        f.write(
            template.render(
                binary_name=args.bin_name,
                binary_description=args.bin_description,
                binary_slug=args.bin_slug,
                python_path=python_path
            )
        )

    # make the binary executable by granting it the necessary permissions
    os.chmod(f"bin/{args.bin_slug}", 0o755)

    print(f"Binary {args.bin_name} created successfully")


def parse_args() -> Args:
    parser = argparse.ArgumentParser(
        description="A simple CLI to store user data"
    )
    parser.add_argument(
        "bin_name",
        metavar="binary name",
        type=str,
        help="The name of the binary"
    )

    parser.add_argument(
        "-d",
        "--bin_description",
        metavar="binary description",
        dest="bin_description",
        type=str,
        help="The description of the binary",
        required=False
    )

    return Args(**vars(parser.parse_args()))


if __name__ == "__main__":
    main(parse_args())
