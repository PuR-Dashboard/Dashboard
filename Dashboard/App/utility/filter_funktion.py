import sklearn, numpy
import pandas as pd




def filter_all(df: pd.DataFrame, filter_df: dict[str:str], negative=False)-> pd.DataFrame:
    df_copy = df.copy(deep=True)

    for k in filter_df:
        df = filter_for_value(df, k, filter_df[k])


    if negative:
        keys = list(df.columns.values)
        i1 = df_copy.set_index(keys).index
        i2 = df.set_index(keys).index
        return df_copy[~i1.isin(i2)]

    else:
        return df

def filter_max_value(df, category, max_value):
    if max_value == None:
        return df

    df2 = df.drop(df.loc[df[category] > str(max_value)].index)
    df2 = df2.reset_index(drop = True)
    return df2


def filter_for_value(df:pd.DataFrame, category:str, set_value:str):
    if set_value == None:
        return df

    df2 = df.drop(df.loc[df[category] != set_value].index)
    df2 = df2.reset_index(drop = True)
    return df2

def filter_for_list(df:pd.DataFrame, category:str, set_list:list):
    if set_list == None or len(set_list) == 0:
        return df

    df2 = df.drop(df.loc[~df[category].isin(set_list)].index)
    df2 = df2.reset_index(drop = True)
    return df2


def filter_for_index(df, index):
    df.drop(index)
    df.reset_index(drop = True)
    return df


def filter_names(df, filteraspect):

    to_delete = []
    index = []
    Deleted = False

    filterchar = [char for char in filteraspect]

    index = 0
    while (index < len(df['location'])):

        Deleted = False

        location = df.iloc[index]['location']
        locationchar =  [char for char in location]

        #einzelnen Buchstaben vergleichen
        for i in range(len(filterchar)):

            #wenn filterwort zu lang ist
            if ( i >= (len(locationchar))):
                Deleted = True
                df.drop(df.loc[df['location']== location].index, inplace = True )
                df.reset_index(drop = True, inplace = True)
                break
                #z = z-1

            #wenn eins nicht identisch ist -> raus löschen
            elif (filterchar[i] != locationchar[i]):
                Deleted = True
                df.drop(df.loc[df['location']== location].index, inplace = True )
                df.reset_index(drop = True, inplace = True)
                break
                #z = z-1


        if (not Deleted):
            index += 1


    return df
