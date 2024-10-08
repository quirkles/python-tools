from typing import Literal, Union, Optional

from pydantic import BaseModel, Field, ConfigDict


class ConfigGetCommandArgs(BaseModel):
    command: Literal["get"]
    key_path: str


class ConfigSetCommandArgs(BaseModel):
    command: Literal["set"]
    key_path: str
    value: str


class ConfigListCommandArgs(BaseModel):
    command: Literal["list"]


class ConfigCommandArgs(BaseModel):
    command: Literal["config"]
    sub_command: Union[
        ConfigGetCommandArgs,
        ConfigSetCommandArgs,
        ConfigListCommandArgs
    ] = Field(discriminator="command")

class TodosRootCommandArgs(BaseModel):
    command: Literal[None]

class TodosSayBearGenerateCommandArgs(BaseModel):
    command: Literal["bear"]
    msg: str


class TodosSayFightGenerateCommandArgs(BaseModel):
    command: Literal["fight"]
    msg: str


class TodosSayCommandArgs(BaseModel):
    command: Literal["say"]
    msg: Optional[str] = Field(default=None)
    sub_command: Optional[Union[
        TodosSayBearGenerateCommandArgs,
        TodosSayFightGenerateCommandArgs
    ]] = Field(discriminator="command", default=None)


class TodosSaveCommandArgs(BaseModel):
    model_config = ConfigDict(extra="allow")
    command: Literal["save"]
    item: str


class TodosListCommandArgs(BaseModel):
    model_config = ConfigDict(extra="allow")
    command: Literal["list"]

TodosCommandArgs = Union[
    TodosSayCommandArgs,
    TodosSaveCommandArgs,
    TodosListCommandArgs
]

class CommandArgs(BaseModel):
    args: Optional[
        Union[
            ConfigCommandArgs,
            TodosRootCommandArgs,
            TodosCommandArgs
        ]
    ] = Field(
        discriminator="command",
        default=None
    )
    verbose: bool = Field(default=False)
