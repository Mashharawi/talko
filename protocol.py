"""Definition of the communication protocol between the clients and servers.

Two server types are supported:
    1. BroadcastServer
    2. DataServer

The BroadcastServer broadcasts conversation messages between users in real time
via a streaming protocol. It communicates with clients by sending and receiving
BroadcastRequests only. Neither the client nor the server send back a response
for these requests.

The DataServer reads and writes data into the database. It communicates with
clients via standard request/response based protocol. The clients send the 
server *Requests and the server always responds back with *Responses.
"""

import dataclasses
from typing import List


def _parse_field(type_, value):
    return type_.from_json(value) if isinstance(value, dict) else value


class _Serializable:
    """A base class which implements JSON serialization for dataclasses."""

    def to_json(self):
        """Returns a JSON object representation of itself."""
        return dataclasses.asdict(self)

    @classmethod
    def from_json(cls, json):
        """Creates a new instance from the given JSON object."""
        kwargs = {}
        for field in dataclasses.fields(cls):
            type_, name, value = field.type, field.name, json[field.name]
            if isinstance(value, list):
                type_ = type_.__args__[0]
                kwargs[name] = [_parse_field(type_, v) for v in value]
            else:
                kwargs[name] = _parse_field(type_, value)
        return cls(**kwargs)
                    


@dataclasses.dataclass(frozen=True)
class BroadcastRequest(_Serializable):
    """Request used for real time conversation message streaming."""
    chat_id: int
    user_id: int
    user_name: str
    message_text: str


# The classes below define the request/response based communication protocol 
# between clients and servers.
@dataclasses.dataclass(frozen=True)
class User(_Serializable):
    user_id: int
    user_name: str


@dataclasses.dataclass(frozen=True)
class Chat(_Serializable):
    chat_id: int
    chat_name: str


@dataclasses.dataclass(frozen=True)
class Message(_Serializable):
    message_id: int
    chat_id: int
    user_id: int
    message_text: str
    message_ts: int


@dataclasses.dataclass(frozen=True)
class InsertUserRequest(_Serializable):
    user_name: str


@dataclasses.dataclass(frozen=True)
class InsertUserResponse(_Serializable):
    user_id: int


@dataclasses.dataclass(frozen=True)
class GetChatsRequest(_Serializable):
    user_id: int


@dataclasses.dataclass(frozen=True)
class GetChatsResponse(_Serializable):
    chats: List[Chat]


@dataclasses.dataclass(frozen=True)
class InsertChatRequest(_Serializable):
    chat_name: str
    user_ids: List[int]


@dataclasses.dataclass(frozen=True)
class InsertChatResponse(_Serializable):
    chat_id: int


@dataclasses.dataclass(frozen=True)
class GetParticipantsRequest(_Serializable):
    chat_id: int


@dataclasses.dataclass(frozen=True)
class GetParticipantsResponse(_Serializable):
    users: List[User]


@dataclasses.dataclass(frozen=True)
class GetMessagesRequest(_Serializable):
    chat_id: int


@dataclasses.dataclass(frozen=True)
class GetMessagesResponse(_Serializable):
    messages: List[Message] 


@dataclasses.dataclass(frozen=True)
class InsertMessageRequest(_Serializable):
    chat_id: int
    user_id: int
    message_text: str
    message_timestamp: int


@dataclasses.dataclass(frozen=True)
class InsertMessageResponse(_Serializable):
    message_id: int
