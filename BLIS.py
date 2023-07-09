#!/usr/bin/env python

# Import required packages
import pathlib
import PySimpleGUI as sg
import os.path
from datetime import date
import copy
import csv
import pandas as pd

sg.theme('DarkGreen')
#-------------------------------------------------------------------------------

def sort_slice(button, asendit, dataframe, starting, rick):
    start_slice = 0
    global asendee
    if rick:
        asendee = not asendit
    else:
        asendee = asendit
    dataframe = dataframe.sort_values(by=[button], ascending=ascend)
    global sub_dataframe
    sub_dataframe = dataframe.copy()
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
# Define starting variables
description="Random inventory object"

wd = os.getcwd()

# Opens the inventory csv as a dataframe or creates a new one
if ".inventory.csv" in os.listdir():
    df = pd.read_csv(".inventory.csv")
    #print("Found it")
    #print(len(df["Order_id"]))

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

if ".lock_file" in os.listdir():
    locked_file = True
else:
    locked_file = False
    with open('.lock_file', 'w') as f:
        f.write("File locked")

sub_df = df.copy()

users = list(df["User"].unique())
firt_user = 0

u_statuses = list(df["Status"].unique())
first_status = 0

companies = list(df["Company"].unique())

if len(df["Order_id"]) > 0:
    new_order_id = max(df["Order_id"])+1
else:
    new_order_id = 1

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

locations = list(df["Location"].unique())

date = date.today()
the_order = 0
ascend = True

#-------------------------------------------------------------------------------
material_entry_column = [
    [sg.Text("Product name"),
    sg.In(size=(49, 2), key="-name-"),
    sg.Push(),
    sg.Text("Company"),
    sg.Combo(companies, size=(15, 5), key="-company-"),
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
    sg.Combo(users, size = (20, 1), key = "-user-"),
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
    sg.Button("Update"),],
    sg.Text("Notes"),
    sg.Multiline(size = (90,5), default_text = "", key = "-notes-"),
    sg.Push(),
    sg.Button("Submit"),
]
# Third column shows the item image and the procedurally generated description
main_font=("Arial bold", 11)
inv_header = [
    [sg.Push(),
    sg.Push(),
    sg.Push(),
    sg.Button("Date", pad = (0,0), size = (12,1), key="-date_button-"),
    sg.Push(),
    sg.Button("Product Name", pad = (0,0), size = (12,1),  key="-product_button-"),
    sg.Push(),
    sg.Button("Company", pad = (0,0), size = (12,1),  key="-company_button-"),
    sg.Push(),
    sg.Button("Price", pad = (0,0), size = (12,1),  key="-price_button-"),
    sg.Push(),
    sg.Button("Req #", pad = (0,0), size = (12,1),  key="-req_button-"),
    sg.Push(),
    sg.Button("PO #", pad = (0,0), size = (12,1),  key="-po_button-"),
    sg.Push(),
    sg.Button("User", pad = (0,0), size = (12,1),  key="-user_button-"),
    sg.Push(),
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
if locked_file:
    layout=[[
    sg.Text("BLIS has detected a locked file, suggesting another instance is running from this directory. \n Please close all other instances before running BLIS to avoid overwriting other members' changes."),
    ], [sg.Push(), sg.Button("OK"), sg.Push()],
    ]
    window = sg.Window("Select a Location", layout = layout)
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            window.close()
            del window
        elif event == "OK":
            #return values2["-location2-"]
            window.close()


else:
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

        # If a row radial button is pressed, its information is loaded into the lines
        elif event.startswith("R") and event != "Reorder":
            bingo = int(event[1:])
            try:
                the_order = sub_df.iloc[bingo+start_slice]["Order_id"]
                #print(sub_df.loc[sub_df["Order_id"] == the_order])
                window["-date-"].update(sub_df.iloc[bingo+start_slice]["Date"])
                window["-name-"].update(sub_df.iloc[bingo+start_slice]["Product Name"])
                window["-user-"].update(sub_df.iloc[bingo+start_slice]["User"])
                window["-company-"].update(sub_df.iloc[bingo+start_slice]["Company"])
                window["-catalog-"].update(sub_df.iloc[bingo+start_slice]["Catalog number"])
                window["-desc-"].update(sub_df.iloc[bingo+start_slice]["Description"])
                window["-unit_price-"].update(sub_df.iloc[bingo+start_slice]["Unit price"])
                window["-unit_number-"].update(sub_df.iloc[bingo+start_slice]["Number"])
                window["-total_price-"].update(sub_df.iloc[bingo+start_slice]["Total price"])
                window["-req-"].update(sub_df.iloc[bingo+start_slice]["Req #"])
                window["-po-"].update(sub_df.iloc[bingo+start_slice]["PO #"])
                window["-status-"].update(sub_df.iloc[bingo+start_slice]["Status"])
                window["-location-"].update(sub_df.iloc[bingo+start_slice]["Location"])
                window["-notes-"].update(sub_df.iloc[bingo+start_slice]["Notes"])
                window["-address-"].update(sub_df.iloc[bingo+start_slice]["Web address"])
                window["-orderID-"].update(sub_df.iloc[bingo+start_slice]["Order_id"])
            except:
                pass

        # Clears the fields for a new order
        elif event == "New":
            #print("Newing")
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

        # Updates values
        elif event == "Update":
            new_price = int(values["-unit_number-"])*float(values["-unit_price-"])
            new_price_str = str(round(new_price, 2))
            window["-total_price-"].update(new_price_str)

            df.loc[df.Order_id == int(values["-orderID-"]), "Date"] = values["-date-"]
            df.loc[df.Order_id == int(values["-orderID-"]), "Product Name"] = values["-name-"]
            df.loc[df.Order_id == int(values["-orderID-"]), "Company"] = values["-company-"]
            df.loc[df.Order_id == int(values["-orderID-"]), "Number"] = values["-unit_number-"]
            df.loc[df.Order_id == int(values["-orderID-"]), "Unit price"] = values["-unit_price-"]
            df.loc[df.Order_id == int(values["-orderID-"]), "Total price"] = values["-total_price-"]
            df.loc[df.Order_id == int(values["-orderID-"]), "Req #"] = values["-req-"]
            df.loc[df.Order_id == int(values["-orderID-"]), "PO #"] = values["-po-"]
            df.loc[df.Order_id == int(values["-orderID-"]), "User"] = values["-user-"]
            df.loc[df.Order_id == int(values["-orderID-"]), "Status"] = values["-status-"]
            df.loc[df.Order_id == int(values["-orderID-"]), "Catalog number"] = values["-catalog-"]
            df.loc[df.Order_id == int(values["-orderID-"]), "Description"] = values["-desc-"]
            df.loc[df.Order_id == int(values["-orderID-"]), "Location"] = values["-location-"]
            df.loc[df.Order_id == int(values["-orderID-"]), "Notes"] = values["-notes-"]
            df.loc[df.Order_id == int(values["-orderID-"]), "Web address"] = values["-address-"]
            sub_df = df.copy()
            for row in range(0,10):
                try:
                    window[(row, 0)].update(sub_df.iloc[row+start_slice]["Date"])
                    window[(row, 1)].update(sub_df.iloc[row+start_slice]["Product Name"])
                    window[(row, 2)].update(sub_df.iloc[row+start_slice]["Company"])
                    window[(row, 3)].update(sub_df.iloc[row+start_slice]["Total price"])
                    window[(row, 4)].update(sub_df.iloc[row+start_slice]["Req #"])
                    window[(row, 5)].update(sub_df.iloc[row+start_slice]["PO #"])
                    window[(row, 6)].update(sub_df.iloc[row+start_slice]["User"])
                    window[(row, 7)].update(sub_df.iloc[row+start_slice]["Status"])
                except:
                    window[(row, 0)].update("")
                    window[(row, 1)].update("")
                    window[(row, 2)].update("")
                    window[(row, 3)].update("")
                    window[(row, 4)].update("")
                    window[(row, 5)].update("")
                    window[(row, 6)].update("")
                    window[(row, 7)].update("")

        # Deletes the current selected order
        elif event == "Delete" and "the_order" in locals():
            df = df[df.Order_id != the_order]
            sub_df = df.copy()
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
            for row in range(0,10):
                try:
                    window[(row, 0)].update(sub_df.iloc[row+start_slice]["Date"])
                    window[(row, 1)].update(sub_df.iloc[row+start_slice]["Product Name"])
                    window[(row, 2)].update(sub_df.iloc[row+start_slice]["Company"])
                    window[(row, 3)].update(sub_df.iloc[row+start_slice]["Total price"])
                    window[(row, 4)].update(sub_df.iloc[row+start_slice]["Req #"])
                    window[(row, 5)].update(sub_df.iloc[row+start_slice]["PO #"])
                    window[(row, 6)].update(sub_df.iloc[row+start_slice]["User"])
                    window[(row, 7)].update(sub_df.iloc[row+start_slice]["Status"])
                except:
                    window[(row, 0)].update("")
                    window[(row, 1)].update("")
                    window[(row, 2)].update("")
                    window[(row, 3)].update("")
                    window[(row, 4)].update("")
                    window[(row, 5)].update("")
                    window[(row, 6)].update("")
                    window[(row, 7)].update("")
            new_order_id = max(sub_df["Order_id"])+1
            window["-orderID-"].update(new_order_id)

        # Adds new order to the stack
        elif event == "Submit" and len(values["-name-"]) > 1:
            start_slice = 0
            new_price = int(values["-unit_number-"])*float(values["-unit_price-"])
            new_price_str = str(round(new_price, 2))
            window["-total_price-"].update(new_price_str)
            new_order = pd.DataFrame({"Order_id": [new_order_id],
            "Date": [values["-date-"]],
            "Product Name": [values["-name-"]],
            "Company": [values["-company-"]],
            "Number": [values["-unit_number-"]],
            "Unit price": [values["-unit_price-"]],
            "Total price": [values["-total_price-"]],
            "Req #": [values["-req-"]],
            "PO #": [values["-po-"]],
            "User": [values["-user-"]],
            "Status": [values["-status-"]],
            "Catalog number": [values["-catalog-"]],
            "Description": [values["-desc-"]],
            "Location": [values["-location-"]],
            "Notes": [values["-notes-"]],
            "Web address": [values["-address-"]]})

            df=pd.concat([new_order, df])
            sub_df = df.copy()
            #sort_slice("Date", False, sub_df, 0, False)
            for row in range(0,10):
                try:
                    window[(row, 0)].update(sub_df.iloc[row]["Date"])
                    window[(row, 1)].update(sub_df.iloc[row]["Product Name"])
                    window[(row, 2)].update(sub_df.iloc[row]["Company"])
                    window[(row, 3)].update(sub_df.iloc[row]["Total price"])
                    window[(row, 4)].update(sub_df.iloc[row]["Req #"])
                    window[(row, 5)].update(sub_df.iloc[row]["PO #"])
                    window[(row, 6)].update(sub_df.iloc[row]["User"])
                    window[(row, 7)].update(sub_df.iloc[row]["Status"])
                except:
                    window[(row, 0)].update("")
                    window[(row, 1)].update("")
                    window[(row, 2)].update("")
                    window[(row, 3)].update("")
                    window[(row, 4)].update("")
                    window[(row, 5)].update("")
                    window[(row, 6)].update("")
                    window[(row, 7)].update("")

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

        # Searches for matches in product name
        elif event == "Search":
            start_slice = 0

            jimmy = values["-search-"].lower()
            sub_df = df[df["Product Name"].str.lower().str.contains(jimmy)].copy()

            for row in range(0,10):
                try:
                    window[(row, 0)].update(sub_df.iloc[row]["Date"])
                    window[(row, 1)].update(sub_df.iloc[row]["Product Name"])
                    window[(row, 2)].update(sub_df.iloc[row]["Company"])
                    window[(row, 3)].update(sub_df.iloc[row]["Total price"])
                    window[(row, 4)].update(sub_df.iloc[row]["Req #"])
                    window[(row, 5)].update(sub_df.iloc[row]["PO #"])
                    window[(row, 6)].update(sub_df.iloc[row]["User"])
                    window[(row, 7)].update(sub_df.iloc[row]["Status"])
                except:
                    window[(row, 0)].update("")
                    window[(row, 1)].update("")
                    window[(row, 2)].update("")
                    window[(row, 3)].update("")
                    window[(row, 4)].update("")
                    window[(row, 5)].update("")
                    window[(row, 6)].update("")
                    window[(row, 7)].update("")

        elif event == "-date_button-":
            buttoni = "Date"
            start_slice = 0
            sort_slice(buttoni, ascend, sub_df, 0, True)
            sub_df = sub_dataframe
            ascend = asendee

        elif event == "-product_button-":
            buttoni = "Product Name"
            start_slice = 0
            sort_slice(buttoni, ascend, sub_df, 0, True)
            ascend = asendee
            sub_df = sub_dataframe

        elif event == "-company_button-":
            start_slice = 0
            buttoni = "Company"
            sort_slice(buttoni, ascend, sub_df, 0, True)
            ascend = asendee
            sub_df = sub_dataframe

        elif event == "-price_button-":
            start_slice = 0
            buttoni = "Total price"
            sort_slice(buttoni, ascend, sub_df, 0, True)
            ascend = asendee
            sub_df = sub_dataframe

        elif event == "-req_button-":
            start_slice = 0
            buttoni = "Req #"
            sort_slice(buttoni, ascend, sub_df, 0, True)
            ascend = asendee
            sub_df = sub_dataframe

        elif event == "-po_button-":
            start_slice = 0
            buttoni = "PO #"
            sort_slice(buttoni, ascend, sub_df, 0, True)
            ascend = asendee
            sub_df = sub_dataframe

        elif event == "-user_button-":
            start_slice = 0
            buttoni = "User"
            sub_df = df[df["User"].str.contains(users[firt_user])].copy()
            if firt_user == len(users)-1:
                firt_user = 0
            else:
                firt_user+=1
            sort_slice(buttoni, ascend, sub_df, 0, True)
            ascend = asendee
            sub_df = sub_dataframe

        elif event == "-status_button-":
            start_slice = 0
            buttoni = "Status"
            sub_df = df[df["Status"].str.contains(u_statuses[first_status])].copy()
            if first_status == len(u_statuses)-1:
                first_status = 0
            else:
                first_status+=1

            sort_slice(buttoni, ascend, sub_df, 0, True)
            ascend = asendee
            sub_df = sub_dataframe

        elif event == "-next-" and len(sub_df) > start_slice+10:
            start_slice += 10
            #print(start_slice)
            for row in range(0,10):
                try:
                    window[(row, 0)].update(sub_df.iloc[row+start_slice]["Date"])
                    window[(row, 1)].update(sub_df.iloc[row+start_slice]["Product Name"])
                    window[(row, 2)].update(sub_df.iloc[row+start_slice]["Company"])
                    window[(row, 3)].update(sub_df.iloc[row+start_slice]["Total price"])
                    window[(row, 4)].update(sub_df.iloc[row+start_slice]["Req #"])
                    window[(row, 5)].update(sub_df.iloc[row+start_slice]["PO #"])
                    window[(row, 6)].update(sub_df.iloc[row+start_slice]["User"])
                    window[(row, 7)].update(sub_df.iloc[row+start_slice]["Status"])
                except:
                    window[(row, 0)].update("")
                    window[(row, 1)].update("")
                    window[(row, 2)].update("")
                    window[(row, 3)].update("")
                    window[(row, 4)].update("")
                    window[(row, 5)].update("")
                    window[(row, 6)].update("")
                    window[(row, 7)].update("")


        elif event == "-previous-" and start_slice > 0:
            start_slice -= 10
            for row in range(0,10):
                try:
                    window[(row, 0)].update(sub_df.iloc[row+start_slice]["Date"])
                    window[(row, 1)].update(sub_df.iloc[row+start_slice]["Product Name"])
                    window[(row, 2)].update(sub_df.iloc[row+start_slice]["Company"])
                    window[(row, 3)].update(sub_df.iloc[row+start_slice]["Total price"])
                    window[(row, 4)].update(sub_df.iloc[row+start_slice]["Req #"])
                    window[(row, 5)].update(sub_df.iloc[row+start_slice]["PO #"])
                    window[(row, 6)].update(sub_df.iloc[row+start_slice]["User"])
                    window[(row, 7)].update(sub_df.iloc[row+start_slice]["Status"])
                except:
                    window[(row, 0)].update("")
                    window[(row, 1)].update("")
                    window[(row, 2)].update("")
                    window[(row, 3)].update("")
                    window[(row, 4)].update("")
                    window[(row, 5)].update("")
                    window[(row, 6)].update("")
                    window[(row, 7)].update("")


    window.close()

    if locked_file != True:
        os.remove(".lock_file")
        df = df.sort_values("Date", ascending = False)
        df.to_csv(".inventory.csv", index = False)
