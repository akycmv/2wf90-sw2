# demutex for the exercise for polynomial arithmetic

import polynomial.add_sub as add_sub
import polynomial.mult_div as mult_div
import polynomial.egcd as egcd
import polynomial.irred as irred


# maps tasks to appropriate module function
def solve(exercise) -> dict[str, list[int] | bool | None]:
    answer: dict[str, list[int] | bool | None] = {"answer": []}
    match exercise["task"]:
        case "addition":
            answer["answer"] = add_sub.add(
                exercise["f"], exercise["g"], exercise["integer_modulus"]
            )
        case "subtraction":
            answer["answer"] = add_sub.sub(
                exercise["f"], exercise["g"], exercise["integer_modulus"]
            )
        case "multiplication":
            answer["answer"] = mult_div.mult(
                exercise["f"], exercise["g"], exercise["integer_modulus"]
            )
        case "long_division":
            q, r = mult_div.div(
                exercise["f"], exercise["g"], exercise["integer_modulus"]
            )
            del answer["answer"]
            answer["answer-q"] = q
            answer["answer-r"] = r
        case "extended_euclidean_algorithm":
            a, b, d = egcd.egcd(
                exercise["f"], exercise["g"], exercise["integer_modulus"]
            )
            answer["answer-a"] = a
            answer["answer-b"] = b
            answer["answer-gcd"] = d
        case "irreducibility_check":
            answer["answer"] = irred.check(exercise["f"], exercise["integer_modulus"])
        case "irreducible_element_generation":
            answer["answer"] = irred.generate(
                exercise["degree"], exercise["integer_modulus"]
            )
        case _:
            pass
    return answer
