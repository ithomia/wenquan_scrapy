import json
import time
import urllib.parse

import jwt
import requests


class BookInfo(object):
    def login(self, account, password):
        api_checklogin = 'http://open.izhixue.cn/checklogin?response_type=code&client_id=wqxuetang&redirect_uri=https://www.wqxuetang.com/v1/login/callbackwq&scope=userinfo&state=https://lib-nuanxin.wqxuetang.com/#/'

        # 创建了一个请求Session
        session = requests.session()
        # 生成登陆参数
        headers = {"Content-Type": 'application/x-www-form-urlencoded;charset=UTF-8',
                   'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
        data = 'account={}&password={}'.format(account, password)
        # 进行请求
        response_checklogin = session.post(api_checklogin, data=data, headers=headers)
        # 解码回调链接
        api_callback = urllib.parse.unquote(response_checklogin.json()['data'])
        # 请求回调链接，并返回需要调Cooike
        response_callback = session.get(api_callback, allow_redirects=False)
        return 'PHPSESSID=' + response_callback.cookies['PHPSESSID']

    def __init__(self, book_id):
        self.base_url = 'https://lib-nuanxin.wqxuetang.com'
        self.params = dict(bid=book_id)
        self.headers = {"Content-Type": 'application/x-www-form-urlencoded;charset=UTF-8',
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
                        'referer': "https://lib-nuanxin.wqxuetang.com/read/pdf/%s" % book_id,
                        'cookie': self.login('account', 'password')}
        self.secret = 'g0NnWdSE8qEjdMD8a1aq12qEYphwErKctvfd3IktWHWiOBpVsgkecur38aBRPn2w'
        self.book_id = book_id
        self.api_k = "/v1/read/k"
        self.api_info = "/v1/read/initread"
        self.book_info = self.get_book_info()
        self.book_name = self.book_info['name'] if self.book_info else ''
        self.book_pages = int(self.book_info['pages']) if self.book_info else 0
        self.aesk = self.get_aesk()

    def get_aesk(self):
        url = self.base_url + self.api_k
        response = requests.get(url, params=self.params, headers=self.headers)
        aesk = response.json()['data']
        self.aesk_time = time.time()
        return json.dumps(aesk)

    def get_book_info(self):
        url = self.base_url + self.api_info
        response = requests.get(url, params=self.params, headers=self.headers)
        print(response.text)
        return response.json()['data'] if response.json()['errcode'] == 0 else None

    def create_img_url(self, page):
        header = {
            "alg": "HS256",
            "typ": "JWT"
        }
        payload = {
            "p": page,
            "t": int(time.time()) * 1000,
            "b": str(self.book_id),
            "w": 1000,
            "k": self.aesk,
            "iat": int(time.time())
        }
        k = jwt.encode(headers=header, payload=payload, key=self.secret).decode()
        img_url = 'https://lib-nuanxin.wqxuetang.com/page/img/{}/{}?k={}'.format(self.book_id, page, k)
        return img_url

    def imgSrcList(self):
        if self.book_info:
            book_pages = int(self.book_info['pages'])
            return [self.create_img_url(page + 1) for page in range(0, book_pages)]
        else:
            return []

    def chapter(self):
        resp = requests.get('https://lib-nuanxin.wqxuetang.com/v1/book/catatree?bid=' + self.book_id,
                            headers=self.headers)
        chapter = resp.text.replace(u'\u3000', u'')
        chapter = json.loads(chapter)
        toc = []

        if chapter['data'] is not None:
            for data in chapter['data']:
                level_1 = [int(data['level']), data['label'], int(data['pnum'])]
                toc.append(level_1)
                if 'children' in data:
                    for children in data['children']:
                        level_2 = [int(children['level']), children['label'], int(children['pnum'])]
                        toc.append(level_2)
            return toc
        else:
            return [[1, '', 1]]
