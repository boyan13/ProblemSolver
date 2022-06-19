class BaseCriteria:

    def __init__(self, name):
        self.__name = name


class QualitativeCrieria(BaseCriteria):
    pass


class DiscreteQuantitativeCriteria(BaseCriteria):
    pass


class ContinuousQuantitativeCriteria(BaseCriteria):
    pass


class WeightedCriteria(BaseCriteria):
    pass


class Ranking(BaseCriteria):
    pass
