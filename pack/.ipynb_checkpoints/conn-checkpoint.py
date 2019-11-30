import pymssql
import pandas
import uuid


def object2sqlstr(o) -> str:
    if isinstance(o, str):
        return "'%s'" % o
    elif isinstance(o, int):
        return str(o)
    elif isinstance(o, float):
        return str(o)
    elif isinstance(o, uuid.UUID):
        return "'%s'" % str(o)
    else:
        raise TypeError()


class Mssql:

    def __init__(self, db_name: str = "SystemData"):
        self.conn = pymssql.connect(server="xyl19880904.club", user="teacher", password="19880904",database= db_name, charset='utf8')
        self.conn.autocommit(True)
        self.cur = self.conn.cursor(as_dict=True)

    def get_conn(self) -> pymssql.Connection:
        return self.conn

    def get_cur(self) -> pymssql.Cursor:
        return self.cur

    def insert(self, table: pandas.DataFrame, table_name: str = "TestPoints"):
        """数据库中添加数据
        :param table: 数据表
        :param tablename: 数据表名称
        """
        datalist = ["(%s)" % ",".join(map(lambda x: object2sqlstr(x), list(row))) for row in table.values]
        values = ",".join(datalist)
        cols = ",".join(table.columns)
        sql = "insert into %(table_name)s (%(cols)s) VALUES %(values)s" % {"table_name": table_name, "values": values,
                                                                           "cols": cols}
        self.get_cur().execute(sql)

    def select(self, table_name: str = "TestPoints", where: str = "1=1"):
        self.get_cur().execute("select * from %s where %s" % (table_name, where))
        return pandas.DataFrame(list(self.get_cur()))

    def groupby(self, groupby_field: list, table_name: str = "TestPoints", where: str = "1=1"):
        sql = "select %s from %s WHERE %s group by %s " % (
            ",".join(groupby_field), table_name, where, ",".join(groupby_field))
        self.get_cur().execute(sql)
        return pandas.DataFrame(list(self.get_cur()))

    def delete(self, table_name: str = "TestPoints", where: str = "1=1"):
        sql = "delete %s where %s" % (table_name, where)
        self.get_cur().execute(sql)

    def __del__(self):
        self.get_cur().close()
        self.get_conn().close()
