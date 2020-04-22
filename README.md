# 网络爬虫以及数据可视化项目实践
```©软件著作权归作者所有。本项目所有数据均来源于网络，仅供学习使用！```<br>

[![standard-readme compliant](https://img.shields.io/badge/Project-51job-brightgreen.svg?style=flat-square)](https://github.com/ra1nv/Python-InternetWormDataVisualization)

## 目录
- [摘要](#摘要)
- [准备工作](#准备工作)
- [获取数据](#获取数据)
- [解析内容](#解析内容)
- [保存数据](#保存数据)
- [项目预览](#项目预览)
- [总结](#总结)

## 摘要
本项目运用Python网络爬虫，Flask框架，Echarts组件以及sqlite3等技术实现对51job招聘网上的广州地区Python相关职业招聘信息的爬取。<br>
目的是为了学习网络爬虫与数据可视化分析相关知识以及初步了解Python相关专业就业形势。使用的软件是Pycharm教育版。<br>
课程参考：[Python爬虫以及数据可视化](https://www.bilibili.com/video/BV12E411A7ZQ)<br>
涉及概念：[网络爬虫](https://zh.wikipedia.org/wiki/%E7%B6%B2%E8%B7%AF%E7%88%AC%E8%9F%B2)、[数据可视化](https://zh.wikipedia.org/wiki/%E6%95%B0%E6%8D%AE%E5%8F%AF%E8%A7%86%E5%8C%96)

## 准备工作
### 引入模块
本项目网络爬虫阶段主要使用BeautifulSoup、re、urllib、sqlite3四个库
### 页面分析
在[51job](https://www.51job.com/)搜索Python并且地区选择广州后进入搜索结果界面，网址格式为  https://search.51job.com/list/030200,000000,0000,00,9,99,Python,2,{x}.html<br>
其中{x}代表当前页数（从1开始）。

## 获取数据
使用urllib库获取页面，在函数里面添加响应头，模拟浏览器访问。
```sh
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
```

## 解析内容
### 获取详情页网址
在搜索结果页面，我们需要的每个详情页超链接都在一个\<div\>的标签中，该标签的的属性为class="dw_table"。使用css选择器定位标签，对字符串正则提取，获取每个职位具体信息的超链接存于列表中。<br>
![image](https://github.com/ra1nv/Python-InternetWormDataVisualization/blob/master/Img/url.png)
```sh
def getUrl(baseurl):
    urllist = [] # 保存每个职位对应的详情链接
    for i in range(1,75): # 共74页
        url = baseurl + str(i) + ".html"
        html = askUrl(url)
        soup = BeautifulSoup(html,"html.parser")
        for item in soup.find_all("div", class_="dw_table"):
            item = str(item)
            link = re.findall(findUrl, item)
            urllist.extend(link)
    return urllist
```
### 获取详情页具体信息
在详情页面，获取职位名称，薪资，公司名称，职能类别，关键字，上班地址，公司信息作为一个列表再依次存入一个列表中.<br>
![image](https://github.com/ra1nv/Python-InternetWormDataVisualization/blob/master/Img/xiangqing.png)
```sh
def getData(urlist):
    datalist = []
    for html in urlist:
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
```
### 正则表达式
```sh
findUrl = re.compile(r'<a href="(.*?)" onmousedown="" target="_blank"') #详情链接正则表达式
findName = re.compile(r'<h1 title="(.*?)">') # 职位名
findCompany = re.compile(r'>(.*?)<em class="icon_b i_link"></em>') # 公司名
findRequirement = re.compile(r'<p class="msg ltype" title="(.*?)"') # 要求
findClass = re.compile(r'/">(.*?)</a>') # 职位类别
findKeyword = re.compile(r'=">(.*?)</a><') # 关键字
findAddress = re.compile(r'上班地址：</span>(.*?)</p>') # 地址
findSalary = re.compile(r'<strong>(.*?)</strong>') # 工资
findInfo = re.compile(r'<div class="tmsg inbox">(.*?)</div>') # 公司信息
```

## 保存数据
采用sqlite3数据库保存数据。
创建表
```sh
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
```
插入数据
```sh
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
```

## 项目预览
![image](https://github.com/ra1nv/Python-InternetWormDataVisualization/blob/master/Img/home.png)
![image](https://github.com/ra1nv/Python-InternetWormDataVisualization/blob/master/Img/info.png)
![image](https://github.com/ra1nv/Python-InternetWormDataVisualization/blob/master/Img/area.png)
![image](https://github.com/ra1nv/Python-InternetWormDataVisualization/blob/master/Img/salary.png)
![image](https://github.com/ra1nv/Python-InternetWormDataVisualization/blob/master/Img/wordtree.png)

## 总结
通过本次项目实践，对Python语言以及项目中使用的库有了更深刻的了解，掌握了网络爬虫的基础知识，也懂得了如何对获取的数据进一步地处理将其转化为可视的图表，对以后的机器学习有所帮助。
