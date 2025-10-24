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
        if exercise["task"] == "extended_euclidean_algorithm":
            answer = {"answer-a": None, "answer-b": None, "answer-gcd": None}
        elif exercise["task"] == "long_division":
            answer = {"answer-q": None, "answer-r": None}
        else:
            answer = {"answer": None}
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

    # helper: check integer is prime (small ranges: deterministic trial division is fine)
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

    # helper: canonical polynomial array check
    # poly must be list of ints, length in [min_len, max_len], coefficients in [0, p-1],
    # and last entry != 0 unless poly == [0].
    def check_poly_array(poly, p, min_len, max_len):
        if not isinstance(poly, list):
            return False
        if len(poly) < min_len or len(poly) > max_len:
            return False
        # entries must be ints
        for c in poly:
            if not isinstance(c, int):
                return False
            if c < 0 or c >= p:
                return False
        # canonical last entry non-zero except for zero polynomial which must be exactly [0]
        if poly == [0]:
            return True
        if poly[-1] == 0:
            return False
        return True

    # helper: is zero polynomial
    def is_zero_poly(poly):
        return isinstance(poly, list) and poly == [0]

    # Basic required keys and types
    if not isinstance(exercise, dict):
        return False
    if (
        "type" not in exercise
        or "task" not in exercise
        or "integer_modulus" not in exercise
    ):
        return False
    typ = exercise["type"]
    task = exercise["task"]
    p = exercise["integer_modulus"]

    # type and task must be strings
    if not isinstance(typ, str) or not isinstance(task, str):
        return False
    # integer_modulus must be int
    if not isinstance(p, int):
        return False

    # Determine modulus range depending on task
    small_tasks = {
        "irreducibility_check",
        "irreducible_element_generation",
        "primitivity_check",
        "primitive_element_generation",
    }
    if task in small_tasks:
        if p < 2 or p > 13:
            return False
    else:
        if p < 2 or p > 509:
            return False

    # modulus must be prime
    if not is_prime(p):
        return False

    # Validate type/task combinations allowed by spec
    poly_tasks = {
        "addition",
        "subtraction",
        "multiplication",
        "long_division",
        "extended_euclidean_algorithm",
        "irreducibility_check",
        "irreducible_element_generation",
    }
    fin_tasks = {
        "addition",
        "subtraction",
        "multiplication",
        "division",
        "inversion",
        "primitivity_check",
        "primitive_element_generation",
    }

    if typ == "polynomial_arithmetic":
        if task not in poly_tasks:
            return False
    elif typ == "finite_field_arithmetic":
        if task not in fin_tasks:
            return False
    else:
        return False

    # lower bound is always 1
    def poly_len_bound_poly_arith(is_mul: bool):
        return 1, (129 if is_mul else 257)

    poly_mod = None
    if typ == "finite_field_arithmetic":
        if "polynomial_modulus" not in exercise:
            return False
        poly_mod = exercise["polynomial_modulus"]
        if not isinstance(poly_mod, list):
            return False
        for c in poly_mod:
            if not isinstance(c, int) or c < 0 or c >= p:
                return False
        if poly_mod == []:
            return False
        if poly_mod[-1] == 0:
            return False
        len_h = len(poly_mod)
        if task == "multiplication":
            if len_h < 1 or len_h > 129:
                return False
        elif task in {"primitivity_check", "primitive_element_generation"}:
            if len_h < 2 or len_h > 7:
                return False
        else:
            if len_h < 2 or len_h > 257:
                return False

        deg_h = len_h - 1
        if task in {
            "addition",
            "subtraction",
            "multiplication",
            "division",
            "inversion",
        }:
            # doc: deg(h) in [2,256]
            if deg_h < 2 or deg_h > 256:
                return False
        elif task in {"primitivity_check", "primitive_element_generation"}:
            if task == "primitivity_check":
                if deg_h < 2 or deg_h > 6:
                    return False
            else:
                if deg_h < 1 or deg_h > 6:
                    return False

    if task in {
        "addition",
        "subtraction",
        "multiplication",
        "long_division",
        "extended_euclidean_algorithm",
    }:
        if "f" not in exercise or "g" not in exercise:
            return False
    elif task in {"division"}:
        if "f" not in exercise or "g" not in exercise:
            return False
    elif task in {"inversion", "primitivity_check"}:
        if "f" not in exercise:
            return False
    elif task in {"irreducibility_check"}:
        if "f" not in exercise:
            return False
    elif task in {"irreducible_element_generation", "primitive_element_generation"}:
        # must have 'degree' key for irreducible_element_generation
        if task == "irreducible_element_generation":
            if "degree" not in exercise:
                return False
            deg = exercise["degree"]
            if not isinstance(deg, int) or deg < 1 or deg > 5:
                return False
        # primitive_element_generation: requires integer_modulus in [2,13] and polynomial_modulus present
    else:
        # unknown task handled earlier, but safeguard
        return False

    # Validate polynomial arrays shapes and ranges
    if "f" in exercise:
        f = exercise["f"]
        if typ == "polynomial_arithmetic":
            # determine multiplication vs other
            min_len, max_len = poly_len_bound_poly_arith(task == "multiplication")
            if not check_poly_array(f, p, min_len, max_len):
                return False
        else:  # finite_field_arithmetic
            # f length must be in [1, len(polynomial_modulus)-1]
            if not isinstance(poly_mod, list):
                return False
            max_len = len(poly_mod) - 1
            if max_len < 1:
                return False
            if not check_poly_array(f, p, 1, max_len):
                return False

    if "g" in exercise:
        g = exercise["g"]
        if typ == "polynomial_arithmetic":
            min_len, max_len = poly_len_bound_poly_arith(task == "multiplication")
            if not check_poly_array(g, p, min_len, max_len):
                return False
        else:
            max_len = len(poly_mod) - 1
            if max_len < 1:
                return False
            if not check_poly_array(g, p, 1, max_len):
                return False

    # f and g are not both zero
    if typ == "polynomial_arithmetic" and task in {
        "long_division",
        "extended_euclidean_algorithm",
    }:
        if is_zero_poly(exercise.get("f", [0])) and is_zero_poly(
            exercise.get("g", [0])
        ):
            return False
        # long division with g == [0] is undefined
        if task == "long_division" and is_zero_poly(exercise.get("g", [0])):
            return False

    # divisor must not be zero polynomial (mod h).
    if typ == "finite_field_arithmetic" and task == "division":
        if is_zero_poly(exercise.get("g", [0])):
            return False

    # f must not be zero
    if typ == "finite_field_arithmetic" and task == "inversion":
        if is_zero_poly(exercise.get("f", [0])):
            return False

    # deg(f) must be in [1,5] and p in [2,13] (checked earlier)
    if task == "irreducibility_check":
        f = exercise["f"]
        # degree = len(f)-1; must be between 1 and 5
        deg = len(f) - 1
        if deg < 1 or deg > 5:
            return False

    # All basic checks passed
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
    solve_exercise("Simple/Exercises/exercise0.json", "Simple/Answers/answer0.json")
