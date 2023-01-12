#!/usr/bin/env python

# Import required packages
import PySimpleGUI as sg
import os.path
from datetime import date
import copy
import csv
import pandas as pd

sg.theme("DarkGreen")
#-------------------------------------------------------------------------------
# Define starting variables
description="Random inventory object"

wd = os.getcwd()

users = ["Jason",
        "Sunnie",
        "Sarah",
        "Jasmin"
]

log_header = [
    "Date",
    "Product Name",
    "User"
]

statuses = ["Submitted",
            "Requisitioned",
            "Ordered",
            "Received",
            "Backordered"
]

locations = ["4 C Walkin",
            "4 C Rad Fridge",
            "-20 C Rad Fridge"
            "-20 C Walkin",
            "-80 Freezer"
]

date = date.today()

#-------------------------------------------------------------------------------

def popup_location():
    layout=[[
    sg.Text("You've entered an item as 'Recieved' without a location. Please select or enter a location."),
    sg.Combo(locations, key = "-location2-"),
    sg.Button("Enter")],
    ]
    window2 = sg.Window("Select a Location", layout = layout)
    while True:
        event2, values2 = window2.read()
        if event2 == "Exit" or event2 == sg.WIN_CLOSED:
            window2.close()
            del window2
        elif event2 == "Enter" and len(values2["-location2-"]):
            #return values2["-location2-"]
            window2.close()

    window2.close()
    del window2


def get_slice(dataframe, set_number, window3):
    for i in list(range(set_number,set_number+9)):
        #print(i)
        row_number = 0
        if i <= len(dataframe)-1:
            print(dataframe.loc[i,"User"])
            window3[values[i,0]].update(dataframe.loc[i,"Date"])
            #print(dataframe.iloc[[i]])
    pass

#-------------------------------------------------------------------------------
material_entry_column = [
    [sg.Text("Product name"),
    sg.In(size=(20, 2), key="-name-"),
    sg.Push(),
    sg.Text("Company"),
    sg.In(size=(15, 2), key="-company-"),
    sg.Push(),
    sg.Text("Catalog number"),
    sg.In(size=(15, 2), key="-catalog-")],
    [sg.Text("Description"),
    sg.In(size=(50, 4), key="-desc-"),
    sg.Push(),
    sg.Text("Number"),
    sg.Combo([1,2,3,4,5,6,7,8,9,10], size = (13,1), default_value = 1)],
    [sg.Text("Web address"),
    sg.In(size=(50, 4), key="-address-"),
    sg.Push(),
    sg.Text("Date"),
    sg.In(default_text = date,size=(15, 2), key="-date-")],
    [sg.Text("User"),
    sg.Combo(users),
    sg.Push(),
    sg.Text("Req #"),
    sg.In(size=(15, 4), key="-req-"),
    sg.Push(),
    sg.Text("PO #"),
    sg.In(size=(15, 4), key="-po-")
    ],
    [sg.Text("Location"),
    sg.Combo(locations, key = "-location-"),
    sg.Push(),
    sg.Text("Status"),
    sg.Combo(statuses, key = "-status-", default_value = statuses[0]),
    sg.Button("Update")],
    sg.Text("Notes"),
    sg.Multiline(size = (40,5), default_text = wd, key = "-notes-"),
]
# Third column shows the item image and the procedurally generated description
main_font=("Arial bold", 11)
inv_header = [
    [sg.Text("Date", pad = (0,0), size = (15,1), justification = 'c'),
    sg.Text("Product Name", pad = (0,0), size = (15,1), justification = 'c'),
    sg.Text("Company", pad = (0,0), size = (15,1), justification = 'c'),
    sg.Text("Req #", pad = (0,0), size = (15,1), justification = 'c'),
    sg.Text("PO #", pad = (0,0), size = (15,1), justification = 'c'),
    sg.Text("User", pad = (0,0), size = (15,1), justification = 'c'),
    sg.Text("Status", pad = (0,0), size = (15,1), justification = 'c')]
]

for row in range(0,10):
    current_row = [
        sg.Input(size = (15,1), pad = (0,0), key = (row,0)),
        sg.Input(size = (15,1), pad = (0,0), key = (row,0)),
        sg.Input(size = (15,1), pad = (0,0), key = (row,0)),
        sg.Input(size = (15,1), pad = (0,0), key = (row,0)),
        sg.Input(size = (15,1), pad = (0,0), key = (row,0)),
        sg.Input(size = (15,1), pad = (0,0), key = (row,0)),
        sg.Input(size = (15,1), pad = (0,0), key = (row,0)),
    ]
    inv_header.append(current_row)

layout=[
    material_entry_column,
    [sg.Text("")],
    inv_header,
    [sg.Button("Previous", key = "-previous-"),
    sg.Button("Next", key = "-next-")],
    [sg.Button("Search"),
    sg.Input("", key="-search-"),
    sg.Push(),
    sg.Button("Sort by"),
    sg.Combo(log_header),
    ]
]



#-------------------------------------------------------------------------------
# Opens the inventory csv as a dataframe or creates a new one
if ".inventory.csv" in os.listdir():
    df = pd.read_csv(".inventory.csv")
    #print("Found it")
else:
    tempDF = {"Order_id": [],
                "Date": [],
                "Product name" : [],
                "Company" : [],
                "Req #" : [],
                "PO #" : [],
                "User" : [],
                "Status" : [],
                "Catalog number" : [],
                "Description" : [],
                "Number" : [],
                "Location" : [],
                "Notes" : []
    }
    df = pd.DataFrame(data = tempDF)
    #print("Made it!")
#print(df.loc[:,"Order_id"])

#-------------------------------------------------------------------------------
window=sg.Window("Lab Inventory System", layout)

# This while true loop is where all the magic happens
while True:
    # events and values are read as the first thing
    event, values = window.read()
    get_slice(df, 0, window)
    # If the exit button is pressed or the window is otherwise closed, the loop breaks
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    elif event == "Update" and values["-status-"] == "Received" and values["-location-"] == "":
        popup_location()


window.close()
df = df.sort_values("Order_id", ascending = False)
df.to_csv(".inventory.csv", index = False)
