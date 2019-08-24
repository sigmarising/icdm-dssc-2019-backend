from algorithm.graph import *
import pandas as pd
import pymysql

DATASET_PATH = './data/icdm_contest_data.csv'


def execute_sql(db, cursor, sql, q=None):
    try:
        if q:
            cursor.execute(sql, q)
        else:
            cursor.execute(sql)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        exit(1)


def main():
    # connect to db
    db = pymysql.connect(
        host="39.98.186.125",
        port=3306,
        db="icdm2019",
        user="root",
        password="Aa123456"
    )
    # get a cursor
    cursor = db.cursor()

    # delete origin data
    print("=> DELETE ORIGIN DATA", end="")
    execute_sql(db, cursor, "DELETE FROM article")
    print(" - DONE")

    data = pd.read_csv(DATASET_PATH)
    for index, row in data.iterrows():
        data_item = {
            "industry": str(row["industry"]),
            "index": str(row["index"]),
            "content": str(row["content"])
        }

        print("=> COMPUTING - " + data_item["industry"] + ":" + data_item["index"])

        graph_weak = text_2_echarts_data_json_str(data_item["content"], 1)
        print("    Weak Graph - DONE")
        graph_medium = text_2_echarts_data_json_str(data_item["content"], 2)
        print("    Medium Graph - DONE")
        graph_strong = text_2_echarts_data_json_str(data_item["content"], 3)
        print("    Strong Graph - DONE")

        print("    INSERT SQL", end="")
        insert_sql = \
            "INSERT INTO `article`(`category`, `identity`, `content`, " \
            "`graphWeak`, `graphMedium`, `graphStrong`)" \
            "VALUES(%s, %s, %s, %s, %s, %s)"
        execute_sql(
            db,
            cursor,
            insert_sql,
            (
                data_item["industry"],
                data_item["index"],
                data_item["content"],
                graph_weak,
                graph_medium,
                graph_strong
            )
        )
        print(" - DONE")

    # disconnect from db
    db.close()


if __name__ == '__main__':
    print("----------- START -----------")
    main()
    print("---------- ALL DONE ----------")
