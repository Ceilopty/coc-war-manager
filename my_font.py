"""字体"""


__author__ = 'Ceilopty'
print('my_font.py imported:', __name__)

def _set(kw):
    options = []
    for k, v in kw.items():
        options.append("-"+k)
        options.append(str(v))
    return tuple(options)

def _get(args):
    options = []
    for k in args:
        options.append("-"+k)
    return tuple(options)

def _mkdict(args):
    options = {}
    for i in range(0, len(args), 2):
        options[args[i][1:]] = args[i+1]
    return options

def read_font(root):
    import tkinter.font as tkFont
    if not root: return
    tk = getattr(root, 'tk', root)
    default_font = tk.splitlist(tk.call("font", "actual", 'TkDefaultFont'))
    default = _mkdict(default_font)
    root.configs['defaultfont'] = default
    font = root.configs['font'] if 'font' in root.configs else {}
    family = font['family'] if 'family' in font else default['family']
    size = int(font['size']) if 'size' in font else default['size']
    print(family, size)
    weight = tkFont.BOLD if 'weight' in root.configs and root.configs['weight'] == 'bold'\
           else tkFont.NORMAL
    editFont = tkFont.Font(root, (family, size, weight))
    root.option_add("*Font", editFont)
    root.editFont = editFont


def getfont(root):
    import tkinter.font
    try:
        ft = tkinter.font.Font(family = 'Microsoft YaHei',size = 10,weight = tkinter.font.NORMAL)
    except:
        try:
            ft = tkinter.font.Font(family = '源ノ角ゴシック Light',size = 10,weight = tkinter.font.NORMAL)      
        except:
            try:
                ft = tkinter.font.Font(family = 'Fixedsys',size = 10,weight = tkinter.font.NORMAL)
            except:
                try:
                    ft = tkinter.font.Font(family = 'ＭＳ ゴシック',size = 10,weight = tkinter.font.NORMAL)
                except:
                    try:
                        ft = tkinter.font.Font(family = 'Courier',size = 10,weight = tkinter.font.NORMAL)
                    except:
                        pass
    print(ft,"got")
    return ft

#字体预览弹出菜单
def font_menu(master,root):
    import tkinter
    if not hasattr(tkinter,'font'):
        try:
            import tkinter.font
        except AttributeError:
            from tkinter import font as tkinterfont
            tkinter.__setattr__('font',tkinterfont)
    
    mainFont = tkinter.font.Font(root,font='TkDefaultFont')
    root.option_add("*Font", mainFont)
    
    def add_value(parent, Var, *List):
        for value in List:
            ft = tkinter.font.Font(family = 'Fixedsys',size = 10,weight = tkinter.font.NORMAL)
            if Var:
                ft.config(size = value)
            else:
                ft.config(family = value)
            parent.add_command(label=str(value),font=ft)
        return parent

    selectfont = tkinter.Menu(master,tearoff=0)
    selectsize = tkinter.Menu(master,tearoff=0)
    fontList = tkinter.font.families()
    sizeList = tuple(range(8,51,2))
    add_value(selectfont, 0, *fontList)
    add_value(selectsize, 1, *sizeList)
    menu = tkinter.Menu(master,tearoff=0)
    
    menu.add_cascade(label='字体预览', menu=selectfont)
    menu.add_cascade(label='字号预览', menu=selectsize)
    def popup(event):
        menu.post(event.x_root, event.y_root)
    master.bind("<Button-3>", popup)

    



# 字体选择按钮
def font_btn(master,root):
    print("I'm new")
    import tkinter
    if not hasattr(tkinter,'font'):
        try:
            import tkinter.font
        except AttributeError:
            from tkinter import font as tkinterfont
            tkinter.__setattr__('font',tkinterfont)
            
    from my_constant import config
    frame = tkinter.Frame(master)
    mainFontDescr = tkinter.Button()["font"]
    mainFont = tkinter.font.Font(root,font=mainFontDescr,size=10)
    root.option_add("*Font", mainFont)
    fontList = tkinter.font.families()
    sizeList = tuple(range(8,51,2))
    entryVar = tkinter.StringVar(root)
    entryVar.set(mainFont.cget("family"))
    entryVar2 = tkinter.IntVar(root)
    entryVar2.set(mainFont.cget("size"))
    print(entryVar.get())
    def setMainFont(varName, *args):
        print("family",entryVar.get())
        mainFont.configure(family = root.globalgetvar(varName))
    entryVar.trace_variable("w", setMainFont)
    def setMainFontSize(varName, *args):
        print("size",entryVar2.get())
        mainFont.configure(size = root.globalgetvar(varName))
    entryVar2.trace_variable("w", setMainFontSize)
    tkinter.OptionMenu(frame, entryVar, *fontList).pack(side=tkinter.LEFT)
    tkinter.OptionMenu(frame, entryVar2, *sizeList).pack(side=tkinter.LEFT)
    return frame 

