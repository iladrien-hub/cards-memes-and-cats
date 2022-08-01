import asyncio
import logging
from pathlib import Path

from aiohttp import web

from .. import security
from ..misc import handler, json_response
from ..repository.roomrepository import RoomRepository
from ..room import Room, Player

PATH_PREFIX = Path("/api/v0")


@handler(path=PATH_PREFIX)
async def index(request):
    return json_response({"status": "ok"})


@handler(path=PATH_PREFIX / "room/list")
async def room_list(request):
    data = request.rel_url.query

    return json_response([
        i.as_dict() for i in RoomRepository.list(
            offset_id=int(data.get('offset_id', 0)),
            limit=data.get('limit', 10)
        )
    ])


@handler(path=PATH_PREFIX / "room/create", method=web.post, required_params=("name",))
async def create_room(request):
    data = await request.post()
    room = RoomRepository.create(name=data['name'])

    asyncio.create_task(room.start())

    return json_response({"room_id": room.id})


@handler(path=PATH_PREFIX / "room/join", method=web.post, required_params=("username", "room_id"))
async def join_room(request):
    data = await request.post()

    room = RoomRepository.get(int(data['room_id']))
    p = room.register_player(data['username'])

    return json_response({
        "token": security.generate_token({
            "pid": p.id,
            "rid": room.id
        })
    })


@handler(path=PATH_PREFIX / "room/leave", method=web.post, authorized=True)
async def leave_room(room: Room, player: Player, request):
    await room.disconnect_player(player, "left")

    return json_response({})


@handler(path=PATH_PREFIX / "room/start", method=web.post, authorized=True)
async def start_game(room: Room, player: Player, request):
    await room.start_game(player)

    return json_response({})


@handler(path=PATH_PREFIX / "game/move", method=web.post, authorized=True, required_params=('card_type', 'card_id'))
async def make_move(room: Room, player: Player, request):
    data = await request.post()
    await room.make_move(player, data['card_type'], int(data['card_id']))
    return json_response({})


@handler(path=PATH_PREFIX / "subscribe/{token}")
async def subscribe(request):
    token = request.match_info['token']
    token_data = security.check_token(token)

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    try:
        room = RoomRepository.get(token_data['rid'])
        player = room.get_player(token_data['pid'])

        player.ws = ws
        await room.connect_player(player)

        try:
            await player.finish_event

        except asyncio.exceptions.CancelledError:
            await room.disconnect_player(player, "connection lost")

    except BaseException as e:
        logging.exception("", exc_info=e)

    return ws
