"""数据类专用"""

print('my_class.py imported:', __name__)

import functools

# MethodDescriptor
class MethodDescriptor:
    def __init__(self, m):
        self._meth = m
    def __get__(self, inst, cls=None):
        if cls is None: cls=type(inst)
        @functools.wraps(self._meth)
        def _inst_meth(*a):
            return self._meth(inst, *a)
        return _inst_meth
def method(f):
    return MethodDescriptor(f)

# Base Property Descriptor: Better work with metaclass
class Descriptor:
    def __new__(cls, *args):
        self = super().__new__(cls)
        self.label = getattr(self, 'label', 'No Label')
        return self
    def __get__(self, instance, owner):
        # print("Getting %s of %s %s"%(self, owner.__qualname__, instance))
        if instance is None: return self
        return instance.__dict__.get(self.label)
    def __set__(self, instance, value):
        instance.__dict__[self.label] = value
    def __repr__(self):
        return '<%s %s at 0x%08X>'%(self.__class__.__qualname__,
                                  self.label,
                                  id(self))
    
class ReadOnlyProperty(Descriptor):
    def __set__(self, instance, value):
        raise AttributeError("can't set attribute")     

class PrivateProperty(ReadOnlyProperty):
    """get rid of
    @property
    def xxx(self):return self.__xxx
    eg.
    class Foo(metaclass=DescriptorOwnerMetaclass):
        foo = PrivateProperty()
    """
    def __init__(self, __Descriptor__=Descriptor):
        self.__Descriptor__ = __Descriptor__
    
class ValueLimitedProperty(Descriptor):
    """A descriptor that forbids invalid values
ValueLimitedProperty(*, valid=None)
ValueLimitedProperty() -> normal property
ValueLimitedProperty(valid=func) -> value-limited property
    whenever assigned, exec func.
    assign if pass, raise ValueError if fail.
    """
    def __new__(cls, *, valid=None):
        new = super().__new__(cls)
        new.valid = valid
        return new
 
    def __set__(self, instance, value):
        if self.valid and not self.valid(value):
            raise ValueError("Negative value not allowed: %s" % value)
        instance.__dict__[self.label] = value

# MetaClass of Classes with Value-Limited Property etc.
class DescriptorOwnerMetaclass(type):
    def __new__(cls, name, bases, attrs):
        print('%s is creating %s'%(cls.__qualname__, name))
        # find all descriptors, auto-set their labels
        private = {}
        for k, v in attrs.items():
            if isinstance(v, Descriptor):
                print("    Found Descriptor %s: %s"%(type(v).__qualname__,k))
                v.label = k
                if isinstance(v, PrivateProperty):
                    v.label = '__' + k
                    private['__'+k] = v.__Descriptor__() 
                    private['__'+k].label = '__' + k
        attrs.update(private)
        return super().__new__(cls, name, bases, attrs)

# 字符显示
class Mystr(str):
    
    """
    str(object='') -> str
    str(bytes_or_buffer[, encoding[, errors]]) -> str


    由于中文长度受字体影响严重，在此定义可以稍好计算宽度的字符串类
    方法位计算实际大约宽度和左对齐扩充到制定宽度

    """
    def __new__(cls, *args, **kwargs):
        "Create and return a special String object"
        return super().__new__(cls, *args, **kwargs)

    @property
    def width(self):
        """
        计算大致宽度，但受不同字体影响宽度并不精确。
        等宽字体会稍好一些。中文按照Courier New换算。
        """
        from unicodedata import east_asian_width
        return int((sum(map(lambda x:224 if x in'FW' else 128 if x in 'Na' else 224 ,map(east_asian_width,self)))+64)/128)

    def print(self, value=10):
        """
        返回给定宽度的Mystr
        若宽度不够则返回自身
        """
        return Mystr(self.ljust(value-self.width+len(self))) if value>self.width else self

class MyDate(str):
    """
    日期排序
    """
    def __new__(cls, s='', *args, **kwargs):
        if isinstance(s, str) and s == '':
            import time
            s = time.time()
        if isinstance(s, float):
            import time
            ISOTIMEFORMAT='%Y.%m.%d'
            s = time.strftime(ISOTIMEFORMAT, time.localtime(s))
        if isinstance(s, tuple): s = '%s.%s.%s'%s
        "Create and return a special String object"
        def findspliter(string):
            spliter = []
            for x in '0123456789':
                string = string.replace(x,'')
            while string:
                spliter.append(string[0])
                string = string.replace(string[0],'')
            return spliter
        if isinstance(s, str):
            s = s.replace(' ','')
            p = findspliter(s)
            spliter = tuple(p)
            while p: s = s.replace(p.pop(), '.')
            if len(s) in (6, 8) and s.isnumeric():
                s = "%s.%s.%s"%(s[:-4],s[-4:-2],s[-2:])
            s = tuple(map(int,s.split('.')))
            s = '%d.%02d.%02d'%s
        return super().__new__(cls, s, *args, **kwargs)
    def __init__(self, s='', *args, **kwargs):
        if self and not self.date:
            raise ValueError('%s is not a date I want.'%self)
    def __hash__(self):
        return hash(str(self))
    def __lt__(self, value):
        if isinstance(value, MyDate):
            return self.date < value.date
        return NotImplemented
    def __gt__(self, value):
        if isinstance(value, MyDate):
            return self.date > value.date
        return NotImplemented
    def __le__(self, value):
        if isinstance(value, MyDate):
            return self.date <= value.date
        return NotImplemented
    def __ge__(self, value):
        if isinstance(value, MyDate):
            return self.date >= value.date
        return NotImplemented
    def __eq__(self, value):
        if isinstance(value, MyDate):
            return self.date == value.date
        return NotImplemented
    @property
    def date(self):
        ymd=self.split('.')
        if len(ymd)==3:
            try:
                y,m,d = map(int, ymd)
                if y < 100: y += 2000
                if m < 1 or m > 12 or d < 1: raise
                if m in (1, 3, 5, 7, 8, 10, 12):
                    if d > 31: raise
                elif m == 2:
                    if y % 400:
                        if y % 100:
                            if y % 4:
                                if d > 28: raise
                            elif d > 29: raise
                        elif d > 28: raise
                    elif d > 29: raise
                elif d>30: raise
                return (y,m,d)
            except:raise ValueError('Invalid Date')
    @property
    def y(self):return self.date[0]
    @property
    def m(self):return self.date[1]
    @property
    def d(self):return self.date[2]
    @property
    def second(self):
        import time
        return time.mktime(self.date+(-time.timezone//3600,)+(0,)*5)
    def __add__(self, value):
        if isinstance(value, str):
            return str.__add__(self, value)
        if isinstance(value, int):
            return MyDate(float.__add__(self.second, value*86400))
        return NotImplemented
    def __radd__(self, value):
        if isinstance(value, str): return str.__add__(value, self)
        return MyDate.__add__(self, value)
    def __sub__(self, value):
        if isinstance(value, int): return MyDate.__add__(self, -value)
        try: value = MyDate(value)
        except: return NotImplemented
        return int((self.second - value.second)//86400)

# 微单元类
class AD(str):
    def __new__(cls, value):
        if not isinstance(value, str): raise TypeError
        if len(value) - 1 : raise ValueError
        if value in 'aA': return 'a'
        if value in 'dD': return 'd'
        raise ValueError
class HallLv(int):
    def __new__(cls, value):
        if 0 <= value <= 10:
            value = value or 10
            return value
        raise
class Order(int):
    def __new__(cls, order, ninsuu=50):
        if 0 <= order <= ninsuu:
            order = order or ninsuu
            return order
        raise
class WrongScore(BaseException):pass
class Result(tuple):
    def __new__(cls, star, percent=100):
        result = (star, percent)
        if not 0 <= percent <= 100: raise
        if star == 0 and percent < 50: return result
        elif star == 1 and percent > 0: return result
        elif star == 2 and 100 > percent > 49: return result
        elif star == 3 and percent == 100: return result
        raise WrongScore

# 历史及贡献数据单元类
class Unit(tuple):
    class _copyto:
        "U.copy() -> a shallow copy of U"
        __qualname__ = 'copyto'
        def __new__(cls, inst):
            return tuple.__new__(type(inst), inst)
    class __des:
        def __get__(self, inst, owner):
            return functools.wraps(Unit._copyto)(functools.partial(Unit._copyto, inst or ()))
            if inst is None: return Unit._copyto
            import types
            return types.MethodType(Unit._copyto, inst)
    copyto = __des()

class HistoryUnit(Unit):
    def __new__(cls, ad='a', m=1, t=1, s=0, p=0, ninsuu=50):
        return super().__new__(cls, (AD(ad),) + (Order(m, ninsuu), Order(t, ninsuu)) + Result(s, p))
    def __getnewargs__(self):
        return self
    @property
    def ad(self):return self[0]
    @property
    def m(self):return self[1]-1
    @property
    def t(self):return self[2]-1
    @property
    def s(self):return self[3]
    @property
    def p(self):return self[4]
    @property
    def diff(self):return self[1]-self[2]
class DonateAD(Unit):
    def __new__(cls, mo, to, ml, tl, s, p, donate=0, ninsuu=50):
        return super().__new__(cls, (Order(mo, ninsuu), Order(to, ninsuu),
                                     HallLv(ml), HallLv(tl)) + Result(s, p) + (donate,))
    def __getnewargs__(self):
        return self
class DonateUnit(Unit):
    "('aos',[540,[(1,1,8,8,3,100),(1,2,8,8,3,100)],[(1，2，8，8，0,12)]] )"
    def __new__(cls, abbr='???', donate=0, attack=None, defend=None):
        attack = attack or []
        defend = defend or []
        return super().__new__(cls, (abbr, [donate, attack, defend]))
    @property
    def abbr(self):return self[0]
    @property
    def donate(self):return self[1][0]
    @donate.setter
    def donate(self, value): self[1][0]=value
    @property
    def attack(self):return self[1][1]
    @property
    def defend(self):return self[1][2]
class MemberDonateUnit(Unit):
    def __new__(cls, donate=None):
        if isinstance(donate, DonateUnit): pass
        elif isinstance(donate, tuple): donate = DonateUnit('???', *donate)
        donate=donate or DonateUnit()
        return super().__new__(cls, (donate.donate, tuple(donate.attack), tuple(donate.defend)))
    @property
    def donate(self):return self[0]
    @property
    def attack(self):return self[1]
    @property
    def defend(self):return self[2]
# 历史和贡献类
class HisDon:
    def __str__(self):
        return self.date if hasattr(self, 'date') and self.date else 'No Date'
    __repr__ = __str__

    def copy(self, resource):
        """
        copy
        :param resource: resource
        """
        if isinstance(resource, self.__class__):
            for attr in dir(resource):
                if attr[0] not in '_c':
                    self.__setattr__(attr, resource.__getattribute__(attr))


# 对战记录类
class HistoryItem(HisDon):
    """
        内存格式：
        八个属性：日期 名称 国家 人数 结果 己方信息 敌方信息 战斗信息
        前三个为字符串 结果为我方地方分数二元整数tuple 人数为数字
        己方信息为10元list 每个list为2元tuple 分别是代号字符串和大本等级个位数
        敌信息为10元个位数list
        战斗信息为列表，包含若干tuple 每个tuple5个元素表示一场战斗
        第一个攻防指示字符 第二三个为我方敌方等级 第四个为星数 第五个为百分比
        文件格式：
        ###分割各次部落战
        之后紧跟日期，之后每行依次为名称，国家，人数，我方得分空格敌方得分
        之后X行分别是1到X号位的代号，我方本等，敌方本等 中间无空格
        最后每行5至7位表示一场战斗"""
    def __init__(self, clan, string: str=''):
        from my_coding import my_encode, my_decode
        """
        
        :type string: str
        :param string:str to initialize a history item instance
        """
        self.clan = clan
        if string:
            str_list = string.split('\n')
            self.date = str_list[0]
            self.name = str_list[1]
            self.kuni = str_list[2]
            self.ninsuu = int(str_list[3])
            temp = str_list[4].split(' ')
            self.kekka = (int(temp[0]), int(temp[1]))
            self.percent = (int(temp[2]), int(temp[3])) if len(temp) == 4 else (0, 0)
            self.mikata = []
            self.teki = []
            for i in range(self.ninsuu):
                temp = str_list[5 + i]
                self.mikata.append(clan[temp[0:-2]])
                self.mikata[i].hslv[self.date]= my_decode(temp[-2])
                self.teki.append(my_decode(temp[-1]))
            self.rekishi = []
            for temp in str_list[5+self.ninsuu:-1]:
                item = HistoryUnit(temp[0],
                                   my_decode(temp[1]),
                                   my_decode(temp[2]),
                                   int(temp[3]),
                                   int(temp[4:]),
                                   self.ninsuu)
                self.rekishi.append(item)
        else: self.clear()
    def __lt__(self, value):
        return self.date < value.date
    def __call__(self):
        print('日期：%s 结果： %s'%(self.date, self.result))
    @property
    def date(self):
        return self.__date
    @date.setter
    def date(self, value):
        self.__date = MyDate(value)
    @property
    def result(self):
        if self.kekka[0]>self.kekka[1]:
            return 'WIN'
        elif self.kekka[0]<self.kekka[1]:
            return 'LOSE'
        else:
            if self.date > MyDate('20150917'):
                flag = self.percent[0]-self.percent[1]
                if flag > 0: return 'WIN'
                elif flag < 0: return 'LOSE'
                else: return 'DRAW'
            else: return 'DRAW'
    def copyto(self, clan=None):
        clan = clan or self.clan
        new = HistoryItem(clan)
        new.date = self.date
        new.name = self.name
        new.kuni = sef.kuni
        new.ninsuu = self.ninsuu
        new.kekka = self.kekka
        new.teki.clear()
        new.teki[:] = self.teki[:]
        new.mikata.clear()
        for i in range(self.ninsuu):
            new.mikata.append(clan[self.mikata[i].abbr])
        new.rekishi.clear()
        for item in self.rekishi:
            new.rekishi.append(item.copyto())
    def copyfrom(self, value):
        self.date = value.date
        self.name = value.name
        self.kuni = value.kuni
        self.ninsuu = value.ninsuu
        self.kekka = value.kekka
        self.teki.clear()
        self.teki[:] = value.teki[:]
        self.mikata.clear()
        for i in range(self.ninsuu):
            self.mikata.append(self.clan[value.mikata[i].abbr])
        self.rekishi.clear()
        for item in value.rekishi:
            self.rekishi.append(item.copyto())
        
    def clear(self):
        """

        clear data
        """
        self.date = MyDate('')
        self.name = ''
        self.kuni = ''
        self.ninsuu = 10
        self.kekka = (0, 0)
        self.percent = (0, 0)
        self.mikata = [None] * 50
        self.teki = [0] * 50
        self.rekishi = []


# 贡献类
class DonateItem(HisDon):
    """
内存格式：
贡献类每个实例代表一次部落战，有date和donateList两个属性
date为日期字符串
donateList为列表，元素均为tuple，每个tuple代表一个人
每个tuple有2个元素：代号字符串，记录list
记录list有3个元素：分值x100(整数)，攻击list，防守list
攻防list里有若干tuple，每个tuple代表一次战斗，tuple由7个整数组成
例：
date='2015.7.23'
donateList=[
    ('aos',[540,[(1,1,8,8,3,100,500),(1,2,8,8,3,100,470)],[(1，2，8，8，0,12,0)]]),
    ('cei',[550,[(2,3,8,8,3,100,470)],[(2,2,8,8,0,12,0),(2,1,8,8,1,51,0)]])]
文件存储格式：
###分割各次部落战，之后紧跟日期，换行
之后每行为一个人的数据，由空格分成 代号 分值的100倍 攻防记录3部分
其中记录由|分为攻防2部分
每部分由+分成每次战斗
每次战斗由7位表示：己方序号，敌方序号，己方本等，地方本等，星数，百分比，贡献
贡献之前用'-'分割
序号及等级由my_encode/my_decode编码解码

例：
###2015.7.23
aos 540 11883-500+12883-470+|1288012-0+
cei 550 23883-470+|2288012-0+2188151-0+"""
    def __init__(self, clan, string: str=''):
        from my_coding import my_encode, my_decode
        """


        :type string: str 
        :param string: string to initial a donate item instance
        """
        self.donateList = []
        self.clan = clan
        if string:
            str_list = string.split('\n')
            self.date = str_list[0]
            for temp0 in str_list[1:-1]:
                temp1 = temp0.split(' ')
                unit = DonateUnit(temp1[0], int(temp1[1]))
                if len(temp1[2]):
                    temp2 = temp1[2].split('|')
                    if len(temp2[0]):
                        attack = filter(None, temp2[0].split('+'))
                        for item in attack:
                            percent, donate = item[5:].split('-')
                            unit.attack.append(DonateAD(my_decode(item[0]),
                                                        my_decode(item[1]),
                                                        my_decode(item[2]),
                                                        my_decode(item[3]),
                                                        int(item[4]),
                                                        int(percent),
                                                        int(donate)))
                    if len(temp2[1]):
                        defend = filter(None, temp2[1].split('+'))
                        for item in defend:
                            percent, donate = item[5:].split('-')
                            unit.defend.append(DonateAD(my_decode(item[0]),
                                                        my_decode(item[1]),
                                                        my_decode(item[2]),
                                                        my_decode(item[3]),
                                                        int(item[4]),
                                                        int(percent),
                                                        int(donate)))
                self.donateList.append(unit)
                
    def __lt__(self, value):
        return self.date < value.date
    def __call__(self):
        print('日期：%s 总贡献： %s'%(self.date,
                               sum((x.donate for x in self.donateList))/100))
    @property
    def date(self):
        return self.__date
    @date.setter
    def date(self, value):
        self.__date = MyDate(value)
    def copyto(self, clan=None):
        clan = clan or self.clan
        new = DoateItem(clan)
        new.date = self.date
        for item in self.donateList:
            new.donateList.append(item.copyto())
    def clear(self):
        """

        clear
        """
        self.donateList = []
        self.date = MyDate('')


# 功能类
class FooMeta(type):
    def __new__(cls, name, bases, attrs, **kwargs):
        print(cls, name, bases, attrs)
        return super().__new__(cls, name, bases, attrs, **kwargs)
class SortedDictMetaclass(type):
    def __new__(cls, name, bases, attrs):
        assert any(issubclass(x, dict) for x in bases)
        if not '__key__' in attrs: attrs['__key__'] = lambda x:x
        elif isinstance(attrs['__key__'], type(lambda:None)): pass
        elif attrs['__key__'] == 'k': attrs['__key__'] = lambda x:x[0]
        elif attrs['__key__'] == 'v': attrs['__key__'] = lambda x:x[1]
        else: attrs['__key__'] = lambda x:x
        @method
        @functools.wraps(dict.items)
        def items(self):
            return sorted(dict.items(self), key=type(self).__key__)
        def __getitem__(self, index):
            if isinstance(index, int): return self.items()[index][1]
            else: return dict.__getitem__(self,index)
        attrs['items'] = items
        attrs['__getitem__'] = __getitem__
        return super().__new__(cls, name, bases, attrs)
    def __init__(self, name, bases, attrs):pass
    
class EasyJsonDict(dict):
    def jsondumps(self,**kw):
        import json
        return json.dumps(self, **kw).replace('[','(').replace(']',')')
    @classmethod
    def jsonloads(cls,string,**kw):
        import json
        string = string.replace('(','[').replace(')',']')
        kw['object_hook'] = getattr(cls, 'object_hook', None)
        result = cls()
        result.update(json.loads(string, **kw))
        return result
    def jsonupdates(self, string, **kw):
        self.update(self.jsonloads(string, **kw))
        
class DateKeyDict(EasyJsonDict):
    def __getitem__(self, index):
        if isinstance(index, int): return self.items()[index][1]
        else: return super().__getitem__(index)
    def items(self):
        return sorted(super().items(),key=lambda x:x[0])
    @property
    def dates(self):
        return sorted(self.keys())

class Descriptor4Dict(Descriptor):
    def __get__(self, inst, instcls):
        if inst is None: return self
        get = super().__get__(inst, instcls)
        if get is None:
            get = type(self)()
            get.label = 'of %s'%inst
            super().__set__(inst, get)
        return get
    
# 成员特殊词典
class _MemberDictDescrptor(Descriptor4Dict, DateKeyDict): pass

class MemberDonate(_MemberDictDescrptor):
    @staticmethod
    def object_hook(x):
        new = MemberDonate()
        for k, v in x.items():
            unit = DonateUnit()
            date = MyDate(k)
            unit.donate, a, d = v
            for i in a: unit.attack.append(DonateAD(*i))
            for i in d: unit.defend.append(DonateAD(*i))
            unit = MemberDonateUnit(unit)
            new[date] = unit
        return new

class HsLv(_MemberDictDescrptor):
    @staticmethod
    def object_hook(x):
        new = HsLv()
        for k, v in x.items(): new[MyDate(k)] = int(v)
        return new
        
class Penalty(_MemberDictDescrptor):
    @staticmethod
    def object_hook(x):
        new = Penalty()
        for k, v in x.items(): new[MyDate(k)] = int(v)
        return new
    @property
    def free(self): return max(map(lambda t:t[0]+t[1], self.items()), default=None)
    
# 部落及成员类
class Clan(metaclass=DescriptorOwnerMetaclass):
    """Clan() -> default Clan object
    Clan(str/Mystr) -> New Clan with the given name.
    Clan(Clan) -> New Clan object (disables the old Clan)

    部落类。由成员及部落战记录构成。支持Key和Index（Slice及负数除外）。
    支持for in。
    内置json的dump和load。
    需要和部落成员类以及战斗记录类一起使用。
    由于属性富含环路，基本知道了一个实例就能找出一串。
    其实例也是程序中最重要的全局变量，所有信息均与其相关。
    
    基本判断与功能见下方方法(功能)
    关键属性(私有):
    __realname:Mystr,部落名称
    __member:dict(abbr:Member),成员词典
    __history:dict(MyDate:HistoryItem),历史词典
    __donate:dict(MyDate:DonateItem),贡献词典
    其他属性(只读):
    realname,部落名
    name,经填充部落名
    member,成员词典
    history,历史列表
    donate,贡献列表
    alive,现役成员词典
    number,现役人数
    totalnum,总人数
    game,比赛场数
    win,胜场
    draw,平局
    lose,负场
    临时属性(只读；修改用接口):
    selected:int,已选参战人数
    th:dict(MyDate:HistoryItem),h
    td:dict(MyDate:DonateItem),d
    方法(公用):
    values()->dict_values,返回总成员view
    sort()->None,将成员按rank从高到低排列，并赋order值作为索引
    clear()->None,清空Clan结构
    copyto()->Clan,返回一个本部落的全新副本，所有子项均新建。
    copyfrom(Clan)->None,继承已有部落的全部信息，并将其成员及历史指向自己，废掉原部落。
    方法(功能):
    __str__->带填充名称
    __repr__->原始名称
    __len__->比赛次数
    __int__->现役人数
    __bool__->有没有人
    __iter__->成员
    __getitem__Index/Key->成员
    __setitem__Index/Key + Value添加成员
    __eq__->return self is value
    __call__ ->打印部落名称，由order顺序call各成员，由日期顺序call各比赛
    方法(内部):
    方法(私有):
    """
    MAXSIZE = 50
    NOW = MyDate()
    def __init__(self, value=None):
        """
        创建部落实例。如果给定已有部落，则以此新实例取代之，所有内容均不新建,
        由于成员及历史指向的改变，原部落随即失去功能。因此，单独的Clan(某已有
        部落)语句讲造成致命后果！已有部落的成员及历史均清空，彻底成空壳了。给
        定名称则新建实例。也可以不给名称创建缺省部落。需要确定属性：
        __realname
        __member
        __history
        __donate
        """
        print('Creating Clan %s'%(value,))
        if value is None: value = 'ななしクラン'
        self.__member = {}
        self.__history = DateKeyDict()
        self.__donate = DateKeyDict()
        if isinstance(value,(str,Mystr)):
            self.__realname = Mystr(value)
        elif isinstance(value, Clan): self.copyfrom(value)
        else: raise TypeError('参数类型不符')
        self._th = DateKeyDict()
        self._td = DateKeyDict()
        self.imah = HistoryItem(self)
        self.imad = DonateItem(self)
        self.selected = 0
        
    "只读属性"
    @property
    def able(self): return tuple(filter(lambda x:x.able, self))
    @property
    def realname(self): return self.__realname
    @property
    def name(self): return self.realname.print()
    @property
    def history(self): return self.__history
    @property
    def donate(self): return self.__donate
    @property
    def h(self): return self._th
    @property
    def hk(self): return sorted(self.h.keys())
    @property
    def hv(self): return sorted(self.h.values())
    @property
    def d(self): return self._td
    @property
    def dk(self): return sorted(self.d.keys())
    @property
    def dv(self): return sorted(self.d.values())
    @property
    def member(self): return self.__member
    @property
    def alive(self): return dict(filter(lambda x:x[1].rank,self.member.items())) # todo
    @property
    def number(self): return len(self.alive)
    @property
    def totalnum(self): return len(self.member)
    @property
    def games(self): return len(self.history)
    @property
    def win(self): return len(list(filter(lambda x:x.result=='WIN',self.history.values())))
    @property
    def lose(self): return len(list(filter(lambda x:x.result=='LOSE',self.history.values())))
    @property
    def draw(self): return len(list(filter(lambda x:x.result=='DRAW',self.history.values())))
    @property
    def datelist(self): return list(sorted(self._th.keys()))

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['selected']
        del state['imad']
        del state['imah']
        state['__history'] = state.pop('_th')
        state['__donate'] = state.pop('_td')
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.__dict__['selected'] = 0
        self.__dict__['imad'] = DonateItem(self)
        self.__dict__['imah'] = HistoryItem(self)
        self.__dict__['_th'] = DateKeyDict()
        self.__dict__['_td'] = DateKeyDict()
        

    def __iter__(self):
        """
        迭代自己按order部落成员。
        """
        return iter(sorted(self.member.values(),reverse=True))


    def __getitem__(self, n):
        """
        用Index和Key提取部落成员。Index则按等级从高到低往后排，
        Key则需使用成员缩写。如果给定成员实例，若该成员在部落中则返回之。
        找不到则返回空值。
        """
        if isinstance(n, Member): return n if n in self else None
        if isinstance(n, str):
            return self.member[n]if n in self.member else None
        elif isinstance(n, int):
            if n>=self.totalnum or n<0: raise IndexError('Invalid Index %s'%n)
            for member in self:
                if member.order == n: return member
            else: return None

    def __setitem__(self, key, value):
        """
        用Key对部落添加成员，Key需为成员缩写。
        若该成员已存在，则进行替换。由于成员的部落属性只读，
        需要在创建该成员时指定本部落，否则会报错。
        同理，Key需要与成员缩写一致。
        用None对成员赋值会永久移除成员，其历史信息也不可取。
        成员离开部落应调用Member.die()
        """
        if not isinstance(key, str): raise KeyError('Invalid Key %s'%key)
        elif key not in self.member:    
            if not isinstance(value, Member):
                raise TypeError('%s is not Member instance'%value)
        elif value is None:
            self.dead[key] = self.member.pop(key)
            return
        if not isinstance(value, Member):
            raise TypeError('%s is not Member instance'%value)
        else:
            if key != value.abbr:
                raise ValueError('Should use Key "%s"'%value.abbr)
            if self != value.clan:
                raise ValueError('This member should not be in our clan.')
            self.member[key] = value
            self.sort()

    "其他method wrapper"
    __bool__ = lambda x:x.number>0
    __int__  = lambda x:x.number
    __str__  = lambda x:x.realname
    __repr__ = lambda x:'<Clan object %s at 0x%X>'%(x.realname,id(x))
    __len__  = lambda x:x.number
    __eq__   = lambda x,y:x is y
    def __hash__(self):
        return hash(self.realname + 'salt')
    def __call__(self):
        print ('部落名：%s\n现役成员%d人:'%(self.name,self.number))
        for index in range(self.number): self[index]()
        print('部落战记录')
        for index in self.hv: index()
        print('贡献记录')
        for index in self.dv: index()
    "method"
    def clearh(self): self._th.clear()
    def cleard(self): self._td.clear()
    def addh(self, his): self._th.update(his)
    def addd(self,don): self._td.update(don)
    def sort(self):
        rank = 0
        for i, member in enumerate(self):
            if rank > 100 and rank == member.rank: member.rank -= 1
            member.order, rank = i, member.rank
    def clear(self):
        self.__member.clear()
        self.selected=0
    def copyto(self):
        clan = Clan(self.__realname)
        for member in self.member:
            clan[member.abbr] = member.copyto(clan)
        for history in self.history:
            clan.__history.update(history.copyto(clan))
        for donate in self.donate:
            clan.__donate.update(donate.copyto(clan))
    def copyfrom(self, clan):
        if not isinstance(clan,Clan):
            raise TypeError('違うタイプ')
        self.__realname = clan.__realname
        for history in clan.history.items():
            self.__history.update({history[0]:history[1].copyto(clan)})
        for donate in clan.donate.items():
            self.__donate.update({donate[0]:donate[1].copyto(clan)})
        self.__member = clan.member
        for member in self:
            member._change_clan(self)
    def jsondumps(self,**kw):
        import json
        print(kw)
        default = lambda x:Clan._clan2dict(x)if isinstance(x,Clan) else Member._member2dict(x) if isinstance(x,Member) else x
        default = kw.pop('default',default)
        return json.dumps(self,default=default,**kw)
    def jsonloads(self,string,**kw):
        import json
        assert isinstance(string,str), '应该是字符串！'
        object_hook = lambda x:Clan._dict2clan(x)if'member'in x else Member._dict2member(x) if 'clan' in x else x
        object_hook = kw.pop('object_hook',object_hook)
        self.copyfrom(json.loads(string,object_hook = object_hook,**kw))
        for member in self:
            member.clan = self
    def _clan2dict(self):
        print('c2d',self)
        return {'realname':self.realname,
                'member':self.member,
                }
    def _dict2clan(self):
        """
        由dict恢复出Clan
        """
        print('d2c',self)
        if isinstance(self, Clan):
            raise TypeError('内部函数别瞎用')
        elif isinstance(self, dict):
            return Clan(self['realname'],member=self['member'])
    def _change_name(self, value):
        self.__realname = Mystr(value)
    def _append_history(self, value):
        if isinstance(value, HistoryItem):
            __history[value.date]=value
        else:
            raise TypeError('Need HistoryItem, %s got'%type(value))
            
    def initialize(self):
        """
        初始化给定部落，尝试从配置文件中读取部落。以后将尝试pickle甚至json方法。
        """
        from my_constant import config
        import traceback
        import os
        iniFile = os.path.join(config['dir'],'data','member.ini')
        encoding = config['read']
        try:
            with open(iniFile, 'r', encoding=encoding) as f:
                string = f.read()  
            memList = list(filter(None, string.split('[')))
            for substring in memList:
                L = list(filter(None, substring.split(']')))
                self[L[0]] = Member.jsonloads(L[1], clan=self)
        except FileNotFoundError:
            import pickle
            with open(os.path.join(config['dir'],'data','member.ini'),encoding=config['read'], mode='w')as f:
                with open(os.path.join(config['dir'],'data','member'),mode='rb')as ff:
                    string = pickle.load(ff)
                f.write(string)
            try:
                with open(os.path.join(config['dir'],'data','Clan'),mode='rb')as ff:
                    self.copyfrom(Clan(pickle.load(ff)))
            except:
                traceback.print_exc()
        except BaseException as e:
            traceback.print_exc()
        else:
            pass
        finally:
            pass
        
_DEFAULT_CLAN = Clan('Default Clan for Members')
class Member(metaclass=DescriptorOwnerMetaclass):
    """
    成员类
    """
    hslv = HsLv()
    donate = MemberDonate()
    penalty = Penalty()
    def __new__(cls, clan=None, **kw):
        if clan is None: return super().__new__(cls)
        if 'abbr' in kw and kw['abbr'] in clan.member:
            return clan[kw['abbr']]
        return super().__new__(cls)
    def __init__(self, clan=None, **kw):
        """
        kw: abbr, name, level, rank, order,
            hslv, donate, penalty
        """
        if 'abbr' in kw and clan and kw['abbr'] in clan.member:
            return
        if not isinstance(clan,Clan): clan = _DEFAULT_CLAN
        self.__name = kw['name']if 'name' in kw else 'ななし'
        self.abbr = kw['abbr']if 'abbr' in kw else '???'
        self.__clan = clan
        self.level = kw['level']if 'level' in kw else 1
        self.__rank = int(kw['rank']if 'rank' in kw else 100)
        self.order = kw['order']if 'order' in kw else 49
        
        if 'hslv' in kw: self.hslv.jsonupdates(kw['hslv'])
        if 'donate' in kw: self.donate.jsonupdates(kw['donate'])
        if 'penalty' in kw: self.penalty.jsonupdates(kw['penalty'])
        
    """def __setstate__(self, state):
        hslv = state.pop('hslv')
        donate = state.pop('donate')
        self.__dict__.update(state)
        self.__dict__['hslv'] = HsLv()
        self.__dict__['hslv'].update(hslv)
        self.__dict__['donate'] = MemberDonate()
        self.__dict__['donate'].update(donate)"""
        

    @property
    def name(self):
        return Mystr(self.__name)
    @property
    def printname(self):
        return self.name.print(15)
    @property
    def abbr(self):
        return self.__abbr
    @abbr.setter
    def abbr(self, value):
        if not isinstance(value, str):
            raise TypeError('Abbreviation should be String')
        if len(value)!=3:
            raise ValueError('Abbreviation should be 3 letters')
        self.__abbr = value
    @property
    def clan(self):
        return self.__clan

    @property
    def level(self):
        return self.__level
    @level.setter
    def level(self, value):
        if not isinstance(value, int):
            try:
                value = int(value)
            except:
                raise TypeError('Level must be an integer')
        if value>10 or value<1:
            raise ValueError('Level must between 1 and 10')
        self.__level=value

    @property
    def rank(self):
        return self.__rank
    @rank.setter
    def rank(self, value):
        if not isinstance(value, int):
            try:
                value = int(value)
            except:
                raise TypeError('Rank must be an integer')
        if value>1100 or value<100:
            raise ValueError('Rank must between 100 and 1100')
        self.__rank=value
    @property
    def state(self):
        free = self.penalty.free or MyDate('2000.1.1')
        return 'normal' if free < MyDate() else 'suspended'
    @property
    def free(self): return self.penalty.free
    @property
    def normal(self): return self.state == 'normal'
    @property
    def suspended(self): return self.state == 'suspended'
    @property
    def able(self): return bool (self.normal and self.rank)
    @property
    def order(self): return self.__order
    @order.setter
    def order(self, value):
        if not isinstance(value, int):
            try:
                value = int(value)
            except:
                raise TypeError('Order must be an integer')
        if value>49 or value<0:
            raise ValueError('Order must between 0~49')
        self.__order=value
    def die(self): self.__rank = 0
    def copyto(self, clan):
        kw={}
        kw['name'] = self.realname
        kw['abbr'] = self.abbr
        kw['level'] = self.level
        kw['rank'] = self.rank
        kw['order'] = self.order
        new = Member(clan, **kw)
        new.hslv.update(self.hslv)
        for date, score in self.donate:
            new.add_donation(date, score)
    def copyfrom():
        pass
    def _member2dict(self):
        print('m2d',self)
        return {'name':self.realname,
                'abbr':self.abbr,
                'clan':self.clan.realname,
                'level':self.level,
                'rank':self.rank,
                'order':self.order
                }
    def _dict2member(self):
        print('d2m',self)
        if isinstance(self, Member):
            raise TypeError('平时不许这么用！这可是内部函数')
        elif isinstance(self,dict):
            print('is dict')
            return Member(self['clan'],
                          name=self['name'],
                          abbr=self['abbr'],
                          level=self['level'],
                          rank=self['rank'],
                          order=self['order'],
                          )
    def _change_name(self, name): self.__name = name
    def _change_clan(self, clan):
        if isinstance(clan, Clan):
            self.__clan = Clan
            
    def __call__(self):
        print('Name:%sLevel:%2d'%(self.__name.ljust(10),self.__level))

    def __eq__(self, value): return id(self)==id(value)

    def __ne__(self, value): return not self.__eq__(value)

    def __le__(self, value): return self.__lt__(value) or self.__eq__(value)

    def __gt__(self, value): return not self.__le__(value)
    
    def __lt__(self, value):
        if self.__rank: return self.__rank<value.__rank
        elif value.__rank: return 1
        else: return self.abbr > value.abbr
    
    def __ge__(self, value): return not self.__lt__(value)

    def __str__(self): return self.name

    def __repr__(self): return '<Member %s at 0x%08X>'%(self, id(self))
    
    __hash__ = lambda x:hash(x.realname)

    
    def add_donation(self, date, score):
        """

        :param date: str of date
        :param score: int of score *100
        """
        if date in self.donate:
            print('已经有这个贡献信息了:%s %s'%(date, self))
            return
        assert isinstance(date, MyDate)
        assert isinstance(score, MemberDonateUnit)
        self.donate[date] = score

    def jsondumps(self,**kw):
        div = '\r\n' if 0 else '\n'
        string = '[%s]%s'%(self.abbr,div)
        for attr in['name', 'abbr', 'level', 'rank', 'order']:
            string += '%s = %s%s'%(attr,self.__getattribute__(attr),div)
        for attr in['hslv', 'donate','penalty']:
            string += '%s = %s%s'%(attr,self.__getattribute__(attr).jsondumps(**kw),div)
        string += div
        return string

    @staticmethod
    def jsonloads(string,**kw):
        div = '\r\n' if 0 else '\n'
        clan = kw.pop('clan', _DEFAULT_CLAN)
        L = [x.split(' = ')for x in string.split(div) if ' = ' in x]
        return Member(clan, **dict(L))

