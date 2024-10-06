import json
from copy import deepcopy
from os import path
from typing import Optional, Union

from pydantic import BaseModel


class Config:
    config: dict
    config_file_name: str
    config_schema: Optional[type[BaseModel]]

    def __init__(
            self,
            config_file_name: str,
            config_schema: Optional[type[BaseModel]] = None,
    ):
        # First we need to check if the config file exists
        self.config_schema = config_schema
        self.config_file_name = path.join(path.expanduser("~"),
                                          f".{config_file_name}.json")
        if not path.exists(self.config_file_name):
            # Create the file if it does not exist
            with open(self.config_file_name, "w") as f:
                f.write("{}")
        # Load the config file
        with open(self.config_file_name, "rt") as f:
            config = json.load(f)
            if config_schema:
                self.config = config_schema(**config).model_dump()
            else:
                self.config = config

    def save(self):
        with open(self.config_file_name, "w") as f:
            json.dump(self.config, f)

    def update(
            self,
            # key_path: a dot separated path to the key to update
            key_path: str,
            # value: the value to update the key to
            value: Union[str, int, float, bool],
    ):
        # If we have a shcema then before we update the config we need to validate the potential new version
        # we will make a deep copy of the current config and update the key with the new value then validate it
        # if it is valid we will update the current config with the new value
        if self.config_schema:
            new_config = deepcopy(self.config)
            key_path = key_path.split(".")
            current = new_config
            for key in key_path[:-1]:
                if key not in current:
                    current[key] = {}
                current = current[key]
            current[key_path[-1]] = value
            try:
                self.config_schema(**new_config)
            except Exception as e:
                print(f"Config update failed, results in invalid configuration: {e}")
                return

        # Update the config
        current = self.config
        key_path = key_path.split(".")
        for key in key_path[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        current[key_path[-1]] = value
        self.save()

    def get(
            self,
            # key_path: a dot separated path to the key to get
            key_path: str
    ):
        current = self.config
        try:
            for key in key_path.split("."):
                current = current[key]
            return current
        except KeyError:
            return None

    def delete(
            self,
            # key_path: a dot separated path to the key to delete
            key_path: str
    ):
        current = self.config
        key_path = key_path.split(".")
        for key in key_path[:-1]:
            current = current[key]
        del current[key_path[-1]]
        self.save()

    def model_dump(self):
        return self.config
