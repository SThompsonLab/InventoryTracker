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

def popup_select(users_list):
    text_choice="Select a user for this session"
    layout = [[sg.Text(text_choice)],
    [sg.Combo(users_list,key='_LIST_',size=(15,len(users_list))),sg.OK()]]
    window3 = sg.Window('Select One',layout=layout)
    event, values = window3.read()
    window3.close()
    del window3
    if len(values['_LIST_']):
        return values['_LIST_']
    else:
        return "Unknown"


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
date = date.today()
the_order = 0
ascend = True
wd = os.getcwd()

# Opens the inventory csv as a dataframe or creates a new one
if ".inventory.csv" in os.listdir():
    df = pd.read_csv(".inventory.csv")
    #print("Found it")
    #print(len(df["Order_id"]))

else:
    tempDF = {"Order_id": [1],
                "Date": [date],
                "Product Name" : [""],
                "Company" : [""],
                "Number" : [1],
                "Unit price": [""],
                "Total price" : [""],
                "Req #" : [""],
                "PO #" : [""],
                "User" : [""],
                "Status" : [""],
                "Catalog number" : [""],
                "Description" : [""],
                "Location" : [""],
                "Notes" : [""],
                "Web address" : [""],
                "Project": ["General"]
    }
    df = pd.DataFrame(data = tempDF)

if ".lock_file" in os.listdir():
    locked_file = True
else:
    locked_file = False


sub_df = df.copy()

users = list(df["User"].unique())
firt_user = 0

u_statuses = list(df["Status"].unique())
first_status = 0

projects = list(df["Project"].unique())

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


#-------------------------------------------------------------------------------

material_entry_column = [
    [sg.Text("Product name"),
    sg.In(size=(49, 2), key="-name-", default_text = df.iloc[0]["Product Name"]),
    sg.Push(),
    sg.Text("Company"),
    sg.Combo(companies, size=(15, 5), key="-company-", default_value = df.iloc[0]["Company"]),
    sg.Push(),
    sg.Text("Catalog number"),
    sg.In(size=(15, 2), key="-catalog-", default_text = df.iloc[0]["Catalog number"]),],
    [sg.Text("Description"),
    sg.In(size=(50, 4), key="-desc-", default_text = df.iloc[0]["Description"]),
    sg.Push(),
    sg.Text("Unit price ($)"),
    sg.In(size=(10,1), key = "-unit_price-", default_text = df.iloc[0]["Unit price"]),
    sg.Push(),
    sg.Text("Number"),
    sg.Combo([1,2,3,4,5,6,7,8,9,10], size = (13,1), default_value = df.iloc[0]["Number"], key = "-unit_number-")],
    [sg.Text("Web address"),
    sg.In(size=(50, 4), key="-address-", default_text = df.iloc[0]["Web address"]),
    sg.Push(),
    sg.Text("Total"),
    sg.In(size = (10,1), key = "-total_price-", disabled = True, default_text = df.iloc[0]["Total price"]),
    sg.Push(),
    sg.Text("Date"),
    sg.In(size=(15, 2), key="-date-", default_text = df.iloc[0]["Date"]),],
    [sg.Text("User"),
    sg.Combo(users, size = (20, 1), key = "-user-", default_value = df.iloc[0]["User"]),
    sg.Push(),
    sg.Text("Project"),
    sg.Combo(projects, size = (20,1), key = "-project-", default_value = df.iloc[0]["Project"]),
    sg.Push(),
    sg.Text("Req #"),
    sg.In(size=(15, 4), key="-req-", default_text = df.iloc[0]["Req #"]),
    sg.Text("PO #"),
    sg.In(size=(15, 4), key="-po-", default_text = df.iloc[0]["PO #"])
    ],
    [sg.Text("Location"),
    sg.Combo(locations, key = "-location-", default_value = df.iloc[0]["Location"]),
    sg.Push(),
    sg.Text("Status"),
    sg.Combo(statuses, key = "-status-", default_value = df.iloc[0]["Status"]),
    sg.Button("Update"),],
    sg.Text("Notes"),
    sg.Multiline(size = (90,5), key = "-notes-", default_text=df.iloc[0]["Notes"]),
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
    sg.Input(size = (10,1), disabled = True, key = "-orderID-", default_text = df.iloc[0]["Order_id"]),],
    inv_header,
    [sg.Button("Previous", key = "-previous-"),
    sg.Button("Next", key = "-next-"),
    sg.Push(),
    sg.Button("Delete"),
    ]
]


#-------------------------------------------------------------------------------
if locked_file:
    layout = layout=[[
    sg.Text("BLIS has detected a locked file, suggesting another instance is running from this directory. \n Please close all other instances before running BLIS to avoid overwriting other members' changes."),
    ], [sg.Push(), sg.Button("OK"), sg.Push()],
    ]
    window3 = sg.Window('Select One',layout=layout)
    event, values = window3.read()
    window3.close()
    del window3


else:
    the_current_user = popup_select(users)
    if the_current_user not in users:
        users.append(the_current_user)
    with open('.lock_file', 'w') as f:
        f.write("File locked by "+the_current_user)

    window=sg.Window("BLIS: Basic Lab Inventory System", layout)
    start_slice = 0
    bingo = 0
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
                window["-project-"].update(sub_df.iloc[bingo+start_slice]["Project"])
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
                window["-orderID-"].update(str(sub_df.iloc[bingo+start_slice]["Order_id"]))
            except:
                pass

        # Clears the fields for a new order
        elif event == "New":
            #print("Newing")
            window["-date-"].update(date.today())
            window["-name-"].update(" ")
            window["-user-"].update(the_current_user)
            window["-project-"].update("General")
            window["-company-"].update(" ")
            window["-catalog-"].update(" ")
            window["-desc-"].update(" ")
            window["-unit_price-"].update("0.00")
            window["-unit_number-"].update(1)
            window["-total_price-"].update("0.00")
            window["-req-"].update(" ")
            window["-po-"].update(" ")
            window["-status-"].update("Submitted")
            window["-location-"].update(" ")
            window["-notes-"].update(" ")
            window["-address-"].update(" ")
            window["-orderID-"].update(new_order_id)

        # Updates values
        elif event == "Update":
            try:
                new_price = int(values["-unit_number-"])*float(values["-unit_price-"])
                new_price_str = str(round(new_price, 2))
                window["-total_price-"].update(new_price_str)
                change_log = "\n"

                try:
                    if str(df.loc[df.Order_id == int(values["-orderID-"]), "Date"][0]) != values["-date-"]:
                        change_log += "Date$"
                    if str(df.loc[df.Order_id == int(values["-orderID-"]), "Product Name"][0]) != values["-name-"]:
                        change_log += "Product Name$"
                    if str(df.loc[df.Order_id == int(values["-orderID-"]), "Company"][0]) != values["-company-"]:
                        change_log += "Company$"
                    if str(df.loc[df.Order_id == int(values["-orderID-"]), "Number"][0]) != str(values["-unit_number-"]):
                        change_log += "Number$"
                    if str(df.loc[df.Order_id == int(values["-orderID-"]), "Unit price"][0]) != values["-unit_price-"]:
                        change_log += "Unit price$"
                    if str(df.loc[df.Order_id == int(values["-orderID-"]), "Total price"][0]) != values["-total_price-"]:
                        change_log += "Total price$"
                    if str(df.loc[df.Order_id == int(values["-orderID-"]), "Req #"][0]) != values["-req-"]:
                        change_log += "Req #$"
                    if str(df.loc[df.Order_id == int(values["-orderID-"]), "PO #"][0]) != values["-po-"]:
                        change_log += "PO #$"
                    if str(df.loc[df.Order_id == int(values["-orderID-"]), "User"][0]) != values["-user-"]:
                        change_log += "User$"
                    if str(df.loc[df.Order_id == int(values["-orderID-"]), "Project"][0]) != values["-project-"]:
                        change_log += "Project$"
                    if str(df.loc[df.Order_id == int(values["-orderID-"]), "Status"][0]) != values["-status-"]:
                        change_log += "Status$"
                    if str(df.loc[df.Order_id == int(values["-orderID-"]), "Catalog number"][0]) != values["-catalog-"]:
                        change_log += "Cat #$"
                    if str(df.loc[df.Order_id == int(values["-orderID-"]), "Description"][0]) != values["-desc-"]:
                        change_log += "Description$"
                    if str(df.loc[df.Order_id == int(values["-orderID-"]), "Location"][0]) != values["-location-"]:
                        change_log += "Location$"
                    if str(df.loc[df.Order_id == int(values["-orderID-"]), "Notes"][0]) != values["-notes-"]:
                        change_log += "Notes$"
                    if str(df.loc[df.Order_id == int(values["-orderID-"]), "Web address"][0]) != values["-address-"]:
                        change_log += "Address$"
                except:
                    change_log+= "Something$"

                change_log = change_log.replace("$" , ", ")
                change_log = change_log[0:len(change_log)-2]
                if change_log == "\n":
                    change_log = ""

                df.loc[df.Order_id == int(values["-orderID-"]), "Date"] = values["-date-"]
                df.loc[df.Order_id == int(values["-orderID-"]), "Product Name"] = values["-name-"]
                df.loc[df.Order_id == int(values["-orderID-"]), "Company"] = values["-company-"]
                df.loc[df.Order_id == int(values["-orderID-"]), "Number"] = values["-unit_number-"]
                df.loc[df.Order_id == int(values["-orderID-"]), "Unit price"] = values["-unit_price-"]
                df.loc[df.Order_id == int(values["-orderID-"]), "Total price"] = new_price_str
                df.loc[df.Order_id == int(values["-orderID-"]), "Req #"] = values["-req-"]
                df.loc[df.Order_id == int(values["-orderID-"]), "PO #"] = values["-po-"]
                df.loc[df.Order_id == int(values["-orderID-"]), "User"] = values["-user-"]
                df.loc[df.Order_id == int(values["-orderID-"]), "Project"] = values["-project-"]
                df.loc[df.Order_id == int(values["-orderID-"]), "Status"] = values["-status-"]
                df.loc[df.Order_id == int(values["-orderID-"]), "Catalog number"] = values["-catalog-"]
                df.loc[df.Order_id == int(values["-orderID-"]), "Description"] = values["-desc-"]
                df.loc[df.Order_id == int(values["-orderID-"]), "Location"] = values["-location-"]
                if change_log != "":
                    df.loc[df.Order_id == int(values["-orderID-"]), "Notes"] = values["-notes-"]+change_log+" updated on "+str(date)+" by "+the_current_user
                df.loc[df.Order_id == int(values["-orderID-"]), "Web address"] = values["-address-"]
                sub_df = df.copy()
                window["-notes-"].update(sub_df.iloc[bingo+start_slice]["Notes"])
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
            except:
                pass

        # Deletes the current selected order
        elif event == "Delete" and "the_order" in locals():
            df = df[df.Order_id != the_order]
            sub_df = df.copy()
            window["-date-"].update(date.today())
            window["-name-"].update("")
            window["-user-"].update("")
            window["-project-"].update("")
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
            try:
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
                "Total price": [new_price_str],
                "Req #": [values["-req-"]],
                "PO #": [values["-po-"]],
                "User": [values["-user-"]],
                "Status": [values["-status-"]],
                "Catalog number": [values["-catalog-"]],
                "Description": [values["-desc-"]],
                "Location": [values["-location-"]],
                "Notes": [values["-notes-"]],
                "Web address": [values["-address-"]],
                "Project": [values["-project-"]],})

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
                window["-project-"].update("")
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
            except:
                pass

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
