from os import kill
import total
import RPC_Thread

import tkinter.messagebox
import time
import threading
def pause(TaskID, part, count):
    if part['text'] == '‖':
        part['text'] = '▶'
        part.update()
        total.RPC_down[count]['ispause'] = True
        RPC_Thread.PauseTask(TaskID)
    else:
        part['text'] = '‖'
        part.update()
        total.RPC_down[count]['ispause'] = False
        RPC_Thread.StartTask(TaskID)
    return 0

def pauseThread(TaskID, part, count):
    Tpause = threading.Thread(target = pause, args= (TaskID, part, count))
    Tpause.start()
    return 0

def killTask(t1):
    Tkill = threading.Thread(target = RPC_Thread.RemoveFile, args= (t1, ))
    Tkill.start()
    return 0

def change(stuff, page):
    pageLimted = (page - 1) * 4     #显示基数
    #如果任务总数比要显示的多或等于就继续
    if len(total.RPC_down) >= pageLimted and page > 0:

        stuff[1][1]['command'] = lambda t1 = '': print()
        stuff[2][1]['command'] = lambda t1 = '': print()
        stuff[3][1]['command'] = lambda t1 = '': print()
        stuff[4][1]['command'] = lambda t1 = '': print()

        stuff[1][2]['command'] = lambda t1 = '': print()
        stuff[2][2]['command'] = lambda t1 = '': print()
        stuff[3][2]['command'] = lambda t1 = '': print()
        stuff[4][2]['command'] = lambda t1 = '': print()
        if pageLimted + 4 <= len(total.RPC_down):
            #直接是4
            countLen = 4
        else:
            #如果比他小，总数减去显示基数则为要历边的数目
            countLen = int(len(total.RPC_down) - pageLimted)
        count = 1
        while count <= countLen:
            stuff[count][0]['text'] = '名称:' + str(total.RPC_down[pageLimted+count]['name']) + '\n'+ str(total.RPC_down[pageLimted+count]['satuation']) + str(total.RPC_down[pageLimted+count]['total_size'])
            if str(total.RPC_down[pageLimted+count]['satuation']) == '已删除':
                stuff[count][1]['text'] = '‖'
                stuff[count][1]['command'] = lambda :print()
                stuff[count][2]['command'] = lambda :print()
            else:
                #对于页面变化时按钮文本不变的补救
                if total.RPC_down[pageLimted+count]['ispause'] == True:
                    stuff[count][1]['text'] = '▶'
                else:
                    stuff[count][1]['text'] = '‖'
                stuff[count][1]['command'] = lambda t1 = total.RPC_down[pageLimted+count]['token'], t2 = stuff[count][1], t3 = pageLimted+count: pauseThread(t1, t2, t3)
                stuff[count][2]['command'] = lambda t1 = total.RPC_down[pageLimted+count]['token']: killTask(t1)
            count += 1
        #没有任务的label就重置
        while count <= 4:
            stuff[count][0]['text'] = ''
            stuff[count][1]['text'] = '‖'
            count += 1
        stuff[1][0].update()
        stuff[2][0].update()
        stuff[3][0].update()
        stuff[4][0].update()
    else:
        tkinter.messagebox('错误', '不存在的页数')
    return 0

def ThreadTask(stuff):
    while True:
        time.sleep(0.05)
        count = 1
        if len(total.RPC_down) != 0:
            #count += 1
            while count <= len(total.RPC_down):
                RPC_Thread.GetDownSta(total.RPC_down[count]['token'], count)
                count += 1
                change(stuff, total.pageMutiTask)
                
        change(stuff, total.pageMutiTask)