import requests
import re
import json

login_url = 'http://app.leisu.com/app/user/login'

headers = {
"User-Agent": "leisu/android",
"sn": "95AQACPK5KQYH",
"aid": "dd055c15ef9d9fc6",
"sign": "4b61b4d3f8970f9cb171cc5006312b26",
"ver": "2.8.1.11291306",
"platform": "1",
"channel": "MeiZu",
"wToken": "BYTR_TEt8taf1c+zVCyRgqC0HFeL/ElZbWOpQ8luMNp3dvn0lFFPruUyZFWH0ss/A61P4xGQOxGEXBkI0g3DqnG2uAvZLtzQIM0vC4FJ2SutxT5GdMgvbr2OQdLCYbZNM0XwCCQrzFjyW7Kk/5ihapRbIB/8PzVo6+OYtnZBUtqgVqbOc7taRZFjnyvb3NAgjk9O7InQqy2k8ZXkCnuS/tGG9wR2HdrWTWW5FA+oNSKYep7nPbhKkEugA44YFEQHEdI04AMjmk/iKLb2OZ5HSpmJYH3es2STqBQTb7UtiuOu37foPzc6bGC9uccR4cSSZfdphfKESttDA0depnsashfwg3NjnfpzE9olxSOAJZCqABvBzcUtCBd1aywpnRoUCWh/oX0y6yCsUKc+n1vNAq06sZWL8g12nxqwpkEKjgqPf9ytjtGQJxvkfi7Hm+6F6bfprkMKCxHYiSP83aerflnyfWeOuni3VcwyxV69wkBWwzCE=&AWER_a00131a58813b4f13cffdcfb940ffe04253ec56610a18",
"Content-Type": "application/x-www-form-urlencoded",
"Content-Length": "35",
"Host": "app.leisu.com",
"Connection": "Keep-Alive",
"Accept-Encoding": "gzip",
"Cookie": "SERVERID=e2e5cd786f48c825d9812ffec607f949|1543824741|1543824735"
 }

data = {"name": '', "password": '', "ver": '2.8.1.11291306'}

r = requests.post(login_url, data=data, headers=headers)
# a = json.loads(r.text)['code']
a = r.text
print(a)
# if (a == 0):
#     token = json.loads(r.text)['token']
#     headers2 = {"Content-Type": "application/x-www-form-urlencoded",
#                 "User-Agent": "'Sports/2.6.4 (iPhone; iOS 11.3.1; Scale/2.00)'", "token": token}
#
#     task_data1 = {"app": "0", "platform": "2", "taskid": "1", "ver": "2.6.4"}
#     task_data2 = {"app": "0", "platform": "2", "taskid": "2", "ver": "2.6.4"}
#     task_data3 = {"app": "0", "platform": "2", "taskid": "3", "ver": "2.6.4"}
#     task_data4 = {"app": "0", "platform": "2", "taskid": "4", "ver": "2.6.4"}
#     task_data5 = {"app": "0", "platform": "2", "taskid": "5",
#                   "ver": "2.6.4"}  # {"code":10013,"msg":"\u7528\u6237\u4e0d\u5b58\u5728"}
#     task_url = 'https://api.leisu.com/app/user/dotask'
#
#     for x in range(1, 11):
#         r1 = requests.post(task_url, data=task_data1, headers=headers2)
#         r2 = requests.post(task_url, data=task_data2, headers=headers2)
#         r3 = requests.post(task_url, data=task_data3, headers=headers2)
#         r4 = requests.post(task_url, data=task_data4, headers=headers2)
#         r5 = requests.post(task_url, data=task_data5, headers=headers2)
