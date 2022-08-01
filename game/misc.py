import pathlib
from typing import Callable

import ujson
from aiohttp import web

from . import security
from .errors import HttpError
from .repository.roomrepository import RoomRepository


def json_response(data, *, status: int = 200, success=True):
    return web.json_response({"success": success, "data": data}, status=status, dumps=ujson.dumps)


def handler(
    *,
    path: pathlib.PurePath,
    method: Callable = web.get,
    required_params: tuple = tuple(),
    authorized: bool = False
):
    def _decor(func):

        async def _wrapper(r: web.Request) -> web.Response:
            try:
                if required_params:
                    data = await r.post()
                    missed_params = [i for i in required_params if i not in data]

                    if missed_params:
                        raise HttpError(
                            status=400,
                            message={"text": "missed required parameters", "params": missed_params}
                        )

                if authorized:
                    token = r.headers['authorization']
                    token_data = security.check_token(token)

                    room = RoomRepository.get(token_data['rid'])
                    player = room.get_player(token_data['pid'])

                    return await func(room, player, r)
                return await func(r)

            except HttpError as e:
                return json_response({"type": type(e).__name__, "message": e.message}, status=e.status, success=False)

            except BaseException as e:
                return json_response({"type": type(e).__name__, "message": str(e)}, status=500, success=False)

        return method(path.as_posix(), _wrapper)

    return _decor
