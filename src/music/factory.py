from .player import Player
from .radio import Radio


def get_player(medium: str):
    if medium == "file":
        return Player()
    elif medium == "url":
        return Radio()
    else:
        assert False