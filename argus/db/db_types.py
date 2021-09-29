from enum import Enum
from typing import Any, Union, Type, TypeVar
from pydantic.dataclasses import dataclass
from pydantic import validator, ValidationError
import re

T = TypeVar("T")


@dataclass
class ArgusUDTBase:

    def __post_init_post_parse__(self):
        self.__class__._typename = None


@dataclass(init=True, repr=True)
class NodeDescription(ArgusUDTBase):
    name: str
    ip: str
    shards: int

    @classmethod
    def from_db_udt(cls, udt):
        return cls(name=udt.name, ip=udt.ip, shards=udt.shards)

    @validator("ip")
    def valid_ip_address(cls, v):
        ip_addr_re = r"(\d{1,3}\.){3}\d{1,3}"
        if not re.match(ip_addr_re, v):
            raise ValidationError(f"Not a valid ip address: {v}")

        ip_by_octets = [int(octet) for octet in v.split(".") if int(octet) <= 255]
        if len(ip_by_octets) != 4:
            raise ValidationError(f"Octets out of range (0, 255): {v}")

        return v


@dataclass(init=True, repr=True)
class PackageVersion(ArgusUDTBase):
    name: str
    version: str
    date: str
    revision_id: str

    @classmethod
    def from_db_udt(cls, udt):
        return cls(name=udt.name, version=udt.version, date=udt.date, revision_id=udt.revision_id)


class NemesisStatus(str, Enum):
    Started = "started"
    Running = "running"
    Failed = "failed"
    Succeeded = "succeeded"


class TestStatus(str, Enum):
    Created = "created"
    Failed = "failed"
    Passed = "passed"


@dataclass(init=True, repr=True)
class NemesisRunInfo(ArgusUDTBase):
    class_name: str
    nemesis_name: str
    duration: int
    target_node: NodeDescription
    status: str
    start_time: int
    end_time: int = 0
    stack_trace: str = ""

    @classmethod
    def from_db_udt(cls, udt):
        target_node = NodeDescription.from_db_udt(udt.target_node)
        return cls(class_name=udt.class_name, nemesis_name=udt.nemesis_name, duration=udt.duration,
                   target_node=target_node, status=udt.status, start_time=udt.start_time, end_time=udt.end_time,
                   stack_trace=udt.stack_trace)


@dataclass(init=True, repr=True)
class EventsBySeverity(ArgusUDTBase):
    severity: str
    event_amount: int
    last_events: list[str]

    @classmethod
    def from_db_udt(cls, udt):
        return cls(severity=udt.severity, event_amount=udt.event_amount, last_events=udt.last_events)


TypeHint = TypeVar("TypeHint")


@dataclass(init=True, repr=True)
class CollectionHint:
    stored_type: TypeHint


@dataclass(init=True, repr=True)
class ColumnInfo:
    name: str
    type: Type[Union[CollectionHint, int, str, T]]
    value: Any
    constraints: list[str]