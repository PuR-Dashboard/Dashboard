<<<<<<< Updated upstream
import sklearn, numpy
import pandas as pd




def filter_for_value(df, category, set_value):

    df.drop(df.loc[df[category] != set_value].index, inplace=True)

    return df



def filter_names(df, filteraspect):

    to_delete = []
    index = []
    Deleted = False

    #nach gratis Plätzen gesucht
    if (filteraspect == "gratis"):

        df.drop(df.loc[df['Preise'] != "gratis"].index, inplace = True )

    #Nach name Suchen
    else:
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
=======
import sklearn, numpy
import pandas as pd




def filter_for_value(df, category, set_value):

    df.drop(df.loc[df[category] != set_value].index, inplace=True)
    df.reset_index(drop = True, inplace = True)
    return df


def filter_for_index(df, index):
    df.drop(index, inplace=True)
    df.reset_index(drop = True, inplace = True)
    return df


def filter_names(df, filteraspect):

    to_delete = []
    index = []
    Deleted = False

    #nach gratis Plätzen gesucht
    if (filteraspect == "gratis"):

        df.drop(df.loc[df['Preise'] != "gratis"].index, inplace = True )

    #Nach name Suchen
    else:
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
>>>>>>> Stashed changes
