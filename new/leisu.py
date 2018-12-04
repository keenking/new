# -*- coding: utf-8 -*-
# @Time    : 2018/12/3 15:53
# @Author  : xqqTest
import requests
import json
def do_task(username,password):
    login_url = 'https://api.leisu.com/app/user/login'

    headers = {"Content-Type": "application/x-www-form-urlencoded",
               "User-Agent": "'Sports/2.6.4 (iPhone; iOS 11.3.1; Scale/2.00)'", }

    data = {"app":"0","name":username,"password":password,"platform":"2","ver":"2.6.4"}

    r = requests.post(login_url, data=data, headers=headers)
    a = json.loads(r.text)['code']
    if(a == 0):
        token = json.loads(r.text)['token']
        headers2 = {"Content-Type": "application/x-www-form-urlencoded",
                   "User-Agent": "'Sports/2.6.4 (iPhone; iOS 11.3.1; Scale/2.00)'","token":token }

        task_data1 = {"app":"0","platform":"2","taskid":"1","ver":"2.6.4"}
        task_data2 = {"app":"0","platform":"2","taskid":"2","ver":"2.6.4"}
        task_data3 = {"app":"0","platform":"2","taskid":"3","ver":"2.6.4"}
        task_data4 = {"app":"0","platform":"2","taskid":"4","ver":"2.6.4"}
        task_data5 = {"app":"0","platform":"2","taskid":"5","ver":"2.6.4"}        #{"code":10013,"msg":"\u7528\u6237\u4e0d\u5b58\u5728"}
        task_url = 'https://api.leisu.com/app/user/dotask'

        for x in range(1,11):
            r1 = requests.post(task_url, data=task_data1, headers=headers2)
            r2 = requests.post(task_url, data=task_data2, headers=headers2)
            r3 = requests.post(task_url, data=task_data3, headers=headers2)
            r4 = requests.post(task_url, data=task_data4, headers=headers2)
            r5 = requests.post(task_url, data=task_data5, headers=headers2)
        return 1
    else:
        return 0


if __name__ == '__main__':
    if do_task('雷速账号','雷速密码') == 1:
        print('do task ok!')
    else:
        print('sorry!!!账号或密码错误~')

