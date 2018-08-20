#coding:utf-8
'''
本程序仅供学习使用 请勿用于其他目的
功能：自动点击关注

使用方法:
0.5.安装Pillow
0.将手机屏幕截图 测量关注按钮的横坐标（如：894） 将所有item_x设置为894
    并测量该特殊像素点的RGB值如(254,109,137) 将RGB设置为(254,109,137)
1.安装adb
2.Android手机打开USB调试
3.连接手机，打开抖音他人关注列表
4.执行程序

问题：
    抖音关注人过多会被禁止


NEWMOREYONG！！！
'''
import os
from PIL import Image
import random
import time

item_x = 894
RGB = (254, 109, 137)


def get_and_save_screen():
    """截图并保存至程序目录中"""
    os.system("adb shell screencap -p /sdcard/screen.png")
    os.system("adb pull /sdcard/screen.png .")


def cal_position():
    """计算每个关注按钮的位置（横坐标第手动计算的894）函数执行后 返回一个生成式"""
    screen = Image.open("screen.png")
    x=screen.size[0]
    y=screen.size[1]
    print(x,y)
    for item_y in range(1,1920):
        if screen.getpixel((item_x,item_y))[:3] ==RGB:
            # print("x:"+str(item_y))
            yield item_y


def next_page():
    """功能：翻页"""
    os.system("adb shell input swipe 666 1560 666 225 560")
    print("成功翻页")


def random_x_and_y(x,y):
    """目的：将x y 随机成新做的坐标  （模拟点击操作)"""
    x = x + random.randint(1,50)
    y = y + random.randint(1,20)
    return x,y



def click_position(x,y):
    """传入参数x，y 功能：点击对应的坐标"""
    str_of_click_pos = "adb shell input tap "+str(x)+" "+str(y)
    os.system(str_of_click_pos)
    print("关注成功")


if __name__ =="__main__":
    for i in range(2):    #2代表页数

        #1.截图
        get_and_save_screen()
        #2.获取纵坐标y
        pos =cal_position()
        #3.遍历y坐标 炳点击
        for item_y in pos:
            item_x= 894 #x手动测量的
            #随机点击位置
            new_x,new_y=random_x_and_y(item_x,item_y)
            #点击位置
            click_position(new_x,new_y)
            time.sleep(1) #关注一个人后暂停一秒
        #4.翻页
        next_page()
        time.sleep(2) #翻页后暂停两秒