def login_headers(host, content_length, login_url):
    headers = {
        "Host": host,
        "Upgrade-Insecure-Requests": "1",
        "DNT": "1",
        "Connection": "close",
        "Content-Length": content_length,
        "Origin": "http://" + host,
        "User-Agent": "python-requests/2.18.4",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": login_url,
        "Accept-Encoding": "gzip,deflate,sdch",
        "Accept-Language": "ru",
        "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
    }
    return headers

def post_headers(host, content_length, referer_url, cookies, sid):

    # Prepare cookies as single string with parameters, sep=';'
    cookies_to_send = ''
    for c in cookies.keys():
        cookies_to_send += c + '=' + cookies[c] + '; '
    cookies_to_send = cookies_to_send[:-2]

    headers = {
        "Host": host,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundary6XVsTPAM8ZoV9kp3",
        "Origin": "http://" + host,
        "User-Agent": "python-requests/2.18.4",
        "Referer": referer_url,
        "Upgrade-Insecure-Requests": "1",
        "DNT": "1",
        "Content-Length": content_length,
        "Cookie": cookies_to_send,
        "Connection": "close"
    }
    return headers
