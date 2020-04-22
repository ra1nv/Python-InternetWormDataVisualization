# 网络爬虫以及数据可视化项目实践
```©软件著作权归作者所有。本项目所有数据均来源于网络，仅供学习使用！```<br>

[![standard-readme compliant](https://img.shields.io/badge/Project-51job-brightgreen.svg?style=flat-square)](https://github.com/ra1nv/Python-InternetWormDataVisualization)

## 目录
- [摘要](#摘要)
- [准备工作](#准备工作)
- [获取数据](#获取数据)
- [](#)
- [](#)


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
其中{x}代表当前页数（从1开始）

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
在搜索结果页面，我们要获取每个职位具体信息的超链接存于列表中

## 项目预览
![image](https://github.com/ra1nv/Python-InternetWormDataVisualization/blob/master/Img/home.png)
![image](https://github.com/ra1nv/Python-InternetWormDataVisualization/blob/master/Img/info.png)
![image](https://github.com/ra1nv/Python-InternetWormDataVisualization/blob/master/Img/area.png)
![image](https://github.com/ra1nv/Python-InternetWormDataVisualization/blob/master/Img/salary.png)
![image](https://github.com/ra1nv/Python-InternetWormDataVisualization/blob/master/Img/wordtree.png)
