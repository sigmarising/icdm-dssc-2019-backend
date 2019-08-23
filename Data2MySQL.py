from algorithm.graph import *
import pandas as pd
import pymysql

DATASET_PATH = './dataset/icdm_contest_data.csv'


def execute_sql(db, cursor, sql):
    try:
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
    execute_sql(db, cursor, "DELETE FROM article")
    print("DELETE ORIGIN DATA")

    data = pd.read_csv(DATASET_PATH)
    for index, row in data.iterrows():
        data_item = {
            "industry": str(row["industry"]),
            "index": str(row["index"]),
            "content": str(row["content"])
        }

        print("Computing - " + data_item["industry"] + ":" + data_item["index"] + " ", end="")

        graph_weak_et = text_2_echarts_data_json_str(data_item["content"], 1, 1)
        print(" 11 ", end="")
        graph_medium_et = text_2_echarts_data_json_str(data_item["content"], 2, 1)
        print(" 21 ", end="")
        graph_strong_et = text_2_echarts_data_json_str(data_item["content"], 3, 1)
        print(" 31 ", end="")
        graph_weak_cd = text_2_echarts_data_json_str(data_item["content"], 1, 2)
        print(" 12 ", end="")
        graph_medium_cd = text_2_echarts_data_json_str(data_item["content"], 2, 2)
        print(" 22 ", end="")
        graph_strong_cd = text_2_echarts_data_json_str(data_item["content"], 3, 2)
        print(" 32 ")

        insert_sql = """INSERT INTO article(`category`, `identity`, `content`,
                `graphWeakEt`, `graphMediumEt`, `graphStrongEt`,
                `graphWeakCd`, `graphMediumCd`, `graphStrongCd`,)
                VALUES('{0}', '{1}', '{2}',
                    '{3}', '{4}', '{5}',
                    '{6}', '{7}', '{8}')               
            """.format(
            data_item["industry"], data_item["index"], "content",
            graph_weak_et, graph_medium_et, graph_strong_et,
            graph_weak_cd, graph_medium_cd, graph_strong_cd
        )
        execute_sql(
            db,
            cursor,
            insert_sql
        )
        print("DONE " + data_item["industry"] + ":" + data_item["index"])

    # disconnect from db
    db.close()


if __name__ == '__main__':
    print("----------- START -----------")
    main()
    print("---------- ALL DONE ----------")
