#------------------------------------------
#BIT502 Assessment 3, Jorj Baigent, 5132617
#------------------------------------------
#------------------------------------------
#IMPORTS
#------------------------------------------
#Imports tkinter and sqlite3
import tkinter as tk
import sqlite3
from tkinter import ttk, messagebox

from colours import FROST_BLUE #Hex code for background colour

#Membership plans and payment plans
from member_options import (
    MEMBERSHIP_PLANS,
    PAYMENT_PLANS
)

#------------------------------------------
#FUNCTIONS
#------------------------------------------

#Configure rows and columns
def config_rows_cols(frame, num_rows, num_cols, row_weight, col_weight):

    for row in range(num_rows):
        frame.rowconfigure(row, weight=row_weight)

    for col in range(num_cols):
        frame.columnconfigure(col, weight=col_weight)


#Creates stat boxes
def create_stat_box(parent, label, value="00"):

    #Creates the box that holds the statistics label and value
    box = ttk.Frame(parent, style="Stats.TFrame")
    box.configure(width=80, height=80)
    box.grid_propagate(False)

    config_rows_cols(box, 2, 1, 1, 1)

    #Widget to hold the label of the stat
    label_widget = ttk.Label(box, text=label, style="StatsLabel.TLabel", anchor="center", justify="center")
    label_widget.grid(row=0, column=0, padx=10, pady=(8, 0), sticky="nsew")


    #Widget to hold the value of the stat
    value_widget = ttk.Label(box, text=value, style="StatsValue.TLabel", anchor="center", justify="center")
    value_widget.grid(row=1, column=0, padx=10, pady=(2, 8), sticky="nsew")
    box.value_label = value_widget

    return box


    
#------------------------------------------
#MAIN FUNCTION
#------------------------------------------
#Creates a statistics screen
def create_statistics_screen(parent, show_screen, main_menu_frame, repository):

    #Creates frame that is returned 
    statistics_frame = tk.Frame(parent, bg=FROST_BLUE)

    #Creates canvas for scrollbar 
    canvas = tk.Canvas(statistics_frame, bg=FROST_BLUE, highlightthickness=0)
    statistics_frame.canvas = canvas

    #Scrollbar code
    scrollbar=ttk.Scrollbar(statistics_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    #Placing canvas and scrollbar
    canvas.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")

    #Configuring columns to eliminate empty space
    statistics_frame.grid_columnconfigure(0, weight=1)
    statistics_frame.grid_rowconfigure(0, weight=1)

    #Creating a frame inside the canvas to place content
    content_frame = tk.Frame(canvas, bg=FROST_BLUE)

    content_frame.columnconfigure(0, weight=1)

    #Creating a window for the content frame
    content_window = canvas.create_window((0,0), window=content_frame, anchor="nw")
    
    #Update the scrollable area when the content changes
    def update_scrollregion(_):
        canvas.configure(scrollregion=canvas.bbox(content_window))
    
    content_frame.bind(
        "<Configure>",
        update_scrollregion
    )
    
    
    #Make content frame the same width as the canvas
    def resize_content(event):
        canvas.itemconfigure(content_window, width=event.width)
    
    canvas.bind(
        "<Configure>",
        resize_content
        )

    #Heading
    title_label = ttk.Label(content_frame, text="Member Statistics", style="Heading.TLabel")
    title_label.grid(row=0, column=0, padx=5, pady=8)


    #Frames to hold different categories of stats
    membership_frame = ttk.LabelFrame(content_frame, text="Memberships:", style="Generic.TLabelframe")
    payment_plan_frame = ttk.LabelFrame(content_frame, text="Payment Plans:", style="Generic.TLabelframe")
    library_card_frame = ttk.LabelFrame(content_frame, text="Library Cards:", style="Generic.TLabelframe")
    extras_frame = ttk.LabelFrame(content_frame, text="Extras:", style="Generic.TLabelframe")
    expected_income_frame = ttk.LabelFrame(content_frame, text="Expected Monthly Income:", style="Primary.TLabelframe")

    #Gridding columns with a for loop
    frames=[membership_frame, payment_plan_frame, library_card_frame, extras_frame, expected_income_frame]
    for row, frame in enumerate(frames):
        frame.grid(row=row + 1, column=0, sticky="ew", padx= 5, pady=5)

    #Configure rows and cols
    config_rows_cols(membership_frame, 1, 4, 1, 1)
    config_rows_cols(payment_plan_frame, 1, 4, 1, 1)
    config_rows_cols(library_card_frame, 1, 4, 1, 1)
    config_rows_cols(extras_frame, 2, 4, 1, 1)


    #Widgets inside membership frame
    membership_types = ["Total:"] + [f"{plan}:" for plan in MEMBERSHIP_PLANS]
    stat_boxes = {}

    #Creating and gridding membership type stat boxes
    for column, label in enumerate(membership_types):
        box = create_stat_box(membership_frame, label)

        box.grid(row=0, column=column, padx=5, pady=5)
        stat_boxes[("membership", label.removesuffix(":"))] = box
        


    #Widgets inside payment plan frame
    payment_plan_types = [f"{plan}:" for plan in PAYMENT_PLANS]

    #Creating and gridding payment plan type stat boxes
    for column, label in enumerate(payment_plan_types):
        box = create_stat_box(payment_plan_frame, label)

        box.grid(row=0, column=column, padx=5, pady=5)
        stat_boxes[("payment", label.removesuffix(":"))] = box
       

    #Widget inside library card frame
    library_box = create_stat_box(library_card_frame, "Library\nCards:")
    library_box.grid(row=0, column=0)
    stat_boxes[("library", "cards")] = library_box
 


    #Widgets inside extras frame
    extras_types= [
        ("Book Rental", "Book\nRental:"),
        ("Private Area Access", "Private Area\nAccess:"),
        ("Monthly Booklet", "Monthly\nBooklet:"),
        ("Online ebook Rental", "Online\neBook\nRental:"),
        ("None", "None:")
    ]

    #Creating and gridding extras types stat boxes
    for index, (key, label) in enumerate(extras_types):

        #Accounts for fifth box - drops down to next row
        row = index // 4
        column = index % 4

        box = create_stat_box(extras_frame, label)
        box.grid(row=row, column=column, padx=5, pady=5)
        stat_boxes[("extras", key)] = box

    #Function to insert rows into income table
    def insert_income_row(type, price, members, income):
        income_table.insert(
            "",
            "end",
            values=(type, f"${price:.2f}", members, f"${income:.2f}")
        )


    #Widgets inside expected income frame

    #Creating income table
    income_columns = ("option", "cost", "members", "income")
    income_table = ttk.Treeview(expected_income_frame, columns=income_columns, show="headings", height=7, style="Income.Treeview")

    #Setting column headers
    income_table.heading(income_columns[0], text="Option")
    income_table.heading(income_columns[1], text="Cost\nPer Unit")
    income_table.heading(income_columns[2], text="Members")
    income_table.heading(income_columns[3], text="Total Income")

    #Setting column widths
    income_table.column(income_columns[0], width=105, anchor="center")
    income_table.column(income_columns[1], width=55, anchor="center")
    income_table.column(income_columns[2], width=55, anchor="center")
    income_table.column(income_columns[3], width=55, anchor="center")

    #Packing table
    income_table.pack(padx=5, pady=5, fill="both")

    #Function to reload statistics and update screen
    def refresh_statistics():

        #Attempts to get membership statistics from repository
        try:
            statistics = repository.get_statistics()

        except sqlite3.Error as error: #Displays an error message if query fails
            messagebox.showerror("Database Error", f"Could not load statistics.\n{error}")
            return

        #Configures value_labels to show the counts for each statistic
        #Total members
        stat_boxes[("membership", "Total")].value_label.configure(
            text=statistics["total"]
        )

        #Membership plans
        for plan, count in statistics["membership_counts"].items():
            stat_boxes[("membership", plan)].value_label.configure(text=count)

        #Payment plans
        for plan, count in statistics["payment_counts"].items():
            stat_boxes[("payment", plan)].value_label.configure(text=count)

        #Library cards
        stat_boxes[("library", "cards")].value_label.configure(
            text=statistics["library_cards"]
        )

        #Extras
        for name, count in statistics["extras_counts"].items():
            stat_boxes[("extras", name)].value_label.configure(text=count)

        #Deletes previous table rows/statistics
        for item in income_table.get_children():
            income_table.delete(item)

        #Inserts updated income rows
        for row in statistics["income_rows"]:
            insert_income_row(*row)

    statistics_frame.refresh = refresh_statistics
    refresh_statistics()

    #Button to navigate back to the main menu
    back_button = ttk.Button(content_frame, text="Back to Main Menu", command=lambda: show_screen(main_menu_frame), style="Secondary.TButton")
    back_button.grid(row=6, column=0, padx=5, pady=8)

   
    

    return statistics_frame

