from pydantic import Field, field_validator, model_validator
from manager.config.schema import PydanticFather
from typing import Literal
from pathlib import Path
import re

class Server(PydanticFather):
    root: Path = "/srv/minecraft"
    engine: Literal["MOJANG", "PAPER", "PURPUR", "FABRIC"] = "PURPUR"
    version_type: Literal["release", "snapshot"] = "release"
    version: str = "latest"

    @field_validator("root")
    @classmethod
    def validate_root(cls, value: Path):
        if not value.exists():
            raise ValueError(f"Path {value} for server root not found.")
        if not value.is_dir():
            raise ValueError(f"Path {value} is not a directory.")
        return value

    @model_validator(mode="after")
    def validate_version(self):

        if self.version == "latest":
            return self

        release_pattern = r"^\d+\.\d+(\.\d+)?$"
        snapshot_pattern = r"^\d{2}w\d{2}[a-z]$"

        if self.version_type == "release":
            if not re.match(release_pattern, self.version):
                raise ValueError(
                    f"Invalid release version format: {self.version}"
                )

        elif self.version_type == "snapshot":
            if not re.match(snapshot_pattern, self.version):
                raise ValueError(
                    f"Invalid snapshot version format: {self.version}"
                )

        return self

class Java(PydanticFather):
    min_ram_gb: int =  Field(default=2, ge=1, le=12)
    max_ram_gb: int =  Field(default=4, ge=1, le=12)

    @model_validator(mode="after")
    def validate_ram(self):
        if self.min_ram_gb < 1 or self.max_ram_gb > 12:
            raise ValueError(f"Ram limits are invalid. Enter numbers"
                             "between 1 and 12 "
                             "(size in GB). Your values were:\n"
                             f"Min: {self.min_ram_gb}\n"
                             f"Max: {self.max_ram_gb}")

        if self.max_ram_gb < self.min_ram_gb:
            raise ValueError(
                "max_ram_gb must be greater than or equal to min_ram_gb"
            )

        return self

class World(PydanticFather):
    seed: str | None = None
    view_distance: int = Field(default=6, ge=2, le=15)
    simulation_distance: int = Field(default=4, ge=2, le=15)

    @model_validator(mode="after")
    def validate_distance(self):
        if self.simulation_distance > self.view_distance:
            raise ValueError("Simulation distance cannot exceed view distance.")
        return self

class Network(PydanticFather):
    port: int = Field(default=25565, ge=1024, le=65535)
    online_mode: bool = False

class Gameplay(PydanticFather):
    motd: str = Field( # Server text
        default="Raspberry Pi Minecraft Server",
        min_length=1,
        max_length=59
    )
    max_players: int = Field(default=10, ge=1, le=50)
    difficulty: Literal[
        "peaceful",
        "easy",
        "normal",
        "hard"
    ] = "normal"
    gamemode: Literal[
        "survival",
        "creative",
        "adventure",
        "spectator"
    ] = "survival"
    hardcore: bool = False
    pvp: bool = True

    @model_validator(mode="after")
    def max_players_warning(self):
        if self.max_players > 25:
            print("WARNING: 25+ players may significantly "
                  "reduce performance on Raspberry Pi devices")

class Config(PydanticFather):
    server: Server
    java: Java
    world: World
    network: Network
    gameplay: Gameplay