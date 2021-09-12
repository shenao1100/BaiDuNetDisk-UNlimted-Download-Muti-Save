import NTG_base
import total

from lxml import etree
import json
import os
import tkinter.messagebox


def GetLanZouInf(url):
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.62'
    }
    result = NTG_base.get(url, header, '', '')[0]
    html = etree.HTML(result)
    result = str(html.xpath('/html/body/div/div/div/table/tr/td/text()')[7])
    result = result.replace('*','\"')
    result = result.replace('\\\\n{','{')
    result = result.replace('\\\\t  \\','')
    result = NTG_base.process_html_text(result)
    #result = json.loads(result)
    return result

def GetUpdateStuation():
    try:
        update_url = total.UpdateUrl
        result = GetLanZouInf(update_url)
        result = json.loads(result)
        Get_version = result['version']
        Get_url = result['url']
        Get_update_inf = result['text'].replace('\\n','\n')
        if total.REV != Get_version:
            ask = tkinter.messagebox.askyesno("有更新,是否更新？",Get_update_inf)
            if ask == True:
                os.system('start ' + Get_url)
    except:
        return 0

def GetCentence(say):
    try:
        cen_url = total.sayUrl
        result = GetLanZouInf(cen_url)
        result = json.loads(result)
        print(result)
        say['text'] = result['msg']
        say.update()
        return 0
    except:
        return 0

def GetMsg():
    try:
        cen_url = total.msgBox
        result = GetLanZouInf(cen_url)
        result = json.loads(result)
        open_ = result['open']
        if open_ == 1 or open_ == '1':
            tkinter.messagebox.showinfo(result['title'], result['msg'])
            if result['exit'] == 1 or result == '1':
                os._exit(0)
        return 0
    except:
        return 0