# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import copy
import sqlite3
from itemadapter import ItemAdapter
from scrapy.utils.project import get_project_settings


class SQLitePipeline(object):
    # 打开数据库
    def __init__(self):
        db_name = get_project_settings()['SQLITE_DB_NAME']
        self.table_name = get_project_settings()['TABLE_NAME']
        self.db_conn = sqlite3.connect(db_name)
        self.db_cur = self.db_conn.cursor()

    def open_spider(self, spider):
        pass

    # 关闭数据库
    def close_spider(self, spider):
        self.db_conn.commit()
        self.db_conn.close()

    # 对数据进行处理
    def process_item(self, item, spider):
        self.create_table()
        # print(len(item.data))
        # print(item.data)
        carItem = copy.deepcopy(item.data)
        print('deepcopy complete')
        self.insert_db(carItem)
        return item

    # 检测表中是否存在相同列
    def is_exist(self, column):
        is_exist_cmd = 'pragma  table_info({});'.format(self.table_name)
        self.db_cur.execute(is_exist_cmd)
        total_column = self.db_cur.fetchall()
        for i in range(len(total_column)):
            if total_column[i][1] == column:
                return True
        return False

    # 创建数据表
    def create_table(self):
        create_table_cmd = 'create table if not exists {}(id integer PRIMARY KEY);'.format(self.table_name)
        self.db_cur.execute(create_table_cmd)
        self.db_conn.commit()

    # 获取id
    def get_id(self):
        get_id_cmd = 'select * from {};'.format(self.table_name)
        self.db_cur.execute(get_id_cmd)
        cur_id = len(self.db_cur.fetchall())
        print(cur_id)
        return cur_id + 1

    # 插入数据
    def insert_db(self, item):
        cur_id = self.get_id()
        for i, j in item.items():
            if not self.is_exist(i):
                add_column_cmd = "alter table {} add column '{}' int default'-';".format(self.table_name, i)
                print(add_column_cmd)
                self.db_cur.execute(add_column_cmd)
                self.db_conn.commit()
            if i == '系列':
                insert_data_cmd = "insert into {} ('{}') values('{}');".format(self.table_name, i, j)
                print(insert_data_cmd)
                self.db_cur.execute(insert_data_cmd)
                self.db_conn.commit()
            else:
                update_data_cmd = "update {} set '{}' = '{}' where id = '{}';".format(self.table_name, i, j, cur_id)
                print(update_data_cmd)
                self.db_cur.execute(update_data_cmd)
                self.db_conn.commit()
