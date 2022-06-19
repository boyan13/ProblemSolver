class Alternative:
    def __init__(self, name: str, criteria: dict):
        self.__name = name
        self.criteria = criteria

    @classmethod
    def are_comparable(cls, alternative1: "Alternative", alternative2: "Alternative") -> bool:
        a1 = {k: type(v) for k, v in alternative1.criteria.items()}
        a2 = {k: type(v) for k, v in alternative2.criteria.items()}
        return a1 == a2
