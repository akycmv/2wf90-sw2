import finite.add_sub as add_sub
import finite.mult_div as mult_div
import finite.prim as prim
import finite.inverse as inverse


def solve(exercise) -> dict[str, list[int] | bool | None]:
    answer: dict[str, list[int] | bool | None] = {"answer": []}
    match exercise["task"]:
        case "addition":
            answer["answer"] = add_sub.add(
                exercise["f"],
                exercise["g"],
                exercise["integer_modulus"],
                exercise["polynomial_modulus"],
            )
        case "subtraction":
            answer["answer"] = add_sub.sub(
                exercise["f"],
                exercise["g"],
                exercise["integer_modulus"],
                exercise["polynomial_modulus"],
            )
        case "multiplication":
            answer["answer"] = mult_div.mult(
                exercise["f"],
                exercise["g"],
                exercise["integer_modulus"],
                exercise["polynomial_modulus"],
            )
        case "division":
            answer["answer"] = mult_div.div(
                exercise["f"],
                exercise["g"],
                exercise["integer_modulus"],
                exercise["polynomial_modulus"],
            )
        case "inversion":
            answer["answer"] = inverse.inverse(
                exercise["f"],
                exercise["integer_modulus"],
                exercise["polynomial_modulus"],
            )
        case "primitivity_check":
            answer["answer"] = prim.check(
                exercise["f"],
                exercise["integer_modulus"],
                exercise["polynomial_modulus"],
            )
        case "primitive_element_generation":
            answer["answer"] = prim.generate(
                exercise["integer_modulus"], exercise["polynomial_modulus"]
            )
        case _:
            pass
    return answer
