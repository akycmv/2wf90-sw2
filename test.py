from solve import solve_exercise
from os.path import join
from json import load
from time import perf_counter


def test_path(path: str):
    """
    helper function for local development to test tests given along with the assignment
    """
    for i in range(0, 18):
        expath = f"exercise{i}.json"
        anspath = f"answer{i}.json"
        anscomp = f"answer-comp{i}.json"

        start_time = perf_counter()
        solve_exercise(join(path, expath), join(path, anscomp))
        end_time = perf_counter()
        elapsed = end_time - start_time

        with open(join(path, f"exercise{i}.json"), "r") as exercise_file:
            exercise = load(exercise_file)

        with (
            open(join(path, anspath), "r") as wantf,
            open(join(path, anscomp), "r") as gotf,
        ):
            want = load(wantf)
            got = load(gotf)
            if exercise["task"] not in [
                "extended_euclidean_algorithm",
                "long_division",
            ]:
                print(expath, want["answer"], got["answer"])
                print("\t", want["answer"] == got["answer"])
            else:
                if exercise["task"] == "extended_euclidean_algorithm":
                    print(
                        expath,
                        want["answer-a"],
                        want["answer-b"],
                        want["answer-gcd"],
                        got["answer-a"],
                        got["answer-b"],
                        got["answer-gcd"],
                    )
                    print("\t", want["answer-a"] == got["answer-a"])
                    print("\t", want["answer-b"] == got["answer-b"])
                    print("\t", want["answer-gcd"] == got["answer-gcd"])
                else:
                    print(
                        expath,
                        want["answer-q"],
                        want["answer-r"],
                        got["answer-q"],
                        got["answer-r"],
                    )
                    print("\t", want["answer-q"] == got["answer-q"])
                    print("\t", want["answer-r"] == got["answer-r"])

        print(f"\tTime taken: {elapsed:.6f} seconds\n")


if __name__ == "__main__":
    test_path(join("tests", "simple"))
    # test_path(join("tests", "realistic"))
