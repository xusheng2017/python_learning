#!/usr/bin/env python
# coding:utf-8

import requests
from hashlib import md5


class RClient(object):

    def __init__(self, username, password, soft_id, soft_key):
        self.username = username
        self.password = md5(password.encode(encoding="utf-8")).hexdigest()
        self.soft_id = soft_id
        self.soft_key = soft_key
        self.base_params = {
            'username': self.username,
            'password': self.password,
            'softid': self.soft_id,
            'softkey': self.soft_key,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'Expect': '100-continue',
            'User-Agent': 'ben',
        }

    def rk_create(self, im, im_type, timeout=60):
        """
        im: 图片字节
        im_type: 题目类型
        """
        params = {
            'typeid': im_type,
            'timeout': timeout,
        }
        params.update(self.base_params)
        files = {'image': ('a.jpg', im)}
        # 添加异常处理,请求三次,如果获取不到响应那么报异常,重新进行打码
        try:
            r = requests.post('http://api.ruokuai.com/create.json', data=params, files=files, headers=self.headers,
                              timeout=timeout)
        except:
            try:
                r = requests.post('http://api.ruokuai.com/create.json', data=params, files=files, headers=self.headers,
                                  timeout=timeout)
            except:
                r = requests.post('http://api.ruokuai.com/create.json', data=params, files=files, headers=self.headers,
                                  timeout=timeout)
        return r.json()

    def rk_demand(self):
        params = {
            'username': self.username,
            'password': self.password
        }
        r = requests.post('http://api.ruokuai.com/info.json', data=params,  headers=self.headers)
        return r.json()['Score']

    def rk_report_error(self, im_id):
        """
        im_id:报错题目的ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://api.ruokuai.com/reporterror.json', data=params, headers=self.headers)
        return r.json()


rc = RClient('xuxuqingfeng2', '1qaz2wsx', '99121', 'ece1ce864fde48cb8327fb79e101bd34')

if __name__ == '__main__':
    rc = RClient('xuxuqingfeng2', '1qaz2wsx', '99121', 'ece1ce864fde48cb8327fb79e101bd34')
    print(rc.rk_demand())
    # im = open('result.png', 'rb').read()
    # res = rc.rk_create(im, 6900)
    # print(rc.rk_create(im, 6900))

