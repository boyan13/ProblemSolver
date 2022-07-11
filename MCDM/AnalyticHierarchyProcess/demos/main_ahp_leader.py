# +====================================================================================================================+
# Internal
from MCDM.AnalyticHierarchyProcess.model import AHPModel, DataModel
# +====================================================================================================================+


if __name__ == '__main__':

    # Expected criteria weights (priority vector):
    #    Experience      -       0.547
    #    Education       -       0.127
    #    Charisma        -       0.270
    #    Age             -       0.056

    DM = DataModel(goal="Choosing a leader.")

    DM.add_criterion('Experience', "Qualitative", "Maximize")
    DM.add_criterion('Education', "Qualitative", "Maximize")
    DM.add_criterion('Charisma', "Qualitative", "Maximize")
    DM.add_criterion('Age', "Qualitative", "Maximize")

    DM.add_alternative('Tom')
    DM.add_alternative('Dick')
    DM.add_alternative('Harris')

    # # Experience
    DM.set_value('Experience', 'Tom', 4)
    DM.set_value('Experience', 'Dick', 8)
    DM.set_value('Experience', 'Harris', 2)
    # Education
    DM.set_value('Education', 'Tom', 6)
    DM.set_value('Education', 'Dick', 1)
    DM.set_value('Education', 'Harris', 7)
    # Charisma
    DM.set_value('Charisma', 'Tom', 9)
    DM.set_value('Charisma', 'Dick', 5)
    DM.set_value('Charisma', 'Harris', 3)
    # Age
    DM.set_value('Age', 'Tom', 3)
    DM.set_value('Age', 'Dick', 2)
    DM.set_value('Age', 'Harris', 1)

    AHP = AHPModel(DM)

    AHP.set_weight('Experience', 'Education', 4)
    AHP.set_weight('Experience', 'Charisma', 3)
    AHP.set_weight('Experience', 'Age', 7)
    AHP.set_weight('Education', 'Charisma', -3)
    AHP.set_weight('Education', 'Age', 3)
    AHP.set_weight('Charisma', 'Age', 5)

    AHP.process(log=True)
