#coding='utf-8'
#仅供学习与参考 请勿用法非法用途！
import time
import requests
import json
from PIL import Image
import getpass
headers ={
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
    "Upgrade-Insecure-Requests": "1"
}
def login_and_getToken():
    #登陆并返回token
    url = "http://xk.xidian.edu.cn/xsxkapp/sys/xsxkapp/student/4/vcode.do?timestamp="+str(int(time.time()*1000))
    ses = requests.session()
    response = ses.get(url,headers=headers)
    pictureTokenJSON = json.loads(response.text)
    pictureToken = pictureTokenJSON['data']['token']
    pictureSrc = "http://xk.xidian.edu.cn/xsxkapp/sys/xsxkapp/student/vcode/image.do?vtoken="+str(pictureToken)
    #print(pictureSrc)
    pictureData = ses.get(pictureSrc,headers=headers).content
    # print(pictureData)
    with open("image.jpg","wb+")as f:
        f.write(pictureData)

    #显示图片
    pil_im = Image.open("image.jpg")
    pil_im.show()

    #获取用户信息
    user = input("请输入学号：")
    # passwd = input("请输入密码：")
    passwd =getpass.getpass()
    # user ="1613012XXXX"
    # passwd = "XXXXXXXX"
    valid_code = input("请输入验证码：")

    #最终生成的登陆url
    login_url ="http://xk.xidian.edu.cn/xsxkapp/sys/xsxkapp/student/check/login.do?"+"timestrap="+str(int(time.time()*1000))+"&loginName="+user+"&loginPwd="+passwd+"&verifyCode="+valid_code+"&vtoken="+pictureToken
    #print(login_url)

    #使用get方法模拟用户登陆
    response_login = ses.get(login_url,headers=headers)
    response_data = response_login.text

    #打印返回的json
    print(response_data)

    #打印token
    print("-------------------final_json:---------------------",end="\n")
    final_token = json.loads(response_data)["data"]["token"]
    print(final_token)
    return final_token
if __name__=="__main__":
    print("hello world!")
    #返回教务处内可各种操作的token
    token=login_and_getToken()

