#!/usr/bin/env python3
# -*- coding: utf-8
"""播放管理"""

__author__ = 'Ceilopty'
print('my_play.py imported:', __name__)

import tkinter
from my_pack import *
 
class Play:
    def __init__(self, top=None):
        self.top = top
        self.clan = top.clan
        self.Replay = [None, 0] # 回放控制
        self.InitFlag = [False] # 读入内容初始化进度
    def show(self, step): # 显示到指定步数
        # 初始化地图贡献
        import tkinter.constants
        import traceback
        from my_constant import config, clanname
        from my_class import DonateUnit, DonateAD, MemberDonateUnit
        _d, _h = self.clan.imad, self.clan.imah
        if not self.InitFlag[0]:
            if not all(self.input.FlagList[:3]):
                self.replay_end()
                return
        self.tatakai.delete(0, tkinter.END)
        _d.date = _h.date
        _d.donateList.clear()
        for i in range(_h.ninsuu): _d.donateList.append(DonateUnit(_h.mikata[i].abbr))
        mikata_map = [[-1, 0]] * _h.ninsuu
        teki_map = [[-1, 0]] * _h.ninsuu
        # 战斗信息--tatakai_listbox
        complete_flag, count = 0, 0
        for item in _h.rekishi:
            count += 1
            if count > step: break
            global abbbb
            abbbb=item
            if item.ad is 'a':
                hoshi, esp = 0, 0
                coe = (10 + 4*(_h.teki[item.t] - _h.mikata[item.m].hslv[_h.date]) +
                           1 * (item.diff))
                coe = 0 if coe < 0 else coe
                ts = teki_map[item.t][0]
                if ts == -1:
                    if item.s == 0:
                        star = '×××'
                    elif item.s == 1:
                        star = '★××'
                        hoshi = 6
                    elif item.s == 2:
                        star = '★★×'
                        hoshi = 16
                    elif item.s == 3:
                        star = '★★★'
                        hoshi = 30
                        esp = 200
                    teki_map[item.t] = [item.s, item.p]
                elif ts == 0:
                    if item.s == 0:
                        star = '×××'
                    elif item.s == 1:
                        star = '★××'
                        hoshi = 6
                        esp = 80
                    elif item.s == 2:
                        star = '★★×'
                        hoshi = 16
                        esp = 80
                    elif item.s == 3:
                        star = '★★★'
                        hoshi = 30
                        esp = 180
                    teki_map[item.t] = [item.s, max(teki_map[item.t][1], item.p)]
                elif ts == 1:
                    if item.s == 0:
                        star = '○××'
                    elif item.s == 1:
                        star = '●××'
                        teki_map[item.t] = [1, max(teki_map[item.t][1], item.p)]
                    elif item.s == 2:
                        star = '●★×'
                        hoshi = 10
                        esp = 80
                        teki_map[item.t] = [2, item.p]
                    elif item.s == 3:
                        hoshi = 24
                        esp = 180
                        star = '●★★'
                        teki_map[item.t] = [3, 100]
                elif ts == 2:
                    if item.s == 0:
                        star = '○○×'
                    elif item.s == 1:
                        star = '●○×'
                    elif item.s == 2:
                        star = '●●×'
                        teki_map[item.t] =[2, max(teki_map[item.t][1], item.p)]
                    elif item[3] == 3:
                        star = '●●★'
                        hoshi = 14
                        esp = 180
                        teki_map[item.t] = [3, 100]
                elif ts == 3:
                    if item[3] == 0:
                        star = '○○○'
                    elif item[3] == 1:
                        star = '●○○'
                    elif item[3] == 2:
                        star = '●●○'
                    elif item[3] == 3:
                        star = '●●●'
                don = hoshi * coe + esp
                dsp = '%2d: 我方%2d号%s攻对方%2d号，结果%3d%%%s贡献%4.2f' % (
                    count, item[1], _h.mikata[item.m].printname,
                    item[2], item.p, star, don/100)
                _d.donateList[item.m].donate += don
                unit = DonateAD(item[1], item[2],
                                _h.mikata[item.m].hslv[_h.date], _h.teki[item.t],
                                item.s, item.p, don)
                _d.donateList[item.m].attack.append(unit)
            else:
                ts = mikata_map[item[1] - 1][0]
                if ts == -1 or ts == 0:
                    if item.s == 0:
                        star = '×××'
                    elif item.s == 1:
                        star = '★××'
                    elif item.s == 2:
                        star = '★★×'
                    elif item.s == 3:
                        star = '★★★'
                    mikata_map[item.m] = [item.s, max(mikata_map[item.m][1], item.p)]
                elif ts == 1:
                    if item[3] == 0:
                        star = '○××'
                    elif item[3] == 1:
                        star = '●××'
                        mikata_map[item.m] = [1, max(mikata_map[item.m][1], item.p)]
                    elif item[3] == 2:
                        star = '●★×'
                        mikata_map[item.m] = [2, item.p]
                    elif item[3] == 3:
                        star = '●★★'
                        mikata_map[item.m] = [3, 100]
                elif ts == 2:
                    if item[3] == 0:
                        star = '○○×'
                    elif item[3] == 1:
                        star = '●○×'
                    elif item[3] == 2:
                        star = '●●×'
                        mikata_map[item.m] = [2, max(mikata_map[item.m][1], item.p)]
                    elif item[3] == 3:
                        star = '●●★'
                        mikata_map[item.m] = [3, 100]
                elif ts == 3:
                    if item[3] == 0:
                        star = '○○○'
                    elif item[3] == 1:
                        star = '●○○'
                    elif item[3] == 2:
                        star = '●●○'
                    elif item[3] == 3:
                        star = '●●●'
                unit = DonateAD(item[1], item[2],
                                _h.mikata[item.m].hslv[_h.date], _h.teki[item.t],
                                item.s, item.p, 0)
                _d.donateList[item.m].defend.append(unit)
                dsp = '%2d: 我方%2d号%s防对方%2d号，结果%3d%%%s' % (
                    count, item[1],
                    _h.mikata[item[1] - 1].printname,
                    item[2], item[4], star)
            self.tatakai.insert(tkinter.END, dsp)
        else:
            if step != config['inf']:
                complete_flag = 1
            elif self.input.FlagList[3] or self.InitFlag[0]:
                for i in range(_h.ninsuu):
                    _h.mikata[i].add_donation(_h.date,
                                              MemberDonateUnit(_d.donateList[i]))
        self.tatakai.yview(tkinter.END)
        # 总结
        # 地图@summary_listbox1
        mikata_points = 0
        teki_points = 0
        mikata_percent = 0
        teki_percent = 0
        self.map.delete(0, tkinter.END)
        for i in range(_h.ninsuu):
            temp = ''
            map_stat = mikata_map[i][0]
            teki_points += map_stat
            teki_percent += mikata_map[i][1]
            if map_stat == -1:
                star = '○○○'
                teki_points += 1
            elif map_stat == 0:
                star = '☺☺☺'
            elif map_stat == 1:
                star = '☠☺☺'
            elif map_stat == 2:
                star = '☠☠☺'
            elif map_stat == 3:
                star = '☠☠☠'
            temp = '%2d.我方%2d本:%s%3s%%' % (i + 1, _h.mikata[i].hslv[_h.date],
                                           star, mikata_map[i][1])
            map_stat = teki_map[i][0]
            mikata_points += map_stat
            mikata_percent += teki_map[i][1]
            if map_stat == -1:
                star = '○○○'
                mikata_points += 1
            elif map_stat == 0:
                star = '✘✘✘'
            elif map_stat == 1:
                star = '✔✘✘'
            elif map_stat == 2:
                star = '✔✔✘'
            elif map_stat == 3:
                star = '✔✔✔'
            temp += '敌方%2d本:%s%3s%%\n' % (_h.teki[i], star, teki_map[i][1])
            self.map.insert(tkinter.END,temp)
        _h.kekka = (mikata_points, teki_points)
        mikata_percent = (mikata_percent * 100 + _h.ninsuu//2 ) // _h.ninsuu
        teki_percent =  (teki_percent * 100 + _h.ninsuu//2 ) // _h.ninsuu
        _h.percent = (mikata_percent, teki_percent)
        self.map.insert(0,'   比分：%s %2d vs %2d %s'\
                                % (clanname, mikata_points, teki_points, _h.name))
        self.map.insert(1, '       %.2f%%       %.2f%%'%(mikata_percent/100, teki_percent/100))
        # 贡献@summary_listbox2
        self.donate.delete(0, tkinter.END)
        for i in range(_h.ninsuu):
            self.donate.insert(tkinter.END,'%2d.%-15s:%4.2f\n'\
                                    % ( i + 1, _h.mikata[i].printname,_d.donateList[i].donate/100))
        if complete_flag:
            self.replay_end()
            tkinter.messagebox.showinfo('完成！', '已全部显示')
            
    def select(self, top):# 选择存档中的战役--以及弹出窗口
        import tkinter.messagebox
        if self.clan.datelist: self.select_top = self.Select(top)
        else:
            tkinter.messagebox.showwarning('提示', '没有战役记录')
            top.focus_force()

    class Select(tkinter.Toplevel):
        def __init__(self, master=None, cnf={}, **kw):
            super().__init__(master, cnf, **kw)
            self.withdraw()
            self.clan = master.clan
            from my_constant import config
            self.title('选择战役')
            self.geometry('500x400+300+200')
            self.resizable(width=False, height=False)
            self.wm_attributes("-topmost", 1)
            self.iconbitmap(config['icon'])
            self.after(500, lambda: self.focus_force())
            frame = tkinter.Frame(self, width=50, heigh=400)
            frame.pack(brn)
            lb = tkinter.Listbox(self, heigh=23, selectmode=tkinter.BROWSE)
            lb.pack(yln)
            sb = tkinter.Scrollbar(self, command=lb.yview)
            sb.pack(yln)
            lb.configure(yscrollcommand=sb.set)
            lb.delete(0, tkinter.END)
            lframe = tkinter.LabelFrame(self, text='预览')
            lframe.pack(bly)
            pm = tkinter.Message(lframe, width=280, text='注意：点击预览将需要重新输入已填写内容！')
            pm.pack(bty)
            tkinter.Button(frame, text='预览', command=lambda: master.play.preview(lb.curselection())).pack(btn)
            tkinter.Button(frame, text='返回', command=self.destroy).pack(btn)
            lb.insert(tkinter.END, '新建（请点预览后返回)')
            for date in self.clan.datelist: lb.insert(tkinter.END, date)
            def key_esc(event): self.destroy()
            self.bind("<Escape>", key_esc)
            def pre(event):
                index = lb.curselection()[0]
                if index:
                    _h = self.clan.h[index-1]
                    text = '日期：%-20s\n对手名称： %-10s\n对手国家： %-10s\n'\
                           '人数： %2d vs %2d\n比赛结果: %2d %.2f%% vs %-2d %.2f%%'\
                           '\n\t%s'\
                           % (_h.date, _h.name, _h.kuni, _h.ninsuu,
                              _h.ninsuu, _h.kekka[0], _h.percent[0]/100,
                            _h.kekka[1], _h.percent[1]/100, _h.result)
                else: text = '新建'
                text += '\n\n\n注意：点击预览将需要\n重新输入已填写内容！'
                pm.configure(text=text)
            lb.bind('<ButtonRelease-1>', pre)
            self.deiconify()

    def preview(self,cur):
        if cur:
            self.InitFlag[0] = bool(cur[0])
            self.input.FlagList[:] = False, False, False, False
            if cur[0]:
                self.clan.imah.copyfrom(self.clan.h[cur[0] - 1])
                self.cls()
                self.infomation()
                self.toggle(False)
                self.flash()
            else: self.init()
                
    def flash(self): # 刷新按钮--显示内存战斗结果
        from my_constant import config
        import tkinter.messagebox
        if all(self.input.FlagList) or all(self.InitFlag):
            self.replay_end()
            self.show(config['inf'])
        else:
            tkinter.messagebox.showwarning('信息不全', '再看看是不是还差了点什么？')
    
    def replay(self): # 回放暂停继续停止按钮--逐行显示对战进程
        import tkinter
        def replay_pause():
            self.Replay[0] = False
        def replay_stop(event):
            self.btn_replay.configure(text='回放')
            self.Replay[0] = False
        self.btn_stop.bind("<Button-1>", replay_stop)
        def replay_next_step():
            from my_constant import config
            if self.Replay[0] and self.Replay[1] < 100:
                self.show(self.Replay[1])
                self.Replay[1] += 1
                self.btn_replay.after(config['wait'], replay_next_step)

        if self.btn_replay.cget('text') == '回放':
            self.Replay[1] = 0
        if self.btn_replay.cget('text') == '暂停':
            self.btn_replay.configure(text='继续')
            replay_pause()
        else:
            self.btn_replay.configure(text='暂停')
            self.Replay[0] = True
            replay_next_step()
            
    def replay_end(self):
        self.Replay[:] = False, 0
        self.btn_replay.configure(text='回放')

    def toggle(self, b, c=None):# 启用禁用
        import tkinter
        self.top.member_lb.canbechanged = b if c is None else c
        state = tkinter.NORMAL if b else tkinter.DISABLED
        for btn in self.input.block:
            btn.configure(state=state)

    def infomation(self): # 刷新基本信息
        import tkinter.constants
        from my_constant import config
        temp = ''
        _h = self.clan.imah
        self.top.member_lb.select_clear(0, tkinter.END)
        # for member in self.clan.alive.values():
            # self.top.boxvar[member.order][0].deselect()
        for i in range(_h.ninsuu):
            temp +='%2d号位 %2d本:%s\n'%(i + 1 ,
                                      _h.mikata[i].hslv[_h.date],
                                      _h.mikata[i])
            # self.top.member_lb.select_set(_h.mikata[i].order)
            # if self.top.boxvar[_h.mikata[i].order][0]:
                #self.top.boxvar[_h.mikata[i].order][0].select()
        self.input.member.message.configure(text=temp)
        self.input.info.date_entry.delete(0, tkinter.END)
        self.input.info.date_entry.insert(0, _h.date)
        self.input.info.name_entry.insert(0, _h.name)
        self.input.info.kuni_entry.insert(0, _h.kuni)
        self.input.member.ninsuu_spinbox.delete(0,tkinter.END)
        self.input.member.ninsuu_spinbox.insert(0, _h.ninsuu)
        self.input.member.status1.config(text='已选：%d'%(_h.ninsuu,))
        i,j,num,lv =0, 0, 1, _h.teki[0]
        while True:
            i+=1
            if i==_h.ninsuu or lv!=_h.teki[i] or num==config['maxnum']:
                self.input.level.level_box[j].delete(0, tkinter.END)
                self.input.level.level_box[j].insert(0, str(lv))
                self.input.level.level_box[j + 50].delete(0, tkinter.END)
                self.input.level.level_box[j + 50].insert(0, str(num))
                if i==_h.ninsuu:
                    break
                else:
                    j+=1
                    lv=_h.teki[i]
                    num=1
            else:
                num+=1      
        for i in range(j+1,config['boxnum']):
            self.input.level.level_box[i].delete(0, tkinter.END)
            self.input.level.level_box[i + 50].delete(0, tkinter.END)
        self.input.level.level_box[100].config(text=str(_h.ninsuu))


    # 清空显示
    def cls(self):
        import tkinter.constants
        from my_constant import config
        self.toggle(True, 0)
        self.input.tatakai.listbox.delete(0, tkinter.END)
        self.input.tatakai.entry.delete(0, tkinter.END)
        self.map.delete(0, tkinter.END)
        self.donate.delete(0, tkinter.END)
        self.input.member.message.config(text='')
        self.input.info.date_label.config(text='')
        self.input.info.name_label.config(text='')
        self.input.info.kuni_label.config(text='')
        self.input.info.date_entry.delete(0, tkinter.END)
        self.input.info.date_entry.insert(0, '15.')
        self.input.info.name_entry.delete(0, tkinter.END)
        self.input.info.kuni_entry.delete(0, tkinter.END)
        self.btn_replay.config(text='回放')
        self.input.member.ninsuu_spinbox.delete(0,tkinter.END)
        self.input.member.ninsuu_spinbox.insert(0,self.clan.imah.ninsuu)
        self.input.member.status2.config(text='应选：%d'%(self.clan.imah.ninsuu,))
        self.input.member.status1.config(text='已选：%d'%(self.clan.selected,))
        for i in range(config['boxnum']):
            self.input.level.level_box[i].delete(0, tkinter.END)
            self.input.level.level_box[i + 50].delete(0, tkinter.END)
            if i < self.clan.imah.ninsuu:
                self.input.level.level_box[i].insert(0, config['level_box'](i))
                self.input.level.level_box[i + 50].insert(0, '1')
            else:
                self.input.level.level_box[i].config(state=tkinter.DISABLED)
                self.input.level.level_box[i + 50].config(state=tkinter.DISABLED)
        self.input.level.level_box[100].config(text=str(self.clan.imah.ninsuu))
        self.top.member_lb.select_clear(0, tkinter.END)
        # for member in self.clan:
            # if self.top.boxvar[member.order][0]:
                # self.top.boxvar[member.order][0].deselect()


    # 清空屏幕及内存
    def init(self,kakunin=False):
        import tkinter
        if kakunin:
            import tkinter.messagebox
            if not tkinter.messagebox.askyesno('确认', '你确定要初始化么？此动作会清空所有以读入或输入数据。'):
                return
        self.top.member_lb.canbechanged = 0
        def do():
            self.cls()
            self.clan.clearh()
            self.clan.cleard()
            self.clan.imah.clear()
            self.clan.imad.clear()
            self.input.FlagList[:] = False, False, False, False
            self.InitFlag[0] = False
            self.input.hslvtogo[0] = True
            self.Replay[:] = None, 0
            self.clan.selected=0
            def do2():
                self.top.member_lb.canbechanged = 100
            self.top.after(260, do2)
        self.top.after(260, do)
        
