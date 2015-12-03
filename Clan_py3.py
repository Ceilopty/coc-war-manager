#! /usr/bin/env python3.4
# -*- coding: utf-8
"""部落战贡献值录入及统计"""

__author__ = 'Ceilopty'

print('Clan_py3', __name__)

_root_dict={}
# 主函数
def main(*args):
    global root
    from my_class import Clan
    from my_constant import config, clanname
    myclan = Clan(clanname)
    myclan.initialize()
    import tkinter
    def MakeRoot(c=[0]):
        if not '%s'%c[0] in _root_dict:
            _root_dict['%s'%c[0]] = tkinter.Tk(className='Manager%s'%c[0])
        result = _root_dict['%s'%c[0]]
        # c[0] += 1
        return result
    root = MakeRoot()
    root.clan = myclan
    root.wm_iconbitmap(default=config['icon'])
    root.withdraw()
    root.onoroff = 1
    root.wcount = 0

    # 读取文件
    import traceback
    import tkinter.messagebox
    import os
    import my_io
    if args:
        
        #tkinter.messagebox.showinfo('args',str(sys.argv)+'\n'+str(args))
        myclan.clearh()
        myclan.cleard()
        for file in args:
            try:
                if os.path.splitext(file)[1]=='.clh':
                    myclan.addh(my_io.read_history(myclan, file))
                elif os.path.splitext(file)[1]=='.cld':
                    myclan.addd(my_io.read_donate(myclan, file))
            except Exception as e:
                traceback.print_exc()
                tkinter.messagebox.showerror('文件出错！','打开失败')
            else:
                tkinter.messagebox.showinfo('成功！', '%s已读入！'%file)
    else:
        myclan.clearh()
        myclan.cleard()
        for file in ('data.cld', 'history.clh'):
            file = os.path.join('save',file)
            if os.path.exists(file):
                if os.path.splitext(file)[1]=='.clh':
                    myclan.addh(my_io.read_history(myclan, file))
                elif os.path.splitext(file)[1]=='.cld':
                    myclan.addd(my_io.read_donate(myclan, file))
                
    # 主循环
    from my_widget import MainWindows
    MainWindows(root)
    while root.onoroff:
        root.mainloop()
    try:root.destroy()
    except:pass

if __name__ == '__main__':
    import os
    import sys
    sys.modules['Clan_py3'] = sys.modules['__main__']
    import cProfile
    # cProfile.run('main()', sort = 'cumulative')
    
    if len(sys.argv)==1:
        if sys.argv[0].endswith('.exe') or sys.argv[0].endswith('.py'):
            main()
    elif sys.argv[1].endswith('.cld') or sys.argv[1].endswith('.clh'):
        main(*filter(lambda x:x.endswith(('.cld','.clh')), sys.argv[1:]))
       
