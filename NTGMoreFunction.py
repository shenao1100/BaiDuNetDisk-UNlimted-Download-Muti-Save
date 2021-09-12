import time
import os

import NTG_base
import NTGGetCore
import total
import RPC_Thread
def ProcessLink(input):
    found = 'https://pan.baidu.com/s/' in input
    if found == True:
        found = '#list/' in input
        if found == True:
            input = NTG_base.getSubstr(input, 'https://pan.baidu.com/s/', '#list/')
        else:
            input = NTG_base.strstr(input, 'https://pan.baidu.com/s/')
        return input
    else:
        return input

def ProcessList(input, Pr):
    #print('PR:', Pr)
    for i in input:
        print(i)
        if i['isdir'] == 0 or i['isdir'] == '0':
            total.File_count += 1
            temp = {
                'File_name': i['server_filename'],
                'File_path': i['path'],
                'MD5': i['md5'],
                'size': i['size'],
                'fs_id': i['fs_id'],
            }
            if Pr == '':
                temp['Realpath'] = NTG_base.get_back_path(temp['File_path'])
            else:
                temp['Realpath'] = NTG_base.get_back_path(temp['File_path'].replace(Pr, '/'))
            #print(temp['File_path'], '下载到', temp['Realpath'])
            total.FilePool[total.File_count] = temp
        else:
            total.Dir_count += 1
            temp = {
                'path': i['path']
            }
            if Pr == '':
                temp['Realpath'] = temp['path']
            else:
                temp['Realpath'] = temp['path'].replace(Pr, '/')
            print('16000', temp['Realpath'])
            total.DirPool[total.Dir_count] = temp
    return 0

#循环解析文件夹
def DirGet(Pr, Surl, Pwd):
    #{1:'/我的资源/文件夹' .....}
    #同下，按照数量不断找文件夹获取文件列表
    #交给list处理，直到处理完成
    while total.seen_dir_count <= total.Dir_count:
        total.seen_dir_count += 1
        if len(total.DirPool) >= total.seen_dir_count:
            single = total.DirPool[total.seen_dir_count]
            list = NTGGetCore.GetFileList(Surl, single['path'], Pwd)
            ProcessList(list, Pr)
    total.Down_Satuation = False
    return 0

#循环添加任务
def FileDown(Path, timestamp, sign, randsk, share_id, uk, BDUSS, STOKEN, part, Pr, bt):
    while True:
        time.sleep(0.1)
        total.seeing_file_count += 1
        if len(total.FilePool) >= total.seeing_file_count and len(total.FilePool) != 0:
            #如果我想下载的文件数量比已经解析的文件数量少，就不下并将下载的文件数量复位
            #如果文件池中数量是0，那就不下
            temp = total.FilePool[total.seeing_file_count]
            #取文件信息列表中的一个为temp
            #取temp中的fsid和size
            fs_id = temp['fs_id']
            size = temp['size']
            part['text'] = '解析下载链接...'
            part.update()
            #扔进函数解出link
            result = NTGGetCore.GetDownloadLink(fs_id, timestamp, sign, randsk, share_id, uk, BDUSS, STOKEN, Pr)
            #把要用户下到的路径和分享链接中的路径合并
            Path_ = Path + temp['Realpath']
            Path_ = Path_.replace('//', '/')
            part['text'] = '创建任务...'
            part.update()
            #在RPC中添加任务，返回token
            d_name = result[1].split('/')[-1]
            r = RPC_Thread.ADDfile(result[0], Path_, d_name)
            #total.RPC_down[total.DdCount]['token'] = r
            add_inf = {
                'name': d_name,
                'total_size': '暂无',
                'token': r,
                'path': Path_,
                'url': result[0],
                'satuation': '等待中',
                'isdownload': False,        #用户下载过的指示，区别是下载过就会出现token
                'ispause': False,           #用户暂停的提示，如果暂停就继续
                'Engstatus': ''
            }
            total.RPC_down[total.dingcount] = add_inf
            total.dingcount += 1
        elif total.Down_Satuation == False and total.seeing_file_count -1 == len(total.FilePool):
            part['text'] = '解析完成, 请去下载任务查看'
            part.update()
            bt.config(state = 'normal')
            bt.update()
            break
        else:
            total.seeing_file_count -= 1

#循环解析并建立文件夹
def DirSave(Pr, path_local, Surl, Pwd, bdstoken, logid, randsk, BDUSS, STOKEN, part):
    #{1:'/我的资源/文件夹' .....}
    #同下，按照数量不断找文件夹获取文件列表
    #交给list处理，直到处理完成
    while total.seen_dir_count <= total.Dir_count:
        total.seen_dir_count += 1
        time.sleep(0.1)
        print(len(total.DirPool) ,'|', total.seen_dir_count)
        if len(total.DirPool) >= total.seen_dir_count:
            single = total.DirPool[total.seen_dir_count]
            list = NTGGetCore.GetFileList(Surl, single['path'], Pwd)
            path_creat = path_local + single['Realpath']
            path_creat = path_creat.replace('//', '/')
            part['text'] = '正在建立文件夹:' + path_creat
            print('建立文件夹', path_creat)
            part.update()
            NTGGetCore.CreateDir(path_creat, bdstoken, logid, randsk, BDUSS, STOKEN)
            ProcessList(list, Pr)
    total.Down_Satuation = False
    return 0

#循环保存文件
def SurlSave(Path, Surl, share_id, from_id,  randsk, login_id, Bdstoken, BDUSS, STOKEN, part, bt):
    while True:
        time.sleep(0.1)
        total.seeing_file_count += 1
        if len(total.FilePool) >= total.seeing_file_count and len(total.FilePool) != 0:
            #如果我想下载的文件数量比已经解析的文件数量少，就不下并将下载的文件数量复位
            #如果文件池中数量是0，那就不下
            temp = total.FilePool[total.seeing_file_count]
            #取文件信息列表中的一个为temp
            #取temp中的fsid和size
            fs_id = temp['fs_id']
            size = temp['size']
            part['text'] = '解析下载链接...'
            part.update()
            #扔进函数解出link
            pathSave = temp['Realpath']
            #合并路径
            path_ = Path + pathSave
            pathTemp = path_.replace('//', '/')
            part['text'] = '保存文件:' + pathTemp
            NTGGetCore.save(pathTemp, Surl, fs_id, share_id, from_id,  randsk, login_id, Bdstoken, BDUSS, STOKEN)
        elif total.Down_Satuation == False and total.seeing_file_count -1 == len(total.FilePool):
            part['text'] = '保存完成'
            part.update()
            bt.config(state = 'normal')
            bt.update()
            break
        else:
            total.seeing_file_count -= 1
    



