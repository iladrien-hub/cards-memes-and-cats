import dataclasses
import itertools


@dataclasses.dataclass
class JokeCard:
    text: str
    accent: str

    id: int = dataclasses.field(default_factory=itertools.count().__next__)


@dataclasses.dataclass
class MemeCard:
    url: str

    id: int = dataclasses.field(default_factory=itertools.count().__next__)
