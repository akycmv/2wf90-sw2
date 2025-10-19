##
# 2WF90 Algebra for Security -- Software Assignment 2
# Polynomial and Finite Field Arithmetic
# solve.py
#
#
# Group number:
# 17
#
# Author names and student IDs:
# Aleksey Chumakov (2077019)
# Dora Tunç (2112108)
# Alp Akin (2079240)
# Guney Kabel (2135140)
##

# Import built-in json library for handling input/output
import json


def solve_exercise(exercise_location: str, answer_location: str):
    """
    solves an exercise specified in the file located at exercise_location and
    writes the answer to a file at answer_location. Note: the file at
    answer_location might not exist yet and, hence, might still need to be created.
    """

    # Open file at exercise_location for reading.
    with open(exercise_location, "r") as exercise_file:
        # Deserialize JSON exercise data present in exercise_file to corresponding Python exercise data
        exercise = json.load(exercise_file)

    ### Parse and solve ###

    # Check type of exercise
    # TODO: check function params
    # TODO: exercise match


# You can call your function from here
# Please do not *run* code outside this block
# You can however define other functions or constants
if __name__ == "__main__":
    solve_exercise("Simple/Exercises/exercise0.json", "Simple/Answers/answer0.json")
