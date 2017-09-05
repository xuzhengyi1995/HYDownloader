'''
Get image list
'''

import re
import base64
import time
import os
from bs4 import BeautifulSoup as bs
from GetHtml import GetHtml


class GetImgList:
    def __init__(self,url):
        self._result=[]
        self._uid="1000"
        self._bid="28e05cbd"
        self._cid=str(time.time()).split('.')[0]
        self._did="4509435"

        self._url=url
        getter=GetHtml()
        getter.set(self._url)
        self._data=getter.get()
        self._process()

    def _process(self):
        bsed=bs(self._data,"html.parser")
        pattern=re.compile(r'&amp;aid=.+?[&"]')
        aid_list=[]
        for i in bsed.find_all("ignore_js_op"):
            r=pattern.search(str(i))
            if(r!=None):
                aid_list.append(r.group(0).split('=')[1].split('&')[0])
        for i in aid_list:
            if (not str(i).isdigit()):

                aid=0
                try:
                    org_base64=str(i).split('%')[0]
                    if(len(org_base64)%3!=0):
                        for k in range(0,3-len(org_base64)%3):
                            org_base64+='='

                    decoded=base64.b64decode(org_base64)
                    t=decoded.decode().split('|')
                    aid=t[0]
                    self._bid=t[1]
                    self._cid=t[2]
                    self._did=t[4]
                except:
                    print('Error in',str(i).split('%')[0])
            else:
                aid=str(i)

            changed_uid=aid+'|'+self._bid+'|'+self._cid+'|'+self._uid+'|'+self._did
            after_aid=base64.b64encode(changed_uid.encode(encoding="utf-8")).decode()
            url='https://l.bdear.xyz/forum.php?mod=attachment&aid='+after_aid
            self._result.append(url)

    def __getitem__(self,position):
        return self._result[position]

    def __len__(self):
        return len(self._result)
