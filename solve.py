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

# polynomial arithmetic handlers
import polynomial.solve as poly_solve
import finite.solve as fin_solve


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
    if not __is_valid(exercise):
        answer = {"answer": None}
        if "task" in exercise and exercise["task"] == "extended_euclidean_algorithm":
            answer = {"answer-a": None, "answer-b": None, "answer-gcd": None}
        elif "task" in exercise and exercise["task"] == "long_division":
            answer = {"answer-q": None, "answer-r": None}
    else:
        answer = __parse_solve(exercise)
    with open(answer_location, "w") as answer_file:
        json.dump(answer, answer_file, indent=4)


def __is_valid(exercise: dict[str, list[int] | int]) -> bool:
    """
    Verifies that exercise is valid and basic preconditions hold (primes, degrees).
    Performs a conservative set of checks based on the assignment specification.

    Returns True iff the input satisfies the structural and domain constraints
    described in the assignment document. Otherwise returns False.
    """

    # check integer is prime
    def is_prime(n: int) -> bool:
        if not isinstance(n, int) or n < 2:
            return False
        if n % 2 == 0:
            return n == 2
        r = int(n**0.5) + 1
        for a in range(3, r, 2):
            if n % a == 0:
                return False
        return True

    if "type" not in exercise or "task" not in exercise:
        return False

    allowed = [
        ("polynomial_arithmetic", "addition"),
        ("polynomial_arithmetic", "subtraction"),
        ("polynomial_arithmetic", "multiplication"),
        ("polynomial_arithmetic", "long_division"),
        ("polynomial_arithmetic", "extended_euclidean_algorithm"),
        ("polynomial_arithmetic", "irreducibility_check"),
        ("polynomial_arithmetic", "irreducible_element_generation"),
        ("finite_field_arithmetic", "addition"),
        ("finite_field_arithmetic", "subtraction"),
        ("finite_field_arithmetic", "multiplication"),
        ("finite_field_arithmetic", "division"),
        ("finite_field_arithmetic", "inversion"),
        ("finite_field_arithmetic", "primitivity_check"),
        ("finite_field_arithmetic", "primitive_element_generation"),
    ]
    type, task = exercise.get("type"), exercise.get("task")
    typ = (type, task)

    if typ not in allowed:
        return False

    if "integer_modulus" not in exercise:
        return False

    p = exercise.get("integer_modulus")
    if not is_prime(p):
        return False

    if type == "finite_field_arithmetic" and "polynomial_modulus" not in exercise:
        return False

    if task in [
        "irreducible_element_generation",
    ]:
        if "degree" not in exercise:
            return False

    if task in [
        "addition",
        "subtraction",
        "multiplication",
        "divisionlong_division",
        "extended_euclidean_algorithm",
    ]:
        if "f" not in exercise or "g" not in exercise:
            return False

    if task in ["irreducibility_check", "primitivity_check"]:
        if "f" not in exercise:
            return False

    return True


def __parse_solve(
    exercise: dict[str, list[int] | int],
) -> dict[str, list[int] | bool | None]:
    """
    Parses exercise by exercise type and returns result of the computation
    """
    # answer-a, answer-b, answer-gcd - extended euclidean
    # answer-q, answer-r - long division
    # answer - otherwise
    if exercise["type"] == "polynomial_arithmetic":
        return poly_solve.solve(exercise)
    else:
        return fin_solve.solve(exercise)


# You can call your function from here
# Please do not *run* code outside this block
# You can however define other functions or constants
if __name__ == "__main__":
    solve_exercise("in.json", "out.json")
