import numpy as np
import unidecode


def unicode_to_int(unicode):
    if unicode is not None:
        my_int = int(unicode)

    else:
        my_int = None

    return my_int


def encode_utf8(df):
    print(df['AuthorList'])
    df['AuthorList'] = df['AuthorList'].astype(str)
    print(df['AuthorList'])
    for i in range(df['AuthorList'].size):
        df['AuthorList'][i] = df['AuthorList'][i].encode('utf-8')

    print(df['AuthorList'])

    # print( df['AuthorList'][0].encode('utf-8'))
    # df['AuthorList'] = df['AuthorList'].str.encode('utf-8')

    # for col in df:
    #     if df[col].dtype!=np.int64:
    #         df[col] = df[col].str.encode('utf-8')
    #         print(df[col])

    df['Id'] = df['Id'].astype(int)

    return df


def remove_accents_from_authors(records_df):
    for i in range(records_df['AuthorList'].size):

        for b in range(len(records_df['AuthorList'][i])):
            records_df['AuthorList'][i][b] = unidecode.unidecode(records_df['AuthorList'][i][b])

    return records_df
