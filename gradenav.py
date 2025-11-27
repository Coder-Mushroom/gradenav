# =============================================================== #
#                                                                 #
#         _____            __    _  __                            #
#        / ___/______ ____/ /__ / |/ /__ __  __  ___  __ __       #
#       / (_ / __/ _ `/ _  / -_)    / _ `/ |/ / / _ \/ // /       #
#       \___/_/  \_,_/\_,_/\__/_/|_/\_,_/|___(_) .__/\_, /        #
#                                             /_/   /___/         #
#                                                                 #
# =============================================================== #
# Author   : Shiba                                                #
# Dev-date : Nov 2025                                             #
# Desc.    : Grades calculator program                            #
# Note     : Grades are represented by a 3 digit positive integer #
# in the range [100, 700], and weights by a positive integer in   #
# the range [0, 100]. This is to prevent float errors.            #
# =============================================================== #
import os
import sys
import json
import lib.sgcalc as sgc
from lib.semfuncs import semfuncs

def main():
    file_path: str = ""
    sem: bool = True
    base_ppa: bool = True
    exp: bool = False

    if len(sys.argv) < 2:
        print("Incorrect number of arguments: at least 1 expected")
        print("Usage: gradenav.py *JSON GRADES FILE* [sem/bppa/cppa (type, sem by default)] [true/false (experiments on?, false by default)]\n")
        return

    file_path = sys.argv[1]
    if not os.path.isfile(file_path):
        print(f"Specified file does not exist: {file_path}\n")
        return

    match len(sys.argv):
        case 3:
            if sys.argv[2] in ["sem", "bppa", "cppa"]:
                sem = True if sys.argv[2] == "sem" else False
                base_ppa = True if sys.argv[2] == "bppa" else False
            elif sys.argv[2] in ["true", "false"]:
                exp = True if sys.argv[2] == "true" else False
        case 4:
            if sys.argv[2] in ["sem", "bppa", "cppa"]:
                sem = True if sys.argv[2] == "sem" else False
                base_ppa = True if sys.argv[2] == "bppa" else False
            if sys.argv[3] in ["true", "false"]:
                exp = True if sys.argv[3] == "true" else False

    prim_grades: str = ""
    with open(file_path, "rt") as grades_file:
        prim_grades = "".join(grades_file.readlines())

    grades_db: dict = json.loads(prim_grades)
    hist_db: dict = grades_db["hist"]
    sem_db: list[dict] = grades_db["sem"]

    # === Grades Experiments Section ===
    if exp:
        print("\033[1;35m[info]\033[0m Experimets turned ON")
        sem_db[2]["tests"][1] = 500
        sem_db[2]["labs"][2] = 550
        sem_db[2]["labs"][3] = 550

        sem_db[3]["tests"][0] = 620
        sem_db[3]["homework"][2] = 500
        sem_db[3]["homework"][3] = 250
    # ==================================

    if not base_ppa or sem:
        for idx, subject in enumerate(sem_db):
            sem_db[idx]["fg"] = semfuncs[subject["subject"]](subject)

    # === Final Grades Experiments Section ===
    fg_exp: bool = False
    if fg_exp:
        print("\033[1;35m[info]\033[0m FINAL GRADES Experimets turned ON")
        sem_db[0]["fg"] = 400
        sem_db[1]["fg"] = 400
        sem_db[2]["fg"] = 400
        sem_db[3]["fg"] = 400
    # ========================================

    print("")
    if sem:
        sgc.pretty_semester(sem_db)
    else:
        sgc.pretty_ppa(hist_db, sem_db, base_ppa)
    print("")

if __name__ == "__main__":
    main()
