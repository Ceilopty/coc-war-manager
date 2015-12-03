#!/usr/bin/env python3
# -*- coding: utf-8
"""自定义文件读写"""

__author__ = 'Ceilopty'
print('my_io.py imported:', __name__)


# 读文件返回流
def read_history(clan, path='history.clh') -> dict:
    import codecs
    from my_constant import config
    from my_class import HistoryItem, DateKeyDict
    """


    :rtype : dict
    :param path: file path to read
    :return: dict of history
    """
    his = DateKeyDict()
    try:
        with codecs.open(path, mode='r', encoding=config['read']) as f:
            temp_str = f.read()
        temp_list = temp_str.split('###')
        for string in temp_list:
            if string:
                value = HistoryItem(clan,string)
                his[value.date] = value
    except FileNotFoundError as e:
        print(e,path)
    return his


def read_donate(clan, path='data.cld') -> dict:
    import codecs
    from my_constant import config
    from my_class import DonateItem, DateKeyDict
    """


    :param path: file path
    :rtype : dict
    """
    don = DateKeyDict()
    try:
        with codecs.open(path, mode='r', encoding=config['read']) as f:
            temp_str = f.read()
        temp_list = temp_str.split('###')
        for string in temp_list:
            if string:
                value = DonateItem(clan,string)
                don[value.date] = value
    except FileNotFoundError as e:
        print(e,path)
    return don

# 由流写文件
def append_history(item, path='history.clh', mode='a', check_exist=True):
    import codecs
    from my_constant import config
    from my_coding import my_encode
    myclan = item.clan if item else None
    import tkinter.messagebox
    """

    :param item: History instance
    :param path: file path
    :param mode: file open mode
    :param check_exist:
    :return: None
    """
    if mode == 'clear':
        with codecs.open(path, mode='w', encoding=config['write']):
            pass
        return
    elif not item:
        return
    elif check_exist:
        if item.date in myclan.h:
            return
    with codecs.open(path, mode=mode, encoding=config['write']) as f:
        f.write('###')
        f.write(item.date + '\n')
        f.write(item.name + '\n')
        f.write(item.kuni + '\n')
        f.write(str(item.ninsuu) + '\n')
        f.write(str(item.kekka[0]) + ' ' + str(item.kekka[1]) + ' ' +\
                str(item.percent[0]) + ' ' + str(item.percent[1])+'\n')
        for i in range(item.ninsuu):
            f.write(item.mikata[i].abbr + my_encode(item.mikata[i].hslv[item.date])\
                    + my_encode(item.teki[i]) + '\n')
        for i in item.rekishi:
            f.write(i[0] + my_encode(i[1]) + my_encode(i[2])\
                    + str(i[3]) + str(i[4]) + '\n')
    if check_exist==True:
        tkinter.messagebox.showinfo('保存成功！', '已保存至' + path)


def append_donate(item, path='data.cpd', mode='a', check_exist=True):
    import codecs
    from my_constant import config
    from my_coding import my_encode
    if item: myclan = item.clan
    import tkinter.messagebox
    """

    :param item: Donate Item instance
    :param path: file path
    :param mode: file open mode
    :param check_exist:
    :return: None
    """
    if mode == 'clear':
        with codecs.open(path, 'w', encoding=config['write']):
            pass
        return
    elif not item:
        return
    elif check_exist:
        if item.date in myclan.d:
            return
    with codecs.open(path, mode=mode, encoding=config['write']) as f:
        f.write('###')
        f.write(item.date + '\n')
        for i in item.donateList:
            f.write(i[0] + ' ' + str(i[1][0]) + ' ')
            if len(i[1][1]):
                for j in i[1][1]:
                    f.write(my_encode(j[0]) + my_encode(j[1]) + my_encode(j[2])\
                            + my_encode(j[3]) + str(j[4]) + str(j[5]) + '-'\
                            + str(j[6]) + '+')
            f.write('|')
            if len(i[1][2]):
                for j in i[1][2]:
                    f.write(my_encode(j[0]) + my_encode(j[1]) + my_encode(j[2])\
                            + my_encode(j[3]) + str(j[4]) + str(j[5]) + '-'\
                            + str(j[6]) + '+')
            f.write('\n')
    if check_exist==True:
        tkinter.messagebox.showinfo('保存成功！', '已保存至' + path)

def read_config():
    import sys
    import os.path
    import codecs
    from my_constant import config
    path = os.path.join(os.path.split(sys.argv[0])[0], 'data', 'config.ini')
    try:
        with codecs.open(path,'r',encoding=config['read']) as f:
            string = f.read()
            configs = {}
            temp = tuple(filter(None,string.split('[')))
            for substring in temp:
                items = tuple(filter(None,substring.split(']')))
                key = items[0]
                configs[key] = {}
                items = tuple(filter(None,items[1].split('\n')))
                for item in items:
                    attr, value = tuple(filter(None,item.split(' = ')))
                    try:
                        value = int(value)
                    except ValueError:pass
                    configs[key][attr] = value
    except: return {}
    else: return configs

def save_config(configs):
    import sys
    import os.path
    import codecs
    from my_constant import config
    path = os.path.join(os.path.split(sys.argv[0])[0], 'data', 'config.ini')
    with codecs.open(path,'w',encoding=config['write']) as f:
        for key, items in configs.items():
            f.write('[' + key + ']\n')
            for attr, value in items.items():
                f.write(attr + ' = ' + str(value) + '\n')
                
                    
            

