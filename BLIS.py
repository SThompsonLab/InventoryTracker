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

# Opens the inventory csv as a dataframe or creates a new one
if ".inventory.csv" in os.listdir():
    df = pd.read_csv(".inventory.csv")
    #print("Found it")
else:
    tempDF = {"Order_id": [],
                "Date": [],
                "Product Name" : [],
                "Company" : [],
                "Number" : [],
                "Unit price": [],
                "Total price" : [],
                "Req #" : [],
                "PO #" : [],
                "User" : [],
                "Status" : [],
                "Catalog number" : [],
                "Description" : [],
                "Location" : [],
                "Notes" : [],
                "Web address" : []
    }
    df = pd.DataFrame(data = tempDF)

sub_df = df

users = list(df["User"].unique())
companies = list(df["Company"].unique())
new_order_id = max(df["Order_id"])+1

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
the_order = 0
ascend = True

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


def sort_slice(button, asendit, dataframe, starting):
    start_slice = 0
    global asendee
    asendee = not asendit
    dataframe = dataframe.sort_values(by=[button], ascending=ascend)
    global sub_dataframe
    sub_dataframe = dataframe
    for row in range(0,10):
        try:
            window[(row, 0)].update(dataframe.iloc[starting]["Date"])
            window[(row, 1)].update(dataframe.iloc[starting]["Product Name"])
            window[(row, 2)].update(dataframe.iloc[starting]["Company"])
            window[(row, 3)].update(dataframe.iloc[starting]["Total price"])
            window[(row, 4)].update(dataframe.iloc[starting]["Req #"])
            window[(row, 5)].update(dataframe.iloc[starting]["PO #"])
            window[(row, 6)].update(dataframe.iloc[starting]["User"])
            window[(row, 7)].update(dataframe.iloc[starting]["Status"])
        except:
            window[(row, 0)].update("")
            window[(row, 1)].update("")
            window[(row, 2)].update("")
            window[(row, 3)].update("")
            window[(row, 4)].update("")
            window[(row, 5)].update("")
            window[(row, 6)].update("")
            window[(row, 7)].update("")
        starting+=1

#-------------------------------------------------------------------------------
material_entry_column = [
    [sg.Text("Product name"),
    sg.In(size=(20, 2), key="-name-"),
    sg.Push(),
    sg.Text("Company"),
    sg.Combo(companies, size=(15, 2), key="-company-"),
    sg.Push(),
    sg.Text("Catalog number"),
    sg.In(size=(15, 2), key="-catalog-")],
    [sg.Text("Description"),
    sg.In(size=(50, 4), key="-desc-"),
    sg.Push(),
    sg.Text("Unit price ($)"),
    sg.In(default_text = "0.00", size=(10,1), key = "-unit_price-"),
    sg.Push(),
    sg.Text("Number"),
    sg.Combo([1,2,3,4,5,6,7,8,9,10], size = (13,1), default_value = 1, key = "-unit_number-")],
    [sg.Text("Web address"),
    sg.In(size=(50, 4), key="-address-"),
    sg.Push(),
    sg.Text("Total"),
    sg.In(default_text = "$0.00", size = (10,1), key = "-total_price-", disabled = True),
    sg.Push(),
    sg.Text("Date"),
    sg.In(default_text = date,size=(15, 2), key="-date-")],
    [sg.Text("User"),
    sg.Combo(users, size = (10, 1), key = "-user-"),
    sg.Push(),
    sg.Push(),
    sg.Push(),
    sg.Text("Req #"),
    sg.In(size=(15, 4), key="-req-"),
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
    sg.Push(),
]
# Third column shows the item image and the procedurally generated description
main_font=("Arial bold", 11)
inv_header = [
    [sg.Push(),
    sg.Button("Date", pad = (0,0), size = (12,1), key="-date_button-"),
    sg.Button("Product Name", pad = (0,0), size = (12,1),  key="-product_button-"),
    sg.Button("Company", pad = (0,0), size = (12,1),  key="-company_button-"),
    sg.Button("Price", pad = (0,0), size = (12,1),  key="-price_button-"),
    sg.Button("Req #", pad = (0,0), size = (12,1),  key="-req_button-"),
    sg.Button("PO #", pad = (0,0), size = (12,1),  key="-po_button-"),
    sg.Button("User", pad = (0,0), size = (12,1),  key="-user_button-"),
    sg.Button("Status", pad = (0,0), size = (12,1),  key="-status_button-")],

]

for row in range(0,10):
    row_id = "R"+str(row)
    try:
        current_row = [
            sg.Radio("", group_id="Radio1", enable_events = True, key = row_id),
            sg.Input(default_text = sub_df.iloc[row]["Date"],size = (15,1), pad = (0,0), key = (row,0), disabled = True),
            sg.Input(default_text = sub_df.iloc[row]["Product Name"],size = (15,1), pad = (0,0), key = (row,1), disabled = True),
            sg.Input(default_text = sub_df.iloc[row]["Company"],size = (15,1), pad = (0,0), key = (row,2), disabled = True),
            sg.Input(default_text = sub_df.iloc[row]["Total price"],size = (15,1), pad = (0,0), key = (row,3), disabled = True),
            sg.Input(default_text = sub_df.iloc[row]["Req #"],size = (15,1), pad = (0,0), key = (row,4), disabled = True),
            sg.Input(default_text = sub_df.iloc[row]["PO #"],size = (15,1), pad = (0,0), key = (row,5), disabled = True),
            sg.Input(default_text = sub_df.iloc[row]["User"],size = (15,1), pad = (0,0), key = (row,6), disabled = True),
            sg.Input(default_text = sub_df.iloc[row]["Status"],size = (15,1), pad = (0,0), key = (row,7), disabled = True),
            ]
    except:
        current_row = [
            sg.Radio("", group_id="Radio1"),
            sg.Input(size = (15,1), pad = (0,0), key = (row,0), disabled = True),
            sg.Input(size = (15,1), pad = (0,0), key = (row,1), disabled = True),
            sg.Input(size = (15,1), pad = (0,0), key = (row,2), disabled = True),
            sg.Input(size = (15,1), pad = (0,0), key = (row,3), disabled = True),
            sg.Input(size = (15,1), pad = (0,0), key = (row,4), disabled = True),
            sg.Input(size = (15,1), pad = (0,0), key = (row,5), disabled = True),
            sg.Input(size = (15,1), pad = (0,0), key = (row,6), disabled = True),
            sg.Input(size = (15,1), pad = (0,0), key = (row,7), disabled = True),
            ]
    inv_header.append(current_row)

layout=[
    material_entry_column,
    [sg.Button("Search"),
    sg.Input("", key="-search-"),
    sg.Push(),
    sg.Button("New"),
    sg.Button("Add"),
    sg.Button("Reorder"),
    sg.Push(),
    sg.Text("Order#"),
    sg.Input(new_order_id, size = (10,1), disabled = True, key = "-orderID-")],
    inv_header,
    [sg.Button("Previous", key = "-previous-"),
    sg.Button("Next", key = "-next-"),
    sg.Push(),
    sg.Button("Delete"),
    ]
]


#-------------------------------------------------------------------------------
window=sg.Window("Lab Inventory System", layout)
start_slice = 0
ascend = True
buttoni = "Date"

# This while true loop is where all the magic happens
while True:
    # events and values are read as the first thing
    event, values = window.read()

    # If the exit button is pressed or the window is otherwise closed, the loop breaks
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    elif event == "Update" and values["-status-"] == "Received" and values["-location-"] == "":
        popup_location()

    elif event == "Update":
        try:
            new_price = int(values["-unit_number-"])*float(values["-unit_price-"])
            new_price_str = str(round(new_price, 2))
            window["-total_price-"].update(new_price_str)
        except:
            pass

    elif event.startswith("R"):
        bingo = int(event[1:])
        try:
            the_order = sub_df.iloc[bingo]["Order_id"]
            #print(sub_df.loc[sub_df["Order_id"] == the_order])
            window["-date-"].update(sub_df.iloc[bingo]["Date"])
            window["-name-"].update(sub_df.iloc[bingo]["Product Name"])
            window["-user-"].update(sub_df.iloc[bingo]["User"])
            window["-company-"].update(sub_df.iloc[bingo]["Company"])
            window["-catalog-"].update(sub_df.iloc[bingo]["Catalog number"])
            window["-desc-"].update(sub_df.iloc[bingo]["Description"])
            window["-unit_price-"].update(sub_df.iloc[bingo]["Unit price"])
            window["-unit_number-"].update(sub_df.iloc[bingo]["Number"])
            window["-total_price-"].update(sub_df.iloc[bingo]["Total price"])
            window["-req-"].update(sub_df.iloc[bingo]["Req #"])
            window["-po-"].update(sub_df.iloc[bingo]["PO #"])
            window["-status-"].update(sub_df.iloc[bingo]["Status"])
            window["-location-"].update(sub_df.iloc[bingo]["Location"])
            window["-notes-"].update(sub_df.iloc[bingo]["Notes"])
            window["-address-"].update(sub_df.iloc[bingo]["Web address"])
            window["-orderID-"].update(sub_df.iloc[bingo]["Order_id"])
        except:
            pass

    elif event == "New":
        window["-date-"].update(date.today())
        window["-name-"].update("")
        window["-user-"].update("")
        window["-company-"].update("")
        window["-catalog-"].update("")
        window["-desc-"].update("")
        window["-unit_price-"].update(0.00)
        window["-unit_number-"].update(1)
        window["-total_price-"].update(0.00)
        window["-req-"].update("")
        window["-po-"].update("")
        window["-status-"].update("Submitted")
        window["-location-"].update("")
        window["-notes-"].update("")
        window["-address-"].update("")
        window["-orderID-"].update(new_order_id)

    elif event == "Delete" and "the_order" in locals():
        df = df[df.Order_id != the_order]
        sub_df = df
        window["-date-"].update(date.today())
        window["-name-"].update("")
        window["-user-"].update("")
        window["-company-"].update("")
        window["-catalog-"].update("")
        window["-desc-"].update("")
        window["-unit_price-"].update(0.00)
        window["-unit_number-"].update(1)
        window["-total_price-"].update(0.00)
        window["-req-"].update("")
        window["-po-"].update("")
        window["-status-"].update("Submitted")
        window["-location-"].update("")
        window["-notes-"].update("")
        window["-address-"].update("")
        window["-orderID-"].update(new_order_id)

    elif event == "Add":
        new_price = int(values["-unit_number-"])*float(values["-unit_price-"])
        new_price_str = str(round(new_price, 2))
        window["-total_price-"].update(new_price_str)
        new_order = [new_order_id,
        values["-date-"],
        values["-name-"],
        values["-company-"],
        values["-unit_number-"],
        values["-unit_price-"],
        values["-total_price-"],
        values["-req-"],
        values["-po-"],
        values["-user-"],
        values["-status-"],
        values["-catalog-"],
        values["-desc-"],
        values["-location-"],
        values["-notes-"],
        values["-address-"]
        ]
        df.loc[len(df)] = new_order
        sub_df = df
        new_order_id = max(df["Order_id"])+1
        window["-date-"].update(date.today())
        window["-name-"].update("")
        window["-user-"].update("")
        window["-company-"].update("")
        window["-catalog-"].update("")
        window["-desc-"].update("")
        window["-unit_price-"].update(0.00)
        window["-unit_number-"].update(1)
        window["-total_price-"].update(0.00)
        window["-req-"].update("")
        window["-po-"].update("")
        window["-status-"].update("Submitted")
        window["-location-"].update("")
        window["-notes-"].update("")
        window["-address-"].update("")
        window["-orderID-"].update(new_order_id)

    elif event == "Search":
        #print(values["-search-"])
        sub_df = df[df["Product Name"].str.contains(values["-search-"])]
        #print(sub_df)
        sort_slice("Date", ascend, sub_df, 0)

    elif event == "-date_button-":
        buttoni = "Date"
        sort_slice(buttoni, ascend, sub_df, 0)
        sub_df = sub_dataframe
        ascend = asendee

    elif event == "-product_button-":
        buttoni = "Product Name"
        sort_slice(buttoni, ascend, sub_df, 0)
        ascend = asendee
        sub_df = sub_dataframe

    elif event == "-company_button-":
        buttoni = "Company"
        sort_slice(buttoni, ascend, sub_df, 0)
        ascend = asendee
        sub_df = sub_dataframe

    elif event == "-price_button-":
        buttoni = "Total price"
        sort_slice(buttoni, ascend, sub_df, 0)
        ascend = asendee
        sub_df = sub_dataframe

    elif event == "-req_button-":
        buttoni = "Req #"
        sort_slice(buttoni, ascend, sub_df, 0)
        ascend = asendee
        sub_df = sub_dataframe

    elif event == "-po_button-":
        buttoni = "PO #"
        sort_slice(buttoni, ascend, sub_df, 0)
        ascend = asendee
        sub_df = sub_dataframe

    elif event == "-user_button-":
        buttoni = "User"
        sort_slice(buttoni, ascend, sub_df, 0)
        ascend = asendee
        sub_df = sub_dataframe

    elif event == "-status_button-":
        buttoni = "Status"
        sort_slice(buttoni, ascend, sub_df, 0)
        ascend = asendee
        sub_df = sub_dataframe

    elif event == "-next-" and len(sub_df) > start_slice+10:
        start_slice += 10
        sort_slice(buttoni, ascend, sub_df, start_slice)
        sub_df = sub_dataframe

    elif event == "-previous-" and start_slice > 0:
        start_slice -= 10
        sort_slice(buttoni, ascend, sub_df, start_slice)
        sub_df = sub_dataframe


window.close()
df = df.sort_values("Order_id", ascending = False)
df.to_csv(".inventory.csv", index = False)
