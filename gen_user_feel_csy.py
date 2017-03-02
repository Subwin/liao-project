# -*- encoding: utf-8 -*-
import csv
import codecs

import pymysql
from pymongo import MongoClient

DB_HOST = 'localhost'


def query_multi(sql):
    db = pymysql.connect(host=DB_HOST, port=3306, user='jianke', password='Jh7703@@', database='jianke_demo',
                         charset='utf8')
    db.autocommit(True)
    with db.cursor() as cursor:
        cursor.execute(sql)
        rows = cursor.fetchall()
    db.close()
    return rows

def query_single(sql):
    db = pymysql.connect(host=DB_HOST, port=3306, user='jianke', password='Jh7703@@', database='jianke_demo',
                         charset='utf8')
    db.autocommit(True)
    with db.cursor() as cursor:
        cursor.execute(sql)
        rows = cursor.fetchone()
    db.close()
    return rows

def gen_csv(filename, headers, rows):
    with codecs.open(filename,'w') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        f_csv.writerows(rows)


def main():
    m_client = MongoClient("localhost", 3718)
    m_db = m_client['curricula-dev']
    collection = m_db['curriculum']

    sql = "SELECT name, telephone, invitation_code FROM sales"
    invitor_rows = query_multi(sql)

    csv_headers = ["注册客户", "客户手机", "客户邮箱", "企业", "课程总计", "草稿课程数量", "版本课程数量",]

    for invitor in invitor_rows:
        sql = "SELECT id, username, telephone, email, company FROM manager WHERE invitation_code = {}".format(invitor[2])

        manager_rows = query_multi(sql)
        csv_rows = []
        for manager in manager_rows:
            csv_row = (
                        str(manager[1]),
                        str(manager[2]),
                        str(manager[3]),
                        str(manager[4]),
                        collection.find({"manage_id":manager[0]}).count(),
                        collection.find({"manage_id":manager[0],"version":0,}).count(),
                        collection.find({"manage_id":manager[0],"version":{"$ne": 0},}).count()
                        )
            csv_rows.append(csv_row)
        print(csv_rows)

        if not csv_rows:
            continue
        filename = invitor[0] + "客户产品体验试用信息" + '.csv'
        gen_csv(filename=filename, headers=csv_headers, rows=csv_rows)

def main2():
    m_client = MongoClient("localhost", 3718)
    m_db = m_client['curricula-dev']
    collection = m_db['curriculum']

    csv_headers = ["注册客户", "客户手机", "客户邮箱", "企业", "课程总计", "草稿课程数量", "版本课程数量"]
    csv_rows = []

    sql = "SELECT id, username, telephone, email, company FROM manager"

    manager_rows = query_multi(sql)
    for manager in manager_rows:
        csv_row = (
            str(manager[1]),
            str(manager[2]),
            str(manager[3]),
            str(manager[4]),
            collection.find({"manage_id": manager[0]}).count(),
            collection.find({"manage_id": manager[0], "version": 0,}).count(),
            collection.find({"manage_id": manager[0], "version": {"$ne": 0},}).count()
        )
        csv_rows.append(csv_row)
        print(csv_row)

    filename = "客户产品体验试用信息总表" + '.csv'
    gen_csv(filename=filename, headers=csv_headers, rows=csv_rows)

if __name__ == "__main__":
    # main()
    main2()
