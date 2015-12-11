"""录入相关"""


print('my_input.py imported:', __name__)


class Input:
    def __init__(self, top=None):
        self.FlagList = [False] * 4  # 输入进度指示
        self.hslvtogo = [True]
        self.top = top
        self.clan = top.clan
        self.block=[]
        self.member = self.Member(self)
        self.info = self.Info(self)
        self.level = self.Level(self)
        self.tatakai = self.Tatakai(self)
    class Member:
        def __init__(self, input=None):
            self.input = input
            self.clan = input.clan
            self.FlagList = input.FlagList
            self.current = ()
            self.now = ()
            self.lb = None
        def new_click_member(self): # 新成员选择跟踪函数
            clan = self.clan
            self.FlagList[0]=False
            selected = [x for x in self.now if x not in self.current]
            deselected = [x for x in self.current if x not in self.now]
            try:
                assert len(selected + deselected) == 1
            except AssertionError:
                print(selected, deselected)
            if selected:
                clan.imah.mikata[clan.selected]=clan.able[selected[0]]
                clan.selected+=1
            else:
                clan.imah.mikata.remove(clan.able[deselected[0]])
                clan.imah.mikata.append(None)
                clan.selected-=1
            self.status1.configure(text='已选：%d'%(clan.selected,))
            temp = ''
            for i in range(clan.selected):
                        temp +='%2d号位 %2d本: %s\n'%\
                                (i + 1 ,clan.imah.mikata[i].level,
                                 clan.imah.mikata[i])
            self.message.configure(text=temp)
            if clan.selected==clan.imah.ninsuu:
                self.FlagList[0] = True
        
        def ninsuu_change(self): # 人数跟踪函数
            import tkinter
            from my_constant import config
            self.FlagList[0], self.FlagList[2]=False, False
            self.clan.imah.ninsuu = int(self.ninsuu_spinbox.get())
            if self.clan.imah.ninsuu>config['maxninsuu']:
                tkinter.messagebox.showinfo('申し訳あるまい',\
                                            '然而%d人以上部落战并搞不起来'%config['maxninsuu'])
                self.ninsuu_spinbox.delete(0, 2)
                self.ninsuu_spinbox.insert(0,str(config['maxninsuu']))
                self.clan.imah.ninsuu=config['maxninsuu']
            else:
                self.status2.config(text='应选：'+str(self.clan.imah.ninsuu))
                self.input.level.change()

    class Info:
        def __init__(self, input=None):
            self.input = input
        def kakunin(self): # 基本信息确认操作
            import tkinter.messagebox
            import traceback
            clan = self.input.clan
            FlagList = self.input.FlagList
            _h = clan.imah
            try:
                temp_date = self.date_entry.get()
                temp_kuni = self.kuni_entry.get()
                temp_name = self.name_entry.get()
                if temp_date in clan.datelist:
                    tkinter.messagebox.showinfo('重复！', '该日期已存在！')
                    FlagList[1]=False
                    return
                _h.date = temp_date
                _h.kuni = temp_kuni
                _h.name = temp_name
                clan.imad.date = temp_date
                self.date_label.configure(text=temp_date)
                self.name_label.configure(text=temp_name)
                self.kuni_label.configure(text=temp_kuni)
                if len(temp_date) and len(temp_name) and len(temp_kuni):
                    FlagList[1] = True
                else:
                    tkinter.messagebox.showwarning('提示！', '是不是有没写全的！')
            except Exception as e:
                FlagList[1] = False
                print('kakunin info', e)
                traceback.print_exc()
                if isinstance(e, ValueError): tkinter.messagebox.showerror('出错了！', '日期格式不正确')
                else: tkinter.messagebox.showerror('出错了！', '不知道怎么回事就快去问Ceilopty！')

    class Level:
        def __init__(self, input = None):
            self.input = input
            self.clan = input.clan
            self.FlagList = input.FlagList
            self.level_box = [None]*101
        def change(self): # 敌方等级跟踪函数
            import tkinter.constants
            from my_constant import config
            done, i=0, 0
            _h = self.clan.imah
            while True:
                num=self.level_box[i + 50].get()
                if done < _h.ninsuu and i<config['boxnum']:
                    if not num:
                        self.level_box[i].config(state=tkinter.NORMAL)
                        self.level_box[i].insert(0, config['level_box'](i))
                        self.level_box[i + 50].config(state=tkinter.NORMAL)
                        self.level_box[i + 50].insert(0, '1')
                    else:
                        lv=int(self.level_box[i].get())
                        num=int(num)
                        for j in range(done,done+num):
                            if j==_h.ninsuu:
                                break
                            _h.teki[j]=lv
                        i+=1
                        done+=num
                        if done>=_h.ninsuu or i==config['boxnum']:
                            break
            for j in range(i,config['boxnum']):
                self.level_box[j].delete(0, tkinter.END)
                self.level_box[j + 50].delete(0, tkinter.END)
                self.level_box[j].config(state=tkinter.DISABLED)
                self.level_box[j + 50].config(state=tkinter.DISABLED)
            self.level_box[100].config(text=str(done))
            self.FlagList[2]=done==_h.ninsuu
        
    class Tatakai:
        def __init__(self, input=None):
            self.input = input
        def add(self): # 战斗记录添加按钮操作
            if self.input.hslv():
                print('I shall return')
                return
            import tkinter.constants
            import tkinter.messagebox
            import traceback
            from my_constant import config
            from my_coding import my_decode
            show = self.input.play.show
            FlagList = self.input.FlagList
            _h = self.input.clan.imah
            _d = self.input.clan.imad
            def trans(string):
                from my_class import HistoryUnit, WrongScore
                ad = string[0]
                if _h.ninsuu==10: func = int
                elif _h.ninsuu==15: func = lambda x:int(x, 16)
                else: func = my_decode
                try:
                    m, t, s = map(func, string[1:4])
                    if s == 3:
                        p = 100
                        if len(string) > 4: tkinter.messagebox.showwarning('多此一举！',\
                                                                           '知道三星了不就够了！')
                    else: p = int(string[4:])
                    result = HistoryUnit(ad, m, t, s, p, _h.ninsuu)
                except WrongScore: tkinter.messagebox.showwarning('岂有此理！', '分数一定是打错了！')
                else: return result
            try:
                temp = self.entry.get()
                self.entry.delete(0, tkinter.END)
                if temp:
                    if temp.lower() == 'end':
                        FlagList[3] = True
                        if all(FlagList): tkinter.messagebox.showinfo('非常好','确实输入完了！')
                        else: tkinter.messagebox.showinfo('？','貌似还有什么没完成')
                        return
                    else: FlagList[3] = False
                    item = trans(temp)
                    if item:
                        if item[0] in 'Aa' and len(_d.donateList):
                            if len(_d.donateList[item[1] - 1].attack) == 2:
                                print('累了')
                                tired = _h.mikata[item[1] - 1].name
                                tkinter.messagebox.showwarning(\
                                    'ドＳ発見！', tired + '已经很累了赶紧让人家休息休息吧')
                                return
                        if len(_h.rekishi):
                            for i in range(len(_h.rekishi)):
                                if _h.rekishi[i][:3] == item[:3]:
                                    print('重了')
                                    return
                        if FlagList[2]:
                            if not len(self.listbox.curselection()):
                                print('没选')
                                _h.rekishi.append(item)
                            else:
                                _h.rekishi.insert(self.listbox.curselection()[-1], item)
                        show(config['inf'])
                    else:
                        tkinter.messagebox.showerror(\
                            '出错了！',\
                            '格式为4-6位(以16进制表示)：\A/D,我方编号,敌方编号,星数,百分比')
                else:
                    show(config['inf'])
            except Exception as e:
                traceback.print_exc()
                FlagList[3] = False
                tkinter.messagebox.showerror('出错了！', '不知道怎么回事就快去问Ceilopty！')
        
        def cancel(self, shortcut=False): # 战斗记录删除按操作
            import tkinter.messagebox
            import tkinter.constants
            import traceback
            from my_constant import config
            self.entry.delete(0, tkinter.END)
            _h = self.input.clan.imah
            FlagList = self.input.FlagList
            show = self.input.play.show
            FlagList[3] = False
            if shortcut:
                if len(_h.reshiki): _h.rekishi.pop()
                else: print('没东西可删')
            else:
                if not len(self.listbox.curselection()): print('没选')
                del_list = list(self.listbox.curselection())
                del_list.reverse()
                for index in del_list: _h.rekishi.pop(index)
            if not len(_h.rekishi): print('删光了')
            try:
                show(config['inf'])
            except Exception as e:
                traceback.print_exc()
                tkinter.messagebox.showerror('出错了！', '不知道怎么回事就快去问Ceilopty！')


    def hslv(self): # 录入历史等级 返回是否需要录入
        hslvtogo = self.hslvtogo
        _h = self.clan.imah
        import tkinter.messagebox
        import traceback
        if not hslvtogo[0]:
            return False
        elif not self.FlagList[0]:
            tkinter.messagebox.showerror('出错了！','人数不正确！我们要打%d人部落战！'\
                                         %(_h.ninsuu,))
            return True
        elif not self.FlagList[1]:
            tkinter.messagebox.showwarning('提示！', '基本信息不完整')
            return True
        elif not self.FlagList[2]:
            tkinter.messagebox.showwarning('提示！', '敌方等级信息不完整')
            return True
        else:
            try:
                for member in filter(None,_h.mikata):
                    member.hslv[_h.date]=member.level
                print('seems done')
            except BaseException as e:
                print (e,member)
                traceback.print_exc()
            except Exception:
                print('Runtime Error')
            else:
                hslvtogo[0] = False
                print('wrote')
        return False
            
    def save(self): # 保存操作
        import traceback
        import my_io
        import tkinter
        try: import tkinter.filedialog
        except: pass
        import my_constant
        if all(self.FlagList):
            if tkinter.messagebox.askyesno('确认',\
                                           '你确定要保存吗？如果文件已不存在将自动创建。'):
                path = tkinter.filedialog.asksaveasfilename(**my_constant.history_opt)
                if path:
                    try:
                        my_io.append_history(self.clan.imah, path)
                    except Exception as e:
                        traceback.print_exc()
                        tkinter.messagebox.showerror('出错了！', '保存失败')
                    else:
                        self.clan.addh(my_io.read_history(self.clan, path))
                        
                path = tkinter.filedialog.asksaveasfilename(**my_constant.donate_opt)
                if path:
                    try:
                        my_io.append_donate(self.clan.imad, path)
                    except Exception as e:
                        traceback.print_exc()
                        tkinter.messagebox.showerror('出错了！', '保存失败')
                    else:
                        self.clan.addd(my_io.read_donate(self.clan, path))
        else:
            tkinter.messagebox.showerror('出错了！', '信息不完整！战斗结束请添加"end"')

