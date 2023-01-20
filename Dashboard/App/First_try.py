import ipyvuetify as v
import pandas as pd
import traitlets
import json
import ipywidgets as widgets
import ipyvuetify as v
from threading import Timer

from traitlets import (Any, Unicode, List)


def create_table():

    table = v.DataTable()
    # create a btn to click on


    # create the object
    #super().__init__()

     # a header
    table.headers = [
        { 'text': 'Charakteristiken:', 'value': 'name'},
        { 'text': '', 'value': 'value' },

    ]

    # 3 initial items
    table.items = [
        {
            'name': 'Adresse:',
            'value': 'Esperantostraße',

        },
        {
            'name': 'Anzahl Stellplätze:',
            'value': 5,

        },
        {
            'name': 'Anzahl der ÖV-Abfahrten:',
            'value': 2 ,

        },
        {
            'name': 'Art der Parkgelegenheit:',
            'value': 'Parkhaus',

        },
        {
            'name': 'Bewirtschaftung:',
            'value': 'Ja',

        },
       {
            'name': 'Netzanbindung:',
            'value': 'Autobahn',

        },
        {
            'name': 'Umliegende Bebauung:',
            'value': 'Schön',

        },

    ]

    # add a slot btn
    table.btn = v.Btn(children=["click to add item"], color="primary", class_='ma-2')
    table.v_slots = [{
        'name': 'top',
        'children': table.btn
    }]

    # js behaviour
    #table.btn.on_event('click', self._on_click)

# def _on_click(self, widget, event, data):

    #new_item = {
     #   'name': 'Cupcake',
      #  'value': 305,

      #}

    #self.items.append(new_item)
    return table

#print(type(create_content()))
table = create_table()
