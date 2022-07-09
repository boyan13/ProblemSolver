# +====================================================================================================================+
# Internal
from MCDM.AnalyticHierarchyProcess.model import AHPModel
# +====================================================================================================================+


if __name__ == '__main__':

    # Expected criteria weights (priority vector):
    #    Experience      -       0.547
    #    Education       -       0.127
    #    Charisma        -       0.270
    #    Age             -       0.056

    AHP = AHPModel(goal="Finding the best laptop.")
    AHP = AHPModel(goal="Finding the best laptop.")

    AHP.add_criteria('Experience', "Qualitative", "Maximize")
    AHP.add_criteria('Education', "Qualitative", "Maximize")
    AHP.add_criteria('Charisma', "Qualitative", "Maximize")
    AHP.add_criteria('Age', "Quantitative", "Minimize")

    AHP.set_weight('Experience', 'Education', 4)
    AHP.set_weight('Experience', 'Charisma', 3)
    AHP.set_weight('Experience', 'Age', 7)
    AHP.set_weight('Education', 'Charisma', -3)
    AHP.set_weight('Education', 'Age', 3)
    AHP.set_weight('Charisma', 'Age', 5)

    AHP.process(log=True)
