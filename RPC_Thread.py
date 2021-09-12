import NTG_base
import total
    
import urllib
import urllib.request
import json
#已弃用的服务端
'''
def service_client(new_socket):
    request = new_socket.recv(1024)
    request = request.decode("gb18030")  #  解码 = 中文所以是gb2312
    request_lines = request.splitlines()  #  按照行('\r', '\r\n', \n')分隔，返回一个包含各行作为元素的列表
    try:
        ret = str(request_lines[0]).split(' ')[1]     #获取用户访问的url - 如 /index.html
        ret = urllib.parse.unquote(ret)
    except:
        return 0

if __name__ == '__main__':
    link = '127.0.0.2'
    port = 1809
    tcp_sever_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_sever_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_sever_socket.bind((link, port))
    tcp_sever_socket.listen(128)
    while True:
        new_socket,client_addr=tcp_sever_socket.accept()
        p=threading.Thread(target=service_client,args=(new_socket,))
        p.start()

'''
def ADDfile(Url, Path, name):
    print('RPC:',Path, name, 'Max:', total.DownMaxTask)
    jsonreq = json.dumps({'jsonrpc':'2.0', 'id':'qwer',
                       'method':'aria2.addUri',
                       'params':[[Url],
                       {'header':'User-Agent: LogStatistic',
                       'max-connection-per-server': str(total.DownThread),
                       'max-concurrent-downloads': str(total.DownMaxTask),
                       'dir': Path,
                       'out': name}]})
    jsonreq = bytes(jsonreq.encode())
    c = urllib.request.urlopen('http://localhost:6800/jsonrpc', jsonreq)
    response = json.loads(c.read())
    TaskID = response['result']
    print('任务Token:', TaskID)
    return TaskID

def GetDownSta(TaskID, part):
    jsonreq = json.dumps({'jsonrpc':'2.0', 'id':'qwer',
                      'method':'aria2.tellStatus',
                      'params':[TaskID]})
    jsonreq = bytes(jsonreq.encode())
    try:
        c = urllib.request.urlopen('http://localhost:6800/jsonrpc', jsonreq)
    except:
        total.RPC_down[part]['total_size'] = ''
        total.RPC_down[part]['token'] = TaskID
        total.RPC_down[part]['satuation'] = '已删除'
        total.RPC_down[part]['Engstatus'] = ''
        return 0
    response = json.loads(c.read())
    #总大小
    Length = NTG_base.size(response['result']['files'][0]['length'])
    Speed = NTG_base.size(response['result']['downloadSpeed'])
    complete = NTG_base.size(response['result']['files'][0]['completedLength'])
    Downlen = int(len(response['result']['files'][0]['uris']))
    downPath = response['result']['dir']
    downstatus = response['result']['status']
    try:
        total.RPC_down[part]['total_size'] = '总大小:' + str(Length[0]) + Length[1] + ' 已下载:' + str(complete[0]) + complete[1] + ' 进度:' + str(round(int(response['result']['files'][0]['completedLength']) / int(response['result']['files'][0]['length']) * 100, 2)) + '%'
    except:
        total.RPC_down[part]['total_size'] = '总大小:' + str(Length[0]) + Length[1] + ' 已下载:' + str(complete[0]) + complete[1] + ' 进度:0.00%'
    total.RPC_down[part]['token'] = TaskID
    total.RPC_down[part]['Engstatus'] = downstatus
    status = {
        'paused': '暂停',
        'active': '下载中',
        'complete': '完成',
    }
    total.RPC_down[part]['satuation'] = status.get(downstatus, '已删除') + ' 速度:' + str(Speed[0]) + Speed[1]
    
    #part['text'] = '总大小:' + str(Length[0]) + Length[1] + ' 速度:' + str(Speed[0]) + Speed[1] + ' 已下载:' + str(complete[0]) + complete[1] + ' 线程数' + str(Downlen) + ' 下载路径' + downPath
    #part.update()
    #print('总大小:',Length[0],Length[1],'速度:',Speed[0],Speed[1],'已下载',complete[0],complete[1],'线程数',Downlen,'下载路径',downPath, end = '\r')
    #print(response['result']['files'][0]['length'], '|', response['result']['files'][0]['completedLength'])
    return response['result']['files'][0]['length'], response['result']['files'][0]['completedLength']


def RemoveFile(TaskID):
    jsonreq = json.dumps({'jsonrpc':'2.0', 'id':'qwer',
                      'method':'aria2.remove',
                      'params':[TaskID]})
    jsonreq = bytes(jsonreq.encode())
    c = urllib.request.urlopen('http://localhost:6800/jsonrpc', jsonreq)
    response = json.loads(c.read())
    print(response)
    return response
#RemoveFile('55c91cc3bfe8bcb4')
def PauseTask(TaskID):
    jsonreq = json.dumps({'jsonrpc':'2.0', 'id':'qwer',
                      'method':'aria2.pause',
                      'params':[TaskID]})
    jsonreq = bytes(jsonreq.encode())
    c = urllib.request.urlopen('http://localhost:6800/jsonrpc', jsonreq)
    response = json.loads(c.read())
    return response

def StartTask(TaskID):
    jsonreq = json.dumps({'jsonrpc':'2.0', 'id':'qwer',
                      'method':'aria2.unpause',
                      'params':[TaskID]})
    jsonreq = bytes(jsonreq.encode())
    c = urllib.request.urlopen('http://localhost:6800/jsonrpc', jsonreq)
    response = json.loads(c.read())
    return response