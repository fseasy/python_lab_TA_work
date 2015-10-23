#coding=utf-8
##@brief : code for temperature translate between fahrenheit2centigrade 
##! FOR AUTO Evaluation System , Should : 
##~ 1. Remove the output for `raw_input`
##~ 2. exit(0) as always !!!

def fahrenheit2centigrade(fahrenheit_value) :
    return ( fahrenheit_value - 32. ) * 5 / 9 

def centigrade2fahrenheit(centigrade_value):
    return ( centigrade_value * 9. / 5) + 32.

def centigrade2kelvin(centigrade_value):
    return centigrade_value + 273.16

def is_meaningful_centigrade(centigrade_value) :
    kelvin_value = centigrade2kelvin(centigrade_value)
    return kelvin_value > 0 # 绝对零度不可达到

def enum(**enums) :
    return type('Enum' , () , enums)

Mode = enum( F2C=1  , C2F=2 )

if __name__ == "__main__" :
    mode_input = raw_input(
    '''
    ----------温度转换器--------
    输入选项进行功能选择
    1. 华氏温度转摄氏温度
    2. 摄氏温度转华氏温度

    ''')
    if mode_input == "1" :
        mode = Mode.F2C
    elif mode_input == "2" :
        mode = Mode.C2F
    else :
        print "Error"
        exit(1)
    temperature_value = raw_input("请输入有物理意义的{0}温度值？".format("华氏" if mode == Mode.F2C else "摄氏"))
    try :
        temperature_value = float(temperature_value)
    except ValueError , e :
        print "Error"
        exit(1)
    if mode == Mode.F2C :
        # temperature value is fahrenheit value
        centigrade = fahrenheit2centigrade(temperature_value)
        if is_meaningful_centigrade(centigrade) :
            print "{:.2f}".format(centigrade)
        else :
            print "Error"
    else :
        # temperature value is centigrade value
        if is_meaningful_centigrade(temperature_value) :
            fahrenheit_value = centigrade2fahrenheit(temperature_value)
            print "{:.2f}".format(fahrenheit_value)
        else :
            print "Error"


