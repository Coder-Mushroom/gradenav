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
# Desc. [MOD] : GradeNav grade calculation functions              #
# Note        : Grades are represented by a 3 digit positive      #
# integer in the range [100, 700], and weights by a positive      #
# integer in the range [0, 100]. This is to prevent float errors. #
# =============================================================== #

def iter_sum(arr: list[int]) -> int:
    sum: int = 0
    for elem in arr:
        sum += elem

    return sum


def normal_avg(grades: list[int]) -> int:
    return iter_sum(grades) // len(grades)


def weighted_avg(grades: list[int], weights: list[int]) -> int:
    if len(grades) != len(weights) or iter_sum(weights) != 100:
        return -1

    sum: int = 0
    for i in range(len(grades)):
        sum += grades[i] * weights[i]

    return sum // 100


def ppa_avg(fgrades: list[int], scredits: list[int]) -> int:
    total_credits: int = iter_sum(scredits)
    sum: int = 0
    for idx, fgrade in enumerate(fgrades):
        sum += fgrade * scredits[idx]

    return sum // total_credits


def transform_to_std_form(grade: int) -> str:
    CLOSING = "\033[0m"
    WARNING = "\033[1;33m"
    FAILING = "\033[1;31m"
    LOW_PASSING = "\033[1;34m"
    MID_PASSING = "\033[1;35m"
    HIGH_PASSING = "\033[1;32m"

    prefix: str = ""
    if grade < 0:
        prefix = WARNING
    elif grade < 395:
        prefix = FAILING
    elif 395 <= grade < 500:
        prefix = LOW_PASSING
    elif 500 <= grade < 600:
        prefix = MID_PASSING
    elif 600 <= grade <= 700:
        prefix = HIGH_PASSING

    grade = abs(grade)
    integer_part: str = str(grade)[0]
    decimal_part: str = str(grade)[1:]

    return prefix + integer_part + "." + decimal_part + CLOSING


def pretty_semester(sem_db: list[dict]):
    subjects: list[str] = [subject["subject"] for subject in sem_db]
    grades: list[int] = [subject["fg"] for subject in sem_db]
    print("=== Semester Final Grades ===")
    for idx, grade in enumerate(grades):
        subject: str = subjects[idx] + ":"
        if grade < 0:
            subject = "\033[1;33m" + subject + "\033[0m"

        print(f">> {subject} {transform_to_std_form(grade)}")
    print("=============================")


def pretty_ppa(hist_db: dict, sem_db: list[dict], base_ppa: bool):
    categories: list[str] = list(hist_db.keys())
    all_fgrades: list[int] = []
    all_scredits: list[int] = []

    if not base_ppa:
        categories.append("Current Semester")
        hist_db["Current Semester"] = sem_db

    print("=== All Final Grades ===")
    for category in categories:
        subtitle: str = f"~~ {category} Subjects ~~"
        print(subtitle)
        cat_subjects: list[str] = [subject["subject"] for subject in hist_db[category]]
        cat_fgrades: list[int] = [subject["fg"] for subject in hist_db[category]]
        all_fgrades.extend([abs(fgrade) for fgrade in cat_fgrades])
        all_scredits.extend([subject["credits"] for subject in hist_db[category]])

        for idx, fgrade in enumerate(cat_fgrades):
            subject: str = cat_subjects[idx] + ":"
            if fgrade < 0:
                subject = "\033[1;33m" + subject + "\033[0m"

            print(f">> {subject} {transform_to_std_form(fgrade)}")
        print("~" * len(subtitle))

    print("========================")
    ppa: int = ppa_avg(all_fgrades, all_scredits)
    print(f">> PPA    : {transform_to_std_form(ppa)}")
    print("========================")
