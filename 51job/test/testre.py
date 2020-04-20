# -*- coding = utf-8 -*-
# @Time : 2020/4/14 16:27
# @Author : rainv
# @File : testre.py
# @Software : PyCharm

import re
from bs4 import BeautifulSoup

findUrl = re.compile(r'<a href="(.*?)" onmousedown="" target="_blank"')
findName = re.compile(r'<h1 title="(.*?)">')
findCompany = re.compile(r'>(.*?)<em class="icon_b i_link"></em>')
findRequirement = re.compile(r'<p class="msg ltype" title="(.*?)"')
findClass = re.compile(r'/">(.*?)</a>')
findKeyword = re.compile(r'=">(.*?)</a><')
findAddress = re.compile(r'上班地址：</span>(.*?)</p>')
findSalary = re.compile(r'<strong>(.*?)/月</strong>')
findInfo = re.compile(r'<div class="tmsg inbox">(.*?)</div>')

datalist = []
html = open("详情.html",'r')

soup = BeautifulSoup(html,"html.parser")
for item in soup.find_all("div", class_="tCompany_center clearfix"):
    datas = []
    item = str(item)

    data = re.findall(findName, item)[0]
    datas.append(data)

    data = re.findall(findCompany, item)[0]
    datas.append(data)

    data = re.findall(findRequirement, item)
    data = data[0].replace('\xa0', '').replace('|', '，')
    datas.append(data)

    data = re.findall(findClass, item)
    if len(data) > 1:
        data = data[0] + ' ' + data[1]
    else:
        pass
    datas.append(data)

    data = re.findall(findKeyword, item)
    if len(data) > 1:
        for i in range(1, len(data)):
            data[0] = data[0] + ' ' + data[i]
    datas.append(data[0])

    data = re.findall(findAddress, item)[0]
    datas.append(data)

    data = re.findall(findSalary, item)[0]
    datas.append(data)

    data = re.findall(findInfo, item)
    data = data[0].replace('<br/>', '')
    datas.append(data)

    datalist.append(datas)
print(datalist)


