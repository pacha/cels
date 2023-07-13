from dataclasses import asdict
from dataclasses import dataclass

from dacite import from_dict


@dataclass
class Baz:
    spam: str
    eggs: str

    def __init__(self, spam: str):
        self.spam = spam
        self.eggs = spam * 3

    @classmethod
    def from_dict(cls, data: dict):
        @dataclass
        class Params:
            spam: str

        params = from_dict(Params, data)
        return cls(**asdict(params))
