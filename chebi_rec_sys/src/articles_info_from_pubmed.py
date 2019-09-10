import sys
import importlib
from Bio import Entrez
import mysql.connector
import pandas as pd
from database import *


def connect(db_name):
    mydb = mysql.connector.connect(
        host='localhost',
        user="mbarros",
        password='1234',
        database=db_name
    )

    return mydb


def remove_article_from_accesion_database(db_name, pub_id):

    mydb = connect(db_name)

    my_cursor = mydb.cursor()

    sql = "DELETE FROM database_accession WHERE accession_number = %s"

    val = (pub_id,)
    my_cursor.execute(sql, val)

    mydb.commit()

    print(my_cursor.rowcount, "record(s) deleted")



def get_articles_info(list_of_pubmed_ids, db_name):
    #list_of_pubmed_ids = ['444557687989,93434556565,3435656565656']

    Entrez.email = "marcia.c.a.barros@gmail.com"
    # "16037249,16620109,18957134"

    handle = Entrez.esummary(db="pubmed", id=list_of_pubmed_ids, retmode="xml")

    records = Entrez.parse(handle)

    documents = []
    records_df = pd.DataFrame.from_dict(records)

    # #while True:
    # for rec in records:
    #     try:
    #         #c = next(records)
    #
    #         documents.append(rec)
    #         print(rec)
    #
    #     except RuntimeError as err:
    #         print("dentro 0", err)
    #         pub_id = str(err).split()[0].split("=")[1][:-1]
    #         print(pub_id)
    #         remove_article_from_accesion_database(db_name, pub_id)
    #         pass
    #
    #     except UnicodeEncodeError as err2:
    #
    #         print("dentro 1", err2)
    #         pass


    # records_df = pd.DataFrame.from_dict(records)
    # pd.set_option('display.max_columns', None)
    # #print(records_df)


    return records_df
    # sys.exit()
    #
    # documents = []
    # for rec in records:
    #     try:
    #         print(rec)
    #         documents.append(rec)
    #     except RuntimeError as err:
    #         print("dentro 0", err)
    #         continue
    #     except UnicodeEncodeError as err:
    #         print("dentro 1", err)
    #         continue
    #
    # handle.close()
    # # records_df = pd.DataFrame.from_dict(records)
    # # pd.set_option('display.max_columns', None)
    # # print(records_df)
    #
    # # for rec in records:
    # #     print(get_year(rec))
    # #     print(get_authors(rec))
    # #     print(get_doi(rec))
    # #     print(get_title(rec))
    #
    # return documents


def get_year(record):
    if 'PubDate' in record:
        year = record['PubDate']
    else:
        year = None

    return year


def get_doi(record):
    if 'doi' in record:
        doi = record['doi']
    else:
        doi = None

    return doi


def get_authors(record):
    if 'AuthorList' in record:
        authors = record['AuthorList']
    else:
        authors = None

    return authors


def get_title(record):
    if 'Title' in record:
        title = record['Title']
    else:
        title = None

    return title


def get_specific_pubmed_ids(records_df, pubmed_ids):
    selected_records = records_df[records_df.Id.isin(pubmed_ids)]

    return selected_records
