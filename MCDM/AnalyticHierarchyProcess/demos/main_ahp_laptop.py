# +====================================================================================================================+
# Internal
from MCDM.AnalyticHierarchyProcess.model import AHPModel, DataModel
# +====================================================================================================================+


if __name__ == '__main__':

    # Expected criteria weights (priority vector):
    #    Price           -       0.6038
    #    Storage         -       0.1365
    #    Camera          -       0.1958
    #    Looks           -       0.0646

    DM = DataModel(goal="Finding the best laptop.")

    DM.add_criterion('Price', "Quantitative", "Minimize")
    DM.add_criterion('Storage', "Quantitative", "Maximize")
    DM.add_criterion('Camera', "Quantitative", "Maximize")
    DM.add_criterion('Looks', "Qualitative", "Maximize")

    AHP = AHPModel(DM)

    AHP.set_weight('Price', 'Storage', 5)
    AHP.set_weight('Price', 'Camera', 4)
    AHP.set_weight('Price', 'Looks', 7)
    AHP.set_weight('Storage', 'Camera', -2)
    AHP.set_weight('Storage', 'Looks', 3)
    AHP.set_weight('Camera', 'Looks', 3)

    AHP.process(log=True)
