import requests
import requests as rq
import json
from urllib.parse import quote  # Python 3+

import ejudge_headers

def boundaryDecorator(d, filepath=''):
	output = ""
	boundary = '------WebKitFormBoundary6XVsTPAM8ZoV9kp3\n'

	for name in d.keys():
		output += boundary
		#if name == 'file':
			# output += 'Content-Disposition: form-data; name="file"; filename="{}"\nContent-Type: application/octet-stream'.format(filepath)
		output += 'Content-Disposition: form-data; name="{}"\n\n{}\n'.format(name, d[name])
	output += '------WebKitFormBoundary6XVsTPAM8ZoV9kp3--'
	return output

login = 'Yozh4'
password = '123'
contest_id = '700110'
problem = '62'
variant = '17'
lang_id = '29' # C + Valgrind
solution_path = 'solution.c'

if __name__ == '__main__':

	with open(solution_path, 'r') as file_to_send:
		file_code = file_to_send.read()
		print(file_code)

	# Enter HTTPS session
	session = rq.Session()

	# Setup basic parameters for login
	login_url = 'http://judge2.vdi.mipt.ru/cgi-bin/new-judge?contest_id={}&locale_id=1&role=5'.format(contest_id)
	host = 'judge2.vdi.mipt.ru'

	# Set POST login payload in urlencoded mode
	send_str = '#Отправить'
	action = quote(send_str.encode('cp1251'))

	payload = "login={}&password={}&contest_id={}".format(login, password, contest_id) + \
			  "&role=6&locale_id=1&action_2={}".format(action)
	content_length = str(len(payload))

	# Configure HTTP POST headers to send
	headers = ejudge_headers.login_headers(host, content_length, login_url)

	# POST data to login
	r = requests.post(login_url, data=payload, headers=headers)
	cookies = r.cookies.get_dict()
	print('Login successful, cookie:', cookies)
	print(r.url)


	SID = r.url[r.url.find('SID')+4:r.url.find('SID')+20]
	print('SID:', SID)


	send_str = 'Отправить!'
	action = quote(send_str.encode('cp1251'))

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

	post_payload = boundaryDecorator(post_payload)

	content_length = str(len(post_payload) + len(file_code))
	post_headers = ejudge_headers.post_headers(host, content_length, login_url, cookies, SID)

	r = requests.post(post_url, data=post_payload, headers=post_headers)
	print('Solution sent!')
	print(r.text)
