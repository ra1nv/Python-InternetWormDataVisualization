# -*- coding = utf-8 -*-
# @Time : 2020/4/18 16:53
# @Author : rainv
# @File : cloud.py
# @Software : PyCharm

import jieba  # 分词
from matplotlib import pyplot as plt # 绘图 数据可视化
from wordcloud import WordCloud # 词云
from PIL import Image # 图片处理
import numpy as np # 矩阵运算
import sqlite3

con = sqlite3.connect('_51job.db')
cur = con.cursor()
sql = 'select jclass from job'
data = cur.execute(sql)
text = ''
for item in data:
    text = text + item[0]
cur.close()
con.close()

cut = jieba.cut(text)
str = ' '.join(cut)
print(len(str))

img = Image.open(r'./tree.jpg') # 打开遮罩图片
img_array = np.array(img) # 将图片转换为数组
wc = WordCloud(
    background_color='white',
    mask = img_array,
    font_path='PingFang.ttc'
)
wc.generate_from_text(str)

fig = plt.figure(1)
plt.imshow(wc)
plt.axis('off') # 显示坐标轴
# plt.show()
plt.savefig(r'./wordtree.png',dpi = 500)