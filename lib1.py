import requests
import json
from datetime import datetime
import smtplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import time
url1="http://xxxxxxxx/api.php/login"#图书馆服务器地址
data1={
"username":"xxxxxxx",
"password":"xxxxxxx",
"from":"mobile"
    }
header={
"User-Agent":"Mozilla/5.0 (Linux; Android 5.1.1; MI 9 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.136 Mobile Safari/537.36 MMWEBID/5055 MicroMessenger/7.0.17.1720(0x27001134) Process/tools WeChat/arm32 NetType/WIFI Language/zh_CN ABI/arm32"
    }
def send_msg(msg):###发送预约情况
    mail_host="smtp.163.com"
    mail_sender="xxxxx"#发送邮箱
    mail_license="xxxxxxx"#客户端授权码
    mail_receivers="xxxxx"#接收邮箱
    mm=MIMEMultipart('related')
    subject_content="预约通知"
    mm["From"] = "sender_name<xxxxx>"#接收邮箱
# 设置接受者,注意严格遵守格式,里面邮箱为接受者邮箱
    mm["To"] = "receiver_1_name<xxxxxx>"#接收邮箱
# 设置邮件主题
    mm["Subject"] = Header(subject_content,'utf-8')
    msg_text=MIMEText(msg,"plain","utf-8")
    mm.attach(msg_text)
    stp=smtplib.SMTP()
    stp.connect(mail_host,25)
    #stp.set_debuglevel(1)#显示发送邮件详细信息
    stp.login(mail_sender,mail_license)
    stp.sendmail(mail_sender,mail_receivers,mm.as_string())
    stp.quit()
def login():
    r1=requests.post(url=url1,data=data1,headers=header).text#获取access_token
    r2=json.loads(r1)
    #print(r1)
    access_Token=r2['data']['_hash_']['access_token']#access_token，预约作为需要验证是否登录
    return access_Token
def get_seatInfo():
    time=str(datetime.now()).split()
    day=time[0]
    startTime=time[1].split('.')[0]
    startTime=startTime[0:-3]#不需要秒，删去秒
    url2="http://xxxxx/api.php/spaces_old?area=22&day="
    url2=url2+day+'&endTime=22:30&segment&startTime='+startTime#获取座位信息地址
    s=requests.get(url=url2).text#获取坐位信息
    s=json.loads(s)
    seat_info=s['data']['list']#位置信息
    return seat_info
def get_freeSeat():
    global my_seat
    seat_info=get_seatInfo()
    for seat in seat_info:
        if seat['status']==1:#位置空闲
            my_seat=seat
            print(my_seat)
            return True
    return False
####开始预约####
def main():
    global my_seat
    if get_freeSeat():
        try:
            access_Token=login()
            url3="http://xxxxx/api.php/spaces/"+str(my_seat['id'])+"/book"#预约地址
            data2={
"access_token":access_Token,
"userid":"xxxxxx",
"type":"1",
"id":str(my_seat["id"]),
"segment":"1383121"
    }
            t=requests.post(url=url3,data=data2,headers=header).text#预约位置
            t=json.loads(t)
            if t['msg']=="预约成功":
                #send_msg("预约成功，座位号:"+my_seat['name'])
                print("预约成功~，座位号:"+my_seat['name'])
                return True
            elif t['status']==0:
                print("你已经预约，不可重复预约~")
                return True
            else:
                print(t)
                #send_msg(t)
                return False
        except Exception as e:
            print(e)
            return False
    else:
        print("暂时无空位")
        #send_msg("暂时无空位")
        return False
if __name__=='__main__':
    while True:        
        if main():
            break
        time.sleep(10)
