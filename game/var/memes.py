import copy
from typing import List

from ..models import MemeCard

_cards = [
    MemeCard(url=f"meme-{i}") for i in range(100)
]


def get() -> List[MemeCard]:
    return copy.deepcopy(_cards)