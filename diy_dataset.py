#!/usr/bin/python

import json
import time
from jd import JD
from database import DataBase


def jd_search(jd: JD, db: DataBase, local_time: str, search_key: str):
    try:
        data = jd.search(search_key)
        data_name = search_key+'_'+local_time

        with open(r'data/'+data_name+'.json', 'w', encoding="utf8") as f:
            json.dump(data, f, ensure_ascii=False)

        db.save(data_name, data)
    except Exception as e:
        print('%s' % e)


if __name__ == '__main__':
    local_time = time.strftime(r'%Y%m%d%H%M%S', time.localtime())

    USER_NAME = ''
    PASS_WORD = ''
    SEARCH_KEY = None
    with open('./user_data.json', 'r', encoding='utf8')as f:
        __json = json.load(f)
        USER_NAME = __json['user_name']
        PASS_WORD = __json['pass_word']
        SEARCH_KEY = __json['search_key']

    jd = JD()
    jd.login(USER_NAME, PASS_WORD)

    db = DataBase('DIY_HOST')


    for _search_key in SEARCH_KEY:
        print('*'*10+_search_key+'*'*10)

        jd_search(jd, db, local_time, _search_key)
