import tkinter as tk
import tkinter.messagebox
import os
import threading
from PIL import Image, ImageTk
import time

from NTGrun import Download
from NTGrun import MutiSave
import NTGMoreFunction
import NTG_base
import total
import NTGServer
import code
import NTGmutiTask

def vi_Dl(COOKIE, Surl, Pwd, Path, part, bt):
    bt.config(state = 'disabled')
    bt.update()
    #COOKIE, Surl_entry.get(), Pwd_entry.get(), target_label['text'], label_satution
    is_file = os.path.exists(Path)
    if is_file == False:
        tkinter.messagebox.showerror('错误', '请前往设置填写下载路径')
        bt.config(state = 'normal')
        bt.update()
        return 0
    elif Surl == '':
        tkinter.messagebox.showerror('错误', '未输入下载链接！')
        bt.config(state = 'normal')
        bt.update()
        return 0
    else:
        Download(COOKIE, Surl, Pwd, Path, part, bt)
        

def vi_save(COOKIE, Surl, Pwd, Path, part, bt):
    bt.config(state = 'disabled')
    bt.update()
    print(COOKIE)
    #Cookie_label['text'], Surl_entry_Save.get(), Pwd_entry_Save.get(), Pth_entry.get(), label_satution_save
    if COOKIE == '' or COOKIE == '请在登陆账号软件设置cookie->':
        tkinter.messagebox.showerror('错误', '请前往设置填写cookie')
        bt.config(state = 'normal')
        bt.update()
        return 0
    else:
        MutiSave(COOKIE, Surl, Pwd, Path, part, bt)

def addPage(stuff):
    
    if total.pageMutiTask * 4 <= len(total.RPC_down):
        total.pageMutiTask += 1
        NTGmutiTask.change(stuff, total.pageMutiTask)
    else:
        tkinter.messagebox.showwarning('警告', '不能再多了')

def negiPage(stuff):
    if total.pageMutiTask - 1 >= 1:
        total.pageMutiTask -= 1
        NTGmutiTask.change(stuff, total.pageMutiTask)
    else:
        tkinter.messagebox.showwarning('警告', '你是想看-1个任务吗？')

def addThread(part, path, change):
    T = int(part['text'])
    if T != 16:
        T += 1
        part['text'] = str(T)
        part.update()
        NTG_base.write_file(path, str(T))
        if change == 'downthread':
            total.DownThread = T
    else:
        T = 1
        part['text'] = str(T)
        part.update()
        NTG_base.write_file(path, str(T))
        if change == 'downthread':
            total.DownThread = T
    print(total.DownThread)
    return 0

def negiThread(part, path, change):
    T = int(part['text'])
    if T != 1:
        T -= 1
        part['text'] = str(T)
        part.update()
        NTG_base.write_file(path, str(T))
        if change == 'downthread':
            total.DownThread = T
    else:
        T = 16
        part['text'] = str(T)
        part.update()
        NTG_base.write_file(path, str(T))
        if change == 'downthread':
            total.DownThread = T
    print(total.DownThread)
    return 0

def ThreadTask(Ldling, Lhsize, Lddsize, Ldpath, Lsatu, page_label):
    while True:
        time.sleep(0.1)
        NTGMoreFunction.taskSatu(Ldling, Lhsize, Lddsize, Ldpath, Lsatu, page_label)

def show(part):
    FrameMain.place_forget()
    part.place(x = 0, y = 0)

def hide(part):
    FrameMain.place(x = 0, y = 0)
    part.place_forget()

def dictionary(part):
    path_text = tk.filedialog.askdirectory()
    part['text'] = path_text
    part.update()
    NTG_base.write_file('./res/conf/path.ntg', path_text)

def Root():
    COOKIE = 'COOKIE = BAIDUID=039935838FA858492D08EB8128C4A033:FG=1; BDUSS=ElMS3Q4d3ZNTUVIaHVoWThjR1htWHZPVk9xNU41Y0dkZ0VrZGNVM0NkS2NuejFoRVFBQUFBJCQAAAAAAAAAAAEAAABaW33GvdDO0sG6xt~G32VkdGUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJwSFmGcEhZhR; BDUSS_BFESS=ElMS3Q4d3ZNTUVIaHVoWThjR1htWHZPVk9xNU41Y0dkZ0VrZGNVM0NkS2NuejFoRVFBQUFBJCQAAAAAAAAAAAEAAABaW33GvdDO0sG6xt~G32VkdGUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJwSFmGcEhZhR; csrfToken=Joad0GLsqdxebfTD2_fdysl-; STOKEN=60f3fcec496f7ef4bf89ecd4a3df945443b8a0b4440b4f2610b47e9bf5301b57; Hm_lvt_7a3960b6f067eb0085b7f96ff5e660b0=1628645485,1628645513,1628645577,1628836511; Hm_lpvt_7a3960b6f067eb0085b7f96ff5e660b0=1628836511; PANPSC=288503388540460989%3AKkwrx6t0uHBQbyw1Bjrj%2FkYemHfSgA%2FT62sxzyFSlhXQLA9BKrymF%2BueiX2U28NGz5AXgqJ5NyDdjE4osJ3wiTgOvhx7XIhXKJFYC78P9YwJzyoDFRsY0ALL1yD3J8rtCMdFTD9lHqQu%2FGN14ZZ7Xl9l5VLCkYtGsG7YZLnfZ%2BUZCTLBKS67EjEZmK5RR4JqKRa8bE2197xXNi79NFj1K%2FgT7Eg6UyTb'
    #颜色设置
    Color0 = '#6e6e91'      #背景色
    Color1 = '#575773'      #标签色
    Color2 = '#49495f'      #按钮色
    Color3 = '#3b3b4e'      #Satu色
    Fcolor = '#eaeaea'      #字体色

    #名称设置
    Name = 'BaiDu NetDisk Download Manager 3'
    Description = '科技 创造一切'

    #参数
    RootSize = '508x310'
    WidthFull = 480
    Height = 25
    FontFamily = 'bold'
    logo = './logo.ico'


    #基础窗口
    root = tk.Tk()
    Img =  tk.PhotoImage(file='./res/show.png')
    donate_url = 'wxp://f2f0mNWRm4FpJsc_C_rjsZTq_NrD2HzyhQie'
    NTG_base.make_qr(donate_url, './res/conf/donate.png')
    photo = Image.open('./res/conf/donate.png')
    photo = photo.resize((190,190))
    img_QR = ImageTk.PhotoImage(photo)
    root.config(bg = Color0)
    root.geometry(RootSize)
    root.resizable(0,0)
    root.iconbitmap(logo)
    root.title(Name)

    global FrameMain
    FrameMain = tk.Frame(root, bg = Color0)
    FrameMain.place(x=0, y=0)
    label_title = tk.Label(FrameMain, bg = Color0, fg = Fcolor, text = Name, font = ('思源黑体', 16, "bold"))
    label_title.grid(row=1, column=0, padx=10, pady=10)

    label_say = tk.Label(FrameMain, bg = Color0, fg = Fcolor, text = Description, font = (FontFamily, ))
    label_say.grid(row=2, column=0, padx=10, pady=10)

    Bt_Main = tk.Button(FrameMain, width=WidthFull, height=Height,relief='flat', compound='center',bg = Color2,
        command = lambda: show(FrameDown),
        bd = -1, text = '下载!', image = Img, fg = Fcolor)
    Bt_Main.grid(row=3, column=0, padx=10, pady=5)

    Bt_Main = tk.Button(FrameMain, width=WidthFull, height=Height,relief='flat', compound='center',bg = Color2,
        command = lambda: show(FrameSave),
        bd = -1, text = '转存!', image = Img, fg = Fcolor)
    Bt_Main.grid(row=4, column=0, padx=10, pady=5)
    
    Bt_Task = tk.Button(FrameMain, width=WidthFull, height=Height,relief='flat', compound='center',bg = Color2,
        command = lambda: show(frameMutiTask),
        bd = -1, text = '任务!', image = Img, fg = Fcolor)
    Bt_Task.grid(row=5, column=0, padx=10, pady=5)

    Bt_Conf = tk.Button(FrameMain, width=WidthFull, height=Height,relief='flat', compound='center',bg = Color2,
        command = lambda: show(FrameSet),
        bd = -1, text = '设置!', image = Img, fg = Fcolor)
    Bt_Conf.grid(row=6, column=0, padx=10, pady=5)

    Bt_Donate = tk.Button(FrameMain, width=WidthFull, height=Height,relief='flat', compound='center',bg = Color2,
        command = lambda: show(FrameDonate),
        bd = -1, text = '赞助', image = Img, fg = Fcolor)
    Bt_Donate.grid(row=7, column=0, padx=10, pady=5)

    label_author = tk.Label(FrameMain, bg = Color0, fg = Fcolor, text = 'Power By NTG')
    label_author.grid(row=8, column=0, padx=10, pady=5)



    FrameDown = tk.Frame(root, bg = Color0)
    FrameDown.place(x=0, y=0)

    label_title = tk.Label(FrameDown, bg = Color0, fg = Fcolor, text = '下载', font = ('思源黑体', 16, "bold"))
    label_title.grid(row=1, column=0, padx=10, pady=10)

    label_info = tk.Label(FrameDown, bg = Color0, fg = Fcolor,font = (FontFamily, ),text = '分享链接>')
    label_info.grid(row=2, column=0, padx=10, pady=0, sticky='W')

    Surl_entry = tk.Entry(FrameDown,relief="flat", bg = Color1, fg = Fcolor, width = 69)
    Surl_entry.grid(row=3, column=0, padx=10, pady=10)

    label_info = tk.Label(FrameDown, bg = Color0, fg = Fcolor,font = (FontFamily, ),text = '提取码>')
    label_info.grid(row=4, column=0, padx=10, pady=0, sticky='W')
    
    Pwd_entry = tk.Entry(FrameDown,relief="flat", bg = Color1, fg = Fcolor, width = 69)
    Pwd_entry.grid(row=5, column=0, padx=10, pady=10)

    Bt_Down = tk.Button(FrameDown, width=WidthFull, height=Height,relief='flat', compound='center',bg = Color2,
        command = lambda: vi_Dl(COOKIE, Surl_entry.get(), Pwd_entry.get(), target_label['text'], label_satution, Bt_Down),
        bd = -1, text = '下载!', image = Img, fg = Fcolor)
    Bt_Down.grid(row=6, column=0, padx=10, pady=5)
    
    Bt_Back = tk.Button(FrameDown, width=WidthFull, height=Height,relief='flat', compound='center',bg = Color2,
        command = lambda: hide(FrameDown),
        bd = -1, text = '返回!', image = Img, fg = Fcolor)
    Bt_Back.grid(row=7, column=0, padx=10, pady=5)

    label_satution = tk.Label(FrameDown,bg = Color3,fg = Fcolor,text = '状态：无',width = 72,height=1)
    label_satution.grid(row=8, column=0, padx=0, pady=20)




    FrameSave = tk.Frame(root, bg = Color0)
    FrameSave.place(x=0, y=0)

    label_info = tk.Label(FrameSave, bg = Color0, fg = Fcolor,font = (FontFamily, ),text = '分享链接>')
    label_info.grid(row=2, column=0, padx=10, pady=5, sticky='W')

    Surl_entry_Save = tk.Entry(FrameSave,relief="flat", bg = Color1, fg = Fcolor, width = 69)
    Surl_entry_Save.grid(row=3, column=0, padx=10, pady=5)

    label_info = tk.Label(FrameSave, bg = Color0, fg = Fcolor,font = (FontFamily, ),text = '提取码>')
    label_info.grid(row=4, column=0, padx=10, pady=0, sticky='W')
    
    Pwd_entry_Save = tk.Entry(FrameSave,relief="flat", bg = Color1, fg = Fcolor, width = 69)
    Pwd_entry_Save.grid(row=5, column=0, padx=10, pady=5)

    label_info = tk.Label(FrameSave, bg = Color0, fg = Fcolor,font = (FontFamily, ),text = '保存到网盘的路径>')
    label_info.grid(row=6, column=0, padx=10, pady=0, sticky='W')

    Pth_entry = tk.Entry(FrameSave,relief="flat", bg = Color1, fg = Fcolor, width = 69)
    Pth_entry.grid(row=7, column=0, padx=10, pady=5)
    Pth_entry.insert(0, '/我的资源')

    Bt_Save = tk.Button(FrameSave, width=WidthFull, height=Height,relief='flat', compound='center',bg = Color2,
        command = lambda: vi_save(Cookie_label['text'], Surl_entry_Save.get(), Pwd_entry_Save.get(), Pth_entry.get(), label_satution_save, Bt_Save),
        bd = -1, text = '转存!', image = Img, fg = Fcolor)
    Bt_Save.grid(row=8, column=0, padx=10, pady=5)
    
    Bt_Back = tk.Button(FrameSave, width=WidthFull, height=Height,relief='flat', compound='center',bg = Color2,
        command = lambda: hide(FrameSave),
        bd = -1, text = '返回!', image = Img, fg = Fcolor)
    Bt_Back.grid(row=9, column=0, padx=10, pady=5)

    label_satution_save = tk.Label(FrameSave,bg = Color3,fg = Fcolor,text = '状态：无',width = 72,height=1)
    label_satution_save.grid(row=10, column=0, padx=0, pady=20)




    FrameSet = tk.Frame(root, bg = Color0)
    FrameSet.place(x=0, y=0)

    label_title = tk.Label(FrameSet, bg = Color0, fg = Fcolor, text = '设置', font = ('思源黑体', 16, "bold"))
    label_title.grid(row=1, column=0, padx=10, pady=10)

    label_info = tk.Label(FrameSet, bg = Color0, fg = Fcolor,font = (FontFamily, ),text = '下载路径>')
    label_info.grid(row=2, column=0, padx=10, pady=0, sticky='W')

    target_label = tk.Label(FrameSet,bg = Color1,fg = Fcolor,width = 69,text = '请按下右侧按钮来选择下载的路径->')
    target_label.grid(row=3, column=0, padx=10, pady=0)

    label_info = tk.Label(FrameSet, bg = Color0, fg = Fcolor,font = (FontFamily, ),text = '您的Cookie>')
    label_info.grid(row=4, column=0, padx=10, pady=0, sticky='W')

    Cookie_label = tk.Label(FrameSet,bg = Color1,fg = Fcolor,width = 69,text = '请在登陆账号软件设置cookie->')
    Cookie_label.grid(row=5, column=0, padx=10, pady=0)

    Bt_from = tk.Button(FrameSet,bg = Color2,fg = Fcolor ,relief="flat",text = '浏览',command = lambda: dictionary(target_label))
    Bt_from.place(x=460,y=65)

    label_info = tk.Label(FrameSet, bg = Color0, fg = Fcolor,font = (FontFamily, ),text = '下载线程(遇到下坏文件的改成1)>')
    label_info.grid(row=6, column=0, padx=10, pady=0, sticky='W')

    frameThread = tk.Frame(FrameSet, bg = Color0)
    frameThread.grid(row=7, column=0, padx=10, pady=0, sticky='W')

    btminues = tk.Button(frameThread, relief='flat', compound='center', bg = Color2, bd = -1, 
        text = '-', image = Img, fg = Fcolor, width = 20, height = 20,
        command = lambda: negiThread(label_thread, './res/conf/Thread.ntg', 'downthread'))
    btminues.grid(row=1, column=1, padx=5, pady=0, sticky='W')

    label_thread = tk.Label(frameThread, bg = Color1, fg = Fcolor,font = (FontFamily, ),text = '5', width = 48)
    label_thread.grid(row=1, column=2, padx=10, pady=0, sticky='W')

    btplus = tk.Button(frameThread, relief='flat', compound='center', bg = Color2, bd = -1, 
        text = '+', image = Img, fg = Fcolor, width = 20, height = 20,
        command = lambda: addThread(label_thread, './res/conf/Thread.ntg', 'downthread'))
    btplus.grid(row=1, column=3, padx=5, pady=0, sticky='W')


    

    #label_info = tk.Label(FrameSet, bg = Color0, fg = Fcolor,font = (FontFamily, ),text = '您的Cookie>')
    #label_info.grid(row=8, column=0, padx=10, pady=0, sticky='W')

    Bt_Back = tk.Button(FrameSet, width=WidthFull, height=Height,relief='flat', compound='center',bg = Color2,
        command = lambda: hide(FrameSet),
        bd = -1, text = '返回!', image = Img, fg = Fcolor)
    Bt_Back.grid(row=100, column=0, padx=10, pady=10)










    FrameDonate = tk.Frame(root, bg = Color0)
    FrameDonate.place(x=0, y=0)

    label_info = tk.Label(FrameDonate, bg = Color0, fg = Fcolor,font = (FontFamily, ),text = '微信支付')
    label_info.grid(row=1, column=0, padx=10, pady=0)

    ShowLabel = tk.Label(FrameDonate, image = img_QR)
    ShowLabel.grid(row=2, column=0, padx=10)

    Bt_Back = tk.Button(FrameDonate, width=WidthFull, height=Height,relief='flat', compound='center',bg = Color2,
        command = lambda: hide(FrameDonate),
        bd = -1, text = '返回!', image = Img, fg = Fcolor)
    Bt_Back.grid(row=3, column=0, padx=10, pady=5)
    Bt_ABT = tk.Button(FrameDonate, width=WidthFull, height=Height,relief='flat', compound='center',bg = Color2,
        command = lambda: tkinter.messagebox.showinfo('Hi', total.about),
        bd = -1, text = '关于!', image = Img, fg = Fcolor)
    Bt_ABT.grid(row=4, column=0, padx=10, pady=5)






















    frameMutiTask = tk.Frame(root, bg = Color0)
    frameMutiTask.place(x=0, y=0)
    
    fTask1 = tk.Frame(frameMutiTask, bg = Color1)
    fTask1.grid(row=1, column=1, padx=10, pady=5)

    T1Title = tk.Label(fTask1, text = '无任务\n1322132', bg = Color1, fg = Fcolor, width = 390, height = 30, image = Img, compound='left')
    T1Title.grid(row=1, column=1, padx=10, pady=5, sticky = 'nw')

    T1Bstart = tk.Button(fTask1, relief='flat', compound='center',bg = Color2, height = 30, width = 30,
        command = print(),
        bd = -1, text = '‖', image = Img, fg = Fcolor)
    T1Bstart.grid(row=1, column=2, padx=0, pady=5)

    T1Bdel = tk.Button(fTask1, relief='flat', compound='center',bg = Color2, height = 30, width = 30,
        command = print(),
        bd = -1, text = '×', image = Img, fg = Fcolor)
    T1Bdel.grid(row=1, column=3, padx=5, pady=5)


    fTask2 = tk.Frame(frameMutiTask, bg = Color1)
    fTask2.grid(row=2, column=1, padx=10, pady=5)

    T2Title = tk.Label(fTask2, text = '无任务\n1322132', bg = Color1, fg = Fcolor, width = 390, height = 30, image = Img, compound='left')
    T2Title.grid(row=1, column=1, padx=10, pady=5, sticky = 'nw')

    T2Bstart = tk.Button(fTask2, relief='flat', compound='center',bg = Color2, height = 30, width = 30,
        command = print(),
        bd = -1, text = '‖', image = Img, fg = Fcolor)
    T2Bstart.grid(row=1, column=2, padx=0, pady=5)

    T2Bdel = tk.Button(fTask2, relief='flat', compound='center',bg = Color2, height = 30, width = 30,
        command = print(),
        bd = -1, text = '×', image = Img, fg = Fcolor)
    T2Bdel.grid(row=1, column=3, padx=5, pady=5)


    fTask3 = tk.Frame(frameMutiTask, bg = Color1)
    fTask3.grid(row=3, column=1, padx=10, pady=5)

    T3Title = tk.Label(fTask3, text = '无任务\n1322132', bg = Color1, fg = Fcolor, width = 390, height = 30, image = Img, compound='left')
    T3Title.grid(row=1, column=1, padx=10, pady=5, sticky = 'nw')

    T3Bstart = tk.Button(fTask3, relief='flat', compound='center',bg = Color2, height = 30, width = 30,
        command = print(),
        bd = -1, text = '‖', image = Img, fg = Fcolor)
    T3Bstart.grid(row=1, column=2, padx=0, pady=5)

    T3Bdel = tk.Button(fTask3, relief='flat', compound='center',bg = Color2, height = 30, width = 30,
        command = print(),
        bd = -1, text = '×', image = Img, fg = Fcolor)
    T3Bdel.grid(row=1, column=3, padx=5, pady=5)


    fTask4 = tk.Frame(frameMutiTask, bg = Color1)
    fTask4.grid(row=4, column=1, padx=10, pady=5)

    T4Title = tk.Label(fTask4, text = '无任务\n1322132', bg = Color1, fg = Fcolor, width = 390, height = 30, image = Img, compound='left')
    T4Title.grid(row=1, column=1, padx=10, pady=5, sticky = 'nw')

    T4Bstart = tk.Button(fTask4, relief='flat', compound='center',bg = Color2, height = 30, width = 30,
        command = print(),
        bd = -1, text = '‖', image = Img, fg = Fcolor)
    T4Bstart.grid(row=1, column=2, padx=0, pady=5)

    T4Bdel = tk.Button(fTask4, relief='flat', compound='center',bg = Color2, height = 30, width = 30,
        command = print(),
        bd = -1, text = '×', image = Img, fg = Fcolor)
    T4Bdel.grid(row=1, column=3, padx=5, pady=5)


    tkTaskStuff = {1: [T1Title, T1Bstart, T1Bdel], 2: [T2Title, T2Bstart, T2Bdel], 3: [T3Title, T3Bstart, T3Bdel], 4: [T4Title, T4Bstart, T4Bdel]}



    frameTaskBt = tk.Frame(frameMutiTask, bg = Color0)
    frameTaskBt.grid(row=5, column=1)
    Bt_pageUp = tk.Button(frameTaskBt, width=100, height=Height,relief='flat', compound='center',bg = Color2,
        command = lambda: negiPage(tkTaskStuff),
        bd = -1, text = '上一页!', image = Img, fg = Fcolor)
    Bt_pageUp.grid(row=0, column=1, padx=10, pady=5)

    page_label = tk.Label(frameTaskBt,bg = Color0,fg = Fcolor,width = 10,text = 'Pw By NTG')
    page_label.grid(row=0, column=2, padx=10, pady=5)

    Bt_pageDown = tk.Button(frameTaskBt, width=100, height=Height,relief='flat', compound='center',bg = Color2,
        command = lambda: addPage(tkTaskStuff),
        bd = -1, text = '下一页!', image = Img, fg = Fcolor)
    Bt_pageDown.grid(row=0, column=3, padx=10, pady=5)

    Bt_Back = tk.Button(frameMutiTask, width=WidthFull, height=Height,relief='flat', compound='center',bg = Color2,
        command = lambda: hide(frameMutiTask),
        bd = -1, text = '返回!', image = Img, fg = Fcolor)
    Bt_Back.grid(row=6, column=1, padx=10, pady=5)



















    FrameDown.place_forget()
    FrameSet.place_forget()
    FrameDonate.place_forget()
    FrameSave.place_forget()
    
    frameMutiTask.place_forget()
    is_file = os.path.exists("./res/conf/path.ntg")
    if is_file == True:
        target_label['text'] = NTG_base.read_file("./res/conf/path.ntg")
        target_label.update()
    is_file = os.path.exists("./res/conf/cookie.ntg")
    if is_file == True:
        Cookie_label['text'] = NTG_base.read_file("./res/conf/cookie.ntg")
        Cookie_label.update()
    is_file = os.path.exists("./res/conf/Thread.ntg")
    if is_file == True:
        label_thread['text'] = NTG_base.read_file("./res/conf/Thread.ntg")
        total.DownThread = int(NTG_base.read_file("./res/conf/Thread.ntg"))
        label_thread.update()
    is_file = os.path.exists("./res/conf/Maxdownload.ntg")
    
    #if is_file == True:
    #    label_thread_MaxTsk['text'] = NTG_base.read_file("./res/conf/Maxdownload.ntg")
    #    total.DownMaxTask = int(NTG_base.read_file("./res/conf/Maxdownload.ntg"))
    #    label_thread_MaxTsk.update()
    #Ttask = threading.Thread(target = ThreadTask, args= (Ldling, Lhsize, Lddsize, Ldpath, Lsatu, page_label))
    #Tdown = threading.Thread(target = NTGMoreFunction.downloadReal, args= ())
    Task = threading.Thread(target = NTGServer.GetCentence, args= (label_say, ))
    Tupd = threading.Thread(target = NTGServer.GetUpdateStuation, args= ())
    Tmsg = threading.Thread(target = NTGServer.GetMsg, args= ())
    TMutiTask = threading.Thread(target = NTGmutiTask.ThreadTask, args= (tkTaskStuff, ))
    Task.start()
    Tupd.start()
    Tmsg.start()
    #Tdown.start()
    #Ttask.start()
    TMutiTask.start()
    root.mainloop()
    os._exit(0)

Root()