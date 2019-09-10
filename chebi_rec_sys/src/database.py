import mysql.connector
import numpy as np
from articles_info_from_pubmed import *


def connect(db_name):
    mydb = mysql.connector.connect(
        host='localhost',
        user='',
        password='',
        database=db_name
    )

    return mydb


def get_database_accession(db_name):
    mydb = connect(db_name)

    my_cursor = mydb.cursor()

    my_cursor.execute("SELECT * from database_accession WHERE type='PubMed citation'")

    myresult = my_cursor.fetchall()

    df = pd.DataFrame(myresult, columns=['id', 'compound_id', 'accession_number', 'type', 'source'])

    return df


def get_pubmed_ids(df):
    pubmed_ids = df.accession_number.unique()

    return pubmed_ids


def get_compound_ids(df):
    compound_ids = df.compound_id.unique()

    return compound_ids


def get_pubmed_ids_by_compound(df, comp_id):
    pumbed_ids_for_compound = df[df.compound_id == comp_id].accession_number
    pumbed_ids_for_compound = np.array(pumbed_ids_for_compound).flatten().astype(int).tolist()

    return pumbed_ids_for_compound


############chebi_rec_sys###############


def insert_compound(db_name, comp_id):
    mydb = connect(db_name)

    my_cursor = mydb.cursor()

    sql = "INSERT INTO compounds (compound_chebi_id) VALUES (%s)"

    val = (comp_id,)
    my_cursor.execute(sql, val)

    mydb.commit()

    return my_cursor.lastrowid


def insert_article(db_name, pub_id, y, d, t):
    mydb = connect(db_name)

    my_cursor = mydb.cursor()

    sql = "INSERT INTO articles (pubmed_id, year, doi, title ) VALUES (%s,%s,%s,%s)"

    val = (pub_id, y, d, t)
    my_cursor.execute(sql, val)

    mydb.commit()

    return my_cursor.lastrowid


def insert_author(db_name, author_name):
    mydb = connect(db_name)

    my_cursor = mydb.cursor()

    sql = "INSERT INTO authors (name) VALUES (%s)"

    val = (author_name,)
    my_cursor.execute(sql, val)

    mydb.commit()

    return my_cursor.lastrowid


def check_compound_exists(db_name, comp_id):
    check = False
    mydb = connect(db_name)

    my_cursor = mydb.cursor()
    sql = "SELECT count(*) FROM compounds WHERE compound_chebi_id = %s"
    val = (comp_id,)

    my_cursor.execute(sql, val)

    myresult = my_cursor.fetchall()

    if myresult[0][0] != 0:
        check = True

    return check


def check_article_exists(db_name, pub_id):
    check = False
    mydb = connect(db_name)

    my_cursor = mydb.cursor()
    sql = "SELECT count(*) from articles WHERE pubmed_id = %s"
    val = (pub_id,)

    my_cursor.execute(sql, val)

    myresult = my_cursor.fetchall()

    if myresult[0][0] != 0:
        check = True

    return check


def insert_compound_article(db_name, comp_id, art_id):
    mydb = connect(db_name)

    my_cursor = mydb.cursor()

    sql = "INSERT INTO compound_article (compound_id, article_id) VALUES (%s,%s)"

    val = (comp_id, art_id)
    my_cursor.execute(sql, val)

    mydb.commit()


def insert_article_author(db_name, art_id, auth_id):
    mydb = connect(db_name)

    my_cursor = mydb.cursor()

    sql = "INSERT INTO article_author (article_id, author_id) VALUES (%s,%s)"

    val = (art_id, auth_id)
    my_cursor.execute(sql, val)

    mydb.commit()

    # return my_cursor.lastrowid


def get_compound_id(db_name, comp_id):
    mydb = connect(db_name)

    my_cursor = mydb.cursor()
    sql = "SELECT id from compounds WHERE compound_chebi_id = %s"
    val = (comp_id, )

    my_cursor.execute(sql, val)

    myresult = my_cursor.fetchall()

    return myresult[0][0]


def get_article_id(db_name, pub_id):
    mydb = connect(db_name)

    my_cursor = mydb.cursor()
    sql = "SELECT id from articles WHERE pubmed_id = %s"
    val = (pub_id,)

    my_cursor.execute(sql, val)

    myresult = my_cursor.fetchall()

    return myresult[0][0]


def fill_chebi_db_rec_sys(unique_compound_ids, chebi_db_rec_sys, df_database_acession_pubmed_citations, records_df):
    count = 0
    for comp in unique_compound_ids:
        print("compound_id ", count, "-----", comp, "of ", unique_compound_ids.shape)
        comp = int(comp)
        if check_compound_exists(chebi_db_rec_sys, comp) == False:
            comp_db_id = insert_compound(chebi_db_rec_sys, comp)

            pubmed_ids_by_compound = get_pubmed_ids_by_compound(df_database_acession_pubmed_citations, comp)

            articles_by_compound = get_specific_pubmed_ids(records_df, pubmed_ids_by_compound)
            print(articles_by_compound.shape)
            sys.stdout.flush()

            for index, row in articles_by_compound.iterrows():
                # check in pubmed_id exists in the database
                if check_article_exists(chebi_db_rec_sys, row.Id) == False:

                    if pd.isnull(row.PubDate):
                        row.PubDate = "NULL"

                    if pd.isnull(row.DOI):
                        row.DOI = "NULL"

                    if pd.isnull(row.Title):
                        row.Title = "NULL"

                    art_db_id = insert_article(chebi_db_rec_sys, row.Id, row.PubDate, row.DOI, row.Title)
                    insert_compound_article(chebi_db_rec_sys, comp_db_id, art_db_id)

                    for auth in row.AuthorList:
                        auth_db_id = insert_author(chebi_db_rec_sys, auth)

                        insert_article_author(chebi_db_rec_sys, art_db_id, auth_db_id)

                else:
                    # get article_id
                    art_db_id = get_article_id(chebi_db_rec_sys, row.Id)
                    insert_compound_article(chebi_db_rec_sys, comp_db_id, art_db_id)

        else:
            comp_db_id = get_compound_id(chebi_db_rec_sys, comp)
            continue

        #if count == 1000:
        #    sys.exit()

        count += 1
