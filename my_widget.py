#!/usr/bin/env python3
# -*- coding: utf-8
"""窗口组件"""

__author__ = 'Ceilopty'
print('my_widget.py imported:', __name__)

from my_pack import *
import tkinter
_main_windows={}
class _MyAttributeError(AttributeError): pass
class MainWindows(tkinter.Toplevel): # 主窗口
    def __new__(cls, master=None, *args, **kwargs):
        if master:
            if hasattr(master, 'wcount'):
                if master.wcount in _main_windows:
                    return _main_windows[master.wcount]
                _main_windows[master.wcount] = new = super().__new__(cls)
                return new
        return super().__new__(cls)
        
    def __init__(self, master=None, cnf={}, **kw):
        if hasattr(self, 'needinit'):
            if self.needinit:self.needinit = False
            else: return
        else: self.needinit = False
        super().__init__(master, cnf, **kw)
        self.withdraw()
        from my_font import read_font
        from my_constant import config
        from my_menu import MenuBar
        from my_io import read_config
        from my_input import Input
        from my_play import Play
        self.root = root = master
        try:
            self.clan = root.clan
        except AttributeError:
            raise _MyAttributeError("Clan not found")
        root.mainWindows = self
        root.configs = read_config()
        read_font(root)
        self.input = Input(self)
        self.play = Play(self)
        self.input.play = self.play
        self.play.input = self.input
        self.block = []
        self.boxvar = dict(zip(range(self.clan.totalnum), (None,)*50))
        self.title(config['title'])
        geometry = '%sx%s+%s+%s'%(root.configs['geometry']['width'],
                        root.configs['geometry']['height'],
                        root.configs['geometry']['x'],
                        root.configs['geometry']['y'],
                        )
        self.geometry(geometry)
        self.resizable(**root.configs['resizable'])
        self.after(500, lambda: self.focus_force())
        self.menubar = MenuBar(self) # 菜单栏
        self.main_frame = self.MainFrame(self)
        self.status_frame = self.StatusFrame(self)
        self.keybindings()
        self.pack()
        self.deiconify()
    @property
    def show_size(self):
        def strs2tuples(*string):
            import re
            result=[]
            for sub in string:
             result.append(tuple(map(int, re.split(r'[x\+]', sub))))
            return tuple(result)
        h = self.winfo_vrootheight()
        w = self.winfo_vrootwidth()
        old = self.geometry()
        main = self.main_frame.winfo_geometry()
        status = self.status_frame.winfo_geometry()
        main, status, old = strs2tuples(main, status, old)
        # print(main, status, old)
        _w = max(main[0], status[0])
        _w = min(_w, w- 2 * self.root.configs['geometry']['x'])
        _h =  main[1] + status[1]
        return _w, _h, old[2], old[3], w, h

    def pack(self):
        self.main_frame.pack(btn)
        self.status_frame.pack(bbn)

    class MainFrame(tkinter.Frame):  # 主要显示区域
        def __init__(self, master=None, cnf={}, **kw):
            kw.update(master.root.configs['mainframe'])
            super().__init__(master, cnf, **kw)
            self.input = master.input
            self.clan = master.clan
            self.root = master.root
            self.play = master.play
            self.member = self.MemberListFrame(self)
            self.middle = self.MiddleFrame(self)           
            self.history = self.Tatakai(self)
            self.summary = self.Summary(self)
            self.buttons = self.Buttons(self)

            
        class MemberListFrame(tkinter.LabelFrame):
            def __init__(self, master=None, cnf={}, **kw):
                kw.update(master.root.configs['memberlist'])
                super().__init__(master, cnf, **kw)
                self.input = master.input
                self.clan = master.clan
                self.pack(bln)
                
                self.maintop = self.master.master
                self.maintop.flashMemberCheckbox = self.creatCheckboxes
                self.sb = tkinter.Scrollbar(self)
                self.lb = tkinter.Listbox(self,
                                          yscrollcommand=self.sb.set,
                                          selectmode=tkinter.MULTIPLE,
                                          exportselection=0)
                self.lb.canbechanged = 1
                self.maintop.member_lb = self.lb
                self.sb.config(command=self.lb.yview)
                self.sb.pack(yrn)                
                self.lb.pack(bly)
                self.output = self.input.member
                self.poll()
                self.creatCheckboxes()

            def poll(self):
                now = self.lb.curselection()
                if now != self.output.current:
                    self.output.now = now
                    if self.lb.canbechanged:
                        self.output.new_click_member()
                    self.output.current = now
                self.after(250, self.poll)
            def creatCheckboxes(self): # 参战人员选择checkbox (listbox)
                self.lb.delete(0,tkinter.END)
                for member in self.clan.able:
                    self.lb.insert(tkinter.END, member.name)
                
        class MiddleFrame(tkinter.Frame):
            def __init__(self, master=None, cnf={}, **kw):
                kw.update(master.root.configs['middleframe'])
                super().__init__(master, cnf, **kw)
                self.pack(bln)
                self.input = master.input
                self.information = self.Information(self)
                self.member = self.Member(self)
                self.tekilv = self.TekiLv(self)
            class Information(tkinter.LabelFrame): # 对战信息
                def __init__(self, master=None, cnf={}, **kw):
                    kw.update({'text':'对战信息', 'heigh':100, 'width':365})
                    super().__init__(master, cnf, **kw)
                    self.pack(btn)
                    self.input = master.input
                    self.creatContents()
                    self.creatButtons()
                def creatContents(self):
                    class ContentsFrames(tkinter.Frame):
                        def __init__(self, master=None, _text='', _name='', cnf={}, **kw):
                            kw.update({'heigh':25, 'width':361})
                            super().__init__(master, cnf, **kw)
                            tkinter.Label(self, text=_text, heigh=1, width=10).pack(bln)
                            self.label = tkinter.Label(self, text='', heigh=1, width=20)
                            setattr(master.input.info, _name+'_label', self.label)
                            self.entry = tkinter.Entry(self, width=19)
                            master.input.block.append(self.entry)
                            setattr(master.input.info, _name+'_entry', self.entry)
                            self.label.pack(bln)
                            self.entry.pack(brn)
                            self.pack(btn)
                    self.date = ContentsFrames(self, '结束日期： ', 'date')
                    self.date.entry.insert(0, '16.')
                    self.name = ContentsFrames(self, '部落名称： ', 'name')
                    self.kuni = ContentsFrames(self, '对手所在地： ', 'kuni')
                def creatButtons(self):
                    self.input.info_kakunin = self.kakunin = tkinter.Button(self, text='确认',
                                                                            command=self.input.info.kakunin)
                    self.kakunin.pack(bbn)
                    self.input.block.append(self.kakunin)
            class Member(tkinter.LabelFrame):
                def __init__(self, master=None, cnf={}, **kw):
                    kw.update({'text':'参战人员', 'heigh':300, 'width':285})
                    super().__init__(master, cnf, **kw)
                    self.pack(bly)
                    self.input = master.input
                    self.ninsuu = self.Ninsuu(self)
                    self.message = tkinter.Message(self, text='', width=285)
                    self.message.pack(bty)
                    self.input.member.message = self.message
                class Ninsuu(tkinter.LabelFrame): # 参战人数选择确认
                    def __init__(self, master=None, cnf={}, **kw):
                        kw.update({'text':'参战人数', 'heigh':300, 'width':15})
                        super().__init__(master, cnf, **kw)
                        self.input = master.input
                        self.pack(bbn)
                        self.ninsuu_spinbox = tkinter.Spinbox(self,value=(10,15,20,25,30,35,40,45,50),
                                                         command=self.input.member.ninsuu_change)
                        self.ninsuu_spinbox.pack(bry)
                        self.input.member.ninsuu_spinbox = self.ninsuu_spinbox
            class TekiLv(tkinter.LabelFrame): # 等级信息
                def __init__(self, master=None, cnf={}, **kw):
                    kw.update({'text':'敌方大本', 'heigh':300, 'width':80})
                    super().__init__(master, cnf, **kw)
                    self.pack(brn)
                    self.input = master.input
                    self.lv = tkinter.LabelFrame(self, text='等级', height=445, width=40)
                    self.n = tkinter.LabelFrame(self, text='人数', height=445, width=40)
                    self.tot = tkinter.LabelFrame(self, text='总计', height=20, width=80)
                    self.tot.pack(bbn)
                    self.n.pack(brn)
                    self.lv.pack(bln)
                    level_box = self.input.level.level_box = [None]*101
                    level_box[100] = tkinter.Label(self.tot, text='0')
                    level_box[100].pack(bbn)
                    from my_constant import config
                    for i in range(config['boxnum']):
                        level_box[i] = tkinter.Spinbox(self.lv, from_=1, to=10,
                                                       width=2, command=lambda:self.input.level.change())
                        level_box[i + 50] = tkinter.Spinbox(self.n, from_=1, to=config['maxnum'],
                                                            width=2, command=lambda:self.input.level.change())
                        level_box[i].delete(0, tkinter.END)
                        level_box[i].insert(0, config['level_box'](i))
                        level_box[i + 50].delete(0, tkinter.END)
                        level_box[i + 50].insert(0, '1')
                        level_box[i].pack()
                        level_box[i + 50].pack()
                        self.input.block.extend([level_box[i], level_box[i + 50]])
                    self.input.level.change()


        class Tatakai(tkinter.LabelFrame): # 战斗信息
            def __init__(self, master=None, cnf={}, **kw):
                kw.update(master.root.configs['tatakai'])
                super().__init__(master, cnf, **kw)
                self.pack(bln)
                self.input = master.input
                self.play = master.play
                self.creatWidgets()
            def creatWidgets(self):
                self.entry = tkinter.Entry(self, width=55)
                def tatakai_add_enter_handler(event):
                    self.input.tatakai.add()
                def tatakai_cancel_control_z_handler(event):
                    self.input.tatakai.cancel(shortcut=True)
                self.entry.bind("<Return>", tatakai_add_enter_handler)
                self.entry.bind("<Control-z>", tatakai_cancel_control_z_handler)
                self.ok = tkinter.Button(self, text='添加', command=self.input.tatakai.add, width=55)
                self.cancel = tkinter.Button(self, text='删除', command=self.input.tatakai.cancel)
                self.listbox = tkinter.Listbox(self, heigh=29, selectmode=tkinter.EXTENDED)
                self.scrollbar = tkinter.Scrollbar(self, command=self.listbox.yview)
                self.listbox.configure(yscrollcommand=self.scrollbar.set)
                self.cancel.pack(xbn)
                self.ok.pack(xbn)
                self.entry.pack(xbn)
                self.scrollbar.pack(yr)
                self.listbox.pack(xtn)
                self.input.tatakai.entry = self.entry
                self.input.tatakai.listbox = self.listbox
                self.play.tatakai = self.listbox
                self.input.block.extend([self.entry, self.ok, self.cancel])

                
        class Summary(tkinter.LabelFrame): # 总结
            def __init__(self, master=None, cnf={}, **kw):
                kw.update(master.root.configs['summary'])
                super().__init__(master, cnf, **kw)
                self.pack(bly)
                self.play = master.play
                self.creatWidgets()
            def creatWidgets(self):
                self.frame1 = tkinter.LabelFrame(self, text='地图详情', heigh=304, width=307)
                self.frame1.pack(bty)
                self.frame2 = tkinter.LabelFrame(self, text='贡献统计', heigh=304, width=307)
                self.frame2.pack(bty)
                self.listbox1 = tkinter.Listbox(self.frame1, heigh=16, selectmode=tkinter.EXTENDED)
                self.listbox2 = tkinter.Listbox(self.frame2, heigh=15, selectmode=tkinter.EXTENDED)
                self.scrollbar1 = tkinter.Scrollbar(self.frame1, command=self.listbox1.yview)
                self.scrollbar2 = tkinter.Scrollbar(self.frame2, command=self.listbox2.yview)
                self.listbox1.configure(yscrollcommand=self.scrollbar1.set)
                self.listbox2.configure(yscrollcommand=self.scrollbar2.set)
                self.listbox1.pack(bly)
                self.listbox2.pack(bly)
                self.scrollbar1.pack(yr)
                self.scrollbar2.pack(yr)
                self.play.map = self.listbox1
                self.play.donate = self.listbox2

                
        class Buttons(tkinter.Frame): # 最右按钮
            def __init__(self, master=None, cnf={}, **kw):
                kw.update(master.root.configs['buttons'])
                super().__init__(master, cnf, **kw)
                self.pack(bln)
                self.input = master.input
                self.play = master.play
                self.clan = master.clan
                self.root = master.root
                tkinter.Button(self, text='刷新', command=lambda:self.play.flash()).pack(btn)
                tkinter.Button(self, text='选择', command=lambda:self.play.select(self.winfo_toplevel())).pack(btn)
                btn_stop = tkinter.Button(self, text='停止')
                btn_replay = tkinter.Button(self, text='回放', command=lambda:self.play.replay())
                btn_replay.pack(btn)
                btn_stop.pack(btn)
                self.play.btn_stop = btn_stop
                self.play.btn_replay = btn_replay
                btn_save = tkinter.Button(self, text='保存', command=lambda:self.input.save())
                btn_save.pack(bbn)
                tkinter.Button(self, text='初始', command=lambda:self.play.init(True)).pack(bbn)
                tkinter.Button(self, text='重启', command=lambda:self.winfo_toplevel().reboot()).pack(bbn)
                self.input.block.append(btn_save)

                
    class StatusFrame(tkinter.Frame):  # 底部信息栏
        def __init__(self, master=None, cnf={}, **kw):
            kw['width'] = 1280
            super().__init__(master, cnf, **kw)
            self.input = master.input
            from my_constant import Version
            self.label1 = tkinter.Label(self, text='已选：0', heigh=1, width=20)
            self.label1.pack(bln)
            self.label2 = tkinter.Label(self, text='应选：10', heigh=1, width=20)
            self.label2.pack(bln)
            self.label3 = tkinter.Label(self, text='版本：' + Version, heigh=1, width=50)
            self.label3.pack(brn)
            self.input.member.status1 = self.label1
            self.input.member.status2 = self.label2

    def keybindings(self):
        def reboot(kakunin=True):
            if kakunin:
                import tkinter.messagebox as messagebox
                if messagebox.askyesno('确认', '你确定要初始化么？此动作等于重启程序。'):
                    from my_io import save_config
                    save_config(self.root.configs)
                    self.destroy()
                    self.root.wcount += 1
                    MainWindows(self.root)
        self.reboot = reboot
        self.bind("<Escape>", reboot)
        def makesure():
            import tkinter.messagebox
            if tkinter.messagebox.askokcancel("退出", "确定要关闭本程序？有好好膜拜CEILOPTY？"):
                from my_io import save_config
                save_config(self.root.configs)
                self.root.onoroff = 0
                self.destroy()
                self.root.destroy()
        self.makesure = makesure
        self.protocol("WM_DELETE_WINDOW", makesure)
        def lb_event(event):
            print(event.widget.curselection(),event.widget.nearest(event.y))
        self.bind_class('Listbox','<Triple-Button-1>',lb_event)
        def log(event):
            print('Type:%s->%s Mouse:(%s,%s)\nInfo:%s'%\
                  (event.widget.master.widgetName\
                   if hasattr(event.widget.master,'widgetName')else None,
                   event.widget.widgetName, event.x, event.y,
                   event.widget.info()if hasattr(event.widget,'info')else None))
        self.bind_all('<Triple-Button-3>',log)
       
        def key_f1_handler(event):
            self.root.Menus['HelpMenu'].how_to()
        self.bind_all("<F1>", key_f1_handler)
        def key_f5_handler(event): # TODO
            self.play.flash()
        self.bind("<F5>", key_f5_handler)
        def key_f12_handler(event):
            self.root.Menus['FileMenu'].save_as()
        self.bind("<F12>", key_f12_handler)
        def key_ctrl_o_handler(event):
            self.root.Menus['FileMenu'].read_h()
        self.bind("<Control-o>", key_ctrl_o_handler)
        def key_alt_o_handler(event):
            self.root.Menus['FileMenu'].read_d()
        self.bind("<Alt-o>", key_alt_o_handler)
        def key_ctrl_h_handler(event):# TODO
            self.play.select(self)
        self.bind("<Control-h>", key_ctrl_h_handler)
        def key_ctrl_d_handler(event):
            self.root.Menus['MemMenu'].mem_don()
        self.bind("<Control-d>", key_ctrl_d_handler)
        def key_control_alt_backspace_handler(event):# TODO
            self.play.init(True)
        self.bind("<Control-Alt-BackSpace>", key_control_alt_backspace_handler)
        def key_control_alt_r_handler(event):
            reboot()
        self.bind("<Control-Alt-r>", key_control_alt_r_handler)
