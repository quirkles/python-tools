import json
from os import path
from typing import Optional, Dict

from src.store.arg_parser.arg_parser import action_choices

home_dir = path.expanduser("~")
datastore_path = path.join(home_dir, ".datastore.json")

if not path.exists(datastore_path):
    with open(datastore_path, "w") as f:
        json.dump({}, f)


class Datastore:
    data: Dict[str, list[str]]

    def __init__(self):
        with open(datastore_path, "r") as f:
            self.data = json.load(f)

    def _save(self):
        with open(datastore_path, "w") as f:
            json.dump(self.data, f)

    def process(
            self,
            key_name: str, action: action_choices, value_or_version: str):
        match action:
            case "put":
                self.put(key_name, value_or_version)
            case "get":
                self.get(key_name, value_or_version)

    def put(self, key_name: str, value: Optional[str]):
        if not value:
            value = input("Enter the value: ")
        if key_name not in self.data:
            self.data[key_name] = []
        self.data[key_name].append(value)
        self._save()

    def get(self, key_name: str, version: Optional[str] = None):
        key_values = self.data.get(key_name)
        if key_values is None:
            print(f'Key "{key_name}" not found')
            return
        if version is None:
            print(key_values[-1])
        else:
            version = int(version) - 1
            if version not in range(len(key_values)):
                print(f"Version {version + 1} not found")
                return
            print(key_values[int(version)])
