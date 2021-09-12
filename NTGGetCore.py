#-*- coding:utf-8 -*-
#===Author: NTGtech===

import urllib
import json
from lxml import etree
import re
import os

import NTG_base
from NTGseeting import DEBUG
import base64
'''
获取Dlink时   -   不变量
    time        从服务器获取的time
    sign        index.php line260
    randsk      已做
    share_id    获取文件列表时可得
获取Dlink时   -   变量
    fs_id       获取文件列表可得
    filesize    获取文件列表可得
    
'''
def GetFileList(Surl, Dir, Password):
    if Dir == '/':
        IsRoot = '1'
    else:
        IsRoot = '0'
    Url = 'https://pan.baidu.com/share/wxlist?channel=weixin&version=2.2.2&clienttype=25&web=1'
    Dir = urllib.parse.quote(Dir).replace('/','%2F')
    Data = "shorturl=" + Surl + "&dir=" + Dir + "&root=" + IsRoot + "&pwd=" + Password + "&page=1&num=1000&order=time"
    header = {
        "User-Agent": "netdisk",
        "Referer": "https://pan.baidu.com/disk/home",
    }
    try:
        result = json.loads(str(NTG_base.post(Url, header, Data, '')[0]))
    except:
        return 'error'
    if result['errno'] == 0 or result['errno'] == '0':
        result = result['data']['list']
    else:
        result = 'error'
    if DEBUG == True:
        NTG_base.write_file('./FileList.html', result)
        input('获取文件列表信息文件已写至FileList.html\n', Surl + '\n' + Dir + '\n' + IsRoot + '\n' + Password)
    return result
#GetFileList('1_Dl7sC5yL0KakOMAJ4XLYg', '/eui', '0', '0000')

def GetRandsk(Surl, Password):
    '''
    获取BDCLND(Randsk)
    '''
    header = {
        'User-Agent': 'netdisk',
    }
    url = 'https://pan.baidu.com/share/wxlist?clienttype=25&shorturl=' + Surl + '&pwd=' + Password
    #with requests.get(url = url, headers = header, stream=True) as fget:
    #    print(fget.headers)
    result = NTG_base.get(url, header, '', '')                       #Get Randsk From Cookie
    if result[0] == 'error':
        return 'error'
    result = result[2].split(';')
    for i in result:
        found = 'BDCLND=' in i
        if found == True:
            Randsk = i.replace('BDCLND=', '')
            break
        else:
            Randsk = ''
    for i in result:
        found = 'BAIDUID=' in i
        if found == True:
            BAIDUID = i.replace('BAIDUID=', '')
            break
        else:
            BAIDUID = ''
    if DEBUG == True:
        NTG_base.write_file('./Randsk.html', Randsk, BAIDUID)
        input('获取Randsk文件已写至Randsk.html\n', Surl + '|' + Password)
    return Randsk, BAIDUID


def GetSign(Surl, Randsk, STOKEN, BDUSS):
    '''
    获取uk, share_id, bdstoken (均不变量)
    '''
    url = 'https://pan.baidu.com/s/' + Surl
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.514.1919.810 Safari/537.36",
		"Cookie": "BDUSS=" + BDUSS + ";STOKEN=" + STOKEN + ";BDCLND=" + Randsk + ";"
    }
    result = NTG_base.get(url, header, '', '')[0]
    #正则获取
    if result[0] == 'error':
        return 'error'
    Sign = re.search(r'locals.mset\((\{.*?\})\);', str(result))
    sign = json.loads(Sign.group(1))
    '''
    Sign_Tree = etree.HTML(result)
    Sign = Sign_Tree.xpath('/html/body/script/text()')
    #此为下策，正则有问题迫不得已
    for i in Sign:                                              
        found = 'locals.mset' in i
        if found == True:
            Sign_ = i
            break
    Sign = NTG_base.getSubstr(Sign_, 'locals.mset({', '});')
    sign = json.loads('{' + Sign + '}')
    
    if DEBUG == True:
        NTG_base.write_file('./Sign_H.html', str(json.dumps(result)))
        NTG_base.write_file('./Sign_J.html', str(json.dumps(sign)))
        input('获取信息(uk share_id bdstoken)文件已写至\nhtml:Sign_H.html  Json:Sign_J.html\n', Surl, Randsk, STOKEN, BDUSS)
    '''
    #获取信息
    uk = sign['uk']
    bdstoken = sign['bdstoken']
    if DEBUG == True:
        NTG_base.write_file('./sign_oring.html', str(json.dumps(result)))
        input('获取根sign文件已写至root.html\n', Surl + '\n' + BDUSS + '\n' + STOKEN + '\n' + Randsk)
    if bdstoken != '':
        share_id = sign['shareid']
        shareid = sign['shareid']
        share_uk = sign['share_uk']
        return uk, share_id, bdstoken, shareid, share_uk
    else:
        return 'error'
    
    

def GetRoot(Surl, BDUSS, STOKEN, Randsk):
    '''

    用于获取Sign(不变量)        TimeStamp(不变量)
    '''
    url = "https://pan.baidu.com/share/tplconfig?surl=" + Surl + "&fields=sign,timestamp&channel=chunlei&web=1&app_id=250528&clienttype=0"
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.514.1919.810 Safari/537.36",
		"Cookie": "BDUSS=" + BDUSS + ";STOKEN=" + STOKEN + ";BDCLND=" + Randsk + ";"
    }
    result = NTG_base.get(url, header, '', '')[0]
    if result[0] == 'error':
        return 'error'
    result = json.loads(result)
    if DEBUG == True:
        NTG_base.write_file('./root.html', str(json.dumps(result)))
        input('获取根目录信息(sign timestamp)文件已写至root.html\n', Surl + '\n' + BDUSS + '\n' + STOKEN + '\n' + Randsk)
    sign = result['data']['sign']
    timestamp = result['data']['timestamp']
    if result['errno'] == 0 or result['errno'] == '0':
        return sign, timestamp
    else:
        return 'error'

def GetDownloadLink(fs_id, timestamp, sign, randsk, share_id, uk, BDUSS, STOKEN, Pr):
    '''
    获取下载链接，转json
    bdstoken isnoualink均为小文件传参，不适用
    uk为分享者的uk
    '''
    #print(fs_id, timestamp, sign, randsk, share_id, uk, BDUSS, STOKEN)
    app_id = '250528'
    #仅包括大文件的链接
    url = 'https://pan.baidu.com/api/sharedownload?app_id=' + app_id + '&channel=chunlei&clienttype=12&sign=' + sign + '&timestamp=' + timestamp + '&web=1'
    data = "encrypt=0&extra=" + urllib.parse.quote('{"sekey":"' + urllib.parse.quote(randsk) + '"}').replace('/','%2F').replace('25', '') + "&fid_list=" + "[" + str(fs_id) + "]" + "&primaryid=" + share_id + "&uk=" + uk + "&product=share&type=nolimit"
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.514.1919.810 Safari/537.36",
		"Cookie": "BDUSS=" + BDUSS.replace(' ', '') + ";STOKEN=" + STOKEN.replace(' ', '') + ";BDCLND=" + randsk.replace('25', '') + ";",
		"Referer": "https://pan.baidu.com/disk/home",
    }
    try:
        result = json.loads(NTG_base.post(url, header, data, '')[0])
    except:
        return 'error'
    #print(url,'\n',data,'\n',header)
    if DEBUG == True:
        NTG_base.write_file('./GetD.html', str(json.dumps(result)))
        input('获取下载链接函数，信息已写至html\n', fs_id, timestamp, sign, randsk, share_id, uk)
    #print(result)
    if result['errno'] == 0 or result['errno'] == '0':
        result = result['list'][0]['dlink'], result['list'][0]['path'].replace(Pr, ''), result['list'][0]['server_filename']
    else:
        result = 'error'
    return result
    '''
    没有 referer 就 112 ，没有 sekey 参数就 118    -20出现验证码
			参数				类型		描述
	list					json array	文件信息列表
	names				json		如果查询共享目录，该字段为共享目录文件上传者的uk和账户名称
	list[0]["category"]	int			文件类型
	list[0]["dlink"]		string		文件下载地址
	list[0]["file_name"]	string		文件名
	list[0]["isdir"]		int			是否是目录
	list[0]["server_ctime"]	int		文件的服务器创建时间
	list[0]["server_mtime"]	int		文件的服务修改时间
	list[0]["size"]		int			文件大小
	list[0]["thumbs"]				缩略图地址
	list[0]["height"]	int			图片高度
	list[0]["width"]		int			图片宽度
	list[0]["date_taken"]	int		图片拍摄时间
    
    '''


def CreateDir(dir, bdstoken, logid, randsk, BDUSS, STOKEN):
    url = 'https://pan.baidu.com/api/create?a=commit&channel=chunlei&web=1&app_id=250528&bdstoken=' + bdstoken + '&logid=' + logid + '&clienttype=0'
    header = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'Content-Length': '45',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.514.1919.810 Safari/537.36",
		"Cookie": "BDUSS=" + BDUSS.replace(' ', '') + ";STOKEN=" + STOKEN.replace(' ', '') + ";BDCLND=" + randsk + ";",
		"Referer": "https://pan.baidu.com/disk/home?",
        'sec-ch-ua': '\"Chromium\";v=\"92\", \" Not A;Brand\";v=\"99\", \"Microsoft Edge\";v=\"92\"',
        'sec-ch-ua-mobile': '?0',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
    }
    dir = dir.replace('//','/')
    data = 'path=' + urllib.parse.quote(dir).replace('/', '%2F') + '&isdir=1&block_list=%5B%5D'
    try:
        result = json.loads(NTG_base.post(url, header, data, '')[0])
    except:
        return 'error'
    if result['errno'] != 0 and result['errno'] != '0':
        return 'error'
    else:
        return 0


def save(SavePath, Surl, fs_id, share_id, from_id,  randsk, login_id, Bdstoken, BDUSS, STOKEN):
    '''
    将分享的文件保存至指定目录
    变量：fs_id, SavePath
    '''
    sekey = urllib.parse.quote(randsk).replace('25', '')
    url = 'https://pan.baidu.com/share/transfer?shareid=' + share_id + '&from=' + from_id + '&sekey=' + sekey + '&ondup=newcopy&async=1&channel=chunlei&web=1&app_id=250528&bdstoken=' + Bdstoken + '&logid=' + login_id + '&clienttype=0'
    header = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'Content-Length': '45',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.514.1919.810 Safari/537.36",
		"Cookie": "BDUSS=" + BDUSS.replace(' ', '') + ";STOKEN=" + STOKEN.replace(' ', '') + ";BDCLND=" + randsk.replace('25', '') + ";",
		"Referer": "https://pan.baidu.com/s/" + Surl,
        'sec-ch-ua': '\"Chromium\";v=\"92\", \" Not A;Brand\";v=\"99\", \"Microsoft Edge\";v=\"92\"',
        'sec-ch-ua-mobile': '?0',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
    }
    #前面变成//的地方都修复成/
    SavePath = SavePath.replace('//','/')
    data = 'fsidlist=' + urllib.parse.quote('[' + str(fs_id) + ']') + '&path=' + urllib.parse.quote(SavePath).replace('/','%2F')
    result = json.loads(NTG_base.post(url, header, data, '')[0])
    if result['errno'] != 0 and result['errno'] != '0':
        return 'error'
