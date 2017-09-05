'''
'Get Html
'''

import urllib.request
import socket
class GetHtml:
    def __init__(self):
        self._url='http://www.baidu.com'
    def set(self,url):
        self._url=url
    def get(self):
        req=urllib.request.Request(self._url)
        req.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0")
        req.add_header("Accept-Encoding","deflate, br")

        is_error=True
        s_retry=0
        while(is_error and s_retry<10):
            try:
                r=urllib.request.urlopen(req,timeout=5)
                r_data=r.read()
                is_error=False
            except urllib.error.HTTPError:
                is_error=True
                s_retry+=1
                print('HTTPError Retry',s_retry,'times')
            except urllib.error.URLError:
                is_error=True
                s_retry+=1
                print('URLError Retry',s_retry,'times')
            except socket.timeout:
                is_error=True
                s_retry+=1
                print('SOCKETError Retry',s_retry,'times')

        return r_data
