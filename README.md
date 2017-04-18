# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: The naked twins constraint specifies that if two boxes in a unit in sudoku share exactly two common values, no other boxes in the same unit can have those two values.  The two boxes that share exactly two common values are 'naked twins'.

Constraint propagation is the principle of simplifying the number of possible solutions for a given problem, by applying a 'constraint' to a set of nodes in a problem and ensuring logical consistency between these nodes. To apply the naked twins constraint to a given unit in sudoku, we iterate over all the boxes in the unit other than the naked twin boxes, and remove from the possible values for a unit the value of the naked twin(s) in that unit.  The removal of a possible value of a box is what we refer to as 'propagation' of a constraint, which helps us to reduce the number of solutions hence simplifying the problem.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: By considering each diagonal as a distinct unit, it is possible to ensure that no
value repeats in a diagonal, which simplifies the number of possible values a given
box can have.   Constraint propagation in this case ensures a sudoku board that has
no repeats along the diagonal and only boards with no repeats along the diagonal will be produced
by agents that use this constraint.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project.
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.
