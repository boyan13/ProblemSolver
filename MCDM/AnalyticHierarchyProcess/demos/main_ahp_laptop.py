# +====================================================================================================================+
# Internal
from MCDM.AnalyticHierarchyProcess.model import AHPModel, DataModel
# +====================================================================================================================+


if __name__ == '__main__':

    # Expected criteria weights (priority vector):
    #       Price           -       0.6038
    #       Storage         -       0.1365
    #       Camera          -       0.1958
    #       Looks           -       0.0646

    DM = DataModel(goal="Finding the best laptop.")

    # Criteria
    DM.add_criterion('Price', "Quantitative", "Minimize")
    DM.add_criterion('Storage', "Quantitative", "Maximize")
    DM.add_criterion('Camera', "Qualitative", "Maximize")
    DM.add_criterion('Looks', "Qualitative", "Maximize")

    # Alternatives
    DM.add_alternative('Laptop1')
    DM.add_alternative('Laptop2')
    DM.add_alternative('Laptop3')

    # Values
    DM.set_value('Price', 'Laptop1', 400.0)
    DM.set_value('Price', 'Laptop2', 200.0)
    DM.set_value('Price', 'Laptop3', 100.0)

    DM.set_value('Storage', 'Laptop1', 1024)
    DM.set_value('Storage', 'Laptop2', 516)
    DM.set_value('Storage', 'Laptop3', 256)

    DM.set_value('Camera', 'Laptop1', 6)
    DM.set_value('Camera', 'Laptop2', 5)
    DM.set_value('Camera', 'Laptop3', 3)

    DM.set_value('Looks', 'Laptop1', 8)
    DM.set_value('Looks', 'Laptop2', 9)
    DM.set_value('Looks', 'Laptop3', 5)

    AHP = AHPModel(DM)
    AHP.set_logging(True)

    AHP.set_weight('Price', 'Storage', 5)
    AHP.set_weight('Price', 'Camera', 4)
    AHP.set_weight('Price', 'Looks', 7)
    AHP.set_weight('Storage', 'Camera', -2)
    AHP.set_weight('Storage', 'Looks', 3)
    AHP.set_weight('Camera', 'Looks', 3)

    AHP.process()
