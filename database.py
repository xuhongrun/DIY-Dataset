#!/usr/bin/python

import sqlite3
import json


class DataBase:
    def __init__(self, database_name: str) -> None:
        self.conn = sqlite3.connect(database_name + '.db')
        self.cur = self.conn.cursor()

    def __del__(self) -> None:
        self.conn.close()

    def save(self, table_name: str, data: json):
        # create table
        self.cur.execute("CREATE TABLE "+table_name+" ( is_self_operated BLOB, brand TEXT, name TEXT NOT NULL, product_name TEXT, product_number TEXT, image TEXT, price NUMERIC, link TEXT, detail TEXT, PRIMARY KEY('product_number', 'product_name'));")
        print("TABLE %s create success !!!" % table_name)
        self.conn.commit()

        # insert data
        sql = "INSERT INTO "+table_name+" (is_self_operated, brand, name, product_name, product_number, image, price, link, detail) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);"
        data_list = []
        for _data in data:
            data_list.append((_data['is_self_operated'], _data['brand'], _data['name'], _data['product_name'], _data['product_number'], _data['image'], _data['price'], _data['link'], _data['detail']))

        try:
            self.cur.executemany(sql, data_list)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print('executemany failed: %s' % e)
