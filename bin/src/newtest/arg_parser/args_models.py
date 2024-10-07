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


class NewtestSayCommandArgs(BaseModel):
    command: Literal["say"]
    msg: str

class NewtestRootCommandArgs(BaseModel):
    command: Literal[None]


class NewtestSaveCommandArgs(BaseModel):
    model_config = ConfigDict(extra="allow")
    command: Literal["save"]
    item: str

class NewtestListCommandArgs(BaseModel):
    model_config = ConfigDict(extra="allow")
    command: Literal["list"]


class NewtestCommandArgs(BaseModel):
    model_config = ConfigDict(extra="allow")
    command: Literal["newtest"]
    args: Union[
        NewtestSayCommandArgs,
        NewtestSaveCommandArgs,
        NewtestListCommandArgs,
        NewtestRootCommandArgs
    ] = Field(discriminator="command")


class CommandArgs(BaseModel):
    args: Optional[Union[
        ConfigCommandArgs,
        NewtestCommandArgs
    ]] = Field(
        discriminator="command",
        default=None
    )
    verbose: bool = Field(default=False)