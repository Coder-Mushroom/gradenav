# =============================================================== #
#                                                                 #
#         _____            __    _  __                            #
#        / ___/______ ____/ /__ / |/ /__ __  __  ___  __ __       #
#       / (_ / __/ _ `/ _  / -_)    / _ `/ |/ / / _ \/ // /       #
#       \___/_/  \_,_/\_,_/\__/_/|_/\_,_/|___(_) .__/\_, /        #
#                                             /_/   /___/         #
#                                                                 #
# =============================================================== #
# Author      : Shiba                                             #
# Dev-date    : Nov 2025                                          #
# Desc. [MOD] : GradeNav current semester functions               #
# Note        : Grades are represented by a 3 digit positive      #
# integer in the range [100, 700], and weights by a positive      #
# integer in the range [0, 100]. This is to prevent float errors. #
# =============================================================== #
from lib.sgcalc import normal_avg, weighted_avg, transform_to_std_form

def eti1001(info: dict) -> int:
    mu_cenia: int = normal_avg(info["cenia"])
    mu_tickets: int = normal_avg(info["tickets"])

    grades: list[int] = [mu_cenia, mu_tickets, info["report"], info["final_proyect"]]
    weights: list[int] = [25, 10, 30, 35]
    final_grade: int = weighted_avg(grades, weights)

    return final_grade


def iic2283(info: dict) -> int:
    mu_tests: int = normal_avg(info["tests"])
    mu_hw: int = normal_avg(info["homework"])
    if mu_tests < 370:
        print(f"\033[1;33m[warn]\033[0m IIC2283: Failing test avg requirement ({transform_to_std_form(mu_tests)} < 3.7)")
    if mu_hw < 370:
        print(f"\033[1;33m[warn]\033[0m IIC2283: Failing homework avg requirement ({transform_to_std_form(mu_hw)} < 3.7)")

    final_grade: int = normal_avg([mu_tests, mu_hw])
    if mu_tests < 370 or mu_hw < 370:
        final_grade *= -1
    return final_grade


def iic2531(info: dict) -> int:
    mu_tests: int = weighted_avg(info["tests"], [30, 30, 40])
    mu_labs: int = normal_avg(info["labs"])

    final_grade = normal_avg([mu_tests, mu_labs])

    return final_grade


def iic2613(info: dict) -> int:
    mu_quizzes: int = normal_avg(info["quizzes"])
    mu_tests: int = normal_avg(info["tests"])
    mu_theory: int = weighted_avg([mu_quizzes, mu_tests], [20, 80])
    hw: list[int] = info["homework"][:]
    hw = hw + hw[1:]
    mu_hw: int = normal_avg(hw)
    if mu_theory < 395:
        print(f"\033[1;33m[warn]\033[0m IIC2613: Failing theory avg (20% quizzes, 80% tests) requirement ({transform_to_std_form(mu_theory)} < 3.95)")
    if mu_hw < 395:
        print(f"\033[1;33m[warn]\033[0m IIC2613: Failing homework avg requirement ({transform_to_std_form(mu_hw)} < 3.95)")

    final_grade = normal_avg([mu_theory, mu_hw])
    if mu_theory < 395 or mu_hw < 395:
        final_grade *= -1
    return final_grade


semfuncs: dict = {
    "ETI1001": eti1001,
    "IIC2283": iic2283,
    "IIC2531": iic2531,
    "IIC2613": iic2613,
}
