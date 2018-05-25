# -*- coding: utf-8 -*-
import requests
import re
import pymysql


# select title,count(*) as count from new group by title having count>1;
# SELECT * FROM new WHERE title='长凳上的假期';
#
# DELETE new
# FROM new
# LEFT JOIN(
#    SELECT MIN(pk_id) AS pk_id
#    FROM new AS newa
#    GROUP BY newa.title
#    ) AS tmp USING (pk_id)
# WHERE tmp.pk_id IS NULL;


def get_all():
    url = 'http://read.poxiaobbs.com'
    r = requests.post(url)
    reg_title = '"posttitlei">(.*)</h2>'
    title = re.findall(reg_title, r.text)[0]
    reg_author = '<div class="postInfo">Author(.*)</div>'
    author = re.findall(reg_author, r.text)[0]
    reg_article = '(<p>.*)<div style="clear:both;'
    article = re.findall(reg_article, r.text)[0]
    return title, author, article

if __name__ == '__main__':
    connection = pymysql.connect(host='193.112.64.245',
                             user='root',
                             password='woaiXLT:1314',
                             db='mryp_cloud',
                             charset='utf8')
    connection.autocommit(1)
    try:
        with connection.cursor() as cursor:
            while True:
                all = get_all()
                title = pymysql.escape_string(all[0])
                author = pymysql.escape_string(all[1])
                article = pymysql.escape_string(all[2])
                sql = '''INSERT INTO mryp (title, author, article) VALUES ('%s','%s','%s'); ''' % (title, author, article)
                cursor.execute(sql)
    finally:
        connection.close()

