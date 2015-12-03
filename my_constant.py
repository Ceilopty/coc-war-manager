"""配置及文字信息"""


print('my_constant.py imported:', __name__)

import os
import sys


# 部落信息
clanname = '萌萌哒部落'
# 版本信息
Version = '1.2.0 beta 2015.12.4'
# 历史版本
VersionHistory ="""
1.2.0 beta 2015.12.4
大幅优化贡献显示算法，现在超快
修复了破坏百分比计算的一个BUG
1.1.1 beta 2015.9.12
增加禁赛管理
1.1.0 beta 2015.8.28
开放部分成员管理功能； 字体字号选项正经多了；直接支持50人部落战
1.0.7 beta 2015.8.10
源代码分块；动态管理；配置文件分离；增加负责恶搞的字体字号选项
1.0.6 beta 2015.8.7
分离成员设定，使得成员修改更加容易；成员选择即时显示;文件编码调整，支持50人部落战
1.0.5 beta 2015.8.6
创建了文件关联，可以双击存档文件读入；拖动复数存档到exe上可批量读入
1.0.4 beta 2015.8.1
修改了窗口大小；人员变更；对基本信息的读取；增加参战人数选项，为扩大战斗规模做准备
1.0.3 beta 2015.7.28
支持贡献读取与显示，增加一些快捷键
1.0.2 beta 2015.7.27
更换了图标，修改了外部存储文件，输入战斗信息时可响应回车，增加了百分比记录。
1.0.1 beta 2015.7.25
更新了读取战斗记录功能，并支持幻灯片播放对战信息
1.0.0 beta 2015.7.24
部落战管理软件，可以导出战斗和贡献信息
"""
# 配置信息
config = dict(wait=500,
              inf=100,
              dir=os.path.split(sys.argv[0])[0],
              title=clanname+' 部落战记录管理 ' + Version,
              icon=os.path.join(os.path.split(sys.argv[0])[0],\
                                'data', 'Clan.ico'),
              write='utf-8', read='utf-8',
              maxnum=15, maxninsuu=50,
              boxnum=15,level_box=lambda i:str(8 - i*4 // 15))



# 文件选择设置
history_opt = options = {}
options['defaultextension'] = '.clh'
options['filetypes'] = [('Ceilopty History files', '.clh'),
                        ('Ceilopty files', ('.clh', '.cld')),
                        ('all files', '.*')]
options['initialfile'] = os.path.join(config['dir'], 'save', 'history.clh')
options['title'] = '选择对战历史文件'
donate_opt = options = {}
options['defaultextension'] = '.cld'
options['filetypes'] = [('Ceilopty Donation files', '.cld'),
                        ('Ceilopty files', ('.clh', '.cld')),
                        ('all files', '.*')]
options['initialfile'] = os.path.join(config['dir'], 'save', 'data.cld')
options['title'] = '选择历史贡献文件'

'''
self.dir_opt = options = {}
options['initialdir'] = 'C:\\'
options['mustexist'] = False
options['parent'] = root
options['title'] = u'选择目录'      
def askdirectory(self):
    return tkFileDialog.askdirectory(**dir_opt)
'''

# 帮助主题
helptxt = """录入顺序：选择成员->输入时间等信息->确认等级->输入战斗信息
成员选择：请从1号位开始顺序选择成员
基本信息：时间格式为6或8位年月日，之间可任意非数字分割，无视空格
战斗信息：每次进攻或防守为一条指令，第1位为A(攻击)/D(防守)，第2、3位为我方位序与敌方位序
第4位为星数，如三星则就此结束，否则继续输入百分比的1-2位整数，之后按确定或者回车。
所有战斗均输入完毕请再输入一条"End"
我方敌方位序永远分别为1位：
15人及以下部落战请以16进制数表示，
15人以上部落战输入方式较为特殊， 用0-9a-zA-Z表示0-61, 大小写敏感
更多问题请咨询Ceilopty
其他字母大小写不敏感
"""

# 快捷键
shortcuts ="""
全局
Esc:退出程序或返回

主界面
Ctrl/Alt+O:文件读取对战历史/贡献
Ctrl+H/D:打开战斗选择/贡献菜单
Ctrl+Alt+退格:界面初始化
Ctrl+Alt+R:重启程序   
F1/F5/F12:帮助/刷新/另存为

战斗输入
Enter/Ctrl+Z:添加/撤销
如需更多快捷键，请联系CEILOPTY
"""




# 附录
"""
# 人员词典 已被ini文件替代
nameDict = {'hau': '-)Haulk(-',
            'yrz': '万事屋',
            'ava': 'avalon',
            'cei': 'Ceilopty',
            'cao': '艹日大雨',
            'sun': 'Suner',
            'bfy': 'Best For You',
            'aos': 'Ao\'s Village',
            '556': '5566',
            'xy0': '~(小Y)~',
            'jh0': '军魂',
            'yuy': '鱼鱼是鱼鱼',
            'mx0': '梦芯',
            'abc': '爱比吸',
            'ce2': 'セイロプティだよ',
            'yon': '永遠愛雙',
            'and': 'Andy',
            'qk0': 'suim-e',
            'jdd': '鸡蛋的家',
            'shj': 'SHJ'}

        for tag in nameDict:
        clan[tag] = Member(nameDict[tag])
        clan[tag].abbr = tag

"""
 
