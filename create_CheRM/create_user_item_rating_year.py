import numpy as np
import csv
import mysql.connector
import sys
import pandas as pd


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
                      tuple(authorIDs.tolist()))

    myresult = my_cursor.fetchall()

    myresult = np.array(myresult, dtype=int).flatten()

    # myresult = pd.DataFrame(myresult, columns=['article_id', 'year'] )

    return myresult


def get_articles_year(db_name, articles_id):
    articles_id = np.unique(articles_id)
    mydb = connect(db_name)

    my_cursor = mydb.cursor()

    format_strings = ','.join(['%s'] * len(articles_id))

    my_cursor.execute("select id, year from articles where id in (%s)" % format_strings,
                      tuple(articles_id.tolist()))

    myresult = my_cursor.fetchall()

    # myresult = np.array(myresult, dtype=int).flatten()

    myresult = pd.DataFrame(myresult, columns=['article_id', 'year'])


    return myresult


def get_items_ids_for_unique_author(db_name, articlesIDs):
    mydb = connect(db_name)

    my_cursor = mydb.cursor()

    format_strings = ','.join(['%s'] * len(articlesIDs))
    my_cursor.execute("select compound_id, article_id from compound_article where article_id in (%s)" % format_strings,
                      tuple(articlesIDs.tolist()))

    myresult = my_cursor.fetchall()

    # myresult = np.array(myresult, dtype=int).flatten()
    myresult = pd.DataFrame(myresult, columns=['compound_id', 'article_id'])

    return myresult


def get_compounds_chebi_ids(db_name, comp_id):
    mydb = connect(db_name)

    my_cursor = mydb.cursor()

    format_strings = ','.join(['%s'] * len(comp_id))
    my_cursor.execute("select compound_chebi_id, id from compounds where id in (%s)" % format_strings,
                      tuple(comp_id.tolist()))

    myresult = my_cursor.fetchall()

    # myresult = np.array(myresult, dtype=int).flatten()
    myresult = pd.DataFrame(myresult, columns=['compound_chebi_id', 'compound_id'])

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

    with open("/mlData/cheRM_total_user_item_rat_year.csv", 'w') as file:

        writer = csv.writer(file, delimiter=',')

        with open("/mlData/cheRM_author_name_id_year.csv", 'w') as file2:
            writer2 = csv.writer(file2, delimiter=',')

            authors_name_unique = get_authors_name_unique(mysql_db_name)


            nameCount = 0
            for name in authors_name_unique:
                print(nameCount, "......", len(authors_name_unique))


                # id unico por autor unico
                writer2.writerow(np.array([nameCount, name]))

                # autor name, id
                author_ids = get_author_ids_by_name(mysql_db_name, name)

                # autor artigos
                articles_ids = get_articles_ids(mysql_db_name, author_ids)



                articles_years = get_articles_year(mysql_db_name, articles_ids)

                # artigo item
                items_ids = get_items_ids_for_unique_author(mysql_db_name, articles_ids)


                item_article_year = pd.merge(items_ids, articles_years, on='article_id')
                compounds_chebi_ids = get_compounds_chebi_ids(mysql_db_name, items_ids.compound_id)
                item_article_year_itemchebi = pd.merge(item_article_year, compounds_chebi_ids, on='compound_id')

                item_article_year_itemchebi['user'] = nameCount
                item_article_year_itemchebi['rating'] = 1

                user_item_rat_year = item_article_year_itemchebi[['user', 'compound_chebi_id', 'rating', 'year']]

                user_item_rat_year.to_csv(file, mode='a', header=False, index=False)

                nameCount += 1

            file.close()
            file2.close()
