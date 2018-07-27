from pymongo import MongoClient
# 链接mongodb数据库
mongo_cli = MongoClient('127.0.0.1', 27017)
# 选择数据库
db = mongo_cli['tianyan']
# 选择集合
col = db['tianyan']


# 添加数据
def insert_data(data, tianyan_logger):
    try:
        col.insert_one(data)
        tianyan_logger.info("insert data sucess!")
    except Exception as e:
        tianyan_logger.error("fail to insert data:{}".format(str(e)))


