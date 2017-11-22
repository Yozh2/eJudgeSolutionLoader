#/usr/local/bin/python3
"""
eJudgeSolutionLoader - a simple Python3 eJudge solution uploader.

Use eJudgeSolutionLoader/main.py -h to get usage help.
"""

import requests
from urllib.parse import quote
import argparse
from sys import argv
import ejudge_headers


def boundaryDecorator(d, filepath=''):
    output = ""
    boundary = '------WebKitFormBoundary6XVsTPAM8ZoV9kp3\n'

    for name in d.keys():
        output += boundary
        #if name == 'file':
            # output += 'Content-Disposition: form-data; name="file"; filename="{}"\nContent-Type: application/octet-stream'.format(filepath)
        output += 'Content-Disposition: form-data; name="{}"\n\n{}\n'.format(name, d[name])

    # Ending boundary
    output += '------WebKitFormBoundary6XVsTPAM8ZoV9kp3--'
    return output

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
        parser.add_argument('-l', "--login", type=str, nargs='?', default='Yozh4',
                            help="The LOGIN of the user that will publish the SOLUTION.")
        parser.add_argument('-p', "--password", type=str, nargs='?', default='123',
                            help="The PASSWORD for the user that will publish the SOLUTION.")
        parser.add_argument("--lang_id", type=int, nargs='?', default=29,
                            help="Language ID on eJudge for appropriate compiler.")
        parser.add_argument('-c', "--clean", action='store_true',
                            help="Reset the situation. Clean logs and temporary files.")
        return parser.parse_args()

    # init main variables
    ARGS = parse_args()
    contest_id = str(ARGS.CONTEST)
    problem = str(ARGS.PROBLEM)
    variant = str(ARGS.VARIANT)
    solution_path = ARGS.SOLUTION
    lang_id = str(ARGS.lang_id)
    login = ARGS.login
    password = ARGS.password

    # Read the solution from the file into string object
    with open(solution_path, 'r', encoding='utf-8') as file_to_send:
        file_code = file_to_send.read()
        print('File {} was read.'.format(file_to_send.name))

    # Enter HTTP session
    session = requests.Session()

    # Setup basic parameters for login
    login_url = 'http://judge2.vdi.mipt.ru/cgi-bin/new-judge?contest_id={}&locale_id=1&role=6'.format(contest_id)
    # login_url = 'http://judge2.vdi.mipt.ru/cgi-bin/new-judge'
    host = 'judge2.vdi.mipt.ru'

    # TODO Future improvements: payload as dictionary
    #    payload = {
    #        'contest_id': contest_id,
    #        'locale_id': '1',
    #        'role': '6',
    #        'login': login,
    #        'password': password,
    #        'action_2': '#Send'
    #    }

    payload = "login={}&password={}&contest_id={}".format(login, password, contest_id) + \
              "&role=6&locale_id=1&action_2=#Send"
    content_length = str(len(payload))

    # Configure HTTP POST headers to send
    headers = ejudge_headers.login_headers(host, content_length, login_url)

    # POST data to login
    r = requests.post(login_url, data=payload, headers=headers)

    cookies = r.cookies.get_dict()
    print('Login successful, cookie:', cookies)
    print(r.url)

    # Slice the response url string to get SID
    SID = r.url[r.url.find('SID')+4:r.url.find('SID')+20]
    print('SID:', SID)

    post_url = u'http://judge2.vdi.mipt.ru/cgi-bin/new-judge'
    post_payload = {
        "SID": SID,
        "problem": problem,
        "variant": variant,
        "lang_id": lang_id,
        "text_form": file_code,
        "file": "",
        "action_40": "Send!"
    }

    post_payload = boundaryDecorator(post_payload).encode('utf-8')

    content_length = str(len(post_payload) + len(file_code))
    post_headers = ejudge_headers.post_headers(host, content_length, login_url, cookies, SID)

    r = requests.post(post_url, data=post_payload, headers=post_headers)
    print('Solution sent!')
    # print(r.text)
