# -*- coding = utf-8 -*-
# @Time : 2020/4/14 16:08
# @Author : rainv
# @File : spider.py
# @Software : PyCharm

from bs4 import BeautifulSoup
import re
import urllib.request, urllib.error
import sqlite3

def main():
    baseurl = "https://search.51job.com/list/030200,000000,0000,00,9,99,Python,2," # 基准链接
    urllist = getUrl(baseurl)
    datalist = getData(urllist)
    # list = ['https://jobs.51job.com/guangzhou/119759191.html?s=01&t=0']
    # datalist = getData(list)
    # print(datalist)
    dbpath = '_51job.db'
    init_db(dbpath)
    saveData(datalist,dbpath)


findUrl = re.compile(r'<a href="(.*?)" onmousedown="" target="_blank"') #详情链接正则表达式
findName = re.compile(r'<h1 title="(.*?)">') # 职位名
findCompany = re.compile(r'>(.*?)<em class="icon_b i_link"></em>') # 公司名
findRequirement = re.compile(r'<p class="msg ltype" title="(.*?)"') # 要求
findClass = re.compile(r'/">(.*?)</a>') # 职位类别
findKeyword = re.compile(r'=">(.*?)</a><') # 关键字
findAddress = re.compile(r'上班地址：</span>(.*?)</p>') # 地址
findSalary = re.compile(r'<strong>(.*?)</strong>') # 工资
findInfo = re.compile(r'<div class="tmsg inbox">(.*?)</div>') # 公司信息

# 列表保存详情链接
def getUrl(baseurl):
    urllist = [] # 保存每个职位对应的详情链接
    for i in range(1,74): # 共73页
        url = baseurl + str(i) + ".html"
        html = askUrl(url)
        soup = BeautifulSoup(html,"html.parser")
        for item in soup.find_all("div", class_="dw_table"):
            item = str(item)
            link = re.findall(findUrl, item)
            urllist.extend(link)
    return urllist

def getData(urlist):
    datalist = []
    for html in urlist:
        if html == 'https://jobs.51job.com/guangzhou-hzq/121213414.html?s=01&amp;t=0':
            continue
        if html == 'https://jobs.51job.com/guangzhou-hzq/121213224.html?s=01&amp;t=0':
            continue
        html = askUrl(html)
        soup = BeautifulSoup(html, "html.parser")
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
            if(data):
                datas.append(data[0])
            else:
                datas.append(' ')

            data = re.findall(findAddress, item)
            if (data):
                datas.append(data[0])
            else:
                datas.append(' ')

            data = re.findall(findSalary, item)
            if (data):
                datas.append(data[0])
            else:
                datas.append(' ')

            data = re.findall(findInfo, item)
            data = data[0].replace('<br/>', '').replace('\xa0', '').replace('"', "'")
            if (data):
                datas.append(data)
            else:
                datas.append(' ')

            datalist.append(datas)
    return datalist

def askUrl(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
    }
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        print(url) # 定位不能解析的网址
        html = response.read().decode("gbk")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html

def init_db(dbpath):
    sql = '''
        CREATE TABLE IF NOT EXISTS job(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        jname TEXT,
        cname TEXT,
        req TEXT,
        jclass TEXT,
        keywords TEXT,
        address TEXT,
        salary TEXT,
        cinfo TEXT);
    '''
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()

def saveData(datalist,dbpath):
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()
    for data in datalist:
        for index in range(len(data)):
            data[index] = '"' + data[index] + '"'
        sql = '''
                INSERT INTO job(jname,cname,req,jclass,keywords,address,salary,cinfo)
                VALUES(%s)
            ''' % ",".join(data)
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    main()