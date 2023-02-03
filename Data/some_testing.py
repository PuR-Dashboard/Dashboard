import json

with open("Urls.json") as json_file:
    json_decoded = json.load(json_file)

json_decoded['Schmeidelberg'] = 'ADDED_VALUE'

with open("Urls.json", 'w') as json_file:
    json.dump(json_decoded, json_file)



"""
@callback(
    [Output("layout_map", "children"),
    Output("sideboard_name_filter" + seitentag, "value"),
    Output("sideboard_address_filter" + seitentag, "value"),
    Output("sideboard_occupancy_filter" + seitentag, "value"),
    Output("sideboard_price_filter" + seitentag, "value"),],
    [Input("placeholder_div_filter" + seitentag, "n_clicks"),
    Input("placeholder_div_adding" + seitentag, "n_clicks"),
    Input("clear_filter_button" + seitentag, "n_clicks"),
    Input("refresh_page", "n_clicks"),
    Input("sideboard_name_filter" + seitentag, "value"),
    Input("sideboard_address_filter" + seitentag, "value"),
    Input("sideboard_occupancy_filter" + seitentag, "value"),
    Input("sideboard_price_filter" + seitentag, "value"),],
    prevent_initial_call=True
)
def update_layout(*args):

    triggered_id = ctx.triggered_id
    #print(triggered_id)

    #manually write characteristics of quick filters
    sidebar_characs = ["location", "address", "occupancy", "price"]

    #num is amount of sidebar elements that are quickfilter, i.e. the last num inputs of this callback
    num = 4
    sidebar_values = args[-num:]
    #print("VALS: ", sidebar_values)
    # index of callback input for
    marks = args[-4]

    if triggered_id == "clear_filter_button" + seitentag:
        reset_data()
        reset_global_filter()
        new_lay = reverse_Map()

        return (new_lay,) + tuple(sidebar_values)
    #elif triggered_id == "sideboard_name_filter" + seitentag or triggered_id == "sideboard_occupancy_filter" + seitentag:
    elif triggered_id == "refresh_page" or triggered_id == "placeholder_div_filter" + seitentag: #or triggered_id == "placeholder_div_adding" + seitentag:
        reset_data()
        filter_data()
        return (create_html_map(glob_vars.data),) + tuple(sidebar_values)

    else:
        print()
        reset_data()
        #sidebar_characs = ["location", "address", "occupancy", "price"]
        assert len(sidebar_characs) == len(sidebar_values)

        for s, val in zip(sidebar_characs, sidebar_values):

            if val == None or val == "":
                glob_vars.current_filter[s] = None
                continue
            else:
                glob_vars.current_filter[s] = val
        #filter_dict = create_filter_dict(administration=args[-2], parking_lots_range=args[-1])
        #print(glob_vars.current_filter)
        filter_data()#glob_vars.current_filter)

        #print(glob_vars.data)

        return (keep_layout_Map(),) + tuple(sidebar_values)

"""


"""
#--------
#layout refresh callback and sidebar handling
#gets confirmation of deletion, update filter etc through placeholder, also inputs from sidebar
@callback(
    [Output("list_layout", "children"),
    Output("sideboard_name_filter" + seitentag, "value"),
    Output("sideboard_address_filter" + seitentag, "value"),
    Output("sideboard_occupancy_filter" + seitentag, "value"),
    Output("sideboard_price_filter" + seitentag, "value"),],
    [Input("placeholder_div_delete_list", "n_clicks"),
    Input("placeholder_div_filter" + seitentag, "n_clicks"),
    Input("placeholder_div_adding" + seitentag, "n_clicks"),
    Input("clear_filter_button" + seitentag, "n_clicks"),
    Input("refresh_page", "n_clicks"),
    Input("sideboard_name_filter" + seitentag, "value"),
    Input("sideboard_address_filter" + seitentag, "value"),
    Input("sideboard_occupancy_filter" + seitentag, "value"),
    Input("sideboard_price_filter" + seitentag, "value"),],
    prevent_initial_call=True
)
def update_layout(*args):
    \"""
    last x args are input values from sidebar
    order important according to sidebar_characs list
    \"""
    triggered_id = ctx.triggered_id

    #manually write characteristics of quick filters
    sidebar_characs = ["location", "address", "occupancy", "price"]

    #num is amount of sidebar elements that are quickfilter, i.e. the last num inputs of this callback
    num = 4
    sidebar_values = args[-num:]
    # index of callback input for

    #if clear filter was pressed reset all filters
    if triggered_id == "clear_filter_button" + seitentag:
        #reet data and filter dictionary
        reset_data()
        reset_global_filter()
        #return refreshed layout with new data and empty value list for inputs
        sidebar_values = [None for x in sidebar_values]
        return (refresh_layout(),) + tuple(sidebar_values)
    #if refresh button pressed
    elif triggered_id == "refresh_page":
        return (refresh_layout(),) + tuple(sidebar_values)
    #if confirmation of successful filtering, deleting, etc is given refresh the page
    elif triggered_id == "placeholder_div_filter" + seitentag or triggered_id == "placeholder_div_adding" + seitentag or triggered_id == "placeholder_div_delete_list":
        return (refresh_layout(),) + tuple(sidebar_values)
    else:
        #sidebar filter triggered
        #first reset data
        reset_data()
        #check for error
        assert len(sidebar_characs) == len(sidebar_values), "Number of filter inputs in sidebar and hardcoded characteristics must be equal"

        #add filter values to dictionary
        for s, val in zip(sidebar_characs, sidebar_values):

            if val == "":
                val = None

            glob_vars.current_filter[s] = val

        #filter with new filter dictionary
        print(glob_vars.current_filter)
        filter_data()

        return (refresh_layout(),) + tuple(sidebar_values)
"""




"""import pandas as pd
import os
import pathlib
from collections import defaultdict
import pages.global_vars as glob_vars


#get the top directory of our app, regardless of depth
#TO-DO: Error if while loop breaks and nothing matching was found
def get_root_dir(name_of_top_folder="App"):
    current_path = pathlib.Path(__file__).parent.resolve()
    parent_path = current_path
    while os.path.basename(parent_path) != name_of_top_folder:
        parent_path = parent_path.parent.absolute()

        if parent_path.parent.absolute() == parent_path:
            break


    parent_path = parent_path.parent.absolute()

    return parent_path


def get_path_to_csv(name_of_csv="Characteristics.csv", app_name="App"):
    data_path = get_root_dir(app_name)

    return os.path.join(data_path, os.path.join("Data", name_of_csv))


#get data stored in our Location Data and return DataFrame
def get_data(name_of_csv="Location_Data.csv", app_name="App"):
    #data_path = get_root_dir(app_name)
    #print(os.path.join(data_path, os.path.join("Data", name_of_csv)))
    df = pd.read_csv(get_path_to_csv(name_of_csv, app_name))
    return df

#DEPRECATED?
def reverse_parking_lot_list(value_list, marks):
    if value_list == None:
        return None

    index_list = set()
    for i in range(1, len(marks)):
        if marks[str(i)] + "-" + marks[str(i+1)] in value_list:
            index_list.add(i)
            index_list.add(i + 1)
    
    index_list = list(index_list)
    return [index_list[0], index_list[-1]]

#DEPRECATED?
def make_parking_lot_list(mini, maxi, values):
    value_list = []

    for i in range(mini, maxi):
        i_range = values[str(i)] + "-" + values[str(i+1)]
        value_list.append(i_range)

    return value_list"""