#!/usr/bin/env python3
# -*- coding: utf-8
"""菜单相关"""


__author__ = 'Ceilopty'

print('my_menu.py imported:', __name__)
from tkinter import *
import tkinter.messagebox as messagebox
from my_pack import *
import time

# dec
def timer(func):
    def wrapper(*args,**kw):
        _time = time.time()
        res = func(*args,**kw)
        print(func,time.time()-_time)
        return res
    return wrapper
        

# 菜单栏
class MenuBar(Menu):
    def __init__(self, parent=None, cnf={}, **kw):
        super().__init__(parent, cnf, **kw)
        self.clan = parent.clan
        self.root = root = parent.root
        root.Menus = {'FileMenu': FileMenu(self),
                      'MemMenu' : MemMenu(self),
                      'HelpMenu': HelpMenu(self),
                      }
        root.Menus['FoneMenu'] = FontMenu(self)
        parent.config(menu=self)

# 文件菜单
class FileMenu(Menu):
    def __init__(self, menubar=None, cnf={}, **kw):
        kw.pop('tearoff',None)
        self.clan = menubar.clan
        super().__init__(menubar, cnf, tearoff=0, **kw)
        self.add_command(label="由文件读入对战历史(Ctrl+O)",\
                         underline=5, command=lambda: self.read_h())
        self.add_command(label="由文件读入贡献(Alt+O)",\
                         underline=5, command=lambda: self.read_d())
        self.add_command(label="另存为(F12)",\
                         underline=5, command=lambda: self.save_as())
        self.add_separator()
        self.add_command(label="退出(Esc)",\
                         underline=0, command=lambda:self._quit())
        menubar.add_cascade(label="文件", menu=self)

    def read_h(self):
        import tkinter.messagebox as messagebox
        import tkinter.filedialog as filedialog
        import my_constant
        import my_io
        import traceback
        try:
            f = filedialog.askopenfilename(**my_constant.history_opt)
            if f:
                self.clan.clearh()
                self.clan.addh(my_io.read_history(self.clan, f))
        except Exception as e:
            print(traceback.print_exc())
            messagebox.showerror('文件出错！',\
                                 '你的文件有问题，管Ceilopty再要一份！')
        else:
            if f: messagebox.showinfo('成功！', '对战历史信息已读入！')
            self.master.master.focus_force()

    def read_d(self):
        import tkinter.messagebox as messagebox
        import tkinter.filedialog as filedialog
        import my_constant
        import my_io
        import traceback
        try:
            f = filedialog.askopenfilename(**my_constant.donate_opt)
            if f:
                self.clan.cleard()
                self.clan.addd(my_io.read_donate(self.clan,f))
        except Exception as e:
            traceback.print_exc()
            messagebox.showerror('文件出错！',\
                                 '你的文件有问题，管Ceilopty再要一份！')
        else:
            if f: messagebox.showinfo('成功！', '贡献信息已读入！')
            self.master.master.focus_force()

    def save_as(self):
        import tkinter.messagebox as messagebox
        import tkinter.filedialog as filedialog
        import my_constant
        import my_io
        import traceback
        try:
            if self.clan.h:
                path = filedialog.asksaveasfilename(**my_constant.history_opt)
                if path:
                    my_io.append_history(None, path, mode='clear')
                    for item in self.clan.hv:
                        my_io.append_history(item, path, check_exist=False)
                    messagebox.showinfo('保存成功！', '已保存至' + path)
            if self.clan.d:
                path = filedialog.asksaveasfilename(**my_constant.donate_opt)
                if path:
                    my_io.append_donate(None, path, mode='clear')
                    for item in self.clan.dv:
                        my_io.append_donate(item, path, check_exist=False)
                    messagebox.showinfo('保存成功！', '已保存至' + path)
        except Exception as e:
            traceback.print_exc()
            messagebox.showerror('出错了！', '保存失败')
        self.master.master.focus_force()

    def _quit(self): self.master.master.makesure()


# 成员菜单
class MemMenu(Menu):
    def __init__(self, menubar=None, cnf={}, **kw):
        kw.pop('tearoff',None)
        self.clan = menubar.clan
        super().__init__(menubar, cnf, tearoff=0, **kw)
        self.add_command(label="成员管理", underline=0,\
                         command=lambda: self.mem_man())
        self.add_command(label="查看贡献(Ctrl+D)", underline=0,\
                         command=lambda: self.mem_don())
        self.add_command(label="由对战历史生成贡献", underline=0,\
                         command=lambda: self.h2d())
        self.add_command(label="停赛记录", underline=0,\
                         command=lambda: self.mem_sus())
        menubar.add_cascade(label="成员", menu=self)

    def mem_man(self): self.MemMan(self)
    def mem_don(self): self.MemDon(self)
    def mem_sus(self): self.MemSus(self)

    class MemMan:
        def __init__(self,Menu=None):
            self.unsaved = False
            clan = Menu.clan
            self.maintop = Menu.master.master
            if False:
                self.mem_save()
            from my_constant import config
            self.icon = config['icon']
            self.clan=clan
            self.top = top = Toplevel()
            top.withdraw()
            top.title('成员管理')
            top.geometry('1000x400+200+200')
            top.resizable(width=False, height=1)
            # top.wm_attributes("-topmost", 1)
            top.iconbitmap(self.icon)
            top.after(500, lambda: top.focus_force())
            btn_fr= Frame(top, width=50, heigh=400)
            btn_fr.pack(brn)

            mem_lf = LabelFrame(top, text='选择成员', width=50, heigh=400)
            mem_lf.pack(bln)
            from MultiCall import MultiCallCreator
            self.lb = mem_lb = MultiCallCreator(Listbox)(mem_lf, heigh=20, selectmode=BROWSE, exportselection=0)
            mem_lb.pack(yln)
            mem_sc = Scrollbar(mem_lf, command=mem_lb.yview)
            mem_sc.pack(yln)
            mem_lb.configure(yscrollcommand=mem_sc.set)
            mem_lb.delete(0, END)

            don_lf = LabelFrame(top, text='贡献一览')
            don_lf.pack(bly)
            self.don = don_lb = Listbox(don_lf, selectmode=EXTENDED)
            don_lb.pack(bly)
            don_sc = Scrollbar(don_lf, command=don_lb.yview)
            don_sc.pack(yln)
            don_lb.configure(yscrollcommand=don_sc.set)

            info = Frame(top)
            info.pack(bln)
            f1 = LabelFrame(info, text='Name')
            f2 = LabelFrame(info, text='Abbr')
            f3 = LabelFrame(info, text='Town Hall Lv')
            f4 = LabelFrame(info, text='Rank')
            f5 = LabelFrame(info, text='Order')
            f6 = LabelFrame(info, text='Dead or Alive')
            f7 = LabelFrame(info, text='Normal or Suspended')
            for i in (f1, f2, f3, f4, f5, f7, f6):i.pack(btn)
            self.name = Entry(f1)
            self.abbr = Entry(f2)
            self.level = Entry(f3)
            self.rank = Entry(f4)
            self.order = Entry(f5)
            self.status = Checkbutton(f6, command=self.member_die, indicatoron=0)
            self.state = Button(f7, command=self.member_sus)
            for i in (self.name, self.abbr, self.level, self.rank, self.order, self.status, self.state):
                i.pack(xtn)
            self.order.config(state=DISABLED)
            # self.message = Message(info, text='aaa')
            # self.message.pack(bbn)
            
            
            Button(btn_fr, text='确定', command=lambda: self.confirm()).pack(btn)
            Button(btn_fr, text='返回', command=lambda: self.beforeleave()).pack(btn)
            self.btn_new= Button(btn_fr, text='新建', command=self.mem_new)
            self.btn_new.pack(btn)
            self.btn_up = Button(btn_fr, text='上移', command=self.up)
            self.btn_up.pack(btn)
            self.btn_down = Button(btn_fr, text='下移', command=self.down)
            self.btn_down.pack(btn)
            Button(btn_fr, text='保存', command=self.mem_save).pack(bbn)
            Button(btn_fr, text='备份', command=self.mem_pickle).pack(bbn)
            Button(btn_fr, text='清空', command=self.clear).pack(bbn)
            
            for i in range(clan.totalnum): mem_lb.insert(tkinter.END, clan[i].name)
            self.keybinding()
            top.wm_deiconify()

        def keybinding(self):
            def abbrOK(value):
                if not value: return 1
                if  all(ord(c)<256 for c in value) and len(value) < 4: return 1
                self.top.after(10,lambda:messagebox.showwarning("提示","请确保Abbr是三位ascii码"))
                return 0
            abbrOk = self.top.register(abbrOK)
            self.abbr.config(validate='all', validatecommand=(abbrOk, '%P'))
            def levelOK(value): return not value or value in map(str, range(1, 11))
            levelOk = self.top.register(levelOK)
            self.level.config(validate='all', validatecommand=(levelOk, '%P'))
            def rankOK(value, why, where, what, old):
                if not value: return 1
                if old is '0'and '%d' == 1: return 0
                try:value = int(value)
                except: return 0
                else: return 0 <= value <= 1100
            rankOk = self.top.register(rankOK)
            self.rank.config(validate='all', validatecommand=(rankOk, '%P', '%d', '%i', '%S', '%s'))
            
            def event_showdon(event): # 显示贡献
                if event.type == '3': # KeyRelease
                    if not self.lb.curselection(): return
                    index = self.lb.curselection()[0]
                elif event.type in '56': # MouseRelease, MouseMotion
                    index = event.widget.nearest(event.y)
                else: return
                member = self.clan[index]
                self.mem_showdon(member)
            def event_showinfo(event): # 刷新信息
                if event.type in '34': # KeyRelease, Double
                    if not self.lb.curselection(): return
                    index = self.lb.curselection()[0]
                elif event.type in '56': # MouseRelease, MouseMotion
                    index = event.widget.nearest(event.y)
                else: return
                member = self.clan[index]
                self.mem_checked(member)
            
            self.lb.event_add('<<ShowDon>>', '<B1-Motion>')
            self.lb.event_add('<<ShowDon>>', '<ButtonRelease-1>')
            self.lb.event_add('<<ShowDon>>', '<KeyRelease-Up>')
            self.lb.event_add('<<ShowDon>>', '<KeyRelease-Down>')
            
            self.lb.event_add('<<ShowInfo>>', '<KeyRelease-Up>')
            self.lb.event_add('<<ShowInfo>>', '<KeyRelease-Down>')
            self.lb.event_add('<<ShowInfo>>', '<ButtonRelease-1>')
            self.lb.event_add('<<ShowInfo>>', '<Double-1>')

            self.lb.bind('<<ShowDon>>', event_showdon)
            self.lb.bind('<<ShowInfo>>', event_showinfo)
            
            def key_enter(event): self.confirm()
            self.top.bind("<Return>", key_enter)
            def key_esc(event): self.beforeleave()
            self.top.bind("<Escape>", key_esc)
            self.top.protocol("WM_DELETE_WINDOW", self.beforeleave)
            
        def up(self):
            if not self.lb.curselection(): return
            index = self.lb.curselection()[0]
            member = self.clan[index]
            upper = self.clan[index-1]
            member.rank, upper.rank = upper.rank, member.rank
            self.flash(1, 0)
            self.lb.select_clear(0, END)
            self.lb.select_set(index-1)
            self.mem_checked(member)
            self.unsaved = True
        def down(self):
            if not self.lb.curselection(): return
            index = self.lb.curselection()[0]
            member = self.clan[index]
            downer = self.clan[index+1]
            member.rank, downer.rank = downer.rank, member.rank
            self.flash(1, 0)
            self.lb.select_clear(0, END)
            self.lb.select_set(index+1)
            self.mem_checked(member)
            self.unsaved = True
        def mem_new(self, c=[0]):
            from my_class import Member
            new = self.name.get(), self.abbr.get(), self.level.get(), self.rank.get()
            if not new[0]: return
            flag = not new[1]
            kw = {}
            kw['name'], kw['abbr'], kw['level'], kw['rank'] = new
            kw['abbr'] = ( kw['abbr'] or '%d'%c[0] ).rjust(3,'_')
            kw['level'] = int (kw['level'] or 1)
            kw['rank'] = kw['rank'] or kw['level'] * 100
            title = "添加成员"
            message = "新成员信息：\n  Name: %s\n  Abbr: %s\n  Town Hall Lv: %s\n  Rank: %s"\
                      ""%(kw['name'], kw['abbr'], kw['level'], kw['rank'])
            if kw['abbr'] in self.clan.member:
                messagebox.showwarning("错误！","该缩写已存在，如需帮助请联系Ceilopty")
                return
            if not messagebox.askyesno(title, message): return
            try:
                new = Member(self.clan, **kw)
                self.clan[kw['abbr']] = new
            except BaseException as e:
                messagebox.showwarning("成员创建失败","错误：%s\n如有疑问请咨询Ceilopty"%e)
            else:
                self.unsaved = True
                if flag: c[0] += 1
                messagebox.showinfo("成员创建成功","即日起成员%s可以参战！"%kw['name'])
                self.flash()
        def member_sus(self):
            import tkinter.messagebox as messagebox
            if not self.lb.curselection(): return
            index = self.lb.curselection()[0]
            member = self.clan[index]
            top = Toplevel()
            top.withdraw()
            top.title('禁赛天数')
            top.iconbitmap(self.icon)
            top.after(500, lambda: top.focus_force())
            date = Entry(top)
            date.insert(0, '%s'%self.clan.NOW)
            date.pack(btn)
            entry = Entry(top)
            def entryOK(value):
                if not value or value.isdecimal(): return 1
                self.top.after(10,lambda:messagebox.showerror('错误','输入天数不合法'))
                return 0
            entryOk = top.register(entryOK)
            entry.config(validate='all', validatecommand=(entryOk, '%P'))
            entry.pack(btn)
            def confirm():
                v = entry.get()
                if not v: return
                v = int(v)
                d = date.get()
                from my_class import MyDate
                try: d = MyDate(d)
                except:
                    messagebox.showerror('错误', '日期错误')
                    return
                if messagebox.askyesno('禁闭%s'%member,'真的要把%s关小黑屋%s天么？'%(member.name,v)):
                    member.penalty.update({d:v})
                    self.flash()
                    self.unsaved = True
                    messagebox.showinfo('提示','已将%s禁赛%s天, 将于%s日全面解禁, 保存后生效'%(member.name,
                                                                            v, member.free))
                    top.destroy()
            def key_enter(event): confirm()
            top.bind("<Return>", key_enter)
            Button(top, text='确认', command=confirm).pack(btn)
            top.bind("<Escape>", lambda event:top.destroy())
            top.wm_deiconify()
        def member_die(self):
            import tkinter.messagebox as messagebox
            if not self.lb.curselection():
                self.status.deselect()
                return
            index = self.lb.curselection()[0]
            member = self.clan[index]
            if messagebox.askyesno('处死%s'%member,'真的要让%s牺牲么？'%member.name):
                member.die()
                self.flash()
                self.unsaved = True
                messagebox.showinfo('提示', '要想让%s复活请联系Ceilopty'%member.name)
            else: self.status.deselect()
        def mem_pickle(self):
            if self.unsaved:
                messagebox.showinfo('还未保存','请先保存后再备份')
                return
            from my_constant import config
            import os
            import pickle
            with open(os.path.join(config['dir'],'data','member.ini'),encoding=config['read'], mode='r')as f:
                with open(os.path.join(config['dir'],'data','member'),mode='wb')as ff:
                    pickle.dump(f.read(), ff)
            with open(os.path.join(config['dir'],'data','Clan'),mode='wb')as ff:
                pickle.dump(self.clan, ff)
        def mem_save(self):
            import os
            import traceback
            from my_constant import config
            try:
                with open(os.path.join(config['dir'],'data','member.ini'), mode='w', encoding=config['read']) as f:
                    for member in sorted(self.clan,reverse=True):
                        f.write(member.jsondumps())
            except BaseException as e:
                traceback.print_exc()
            else:
                self.unsaved = False
                tkinter.messagebox.showinfo('信息', '保存成功 重启生效')
        def mem_showdon(self, member):
            self.don.delete(0, tkinter.END)
            for k, v in member.donate.items():
                self.don.insert(tkinter.END, '日期： %s 总贡献： %s'%(k, v.donate/100))
                if v.attack: self.don.insert(tkinter.END, '    进攻：')
                for a in v.attack:
                    self.don.insert(tkinter.END, '        %2d号位%2d本攻打%2d号位%2d本，结果%d星%3d%%，贡献：%4.2f'\
                                    %(a[0], a[2], a[1], a[3], a[4], a[5], a[6]/100))
                if v.defend: self.don.insert(tkinter.END, '    防守：')
                for d in v.defend:
                    self.don.insert(tkinter.END, '        %2d号位%2d本防守%2d号位%2d本，结果%d星%3d%%，贡献：%4.2f'\
                                    %(d[0], d[2], d[1], d[3], d[4], d[5], d[6]/100))
        def mem_checked(self, member):
            self.clear(0, 0)
            self.name.insert(0, member.name)
            self.abbr.insert(0, member.abbr)
            self.abbr.config(state=DISABLED)
            self.level.insert(0, member.level)
            self.rank.insert(0, member.rank)
            self.order.config(state=NORMAL)
            self.order.insert(0, member.order)
            self.order.config(state=DISABLED)
            self.btn_new.config(state=DISABLED)
            stat = 'Alive' if member.rank else 'Dead'
            self.status.config(text=stat)
            if stat == 'Alive':
                if member.normal: self.state.config(state=NORMAL, text=member.state.capitalize())
                else: self.state.config(text='%s until %s'%(member.state.capitalize(),
                                                            member.free),
                                        state=DISABLED)
                if member.order == 0: self.btn_up.config(state=DISABLED)
                if member.order == self.clan.number - 1 : self.btn_down.config(state=DISABLED)
                self.status.config(state=NORMAL)
                self.status.deselect()
            else:
                self.state.config(text=stat, state=DISABLED)
                self.rank.config(state=DISABLED)
                self.status.select()
                self.status.config(state=DISABLED)
                self.btn_up.config(state=DISABLED)
                self.btn_down.config(state=DISABLED)
            
        def confirm(self):
            if not self.lb.curselection(): return
            index = self.lb.curselection()[0]
            member = self.clan[index]
            old = member.name, member.level, member.rank
            new = self.name.get(), self.level.get(), self.rank.get()
            if tuple(map(str,old)) == new: return
            title = "确认修改？"
            message = "原信息：\n\tName: %s\tTown Hall Lv: %2d\tRank: %4d\n\n"\
                      "新信息：\n\tName: %s\tTown Hall Lv: %2s\tRank: %4s\n\n"\
                      "确认修改？"% (old + new)
            if messagebox.askyesno(title, message):
                try:
                    member._change_name(new[0])
                    member.level, member.rank = new[1:]
                except BaseException as e:
                    messagebox.showwarning("修改失败","错误：%s\n如需帮助请咨询Ceilopty"%(e,))
                else:
                    messagebox.showinfo("修改成功","修改已生效， 永久修改请保存。")
                    self.unsaved = True
            else: pass
            self.flash(0,0)
            self.lb.select_set(member.order)
            self.mem_checked(member)
        def flash(self, lb=True, don=True):
            self.clan.sort()
            self.lb.delete(0, tkinter.END)
            for i in range(self.clan.totalnum): self.lb.insert(tkinter.END, self.clan[i].name)
            self.clear(lb, don)
        def clear(self, lb=True, don=True):
            self.btn_new.config(state=NORMAL)
            self.btn_up.config(state=NORMAL)
            self.btn_down.config(state=NORMAL)
            self.name.delete(0, END)
            self.abbr.config(state=NORMAL)
            self.abbr.delete(0, END)
            self.level.delete(0, END)
            self.rank.config(state=NORMAL)
            self.rank.delete(0, END)
            self.order.config(state=NORMAL)
            self.order.delete(0, END)
            self.order.config(state=DISABLED)
            self.status.config(text='')
            self.state.config(state=DISABLED, text='')
            if don:self.don.delete(0, END)
            if lb: self.lb.select_clear(0, END)
        def beforeleave(self):
            if self.unsaved:
                henji = messagebox.askyesnocancel('还未保存','真的要退出吗？修改已生效，但若不保存'
                                                  '，重启程序后将恢复。\n保存？不保存？返回？')
                if henji is True: self.mem_save()
                elif henji is False: pass
                elif henji is None: return
                else: raise RuntimeError
            self.maintop.flashMemberCheckbox()
            self.top.destroy()
        
    class MemDon:
        def __init__(self, Menu=None):
            clan = Menu.clan
            import tkinter.messagebox as messagebox
            if not clan or not len(clan.d):
                tkinter.messagebox.showwarning('提示', '请先读入贡献数据')
                return
            from my_constant import config
            self.clan = clan
            self.order = sv = StringVar()
            self.top = top = Toplevel()
            top.withdraw()
            top.title('成员贡献')
            top.geometry('1000x400+200+200')
            top.resizable(width=False, height=1)
            # top.wm_attributes("-topmost", 1)
            top.iconbitmap(config['icon'])
            top.after(500, lambda: top.focus_force())
            bf = Frame(top, width=50, heigh=400)
            bf.pack(brn)

            df = LabelFrame(top, text='选择日期', width=50, heigh=400)
            df.pack(bln)
            dr = Radiobutton(df, indicatoron=0, text='日期优先', value='date', variable=sv)
            dr.pack(xbn)
            dr.select()
            self.dl = dl = Listbox(df, heigh=23, selectmode=EXTENDED, exportselection=0)
            dl.pack(yln)
            ds = Scrollbar(df, command=dl.yview)
            ds.pack(yln)
            dl.configure(yscrollcommand=ds.set)
            dl.delete(0, END)

            mf = LabelFrame(top, text='选择成员', width=50, heigh=400)
            mf.pack(bln)
            mr = Radiobutton(mf, indicatoron=0, text='成员优先', value='member', variable=sv)
            mr.pack(xbn)
            self.ml = ml = Listbox(mf, heigh=20, selectmode=EXTENDED, exportselection=0)
            ml.pack(yln)
            ms = Scrollbar(mf, command=ml.yview)
            ms.pack(yln)
            ml.configure(yscrollcommand=ms.set)
            ml.delete(0, END)

            lf =LabelFrame(top, text='贡献一览')
            lf.pack(bly)
            self.message = tl = Listbox(lf, selectmode=EXTENDED)
            tl.pack(bly)
            ts = Scrollbar(lf, command=tl.yview)
            ts.pack(yln)
            tl.configure(yscrollcommand=ts.set)
            self.date = []
            self.member = []
            Button(bf, text='确定', command=lambda: self.show_me()).pack(btn)
            Button(bf, text='返回', command=top.destroy).pack(btn)
            for date in clan.dk:
                dl.insert(END, date)
                self.date.append(date)
            for member in clan:
                ml.insert(END, member.name)
                self.member.append(member)
            dl.select_set(0, END)
            ml.select_set(0, END)
            self.alldonates = tuple(self._donate_iter())
            self.keybinding()
            top.wm_deiconify()

        def keybinding(self):
            def key_enter(event): self.show_me()
            def key_esc(event): top.destroy()
            self.top.bind("<Return>", key_enter)
            self.top.bind("<Escape>", key_esc)

        def _donate_iter(self):
            war_index, donate_index = 0, 0
            while True:
                try:
                    part1 = self.clan.dv[war_index].date
                    try:
                        part2 = self.clan.dv[war_index].donateList[donate_index]
                        donate_index += 1
                        yield (part1, part2)
                    except IndexError:
                        donate_index = 0
                        war_index += 1
                except IndexError:
                    return 'End of Donates'

        def show_me(self):
            def sp(n): return '    '*n
            alldonates = self.alldonates
            dates = tuple(self.date[index] for index in self.dl.curselection())
            members = tuple(self.member[index].abbr for index in self.ml.curselection())

            def memberonly(index): return lambda x: x[1][0] == self.member[index].abbr
            def datein(x):return x[0] in dates
            def memberin(x): return x[1][0] in members
            def okdonates():
                if self.order.get() == 'date':
                    return filter(memberin, filter(datein, alldonates))
                else:
                    box=[]
                    for j in self.ml.curselection():
                        box.extend(filter(datein,filter(memberonly(j), alldonates)))
                    return box
            self.message.delete(0, tkinter.END)
            total, count_t, count_a, count_d = 0, 0, 0, 0
            for item in okdonates():
                hiduke, donate = item
                name = self.clan[donate[0]].printname
                donate = donate[1]
                score = donate[0]/100
                total = total + score
                count_t += 1
                attack, defence = donate[1:]
                self.message.insert(tkinter.END, '日期：' + hiduke + sp(2) +'成员：' + name + sp(2) + '贡献：' + str(score))
                if attack:
                    self.message.insert(tkinter.END, sp(2) + '出击%d次：' % len(attack))
                    for war in attack:
                        count_a += 1
                        output = (war[0], war[2], war[1], war[3], war[4], war[5], war[6]/100)
                        self.message.insert(tkinter.END, sp(4) + '以%2s号位%2s本之身挑战对方%2s号位%2s本'
                                            '        取得%s星%3s%%%4.2f贡献' % output)
                if defence:
                    self.message.insert(tkinter.END, sp(2) + '被打%d次：' % len(defence))
                    for war in defence:
                        count_d += 1
                        output = (war[0], war[2], war[1], war[3], war[4], war[5])
                        self.message.insert(tkinter.END, sp(4) + '用%s号位%s本肉身抵挡对方%s号位%s本        被打%s星%s%%' % output)
            if count_t: self.message.insert(0, '贡献总计：%4.2f%s条目数：%3d%s总攻击次数：%3d%s总防守次数：%3d%s平均：%4.2f' % (
                total, sp(2), count_t, sp(2), count_a, sp(2), count_d, sp(2), total / count_t))
            else: self.message.insert(tkinter.END, '没有符合条件的记录')
    class MemSus:
        def __init__(self,Menu=None):
            clan = Menu.clan
            self.now = clan.NOW
            self.maintop = Menu.master.master
            from my_constant import config
            self.clan=clan
            self.top = top = Toplevel()
            top.withdraw()
            top.title('停赛记录 %s'%self.now)
            top.geometry('1000x400+200+200')
            top.resizable(width=False, height=1)
            # top.wm_attributes("-topmost", 1)
            top.iconbitmap(config['icon'])
            top.after(500, lambda: top.focus_force())

            self.sus = sus_lb = Text(top)
            sus_lb.pack(bly)
            sus_sc = Scrollbar(top, command=sus_lb.yview)
            sus_sc.pack(yln)
            sus_lb.configure(yscrollcommand=sus_sc.set)

            self.show()
            
            self.keybinding()
            top.wm_deiconify()

        def keybinding(self):  
            self.top.bind("<Escape>", lambda event:self.top.destroy())
            self.top.protocol("WM_DELETE_WINDOW", self.top.destroy)
            
        def show(self):
            self.sus.delete(0., tkinter.END)
            flag = 0
            for member in self.clan:
                if member.rank == 0:
                    self.sus.insert(tkinter.END, '%s\n\t状态： %s\n'%(member.name,'Gone'))
                    continue
                if not member.penalty: continue
                flag =1
                self.sus.insert(tkinter.END, '%s\n\t状态： %s\n'%(member.name,member.state.capitalize()))
                for k, v in member.penalty.items():
                    self.sus.insert(tkinter.END, '\t停赛期间： %s - %s 计%s天\n'%(k, k+v, v))
            if not flag: self.sus.insert(tkinter.END, '没有禁赛记录')
    def h2d(self):
        import my_constant
        import tkinter.messagebox as messagebox
        import tkinter.filedialog as filedialog
        import my_io
        import traceback
        play = self.master.master.play
        if not self.clan.h:
            FileMenu.read_h(self)
            if not self.clan.h: return
        path = filedialog.asksaveasfilename(**my_constant.donate_opt)
        if path:
            try:
                my_io.append_donate(None, path, mode='clear')
                my_io.append_history(None, path + '.clh', mode='clear')
                for item in self.clan.hv:
                    self.clan.imah.copyfrom(item)
                    play.InitFlag[0] = True
                    play.flash()
                    play.InitFlag[0] = False
                    my_io.append_donate(self.clan.imad, path, check_exist=False)
                    my_io.append_history(self.clan.imah, path+ '.clh', check_exist=False)
                play.cls()
            except Exception as e:
                print('path=%s\n%s'%(path,e))
                traceback.print_exc()
                messagebox.showerror('出错了！', '保存失败')
            else: messagebox.showinfo('保存成功！', '已保存至' + path)

# 帮助菜单
class HelpMenu(Menu):
    def __init__(self, menubar=None, cnf={}, **kw):
        kw.pop('tearoff',None)
        super().__init__(menubar, cnf, tearoff=0, **kw)
        self.add_command(label="关于", underline=0, command=self.about)
        self.add_separator()
        self.add_command(label="快捷键一览", underline=0, command=self.shortcut)
        self.add_command(label="帮助主题(F1)", underline=0, command=self.how_to)
        self.add_command(label="历史版本", underline=0, command=self.history_version)
        menubar.add_cascade(label="帮助", menu=self)
        
    def history_version(self):
        import my_constant
        import tkinter.messagebox as messagebox
        messagebox.showinfo('历史版本', my_constant.VersionHistory)

    def how_to(self):
        import my_constant
        import tkinter.messagebox as messagebox
        messagebox.showinfo('HowTo', my_constant.helptxt + "\n如果有其他疑问："
                            "Ask Ceilopty for help\n""Q群364928737")

    def shortcut(self):
        #import imp
        import my_constant
        #imp.reload(my_constant)
        import tkinter.messagebox as messagebox
        messagebox.showinfo('快捷键列表', my_constant.shortcuts)

    def about(self):
        import my_constant
        import tkinter.messagebox as messagebox
        messagebox.showinfo('About', '这是一个Python3 GUI程序，帮助实现部落战记录\n版本信息：'
                            + my_constant.Version + ' by Ceilopty')

class FontMenu(Menu):
    def __init__(self, menubar=None, cnf={}, **kw):
        import tkinter.font as TkFont
        kw.pop('tearoff',None)
        self.root = menubar.root
        super().__init__(menubar, cnf, tearoff=0, **kw)
        def change_wsize(func=None):
            def wrapper(*args):
                temp = None
                def before():
                    # print()
                    # print('before',self.root.mainWindows.geometry())
                    oldsize = self.root.mainWindows.show_size
                    # print('should', oldsize)
                    xy = tuple(oldsize[2:4])
                    # print('xy',xy)
                    oldsize = '%dx%d+0+0'%oldsize[4:]
                    self.root.mainWindows.geometry(oldsize)
                    # self.root.mainWindows.withdraw()
                    nonlocal temp
                    temp = xy
                def do():
                    before()
                    result = func(*args) if func else None
                    self.after(1000, after)
                    return result
                def after():
                    nonlocal temp
                    xy = temp
                    newsize = self.root.mainWindows.show_size
                    # print('new',newsize)
                    newsize = '%dx%d+%d+%d'%(newsize[:2] + xy)
                    self.root.mainWindows.geometry(newsize)
                    # print('new',newsize)
                    # self.root.mainWindows.deiconify()
                return do()
            return wrapper
        def command(Var, index):
            @change_wsize
            def func():
                ft = self.root.editFont
                if Var:
                    size = (sizeList[index])
                    ft.config(size = size)
                    self.root.configs['font']['size'] = str(size)
                else:
                    family = (fontList[index])
                    ft.config(family = family)
                    self.root.configs['font']['family'] = family
                
            return func
        @change_wsize
        def reset():
            self.root.editFont.config(**self.root.configs['defaultfont'])
        def add_value(parent, Var, *List):
            for index, value in enumerate(List):
                ft = TkFont.Font(family = 'Fixedsys',
                                 size = 10,
                                 weight = TkFont.NORMAL)
                if Var:
                    ft.config(size = value)
                else:
                    ft.config(family = value)
                parent.add_command(label=str(value),font=ft,
                                   command=command(Var, index))
            return parent
        

        selectfont = tkinter.Menu(self,tearoff=0)
        selectsize = tkinter.Menu(self,tearoff=0)
        fontList = TkFont.families()
        sizeList = tuple(range(8,51,1))
        add_value(selectfont, 0, *fontList)
        add_value(selectsize, 1, *sizeList)
        self.add_cascade(label='字体设置', menu=selectfont)
        self.add_cascade(label='字号设置', menu=selectsize)
        self.add_command(label='字体重置', command=reset)
        def popup(event):self.post(event.x_root, event.y_root)
        self.bind("<Button-3>", popup)
        menubar.add_cascade(label='字体', menu=self)
    
