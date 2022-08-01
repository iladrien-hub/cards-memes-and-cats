import copy
from typing import List

from ..models import JokeCard

_cards = [
    JokeCard(text=f"joke-{i}", accent="") for i in range(100)
]


def get() -> List[JokeCard]:
    return copy.deepcopy(_cards)


