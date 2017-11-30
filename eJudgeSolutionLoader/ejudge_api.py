"""
ejudge_api - the simple eJudge API for Python 3.

Use sign_in(contest_id, login, password) function to login as the
administrator and get session_id (SID) and cookies.

Use send_solution(...) to send files to eJudge server to check them.
You can specify the contest, problem, variant and compiler (lang_id)
"""

# Necessary packages
import os
import requests
from urllib.parse import quote

# Local imports
import ejudge_headers

def sign_in(contest_id, login, password):
    """
    sign_in(contest_id, login, password)

    Use this method to login to eJudge as the administrator to the
    contest required. You must specify login and password either.

    Returns the HTTP session, response URL, session_id and cookies.
    """

    # Setup basic parameters for login
    login_url = 'http://judge2.vdi.mipt.ru/cgi-bin/new-judge'
    host = 'judge2.vdi.mipt.ru'
    payload = {
        'login': login,
        'password': password,
        'contest_id': contest_id,
        'role': '6',
        'locale_id': '0',
        'action_2': 'Submit'
    }
    content_length = str(len(payload))

    # Configure HTTP POST headers to send
    headers = ejudge_headers.login_headers(host, content_length, login_url)

    # POST data to login
    r = requests.post(login_url, data=payload, headers=headers)

    # Get cookies and SID from the response
    cookies = r.cookies.get_dict()
    print('Login successful, cookie EJSID:', cookies['EJSID'])
    print(r.url)

    # Slice the response url string to get SID
    SID = r.url[r.url.find('SID')+4:r.url.find('SID')+20]
    print('SID:', SID)

    return r.url, SID, cookies

def send_solution(SID, cookies, contest_id, problem, variant, lang_id, file_code):

    def boundaryDecorator(d, filepath=''):
        """
        Prepare the POST request body to send.
        All required parameters from the "d" dictionary will be wrapped in boundaries.

        """
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

    def get_lang_id(option=None, path=None):

        lang_id = {
            'gcc': '2',
            'g++': '3',
            'gcc-vg': '28',
            'g++-vg': '29',
            'clang': '51',
            'clang++': '52'
        }

        if option:
            return lang_id.get(option, None)
        elif path and os.path.exists(path):
            ext = os.path.splitext(path)[-1]     # get the file extension of the solution path
            ext_match = {'c':'gcc', 'cpp':'g++'}
            return lang_id.get(ext_match.get(ext, None), None)
        else:
            return None

    host = 'judge2.vdi.mipt.ru'
    post_url = 'http://judge2.vdi.mipt.ru/cgi-bin/new-judge'
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
    post_headers = ejudge_headers.post_headers(host, content_length, post_url, cookies, SID)

    r = requests.post(post_url, data=post_payload, headers=post_headers)
    print('Solution sent!')
