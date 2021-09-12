#-*- coding:utf-8 -*-

import NTGGetCore
import NTGMoreFunction
import total
import NTG_base

import os
import threading
import re
import json
import base64
import tkinter.messagebox
def about(COOKIE):
    print()

def MutiSave(COOKIE, Surl, Pwd, Path, part, bt):
    '''
    先用GetRandsk获取Randsk
    再用GetSign, GetRoot获取不变量
    移交GetFileList获取列表
    最后传到GetDownloadLink获取参数 链接
    '''
    total.Down_Satuation = False
    total.DirPool = {}
    total.FilePool = {}
    total.seen_dir_count = 0
    total.seeing_dir_count = 0
    total.Dir_count = 0
    total.File_count = 0
    total.seeing_file_count = 0
    total.RPC_satuation = {}
    total.RPC_error = {}

    Surl = NTGMoreFunction.ProcessLink(Surl)
    total.Down_Satuation = True
    STOKEN = re.search(r'STOKEN=(.+?);', str(COOKIE))
    STOKEN = STOKEN.group(1)
    BDUSS = re.search(r'BDUSS=(.+?);', str(COOKIE))
    BDUSS = BDUSS.group(1)
    
    if BDUSS == '' or STOKEN == '':
        tkinter.messagebox.showerror('错误', 'COOKIE处理失败,请联系管理员')
        bt.config(state = 'normal')
        bt.update()
        return 0
    else:
        try:
            part['text'] = '解析信息中...'
            part.update()
            result = NTGGetCore.GetRandsk(Surl, Pwd)
            Randsk = result[0]
            BAIDUID = result[1]

            Sign_list = NTGGetCore.GetSign(Surl, Randsk, STOKEN, BDUSS)
            if Sign_list == 'error':
                tkinter.messagebox.showerror('错误', '获取信息时出错[SL]')
                bt.config(state = 'normal')
                bt.update()
                return 0
            Sign_true = NTGGetCore.GetRoot(Surl, BDUSS, STOKEN, Randsk)
            if Sign_true == 'error':
                tkinter.messagebox.showerror('错误', '获取信息时出错[RT]')
                bt.config(state = 'normal')
                bt.update()
                return 0
            Uk = Sign_list[0]
            Share_id = str(Sign_list[1])
            Bdstoken = Sign_list[2]
            Sign = Sign_true[0]
            TimeStamp = str(Sign_list[3])
            share_uk = str(Sign_list[4])
            login_id = base64.b64encode(bytes(BAIDUID.encode()))
            login_id = login_id.decode()
        except:
            tkinter.messagebox.showerror('错误', '信息获取失败')
            bt.config(state = 'normal')
            bt.update()
            return 0
        part['text'] = '获取文件列表...'
        part.update()
        list = NTGGetCore.GetFileList(Surl, '/', Pwd)
        if list == 'error':
            tkinter.messagebox.showerror('错误', '获取根目录文件列表时出错')
            bt.config(state = 'normal')
            bt.update()
            return 0
        pathReplace = list[0]['path'].split('/')[:-1]
        print(list[0])
        Pr = ''
        for i in pathReplace:
            if i != '':
                Pr = Pr + '/' + i
        print(Pr)
        NTGMoreFunction.ProcessList(list, Pr)
        Tfile = threading.Thread(target = NTGMoreFunction.SurlSave, args= (Path, Surl, Share_id, share_uk,  Randsk, login_id, Bdstoken, BDUSS, STOKEN, part, bt))
        Tdir = threading.Thread(target = NTGMoreFunction.DirSave, args= (Pr, Path, Surl, Pwd, Bdstoken, login_id, Randsk, BDUSS, STOKEN, part))
        Tfile.start()
        Tdir.start()
        


def Download(COOKIE, Surl, Pwd, Path, part, bt):
    '''
    先用GetRandsk获取Randsk
    再用GetSign, GetRoot获取不变量
    移交GetFileList获取列表
    最后传到GetDownloadLink获取参数 链接
    '''
    #重置所有变量
    total.Down_Satuation = False
    total.DirPool = {}
    total.FilePool = {}
    total.seen_dir_count = 0
    total.seeing_dir_count = 0
    total.Dir_count = 0
    total.File_count = 0
    total.seeing_file_count = 0
    total.RPC_satuation = {}
    total.RPC_error = {}
    #处理分享链接
    Surl = NTGMoreFunction.ProcessLink(Surl)
    #设置变量
    total.Down_Satuation = True
    #正则获取cookie信息
    STOKEN = re.search(r'STOKEN=(.+?);', str(COOKIE))
    STOKEN = STOKEN.group(1)
    BDUSS = re.search(r'BDUSS=(.+?);', str(COOKIE))
    BDUSS = BDUSS.group(1)
    #如果获取的到没报错继续
    if BDUSS == '' or STOKEN == '':
        tkinter.messagebox.showerror('错误', 'cookie处理错误')
        bt.config(state = 'normal')
        bt.update()
        return 0
    else:
        part['text'] = '解析信息中...'
        part.update()
        #获取Randsk，sign，root页面的信息
        Randsk = NTGGetCore.GetRandsk(Surl, Pwd)[0]
        Sign_list = NTGGetCore.GetSign(Surl, Randsk, STOKEN, BDUSS)
        if Sign_list == 'error':
            tkinter.messagebox.showerror('错误', '获取信息时出错[SL]')
            bt.config(state = 'normal')
            bt.update()
            return 0
        Sign_true = NTGGetCore.GetRoot(Surl, BDUSS, STOKEN, Randsk)
        if Sign_true == 'error':
            tkinter.messagebox.showerror('错误', '获取信息时出错[RT]')
            bt.config(state = 'normal')
            bt.update()
            return 0
        #处理获取到的信息，取Uk，shareID，bdstoken（小文件需要），Sign，Timestamp
        Uk = Sign_list[4]
        Share_id = str(Sign_list[1])
        Bdstoken = Sign_list[2]
        Sign = Sign_true[0]
        TimeStamp = str(Sign_true[1])

        part['text'] = '解析文件列表...'
        part.update()
        #获取第一级文件列表
        list = NTGGetCore.GetFileList(Surl, '/', Pwd)
        if list == 'error':
            tkinter.messagebox.showerror('错误', '获取根目录文件列表时出错')
            bt.config(state = 'normal')
            bt.update()
            return 0
        #百度网盘链接分享的路径是分享者网盘中的路径
        #分享一个[补丁.zip]获取到的可能是[/我的资源/学习/补丁.zip]
        #获取需要replace掉的玩意(/我的资源/学习)
        #因为是分享链接的根目录，所以我们想要的路径都是(/名字)需要替换的就是文件名前面的那些
        #把文件名前面的转列表
        pathReplace = list[0]['path'].split('/')[:-1]
        Pr = ''
        #求出需要replace的
        for i in pathReplace:
            if i != '':
                Pr = Pr + '/' + i
        #处理的时候传入需要replace就行
        NTGMoreFunction.ProcessList(list, Pr)
        Tdir = threading.Thread(target = NTGMoreFunction.DirGet, args= (Pr, Surl, Pwd))
        Tfile = threading.Thread(target = NTGMoreFunction.FileDown, args= (Path, TimeStamp, Sign, Randsk, Share_id, Uk, BDUSS, STOKEN, part, Pr, bt))
        #TDown = 
        Tfile.start()
        Tdir.start()
    return 0

def m():
    logo = '''
==================================================
|               BDNDM Rev2.0                     |
==================================================
         ____    ____________________________
        /    |\ /  ___    ___________________|\\
       /  |  | /  / __|  |\__________________\|
      /  /|  |/  / /  |  ||
     /  / |  |  / /   |  ||    Technology 
    /__/ /|____/ /    |__||      Create
    \__\/  \___\/      \_\|       Fun
    
                Power By NTGtech
--------------------------------------------------'''
    print(logo)
    is_file = os.path.exists("./res/conf/cookie.ntg")
    if is_file == True:
        COOKIE = NTG_base.read_file('./res/conf/cookie.ntg')
        
    else:
        print('      COOKIE文件缺失，请使用正确的方式启动程序！')
        print('---------------------------------------------------')
        input('按回车键退出...')
        os._exit(0)
