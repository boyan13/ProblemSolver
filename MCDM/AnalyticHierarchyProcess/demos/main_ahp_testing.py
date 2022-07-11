# +====================================================================================================================+
# Internal
from MCDM.AnalyticHierarchyProcess.model import AHPModel, DataModel
# +====================================================================================================================+


if __name__ == '__main__':

    DM = DataModel()

    DM.add_criterion('price', "Quantitative", "Minimize")
    DM.add_criterion('power', "Quantitative", "Maximize")

    DM.add_alternative('Barbosa')
    DM.add_alternative('Jack')
    DM.add_alternative('SaoFeng')

    alternatives = ('Barbosa', 'Jack', 'SaoFeng')

    for a, v in zip(alternatives, [100, 10, 9.9]):
        DM.set_value('price', a, v)

    for a, v in zip(alternatives, [100, 60, 60]):
        DM.set_value('power', a, v)

    AHP = AHPModel(DM)

    AHP.set_weight('price', 'power', 9)

    AHP.process(log=True)
