#!/usr/bin/python

import json
import time
from jd import JD
from database import DataBase


local_time = time.strftime(r'%Y%m%d%H%M%S', time.localtime())

USER_NAME = ''
PASS_WORD = ''
with open('./user_data.json', 'r', encoding='utf8')as f:
    __json = json.load(f)
    USER_NAME = __json['user_name']
    PASS_WORD = __json['pass_word']

db = DataBase('DIY_HOST')


jd = JD()
jd.login(USER_NAME, PASS_WORD)


try:
    cpu_data = jd.search('CPU')
    cpu_data_name = 'cpu_data_' + local_time
    with open(r'data/'+cpu_data_name+'.json', 'w', encoding="utf8") as f:
        json.dump(cpu_data, f, ensure_ascii=False)
    db.save(cpu_data_name, cpu_data)
except Exception as e:
    print('%s' % e)


try:
    graphics_data = jd.search('显卡')
    graphics_data_name = '显卡_data_' + local_time
    with open(r'data/'+graphics_data_name+'.json', 'w', encoding="utf8") as f:
        json.dump(graphics_data, f, ensure_ascii=False)
    db.save(graphics_data_name, graphics_data)
except Exception as e:
    print('%s' % e)


try:
    motherboard_data = jd.search('主板')
    motherboard_data_name = 'motherboard_data_' + local_time
    with open(r'data/'+motherboard_data_name+'.json', 'w', encoding="utf8") as f:
        json.dump(motherboard_data, f, ensure_ascii=False)
    db.save(motherboard_data_name, motherboard_data)
except Exception as e:
    print('%s' % e)


try:
    memory_data = jd.search('内存')
    memory_data_name = 'memory_data_' + local_time
    with open(r'data/'+memory_data_name+'.json', 'w', encoding="utf8") as f:
        json.dump(memory_data, f, ensure_ascii=False)
    db.save(memory_data_name, memory_data)
except Exception as e:
    print('%s' % e)


try:
    harddisk_data = jd.search('硬盘')
    harddisk_data_name = 'harddisk_data_' + local_time
    with open(r'data/'+harddisk_data_name+'.json', 'w', encoding="utf8") as f:
        json.dump(harddisk_data, f, ensure_ascii=False)
    db.save(harddisk_data_name, harddisk_data)
except Exception as e:
    print('%s' % e)


try:
    fan_data = jd.search('风扇')
    fan_data_name = 'fan_data_' + local_time
    with open(r'data/'+fan_data_name+'.json', 'w', encoding="utf8") as f:
        json.dump(fan_data, f, ensure_ascii=False)
    db.save(fan_data_name, fan_data)
except Exception as e:
    print('%s' % e)


try:
    power_data = jd.search('电源')
    power_data_name = 'power_data_' + local_time
    with open(r'data/'+power_data_name+'.json', 'w', encoding="utf8") as f:
        json.dump(power_data, f, ensure_ascii=False)
    db.save(power_data_name, power_data)
except Exception as e:
    print('%s' % e)


try:
    chassis_data = jd.search('机箱')
    chassis_data_name = 'chassis_data_' + local_time
    with open(r'data/'+chassis_data_name+'.json', 'w', encoding="utf8") as f:
        json.dump(chassis_data, f, ensure_ascii=False)
    db.save(chassis_data_name, chassis_data)
except Exception as e:
    print('%s' % e)
