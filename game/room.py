import asyncio
import dataclasses
import logging
import random
from collections import deque
from typing import Optional, Dict, Callable, List, Deque, Tuple

import ujson
from aiohttp.web_ws import WebSocketResponse

from . import events
from .errors import HttpError
from .events import Event
from .models import JokeCard, MemeCard
from .var import jokes, memes


@dataclasses.dataclass
class Player:
    id: int
    username: str

    finish_event: asyncio.Future

    ws: Optional[WebSocketResponse] = None
    jokes: List[JokeCard] = dataclasses.field(default_factory=list)
    memes: List[MemeCard] = dataclasses.field(default_factory=list)

    def __str__(self):
        return f"Player(id={self.id}, username={self.username})"

    def format_dict(self, p: 'Player', admin: bool):
        return {
            "id"      : p.id,
            "username": p.username,
            "self"    : self == p,
            "admin"   : admin
        }

    async def send_event(self, evt: Event):
        try:
            await self.ws.send_str(ujson.dumps(dataclasses.asdict(evt)))
        except BaseException as e:
            logging.warning(f"failed to send event to {self}: {e}")

    async def clear(self):
        self.jokes.clear()
        self.memes.clear()

        await self.send_event(events.clear_cards())

    async def give_joke(self, card: JokeCard):
        self.jokes.append(card)
        await self.send_event(events.give_card("joke", dataclasses.asdict(card)))

    async def give_meme(self, card: MemeCard):
        self.memes.append(card)
        await self.send_event(events.give_card("meme", dataclasses.asdict(card)))

    async def get_card(self, card_type: str, card_id: int):
        l = {"meme": self.memes, "joke": self.jokes}[card_type]
        return {i.id: i for i in l}.get(card_id)

    async def remove_card(self, card_type: str, card: object):
        l = {"meme": self.memes, "joke": self.jokes}[card_type]
        l.remove(card)

        await self.send_event(events.remove_card(card_type, card.id))



class Room:
    __ROOM_IDLE_TIMEOUT = 600
    __STOP_EVENT = object()

    def __init__(self, id: int, name: str, on_finish: Callable):
        self.id = id
        self.name = name

        self._event_q: asyncio.Queue = asyncio.Queue()
        self._task: Optional[asyncio.Task] = None

        self._waiting_players: Dict[int, Player] = dict()
        self._players: Dict[int, Player] = dict()
        self._admin: Optional[Player] = None

        self._next_player_id: int = 0

        self._logger: logging.Logger = logging.getLogger(f"Room[#{id}]")
        self._on_finish: Callable = on_finish

        self._is_started: bool = False

        self._jokes: Optional[List[JokeCard]] = None
        self._memes: Optional[List[MemeCard]] = None

        self._players_deque: Optional[Deque] = None
        self._next_move: Optional[Tuple[Player, str]] = None

    # region: Management Methods

    def as_dict(self) -> dict:
        return {
            "room_id": self.id,
            "name"   : self.name
        }

    async def start(self):
        self._task = asyncio.create_task(self._run())

    async def stop(self):
        if self._task:
            await self._event_q.put(self.__STOP_EVENT)
            await self._task

    # endregion

    # region: Player Management Methods

    def register_player(self, username: str) -> Player:
        self._next_player_id += 1

        p = Player(username=username, id=self._next_player_id, finish_event=asyncio.Future())
        self._waiting_players[p.id] = p

        return p

    def get_player(self, player_id: int) -> Player:
        if player_id in self._players:
            return self._players[player_id]
        return self._waiting_players[player_id]

    async def connect_player(self, player: Player):
        del self._waiting_players[player.id]
        self._players[player.id] = player
        self._logger.info(f"{player} connected")

        for p in self._players.values():
            await p.send_event(events.player_joined(
                player=p.format_dict(player, admin=self._admin == player),
                players_list=[p.format_dict(i, admin=self._admin == i) for i in self._players.values()]
            ))

        await self._ensure_admin()

    async def disconnect_player(self, player: Player, reason: str):
        if self._admin == player:
            self._admin = None

        if player.id in self._players:
            for p in self._players.values():
                await p.send_event(events.player_left(
                    player=p.format_dict(player, player == self._admin),
                    reason=reason,
                    players_list=[p.format_dict(i, i == self._admin) for i in self._players.values() if i != player]
                ))

            self._players.pop(player.id)

            if reason != 'connection lost':
                player.finish_event.set_result(None)

        if player.id in self._waiting_players:
            del self._waiting_players[player.id]

        self._logger.info(f"{player} disconnected")

        await self._ensure_admin()

    async def _ensure_admin(self):
        if not self._players:
            await self.stop()
            return

        if self._admin is None:
            self._admin = next(iter(self._players.values()))
            self._logger.info(f"admin changed: {self._admin}")

            for p in self._players.values():
                await p.send_event(events.set_admin(p.format_dict(self._admin, True)))

    # endregion

    # region: Game

    async def fire_event(self, event: Event):
        for p in self._players.values():
            await p.send_event(event)

    async def start_game(self, player: Player):
        if player != self._admin:
            raise HttpError(status=403, message=HttpError.Message(text="not permitted"))

        if len(self._players) < 2:
            raise HttpError(status=403, message=HttpError.Message(text="not enough players"))

        self._is_started = True
        await self._event_q.put(events.game_started(player.username))

    async def make_move(self, player: Player, card_type: str, card_id: int):
        if (player, card_type) != self._next_move:
            raise HttpError(status=400, message=HttpError.Message(text="wrong move"))

        card = await player.get_card(card_type, card_id)
        if not card:
            raise HttpError(status=403, message=HttpError.Message(text="not permitted"))

        await self._event_q.put(events.player_made_move(
            player,
            card_type,
            card
        ))

    # endregion

    # region: Events Handling

    async def _handle_start_game_event(self, evt: Event):
        await self.fire_event(evt)

        self._memes = memes.get()
        self._jokes = jokes.get()

        random.shuffle(self._memes)
        random.shuffle(self._jokes)

        for p in self._players.values():
            await p.clear()

            for _ in range(3):
                await p.give_joke(self._jokes.pop())
                await p.give_meme(self._memes.pop())

        self._players_deque = deque(list(self._players.values()))

        await self._players_deque[0].send_event(events.your_turn("meme"))
        self._next_move = (self._players_deque[0], "meme")

    async def _handle_move(self, evt: Event):
        player = evt.data['player']
        await player.remove_card(evt.data['turn_type'], evt.data['card'])

        for p in self._players.values():
            await p.send_event(events.player_made_move(
                player=p.format_dict(player, player == self._admin),
                turn_type=evt.data['turn_type'],
                card=dataclasses.asdict(evt.data['card'])
            ))

        if evt.data['turn_type'] == 'joke':
            await player.give_joke(self._jokes.pop())
            await self._players_deque[0].send_event(events.your_turn("meme"))
            self._next_move = (self._players_deque[0], "meme")

        else:
            await player.give_meme(self._memes.pop())

            self._players_deque.rotate(1)
            await self._players_deque[0].send_event(events.your_turn("joke"))
            self._next_move = (self._players_deque[0], "joke")

    # endregion

    async def _get_next_event(self):
        return await asyncio.wait_for(self._event_q.get(), timeout=self.__ROOM_IDLE_TIMEOUT)

    async def _run(self):
        self._logger.info("starting processing event queue...")

        try:
            while (evt := await self._get_next_event()) != self.__STOP_EVENT:
                if evt.type == events.EVENT_TYPE_GAME_STARTED:
                    await self._handle_start_game_event(evt)

                elif evt.type == events.EVENT_TYPE_PLAYER_MADE_MOVE:
                    await self._handle_move(evt)

                else:
                    print(evt)

            else:
                self._logger.info("received finish event...")

        except asyncio.exceptions.TimeoutError:
            self._logger.info("room was idle for a long time. finishing...")

            e = events.room_closed(
                reason=f"{self.__ROOM_IDLE_TIMEOUT}sec idle timeout",
                timeout=self.__ROOM_IDLE_TIMEOUT
            )

            for idx, player in self._players.items():
                await player.send_event(e)
                player.finish_event.set_result(None)

        except BaseException as e:
            self._logger.exception("", exc_info=e)

        finally:
            self._on_finish(self)
            self._logger.info("room has been finished successfully")
