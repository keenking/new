# -*- coding: utf-8 -*-
from multiprocessing.pool import Pool
import pymysql
import requests
import json
import exifread
from io import BytesIO
import configparser
import hashlib
import logging
import base64

# 配置logging
logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='weibo.log',
                    filemode='w')

cf = configparser.ConfigParser()
cf.read("ConfigParser.conf")

# 读取配置mysql
db_host = cf.get("mysql", "db_host")
db_port = cf.getint("mysql", "db_port")
db_user = cf.get("mysql", "db_user")
db_pass = cf.get("mysql", "db_pass")
db = cf.get("mysql", "db")

# 创建连接
conn = pymysql.connect(host=db_host, user=db_user, passwd=db_pass, db=db, port=db_port, charset='utf8')
# 获取游标
cursor = conn.cursor()

# 创建insert_sql
insert_blog_sql = (
    "INSERT IGNORE INTO blog(userid, id, blog_text, lat, lng, created_time) VALUES('{uid}', '{id}','{blog_text}','{lat}','{lng}','{created_time}')"
)

insert_pic_sql = (
    "INSERT IGNORE INTO pics(pic_url, pic_bin, md5, exif) VALUES ('{pic_url}','{pic_bin}','{md5}','{exif}')"
)

insert_relationship_sql = (
    "INSERT IGNORE INTO relationship(id, md5) VALUES ('{id}','{md5}')"
)

uid = []

with open('./data/final_id.txt', 'r') as f:
    for i in f.readlines():
        uid.append(i.strip('\r\n'))


# 处理图片数据
def handle_pic(pic_url):
    large_pic_url = pic_url.replace('thumbnail', 'large')
    large_bin = requests.get(large_pic_url)
    return large_bin.content


def get_poiid_info(uid):
    try:
        url = 'https://api.weibo.com/2/statuses/user_timeline.json'
        load = {
            'access_token': 'xxxxxxxxxx',
            'uid': uid,
            'count': 100,
            'feature': 2,
            'trim_user': 1
        }
        get_info = requests.get(url=url, params=load, timeout=(10, 10))
        if get_info.status_code != 200:
            logging.warning(ConnectionError)
            pass
        info_json = json.loads(get_info.content)
        info_json['uid'] = uid
        statuses = info_json['statuses']
        # 处理筛选微博数据
        for status in statuses:
            id = status['idstr']
            if status['geo'] is not None:
                lat = status['geo']['coordinates'][0]
                lng = status['geo']['coordinates'][1]
                pic_urls = status['pic_urls']

                # 判断是否在北京
                if (115.7 < lng < 117.4) and (39.4 < lat < 41.6):
                    # 若在北京,插入blog数据进库
                    blog_text = status['text'].replace('\'', '\'\'')
                    created_time = status['created_at']
                    try:
                        cursor.execute(
                            insert_blog_sql.format(uid=uid, id=id, blog_text=blog_text, lat=lat, lng=lng,
                                                   created_time=created_time))
                    except pymysql.err.OperationalError as e_blog:
                        logging.warning(e_blog.args[1])
                        pass

                    # conn.commit()
                    # 处理图片
                    for pic_url in pic_urls:
                        # 获取原图片二进制数据
                        pic_bin = handle_pic(pic_url['thumbnail_pic'])

                        # 读取exif 数据
                        pic_file = BytesIO(pic_bin)  # 将二进制数据转化成文件对象便于读取exif数据信息和生成MD5
                        tag1 = exifread.process_file(pic_file, details=False, strict=True)
                        tag = {}
                        for key, value in tag1.items():
                            if key not in (
                                    'JPEGThumbnail', 'TIFFThumbnail', 'Filename',
                                    'EXIF MakerNote'):  # 去除四个不必要的exif属性，简化信息量
                                tag[key] = str(value)
                        tags = json.dumps(tag)  # dumps为json类型 此tag即为exif的json数据
                        # 生成MD5
                        MD5 = hashlib.md5(pic_file.read()).hexdigest()
                        # 首先把二进制图片用base64 转成字符串之后再存
                        try:
                            cursor.execute(
                                insert_pic_sql.format(pic_url=pic_url['thumbnail_pic'].replace('thumbnail', 'large'),
                                                      pic_bin=str(base64.b64encode(pic_bin))[2:-1], md5=MD5,
                                                      exif=tags))
                        except pymysql.err.OperationalError as e_pic:
                            logging.warning(e_pic.args[1])
                            pass
                        try:
                            cursor.execute(insert_relationship_sql.format(id=id, md5=MD5))
                        except pymysql.err.OperationalError as e_relation:
                            logging.warning(e_relation)
                            pass
                        conn.commit()

                else:
                    logging.info(id + " is Not in Beijing")
                    pass
            else:
                logging.info(id + ' Geo is null')
                pass
    except pymysql.err.OperationalError as e:
        logging.error(e.args[1])
        pass


def judge_conn(i):
    global conn
    try:
        conn.ping(True)
        get_poiid_info(i)
    except pymysql.err.OperationalError as e:
        logging.error('Reconnect')
        conn = pymysql.connect(host=db_host, user=db_user, passwd=db_pass, db=db, charset='utf8')
        get_poiid_info(i)


def handle_tuple(a_tuple):
    read_uid_set = []
    for i in a_tuple:
        read_uid_set.append(i[0])
    return set(read_uid_set)


if __name__ == '__main__':
    sql_find_uid = (
        "SELECT userid FROM blog"
    )
    cursor.execute(sql_find_uid)
    read_uid_tuple = cursor.fetchall()
    read_list = handle_tuple(read_uid_tuple)
    print(len(read_list))

    new_uid = set(uid).difference(read_list)
    print(len(new_uid))

    pool = Pool()
    pool.map(judge_conn, list(new_uid))
