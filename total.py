'''
运行时的变量将暂存于此
'''
#告诉整个程序下载是否停止
Down_Satuation = False
#文件夹池
DirPool = {}
#文件池
FilePool = {}
#已经浏览过的文件夹的数量
seen_dir_count = 0
#正在浏览的文件夹数量
seeing_dir_count = 0
#已找到的文件夹数量
Dir_count = 0
#已找到的文件的数量
File_count = 0
#已处理的文件数量
seeing_file_count = 0
#RPC返回文本, 使用时需先转为str在把" ' "replace为" " "
RPC_satuation = {}

RPC_error = {}
#下载信息数
RPC_count = 0
#下载信息(链接，路径，名称)
#名称 大小 下载 路径 状态
#{name, total_size, d_size, path, url, satuation}
RPC_down = {}
#页数
seeing_page = 1
#已下载数量
DdCount = 0
#记录下载的数量
dingcount = 1

pageMutiTask = 1
#下载线程
DownThread = 5
#下载任务
DownMaxTask = 3
REV = '3.6'



about = '''
NTG 2021 - (个人)版权所有
QQ:3052381496

版本:''' + REV + '''
广告招租

已授权给：MoeFireStudio
特别鸣谢：YuanTuo666

测试时间至9月12日
'''


UpdateUrl = 'https://ntgpro.lanzoui.com/iROFHst1abe'

sayUrl = 'https://ntgpro.lanzoui.com/iCpKZst1aha'

msgBox = 'https://ntgpro.lanzoui.com/iBA6jst1ave'