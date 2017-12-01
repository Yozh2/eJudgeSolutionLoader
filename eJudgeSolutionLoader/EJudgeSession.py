# Necessary packages
import requests

# Local imports
import ejudge_headers

class EJudgeSession():

    url = 'http://judge2.vdi.mipt.ru/cgi-bin/new-judge'
    host = 'judge2.vdi.mipt.ru'
    role = '6' # administrator

    def __init__(self, contest_id='000000', login='user', password='qwerty'):
        self.contest_id = contest_id
        self.login = login
        self.password = password
        self.cookies = dict()
        self.SID = ''

    def sign_in(self):
        # Setup basic parameters for login
        payload = {
            'login': self.login,
            'password': self.password,
            'contest_id': self.contest_id,
            'role': self.role,
            'locale_id': '0',
            'action_2': 'Submit'
        }
        content_length = str(len(payload))

        # Configure HTTP POST headers to send
        headers = ejudge_headers.login_headers(self.host, content_length, self.url)

        # POST data to login
        r = requests.post(self.url, data=payload, headers=headers)
        self.response_url = r.url

        # Get cookies and SID from the response
        self.cookies = r.cookies.get_dict()
        print('Login successful, cookie EJSID:', self.cookies['EJSID'])
        print(r.url)

        # Slice the response url string to get SID
        self.SID = r.url[r.url.find('SID')+4:r.url.find('SID')+20]
        print('SID:', self.SID)

    def send_solution(self, solution):

        # prepare POST body payload
        post_payload = {
            "SID": self.SID,
            "problem": solution.problem,
            "variant": solution.variant,
            "lang_id": solution.lang_id,
            "text_form": solution.code,
            "file": "",
            "action_40": "Send!"
        }
        # wrap payload in boundaries
        solution.decorate_body(post_payload)
        post_headers = ejudge_headers.post_headers(self.host, solution.content_length,
                                                   self.url, self.cookies, self.SID)

        # self.print_debug_info(solution)

        r = requests.post(self.url, data=solution.post_body, headers=post_headers)
        print('Solution sent!')

    def print_debug_info(self, solution):
        print(self.url)
        print(self.SID)
        print(self.cookies)
        print(solution.post_body)
        print(solution.content_length)
        print(solution.code)
        print(solution.lang_id)
