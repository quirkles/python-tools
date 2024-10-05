# Pyton cli tools

This is a repo designed to make it easy to build and develop python cli tools. It is a simple template that you can use to get started with your own cli tool.

## Installation

### Pyenv (recommended)

Its recommended to use pyenv to manage your python versions. You can install pyenv by following the instructions [here](https://github.com/pyenv/pyenv)

### Virtualenv

Create a virtualenv using the version of python you want to use. You can do this by running the following command:

```bash
python -m venv .venv
```

Activate the virtualenv by running:

```bash
source .venv/bin/activate
```

Install the dependencies by running:

```bash
pip install -r requirements.txt
```

## How to use

This repo contains a python script that will create two things for you:

- A python module under `/bin/src` that contains the logic for your cli tool
- A python executable with a shebang under `/bin` that will run your cli tool

Once a binary has been created, you can run it by running the following command:

```bash
./bin/<binary_name> --help
```

The intention is that you would add this bin directory to your path so that you can run the binary from anywhere.

## Usage

Running `python create_bin.py` will create a new binary for you. You can pass the following arguments to the script:

- The name of the binary you want to create
- -d or --description: A description of what the binary does (optional)

eg:

```bash
python create_bin.py my_binary -d "This is a binary that does something"
```

If a binary already exists with the same name, the script will ask you if you want to overwrite it.

```bash
> python create_bin.py my_binary -d "This is a binary that does something"

Creating new binary: my_binary
Description: This is a binary that does something
Binary with name my_binary already exists
Do you want to delete and replace it? (y/n): y

> my_binary -h

usage: my_binary [-h] [--verbose]

This is a binary that does something

options:
  -h, --help     show this help message and exit
  --verbose, -v  Verbose output

```