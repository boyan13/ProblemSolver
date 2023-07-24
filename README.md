# ProblemSolver

### New Bulgarian University
### CSCB803 Decision-Making Systems - Final Project

A tool based on the theory of *Multi-Criterial Decision Making (MCDM)*, implementing the *Analytic Hierarchy Process* method. Step-by-step logging can be toggled on from `EDIT > Toggle logs`. This will cause intermediary calculation steps to print out the states of matrices and other such structures into the console output.

A console demo can be found at `MCDM.AnalyticHierarchyProcess.demos main_ahp_laptop.py`. You can run this script as main as long as the working directory remains the project root or you move the script there.

![main image](readme_imgs/mainA.png)

---

### The Process

#### Step 1
Enter criteria and options among which to choose based on the criteria (alternatives).
![ui demo image 1](readme_imgs/1.png)
#### Step 2
Enter specific values for each criterion, for each alternative.
![ui demo image 2](readme_imgs/2.png)
#### Step 3
Evaluate pair-wise importance. Note that ambiguity in these preference ratings will prevent progress (some ambiguity is allowed but not above a given threshold). 
![ui demo image 3](readme_imgs/3.png)
#### Step 4
Review rankings for each alternative and make a decision.
![ui demo image 4](readme_imgs/4.png)

---

### Demo output (`MCDM.AnalyticHierarchyProcess.demos main_ahp_laptop.py`)

![console demo image 1](readme_imgs/o1.png)
![console demo image 2](readme_imgs/o2.png)
![console demo image 3](readme_imgs/o3.png)
![console demo image 4](readme_imgs/o4.png)
![console demo image 5](readme_imgs/o5.png)
![console demo image 6](readme_imgs/o6.png)
![console demo image 7](readme_imgs/o7.png)
![console demo image 8](readme_imgs/o8.png)
