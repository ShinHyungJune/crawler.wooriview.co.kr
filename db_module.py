import pymysql

def db_info_Security():
    db_infor = {}
    db_infor['user'] = 'ssagudwns'
    db_infor['passwd'] = '!!Ssa4141'
    db_infor['host'] = '52.78.113.119'
    db_infor['db'] = 'whatpick'
    db_infor['charset'] = 'utf8'

    return db_infor

def db_common_connect():
    db_information = db_info_Security()

    user = db_information['user']
    passwd = db_information['passwd']
    host = db_information['host']
    db = db_information['db']
    charset = db_information['charset']

    db_conn = pymysql.connect(
        user=user,
        passwd=passwd,
        host=host,
        db=db,
        charset=charset
    )

    db_conn.set_charset('utf8mb4')

    return db_conn

def db_execution_upd_from_sql(db_con, sqlset):
    db_cursor = db_con.cursor()

    db_cursor.execute(sqlset)
    result_set = db_cursor.fetchall()
    db_cursor.close()

    return result_set

db_con = db_common_connect()
sqlset = 'select * from cars'
result_list = db_execution_upd_from_sql(db_con, sqlset)
for key, value in enumerate(result_list):
    print(value)
