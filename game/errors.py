from typing import TypedDict


class HttpError(Exception):

    class Message(TypedDict):
        text: str

    def __init__(self, status, message):
        self.message = message
        self.status = status


class UsernameOccupiedError(HttpError):
    def __init__(self, username: str):
        super(UsernameOccupiedError, self).__init__(
            status=403,
            message={"text": f"username \"{username}\" already occupied"}
        )
