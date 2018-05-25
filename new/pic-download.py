import requests
import os
import configparser
import pymysql
import base64

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6",
    "Accept-Language": "zh-cn",
    "DNT": "1",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive"
}

cf = configparser.ConfigParser()
cf.read("configparser.conf")

# 读取配置mysql
db_host = cf.get("mysql", "db_host")
db_port = cf.getint("mysql", "db_port")
db_user = cf.get("mysql", "db_user")
db_pass = cf.get("mysql", "db_pass")
db = cf.get("mysql", "db")

#连接数据库
# conn = pymysql.connect(host=db_host, user=db_user, passwd=db_pass, db=db, port=db_port, charset='utf8')
# cursor = conn.cursor()
# insert_pic_sql = (
#     "INSERT IGNORE INTO pics(pic_bin) VALUES ('{pic_bin}')"

for i in range(1, 500):
    data = {"image": i}
    url = 'http://picsum.photos/g/1920/1080/?image=%s'% i
    r = requests.get(url, headers= headers, data= data)
    pic_bin = r.content
    name = str(i) +'.png'
    prename = 'F:\\testgit\\new\\static\\images\\g1920\\'
    pathname = os.path.join(prename,name)
    with open(pathname, 'wb')as f:
        f.write(r.content)
        f.close()


# cursor.execute(insert_pic_sql.format(pic_bin=str(base64.b64encode(pic_bin))[2:-1]))
# conn.commit()
# if __name__ == '__main__':
#     url = 'http://read.poxiaobbs.com/'
#     r = requests.get(url)
#     print(r.text)