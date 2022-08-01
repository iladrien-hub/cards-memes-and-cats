from typing import Dict

from ..errors import HttpError
from ..room import Room


class RoomRepository:
    __next_pk = 10_000

    __rooms: Dict[int, Room] = dict()
    __room_name_idx: Dict[str, int] = dict()

    @classmethod
    def get(cls, _id: int) -> Room:
        if _id not in cls.__rooms:
            raise HttpError(status=404, message=HttpError.Message(text="room not found"))

        return cls.__rooms[_id]

    @classmethod
    def create(cls, name: str):
        _id = cls.__next_pk
        cls.__next_pk += 1

        if name in cls.__room_name_idx:
            raise HttpError(status=403, message=HttpError.Message(text=f"room with name \"{name}\" already exists"))

        room = Room(_id, name, cls.remove)
        cls.__rooms[room.id] = room
        cls.__room_name_idx[room.name] = room.id

        return room

    @classmethod
    def list(cls, offset_id: int, limit: int):
        rooms_iter = iter(cls.__rooms.values())
        try:
            if offset_id:
                while next(rooms_iter).id != offset_id:
                    pass

            for _, room in zip(range(limit), rooms_iter):
                yield room

        except StopIteration:
            pass

    @classmethod
    def remove(cls, room: Room):
        cls.__rooms.pop(room.id)
        cls.__room_name_idx.pop(room.name)
