from database import *
from articles_info_from_pubmed import *
from convertors import *


pd.set_option('display.max_columns', None)

if __name__ == '__main__':

    chebi_mysql = 'testdb'
    chebi_db_rec_sys = "chebi_rec_sys"

    df_database_acession_pubmed_citations = get_database_accession(chebi_mysql)
    all_pubmed_ids = np.array(df_database_acession_pubmed_citations.accession_number.unique())

    records_df = pd.DataFrame()
    count = 0
    for ids in np.array_split(all_pubmed_ids, 7):
        print(count)
        print(ids.shape)
        sys.stdout.flush()
        list_of_pubmed_ids = ','.join(ids)

        if count == 0:

            temp = get_articles_info(list_of_pubmed_ids, chebi_mysql)
            records_df = temp

        else:

            temp = get_articles_info(list_of_pubmed_ids, chebi_mysql)
            records_df = records_df.append(temp, ignore_index=True)
            print(records_df.shape)

        count+=1


    #list_of_pubmed_ids = ','.join(np.array(df_database_acession_pubmed_citations.accession_number.head(1000).unique()))
    #print(df_database_acession_pubmed_citations.accession_number.unique().shape)

    # list of pubmed ids


    #records_df = get_articles_info(list_of_pubmed_ids, chebi_mysql)

    print(records_df.shape)


    '''

    for rec in records:
        try:
            if 'Item' in rec:
                print(rec)
           # print("")
        except RuntimeError:
            print("11111111111111111111111111111122222222222222222222222222222222LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL3333333333333333333333333333333333")
            pass

        except UnicodeEncodeError:
            continue
    '''

    # records_df = pd.DataFrame.from_dict(records)
    # print("here3")
    records_df['Id'] = records_df['Id'].astype(int)
    #
    records_df = remove_accents_from_authors(records_df)

    #

    #
    # # list of compunds IDs
    unique_compound_ids = get_compound_ids(df_database_acession_pubmed_citations)
    #
    fill_chebi_db_rec_sys(unique_compound_ids, chebi_db_rec_sys, df_database_acession_pubmed_citations, records_df)
