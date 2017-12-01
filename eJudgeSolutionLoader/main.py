#!/usr/local/bin/python3
"""
eJudgeSolutionLoader - a simple Python3 eJudge solution uploader.

Use eJudgeSolutionLoader/main.py -h to get usage help.
"""

import requests
import argparse
from sys import argv

# Local imports
# import ejudge_api
from EJudgeSession import EJudgeSession
from EJudgeSolution import EJudgeSolution

if __name__ == "__main__":

    def parse_args():
        """Parses arguments and returns args object to the main program"""
        parser = argparse.ArgumentParser(prog='python3 main.py',
                                         conflict_handler='resolve')
        parser.add_argument("CONTEST", type=int,
                            help="The eJudge contest_id user wants upload solutions to.")
        parser.add_argument("PROBLEM", type=int,
                            help="the number of PROBLEM in the CONTEST")
        parser.add_argument("VARIANT", type=int,
                            help="The number of VARIANT of the PROBLEM in the CONTEST.")
        parser.add_argument("SOLUTION", type=str,
                            help="The path to the SOLUTION to upload.")
        parser.add_argument('-d', "--directory", action='store_true',
                            help="The SOLUTION is the path to the directory with solution files.")
        parser.add_argument('-l', "--login", type=str, nargs='?', default='Yozh4',
                            help="The LOGIN of the user that will publish the SOLUTION.")
        parser.add_argument('-p', "--password", type=str, nargs='?', default='123',
                            help="The PASSWORD for the user that will publish the SOLUTION.")
        parser.add_argument('-c', "--compiler", type=str, nargs='?', default='gcc',
                            help="The compiler to be used to build the SOLUTION.")
        parser.add_argument("--lang_id", type=int, nargs='?', default=29,
                            help="Language ID on eJudge for appropriate compiler.")
        return parser.parse_args()

    # init main variables
    ARGS = parse_args()
    contest_id = str(ARGS.CONTEST)
    problem = str(ARGS.PROBLEM)
    variant = str(ARGS.VARIANT)
    solution_path = ARGS.SOLUTION
    lang_id = str(ARGS.lang_id)         # old version for ejudge_api
    compiler = str(ARGS.compiler)
    login = ARGS.login
    password = ARGS.password

    # ==============================================================================================

    # Commented version shows ejudge_api variant of usage
    # file_code = read_code(solution_path)
    # url, SID, cookies = ejudge_api.sign_in(contest_id, login, password)
    # ejudge_api.send_solution(SID, cookies, contest_id, problem, variant, lang_id, file_code)

    session = EJudgeSession(contest_id, login, password)
    session.sign_in()

    solution = EJudgeSolution(contest_id, problem, variant, compiler, solution_path)
    session.send_solution(solution)
