import dataclasses

EVENT_TYPE_ROOM_CLOSED = (0, "RoomClosed")
EVENT_TYPE_PLAYER_JOINED = (1, "PlayerJoined")
EVENT_TYPE_PLAYER_LEFT = (2, "PlayerLeft")
EVENT_TYPE_SET_ADMIN = (3, "SetAdmin")
EVENT_TYPE_GAME_STARTED = (4, "GameStarted")
EVENT_TYPE_CLEAR_CARDS = (5, "ClearCards")
EVENT_TYPE_GIVE_CARD = (6, "GiveCard")
EVENT_TYPE_YOUR_TURN = (7, "YourTurn")
EVENT_TYPE_PLAYER_MADE_MOVE = (8, "PlayerMadeMove")
EVENT_TYPE_REMOVE_CARD = (9, "RemoveCard")


@dataclasses.dataclass
class Event:
    type: tuple
    data: dict = dataclasses.field(default_factory=dict)


def room_closed(reason: str, timeout: int):
    return Event(type=EVENT_TYPE_ROOM_CLOSED, data={
        "reason" : reason,
        "timeout": timeout
    })


def player_joined(player, players_list):
    return Event(type=EVENT_TYPE_PLAYER_JOINED, data={
        "player": player,
        "list"  : players_list
    })


def player_left(player, reason, players_list):
    return Event(type=EVENT_TYPE_PLAYER_LEFT, data={
        "player": player,
        "reason": reason,
        "list"  : players_list
    })


def set_admin(player):
    return Event(type=EVENT_TYPE_SET_ADMIN, data={"player": player})


def game_started(initiator):
    return Event(type=EVENT_TYPE_GAME_STARTED, data={"initiator": initiator})


def clear_cards():
    return Event(type=EVENT_TYPE_CLEAR_CARDS)


def give_card(card_type: str, data: dict):
    return Event(type=EVENT_TYPE_GIVE_CARD, data={
        "type": card_type,
        "card": data
    })


def your_turn(turn_type: str):
    return Event(type=EVENT_TYPE_YOUR_TURN, data={
        "turn_type": turn_type
    })


def player_made_move(player: dict | object, turn_type: str, card: dict | object):
    return Event(type=EVENT_TYPE_PLAYER_MADE_MOVE, data={
        "player"   : player,
        "turn_type": turn_type,
        "card"     : card
    })


def remove_card(card_type: str, card_id: int):
    return Event(type=EVENT_TYPE_REMOVE_CARD, data={
        "card_type": card_type,
        "card_id"  : card_id
    })
