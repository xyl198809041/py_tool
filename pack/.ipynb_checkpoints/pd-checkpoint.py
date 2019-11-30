import pandas as pd
import asq
import os
import uuid
from pack import conn
import time
import re
import numpy as np


def data_in_dbtable(data: pd.DataFrame, database_col: dict) -> pd.DataFrame:
    DataTable = pd.DataFrame(columns=list(database_col))
    InDataList = [col for col in database_col if database_col[col] in data.columns]
    OutDataList = [col for col in database_col if database_col[col] not in data.columns]
    for col in InDataList:
        DataTable[col] = data[database_col[col]]
    for col in OutDataList:
        DataTable[col] = DataTable[col].fillna(database_col[col])
    return DataTable


def add_testset(testname: str = "考试", Grade: int = 3, year: int = time.localtime().tm_year,
                month: int = time.localtime().tm_mon):
    database_col = {'Grade': Grade,
                    'TestName': testname,
                    "Year": year,
                    "Month": month, }
    # 打印标题
    print("%s-%s %s" % (year, month, testname))
    return pd.DataFrame(list(database_col.values()), list(database_col)).T


# 'Grade': 3,
# 'TestName': testname,
# "TestGuid": uuid.uuid1(),
# "Year": year,
# "Month": month,
def excel2table_by(path: str, test_id: uuid.UUID):
    """北苑成绩单导入
    :param path:路径
    :param test_id:试卷设置id
    """
    database_col = {'StudentName': "姓名",
                    'Class': "班级",
                    'ShuXue_Point': "数学",
                    'YuWen_Point': "语文",
                    'YingYu_Point': "英语",
                    'KeXue_Point': "科学",
                    'SiZheng_Point': "政治",
                    'TestSetId': test_id}

    # 加载数据
    pf = pd.DataFrame(pd.read_excel(path, header=1))
    # 数据清洗
    pf.drop(0, inplace=True)
    pf["班级"] = pf["班级"].map(lambda x: x.replace("班", ""))
    pf["班级"] = pf["班级"].astype(int)
    pf["姓名"] = pf["姓名"].map(lambda x: x.replace(" ", ""))
    pf["科学"] = pf["生化"] + pf["物理"]

    # 无效数据删除
    DelCol = [col for col in pf.columns if col not in [database_col[col] for col in list(database_col)]]
    pf.drop(DelCol, axis=1, inplace=True)
    return data_in_dbtable(pf, database_col)


def excel2table_gc(path: str, test_id: uuid.UUID):
    """拱宸成绩单导入
    :param path:路径
    :param test_id:试卷设置id
    """
    database_col = {'StudentName': "姓名",
                    'Class': "班级",
                    'ShuXue_Point': "数学",
                    'YuWen_Point': "语文",
                    'YingYu_Point': "英语",
                    'KeXue_Point': "科学",
                    'SiZheng_Point': "社会",
                    'TestSetId': test_id}

    # 加载数据
    pf = pd.DataFrame(pd.read_excel(path, header=0))
    # 数据清洗
    pf.drop(0, inplace=True)
    pf["班级"] = pf["班级"].map(lambda x: re.match("(\d{1,2})", str(x)).group(1))
    pf["班级"] = pf["班级"].astype(int)
    pf["姓名"] = pf["姓名"].map(lambda x: x.replace(" ", ""))
    if "社会" not in pf.keys():
        pf["社会"] = 0

    pf = pf.replace(np.nan, 0)
    # pf["科学"] = pf["生化"] + pf["物理"]
    # 无效数据删除
    DelCol = [col for col in pf.columns if col not in [database_col[col] for col in list(database_col)]]
    pf.drop(DelCol, axis=1, inplace=True)
    return data_in_dbtable(pf, database_col)


def get_path() -> str:
    Pathlist = asq.query(os.listdir(os.getcwd())).where(lambda x: x.find(".xlsx") != -1).to_list()
    for path in Pathlist:
        a = input(path + "Y/N")
        if a.upper() == "Y":
            return path
    return ""


def get_all_test() -> str:
    """获取所有考试记录,并返回选择项"""
    data = conn.Mssql().groupby(["TestName", "Id", "Grade", "Year", "Month"], "TestSets")
    data2str = ["{row[0]}、{row[1].Year}-{row[1].Month} 初{row[1].Grade} {row[1].TestName}".format(row=row) for row in
                data.iterrows()]
    [print(s) for s in data2str]
    a = input("输入序号")
    if int(a) in data.index:
        return data.loc[int(a)].Id
    else:
        return ""


def delete_testpoint_by_testguid(guid: uuid.UUID):
    conn.Mssql().delete(table_name='TestSets', where="Id='%s'" % guid)
    print("成功")


# 分析
def get_testpoint_by_studentname(studentname: str = "诸佳铭") -> pd.DataFrame:
    """获取某学生成绩"""
    data = conn.Mssql().select(table_name='TestPoints,TestSets', where="TestPoints.TestSetId=TestSets.Id and "
                                                                       "StudentName='%s'" % studentname)
    return data


def get_testpoint_by_testguid(guid: uuid.UUID) -> pd.DataFrame:
    """获取某次考试成绩"""
    data = conn.Mssql().select(table_name='TestPoints,TestSets', where="TestPoints.TestSetId=TestSets.Id and "
                                                                       "TestPoints.TestSetId='%s'" % guid)
    return data
