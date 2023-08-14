from pydantic import BaseModel

from ..type import FineTune

_FINE_TUNES_REPO = {}


class FineTuneRepo(BaseModel):

    @staticmethod
    def get(id: str):
        return _FINE_TUNES_REPO.get(id)
    

    @staticmethod
    def add(fine_tune: FineTune):
        _FINE_TUNES_REPO[fine_tune.id] = fine_tune


    @staticmethod
    def getAll():
        return list(_FINE_TUNES_REPO.values())