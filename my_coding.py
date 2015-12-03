"""自定义编码"""


print('my_coding.py imported:', __name__)

# 编码
def my_encode(integer:'0~61') -> 'c(0-9a-zA-Z)':
    if not isinstance(integer,int):
        raise TypeError('int needed, %s got'%type(integer))
    if integer<0 or integer>61:
        raise ValueError('should >= 0 and <= 61')
    if integer<10:
        return chr(integer+48)
    elif integer <36:
        return chr(integer+87)
    else:
        return chr(integer+29)
def my_decode(c:'0-9a-zA-Z') -> 'integer(0~61)':
    if not isinstance(c,str):
        raise TypeError('char needed, %s got'%type(c))
    if not len(c)==1:
        raise ValueError('one-character string needed')
    if not c.isalnum():
        raise ValueError('illegal char')
    if c.isnumeric():
        return ord(c)-48
    elif c.islower():
        return ord(c)-87
    else:
        return ord(c)-29
    
# 单位字符串数字转换
def my_str(num) -> str:
    """
    convert 0, 1-9 to 10, 1-9
    :rtype : str
    :param num: number to convert
    :return: str
    """
    return str(num % 10)


def my_int(string: str) -> int:
    """
    convert 1-9,10 to 1-9, 0
    :type string: str
    :param string:string to convert
    :rtype :int
    """
    return 10 - (10 - int(string)) % 10
