def login_headers(host, content_length, login_url):
    headers = {
        "Host": host,
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "Connection": "keep-alive",
        "Content-Length": content_length,
        "Origin": host,
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": 'http://judge2.vdi.mipt.r/cgi-bin/new-judge?contest_id={}&locale_id=1&role=5',
        "Accept-Encoding": "gzip,deflate,sdch",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
    }
    return headers

def post_headers(host, content_length, referer_url, cookies, sid):

    cookies_to_send = ''
    for c in cookies.keys():
        cookies_to_send += c + '=' + cookies[c] + '; '
    cookies_to_send = cookies_to_send[:-2]
    print(cookies_to_send)

    headers = {
        "Host": host,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundary6XVsTPAM8ZoV9kp3",
        "Origin": host,
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
        "Referer": referer_url,
        "Upgrade-Insecure-Requests": "1",
        "DNT": "1",
        "Content-Length": content_length,
        "Cookie": cookies_to_send,
        "Connection": "close"
    }
    return headers
