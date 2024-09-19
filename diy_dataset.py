import json
from jd import JD


USER_NAME = ''
PASS_WORD = ''
with open('./user_data.json', 'r', encoding='utf8')as f:
    __json = json.load(f)
    USER_NAME = __json['user_name']
    PASS_WORD = __json['pass_word']


jd = JD()
jd.login(USER_NAME, PASS_WORD)


chassis_data = jd.search('机箱')
with open(r'data/chassis.json', 'w', encoding="utf8") as f:
    json.dump(chassis_data, f, ensure_ascii=False)


cpu_data = jd.search('CPU')
with open(r'data/cpu.json', 'w', encoding="utf8") as f:
    json.dump(cpu_data, f, ensure_ascii=False)


motherboard_data = jd.search('主板')
with open(r'data/motherboard.json', 'w', encoding="utf8") as f:
    json.dump(motherboard_data, f, ensure_ascii=False)


heat_sink_data = jd.search('散热器')
with open(r'data/heat_sink.json', 'w', encoding="utf8") as f:
    json.dump(heat_sink_data, f, ensure_ascii=False)


harddisk_data = jd.search('硬盘')
with open(r'data/harddisk.json', 'w', encoding="utf8") as f:
    json.dump(harddisk_data, f, ensure_ascii=False)


power_data = jd.search('电源')
with open(r'data/power.json', 'w', encoding="utf8") as f:
    json.dump(power_data, f, ensure_ascii=False)


memory_data = jd.search('内存')
with open(r'data/memory.json', 'w', encoding="utf8") as f:
    json.dump(memory_data, f, ensure_ascii=False)
