'''
Get all
'''
import os
from GetHtml import GetHtml
from GetImgList import GetImgList
import re
import threading

def download_img_list(img_dir,img_url,page):
    print("Start download",img_dir)
    test=GetImgList(img_url)
    s=0
    img_getter=GetHtml()

    for i in test:
        print('Page:',page,'**',img_dir,'Now downloading',s+1,"/",len(test))
        img_getter.set(str(i))
        fs=open(img_dir+'\\'+str(s)+'.jpg','wb')
        fs.write(img_getter.get())
        fs.close()
        s=s+1

title="***HY论坛翻译漫画自动下载器***"
info="下载到目录下Download文件夹，输入下载起始页数"
start=1
end=3

print(title)
print(info)

t_start='n'
t_end='n'
while(not t_start.isdigit()):
    t_start=input("请输入开始页码(整数数字)：")

while(not t_end.isdigit()):
    t_end=input("请输入截至页码(整数数字)：")

start=int(t_start)
end=int(t_end)

base_url="https://l.bdear.xyz/forum-15/"
base_t_url="https://l.bdear.xyz/"

find_tid=re.compile(r'<a href="thread-.*?</a>')
re_tid=re.compile(r'thread-.*?/')
re_title=re.compile(r'>.*?<')

if(not os.path.exists('.\\Download')):
    os.mkdir('.\\Download')

threads=[]
t_sum=0
m_sum=0
for i in range(int(start),int(end)+1):
    url=base_url+str(i)+'.html'

    ht=GetHtml()
    ht.set(url)
    html=str(ht.get().decode('utf-8','ignore'))

    all_tid=find_tid.findall(html)
    for data in all_tid:
        if(re_title.search(data)!=None):
            tid=re_tid.search(data).group(0).split('/')[0]
            title=re_title.search(data).group(0).split('>')[1].split('<')[0].replace('.','').replace(':','-').replace('/','-').replace('?','-')

            if(title.isdigit()):
                continue
            else:
                img_dir='.\\Download\\'+title
                t_url=base_t_url+tid+'/1-1.html'

                m_sum+=1
                print('No.',m_sum,img_dir.split('\\')[2],':',t_url)

                if(not os.path.exists(img_dir)):
                    os.mkdir(img_dir)
                    t_temp=threading.Thread(target=download_img_list,args=(img_dir,t_url,i,))
                    threads.append(t_temp)
                    t_sum=t_sum+1

                if(t_sum==10):
                    t_sum=0
                    for t in threads:
                        t.start()
                    for t in threads:
                        t.join()
                    threads.clear()

if(t_sum!=0):
    t_sum=0
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    threads.clear()
