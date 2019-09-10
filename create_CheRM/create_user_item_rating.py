import numpy as np
import csv
import mysql.connector
import sys


def get_authors_name_unique(db_name):
    '''
    :param conn: connection to database
    :return: 1d numpy array with the unique shortNames
    '''

    mydb = connect(db_name)

    my_cursor = mydb.cursor()

    my_cursor.execute("select distinct name from authors order by name")

    myresult = my_cursor.fetchall()
    myresult = np.array(myresult, dtype=str).flatten()

    return myresult


def get_author_ids_by_name(db_name, name):
    mydb = connect(db_name)

    my_cursor = mydb.cursor()

    sql = "select id from authors where name = %s"
    val = (name,)
    my_cursor.execute(sql, val)

    myresult = my_cursor.fetchall()
    myresult = np.array(myresult, dtype=int).flatten()

    return myresult


def get_articles_ids(db_name, authorIDs):
    mydb = connect(db_name)

    my_cursor = mydb.cursor()

    format_strings = ','.join(['%s'] * len(authorIDs))
    my_cursor.execute("select article_id from article_author where author_id in (%s)" % format_strings,
                      tuple(authorIDs))

    myresult = my_cursor.fetchall()

    myresult = np.array(myresult, dtype=int).flatten()

    return myresult


def get_items_ids_for_unique_author(db_name, articlesIDs):
    mydb = connect(db_name)

    my_cursor = mydb.cursor()

    format_strings = ','.join(['%s'] * len(articlesIDs))
    my_cursor.execute("select compound_id from compound_article where article_id in (%s)" % format_strings,
                      tuple(articlesIDs))

    myresult = my_cursor.fetchall()

    myresult = np.array(myresult, dtype=int).flatten()

    return myresult


def get_compounds_chebi_ids(db_name, comp_id):
    mydb = connect(db_name)

    my_cursor = mydb.cursor()

    format_strings = ','.join(['%s'] * len(comp_id))
    my_cursor.execute("select compound_chebi_id from compounds where id in (%s)" % format_strings,
                      tuple(comp_id))

    myresult = my_cursor.fetchall()

    myresult = np.array(myresult, dtype=int).flatten()

    return myresult


def connect(db_name):
    mydb = mysql.connector.connect(
        host='localhost',
        user="",
        password='',
        database=db_name
    )

    return mydb


if __name__ == '__main__':

    mysql_db_name = "chebi_rec_sys"

    with open("cheRM_total.csv", 'wb') as file:

        writer = csv.writer(file, delimiter=',')

        with open("cheRM_author_name_id.csv", 'wb') as file2:

            writer2 = csv.writer(file2, delimiter=',')

            authors_name_unique = get_authors_name_unique(mysql_db_name)

            nameCount = 0
            for name in authors_name_unique:
                print(nameCount, "......", len(authors_name_unique))
                writer2.writerow(np.array([nameCount, name]))

                author_ids = get_author_ids_by_name(mysql_db_name, name)

                articles_ids = get_articles_ids(mysql_db_name, author_ids)

                items_ids = get_items_ids_for_unique_author(mysql_db_name, articles_ids)
                compounds_chebi_ids = get_compounds_chebi_ids(mysql_db_name, items_ids)

                clusterID, count = np.unique(items_ids, return_counts=True)

                for clust, c, cheb_id in zip(clusterID, count, compounds_chebi_ids):
                    array = np.array([nameCount, cheb_id, c])

                    writer.writerow(array)

                nameCount += 1

            file.close()
            file2.close()
