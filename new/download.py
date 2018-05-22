
import requests
import re
import pymysql
url = 'http://read.poxiaobbs.com'
r = requests.post(url)
reg_title = '"posttitlei">(.*)</h2>'
title = re.findall(reg_title, r.text)[0]
reg_author = '<div class="postInfo">Author(.*)</div>'
author = re.findall(reg_author, r.text)[0]
reg_article = '(<p>.*)<div style="clear:both;'
article = re.findall(reg_article, r.text)[0]
print(title,author,article)
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root123', db='order', charset='utf8')
cursor = conn.cursor()
sql = '''INSERT INTO new (title, author, article) VALUES ('%s','%s','%s'); ''' % (title, author, article)
cursor.execute(sql)
conn.commit()
cursor.close()
conn.close()

