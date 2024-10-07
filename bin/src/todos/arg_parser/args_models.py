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
    args: Union[
        ConfigGetCommandArgs,
        ConfigSetCommandArgs,
        ConfigListCommandArgs
    ] = Field(discriminator="command")


class TodosSayCommandArgs(BaseModel):
    command: Literal["say"]
    msg: str


class TodosRootCommandArgs(BaseModel):
    command: Literal[None]


class TodosSaveCommandArgs(BaseModel):
    model_config = ConfigDict(extra="allow")
    command: Literal["save"]
    item: str


class TodosListCommandArgs(BaseModel):
    model_config = ConfigDict(extra="allow")
    command: Literal["list"]


class TodosCommandArgs(BaseModel):
    model_config = ConfigDict(extra="allow")
    command: Literal["todos"]
    args: Union[
        TodosSayCommandArgs,
        TodosSaveCommandArgs,
        TodosListCommandArgs,
        TodosRootCommandArgs
    ] = Field(discriminator="command")


class CommandArgs(BaseModel):
    args: Optional[Union[
        ConfigCommandArgs,
        TodosCommandArgs
    ]] = Field(
        discriminator="command",
        default=None
    )
    verbose: bool = Field(default=False)
