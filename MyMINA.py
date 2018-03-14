#!/usr/bin/envpython
#-*-coding:utf-8-*-

import urllib2
import requests
from bs4 import BeautifulSoup
import sys
import re

wd="" # change to your working directory

memlist = ("錦戸","丸山","横山","村上","渋谷","大倉","安田")
for mem in memlist:
    pattern = mem
    for pagenum in range(1,2):
        url="http://888eight888.blog84.fc2.com/?q=%s&page=%d" %(pattern ,pagenum)
        c=requests.get(url).content
        print url
        soup=BeautifulSoup(c,"lxml")
        urllist=soup.find_all('a',href=re.compile(r'entry'))

        for links in urllist:
          if pattern in links.text.encode('utf-8'):
            myhref=links.get('href')
            link=r"http://888eight888.blog84.fc2.com/"+myhref
            d=requests.get(link)
            soud=BeautifulSoup(d.content,"lxml")

            a=soud.findAll('title')[0]
            tit=a.contents[0].encode('utf-8')
            title=tit.replace('関ジャニ戦隊∞レンジャー ',r"")
            title = title.replace(r'/', r" ")

            date=soud.findAll('div', attrs={'class': 'entry_date'})
            mydate=date[1].contents[0].encode('utf-8')
            myda=mydate.replace(r'/', r'')
            m=re.search('(\d{8})', myda)
            if m : myd = m.group(1)

            myfile='%s %s %s.txt'%(pattern,myda,title)
            mydir=wd+myfile

            div=soud.findAll('div',attrs={'class':'entry_text'})
            mycont=div[2].contents

            with open(mydir,'w') as f:
                for lines in mycont:
                    if r'<style>' in str(lines.encode('utf-8')):
                        break
                    else:
                        f.write(lines.encode('utf-8'))
