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

from colours import FROST_BLUE, NAVY_BLUE, TURQUOISE #Imports variables storing hex codes 
from member_options import MEMBERSHIP_PLANS, PAYMENT_PLANS #Imports payment and membership plans

#------------------------------------------
#MAIN FUNCTION
#------------------------------------------

def create_search_screen(parent, show_screen, main_menu_frame, repository):
    """Create the search screen without creating a second Tk root."""

    #Creates a frame to hold content
    search_frame = tk.Frame(parent, bg=FROST_BLUE)

    #Heading
    title_label = ttk.Label(
        search_frame, text="Search Members", style="Heading.TLabel"
    )

    #Brief instruction label
    instruction_label = ttk.Label(
        search_frame,
        text="Enter one or more search criteria",
        style="Instruction.TLabel",
    )

    #Search criteria frame - holds entry boxes for users to enter search criteria
    search_criteria_frame = ttk.LabelFrame(
        search_frame,
        text="Search Criteria:",
        style="Generic.TLabelframe",
        padding=6,
    )

    #Variables to hold user input
    member_id_search = tk.StringVar(search_frame)
    name_search = tk.StringVar(search_frame)
    membership_plan_search = tk.StringVar(search_frame, "All Plans")
    payment_plan_search = tk.StringVar(search_frame, "All Payment Plans")
    partial_search = tk.BooleanVar(search_frame, False)
    search_frame.search_variables = (
        member_id_search,
        name_search,
        membership_plan_search,
        payment_plan_search,
        partial_search,
    )

    # Reuse the same valid membership and payment choices as registration.
    membership_plan_values = ("All Plans",) + MEMBERSHIP_PLANS
    payment_plan_values = ("All Payment Plans",) + PAYMENT_PLANS

    #Widgets inside search criteria frame
    #Labels
    member_id_lbl = ttk.Label(search_criteria_frame, text="Member ID:", style="Field.TLabel")
    last_name_lbl = ttk.Label(search_criteria_frame, text="Last Name:", style="Field.TLabel")
    membership_plan_lbl = ttk.Label(search_criteria_frame, text="Membership Plan:", style="Field.TLabel")
    payment_plan_lbl = ttk.Label(search_criteria_frame, text="Payment Plan:", style="Field.TLabel")

    #Entry fields
    member_id_entry = ttk.Entry(
        search_criteria_frame,
        style="Form.TEntry",
        textvariable=member_id_search,
        width=24,
    )
    last_name_entry = ttk.Entry(
        search_criteria_frame,
        style="Form.TEntry",
        textvariable=name_search,
        width=24,
    )

    #Adds a light gray placeholder inside the search entry boxes
    def add_placeholder(entry, hint):
        entry.insert(0, hint)
        entry.configure(foreground="#8aa0ad")

        def clear_hint(event):
            if entry.get() == hint:
                entry.delete(0, tk.END)
                entry.configure(foreground="#182f4f")

        def restore_hint(event):
            if not entry.get():
                entry.insert(0, hint)
                entry.configure(foreground="#8aa0ad")

        entry.bind("<FocusIn>", clear_hint)
        entry.bind("<FocusOut>", restore_hint)

    #Adds hint for users inside entry boxes
    add_placeholder(member_id_entry, "Optional ID")
    add_placeholder(last_name_entry, "Search by last name")

    #Dropdown boxes
    member_plan_dropdown = ttk.Combobox(
        search_criteria_frame,
        values=membership_plan_values,
        textvariable=membership_plan_search,
        state="readonly",
        style="Search.TCombobox"
    )
    payment_plan_dropdown = ttk.Combobox(
        search_criteria_frame,
        values=payment_plan_values,
        textvariable=payment_plan_search,
        state="readonly",
        style="Search.TCombobox"
    )

    #Set initial dropdown values
    membership_plan_search.set("All Plans")
    payment_plan_search.set("All Payment Plans")
    member_plan_dropdown.set("All Plans")
    payment_plan_dropdown.set("All Payment Plans")

    #Partial search checkbox
    partial_search_check = ttk.Checkbutton(
        search_criteria_frame,
        text="Allow partial search",
        variable=partial_search,
        style="RightIndicator.TCheckbutton"
    )

    #Clear and search buttons
    clear_form_btn = ttk.Button(search_criteria_frame, text="Clear", style="Secondary.TButton")
    search_form_btn = ttk.Button(search_criteria_frame, text="Search", style="Submit.TButton")

    #Search results frame - holds a table that displays search results
    search_results_frame = ttk.LabelFrame(
        search_frame, text="Search Results:", style="Generic.TLabelframe"
    )

  

    #Search results table

    #List to hold column ids
    search_results_cols = ["member_id", "member_name", "member_plan", "view_more"]

    #Creating the search results table
    search_results_table = ttk.Treeview(
        search_results_frame,
        columns=search_results_cols,
        show="headings",
        style="Search.Treeview",
        height=5,
    )

    #Define column headings
    search_results_table.heading("member_id", text="ID")
    search_results_table.heading("member_name", text="Name")
    search_results_table.heading("member_plan", text="Plan")
    search_results_table.heading("view_more", text="View More")

    search_results_table.column("member_id", width=55, anchor="center", stretch=True)
    search_results_table.column("member_name", width=150, anchor="w", stretch=True)
    search_results_table.column("member_plan", width=90, anchor="w", stretch=True)
    search_results_table.column("view_more", width=90, anchor="center", stretch=False)
    search_results_table.tag_configure(
        "more_hover",
        background=TURQUOISE,
        foreground=NAVY_BLUE,
        font=("Arial", 10, "bold")
    )

    #Label that shows if no results were found
    no_results_label = ttk.Label(search_results_frame, text="No members matched those search criteria.\nPlease try again with a different term.", style="Instruction.TLabel", anchor="center", justify="center")

    #Shows the results table if there are results
    def show_results_table():
        no_results_label.pack_forget()
        if not search_results_table.winfo_manager():
            search_results_table.pack(fill="both", expand=True, padx=8, pady=8)

    #Shows a message if no search results are found
    def show_no_results():
        search_results_table.pack_forget()
        no_results_label.pack(fill="both", expand=True, padx=8, pady=8)

    #Clears previous search results
    def clear_results():
        for item in search_results_table.get_children():
            search_results_table.delete(item)
        show_results_table()

    #Searches for members
    def search_members():

        clear_results() #Clears previous results first

        member_id = member_id_entry.get().strip() #Gets the member ID input by user

        if member_id == "Optional ID": #Member ID not entered

            member_id = ""

        if member_id and not member_id.isdigit(): #Invalid member ID entered

            messagebox.showwarning("Invalid ID", "Member ID must contain digits only")
            return

        last_name = last_name_entry.get().strip() #Gets last name input by user

        if last_name == "Search by last name": #Last name not entered
            last_name = ""

        #Tries to search for members
        try:

            results = repository.search_members(
                member_id=member_id or None,
                last_name=last_name,
                membership_plan=(
                    None if membership_plan_search.get() == "All Plans"
                    else membership_plan_search.get()
                ),
                payment_plan=(
                    None if payment_plan_search.get() == "All Payment Plans"
                    else payment_plan_search.get()
                ),
                partial=partial_search.get()
            )

        except (sqlite3.Error, ValueError) as error: #Shows error message if query was unsuccessful
            messagebox.showerror("Search Error", f"Could not search members.\n{error}")
            return

        #Inserts any results found
        for member in results:
            search_results_table.insert(
                "",
                tk.END,
                values=(
                    member["MemberID"],
                    f"{member['First_Name']} {member['Last_Name']}",
                    member["Membership_Plan"],
                    "[ More > ]"
                )
            )

        if not results: #Displays no results label if no results were found
            show_no_results()

    #Creates a TopLevel that shows when View More is pressed in the search results
    def show_member_details(member_id):

        #Attempts to get member details
        try:

            member = repository.get_member(member_id)

        except sqlite3.Error as error: #Displays error message is query was unsuccessful

            messagebox.showerror("Database Error", f"Could not retrieve member details.\n{error}")
            return

        if member is None:
            return

        #Gets selected extras
        selected_extras = [
            name for name, column in (
                ("Book Rental", "Extra_Book_Rental"),
                ("Private Area Access", "Extra_Private_Area"),
                ("Monthly Booklet", "Extra_Booklet"),
                ("Online ebook Rental", "Extra_Ebook_Rental")
            ) if member[column]
        ]

        #Gets members details
        details = (
            ("Member ID", member["MemberID"]),
            ("First Name", member["First_Name"]),
            ("Last Name", member["Last_Name"]),
            ("Address", member["Address"]),
            ("Mobile", member["Mobile"]),
            ("Membership Plan", member["Membership_Plan"]),
            ("Payment Plan", member["Payment_Plan"]),
            ("Extras", ", ".join(selected_extras) if selected_extras else "None"),
            ("Library Card", "Yes" if member["Has_Library_Card"] else "No"),
            ("Library Card Number", member["Library_Card_Number"] or "N/A")
        )

        #Creates a TopLevel for member details
        details_window = tk.Toplevel(search_frame)
        details_window.title("Member Details")
        details_window.geometry("420x460")
        details_window.resizable(False, False)
        details_window.transient(search_frame.winfo_toplevel())

        #Creates a LabelFrame for the member details
        details_frame = ttk.LabelFrame(
            details_window,
            text="Member Details",
            style="Generic.TLabelframe",
            padding=8
        )

        details_frame.pack(fill="both", expand=True, padx=10, pady=10)
        details_frame.columnconfigure(1, weight=1)

        #Adds labels for each label and value in details
        for row, (label, value) in enumerate(details):

            ttk.Label(
                details_frame, 
                text=f"{label}:",
                style="Field.TLabel"
            ).grid(row=row, column=0, sticky="nw", padx=6, pady=5)

            ttk.Label(
                details_frame,
                text=value,
                style="Field.TLabel",
                wraplength=245,
                justify="left"
            ).grid(row=row, column=1, sticky="w", padx=6, pady=5)

        #OK button to exit window
        ttk.Button(
            details_window,
            text="OK",
            command=details_window.destroy,
            style="Secondary.TButton"
        ).pack(pady=(0, 10))
        details_window.protocol("WM_DELETE_WINDOW", details_window.destroy)
        details_window.grab_set()
        details_window.focus_set()

    #Shows members details when a cell is clicked
    def show_details_from_cell(event):

        if (
            search_results_table.identify_region(event.x, event.y) != "cell"
            or search_results_table.identify_column(event.x) != "#4"
        ): #Checks that a cell was clicked and that it was a cell in the 4th column - the View More column
            
            return #Returns if click was not in a cell in column 4

        #Gets the row that was clicked
        item = search_results_table.identify_row(event.y)

        #Returns if there was no item under the click
        if not item:
            return

        #Highlights the selected row
        search_results_table.selection_set(item)

        #Reads the rows data and saves the member ID
        member_id = search_results_table.item(item, "values")[0]

        #Opens the TopLevel with members details
        show_member_details(member_id)

        return "break"

    #Stores the row currently being hovered over
    hovered_item = None

    #Hover behaviour for the results table
    def update_results_cursor(event):

        #Lets the function update hovered_item
        nonlocal hovered_item

        #Checks the cursor is over a cell in the table and in the 4th column
        is_more_cell = (
            search_results_table.identify_region(event.x, event.y) == "cell"
            and search_results_table.identify_column(event.x) == "#4"
        )

        #Changes cursor to a clickable hand cursor if the cursor is over the View More column
        search_results_table.configure(cursor="hand2" if is_more_cell else "")

        #Finds row cursor is on if cursor is also over a cell in column 4
        item = search_results_table.identify_row(event.y) if is_more_cell else "" #Sets to empty string if cursor isn't over a row on the table

        #If cursor is still over the same row
        if item == hovered_item:
            return

        #If there was a previous hovered row, check if that row still exists
        if hovered_item and search_results_table.exists(hovered_item):
            search_results_table.item(hovered_item, tags=()) #Clears tag from previously hovered row so the hover highlight is removed

        #Stores current hovered row
        hovered_item = item

        #If there is a row, custom hover tag is applied
        if hovered_item:
            search_results_table.item(hovered_item, tags=("more_hover"))

    #Resets the search form and table to their original states
    def clear_form():
        #Sets member ID and last name entry to be blank
        member_id_search.set("")
        name_search.set("")

        #Sets membership plan selection to default 'All Plans'
        membership_plan_search.set("All Plans")

        #Sets payment plan selection to default 'All Payment Plans'
        payment_plan_search.set("All Payment Plans")

        #Sets partial search checkbox to False
        partial_search.set(False)

        #Clears any previous results
        clear_results()

        #Adds placeholders to member ID and last name entry
        for entry, hint in (
            (member_id_entry, "Optional ID"),
            (last_name_entry, "Search by last name")
        ):
            entry.delete(0, tk.END)
            entry.insert(0, hint)
            entry.configure(foreground="#8aa0ad")

    #Adds command to clear button
    clear_form_btn.configure(command=clear_form)

    #Adds command to search button
    search_form_btn.configure(command=search_members)

    search_results_table.bind("<Button-1>", show_details_from_cell)
    search_results_table.bind("<Motion>", update_results_cursor)


    #Button to navigate back to main menu
    back_button = ttk.Button(
        search_frame,
        text="Back to Main Menu",
        command=lambda: show_screen(main_menu_frame),
        style="Secondary.TButton",
    )

    #Widget placement
    title_label.pack(pady=(5, 0))
    instruction_label.pack(pady=(0, 8))
    search_criteria_frame.pack(fill="x", padx=0, pady=4)
    search_results_frame.pack(fill="both", expand=True, padx=0, pady=4)

    for column in range(4):
        search_criteria_frame.columnconfigure(
            column, weight=1, uniform="search_columns"
        )

    member_id_lbl.grid(row=0, column=0, sticky="w", padx=8, pady=(2, 1))
    member_id_entry.grid(
        row=1, column=0, columnspan=2, sticky="ew", padx=8, pady=(0, 8)
    )

    last_name_lbl.grid(row=0, column=2, sticky="w", padx=8, pady=(2, 1))
    last_name_entry.grid(
        row=1, column=2, columnspan=2, sticky="ew", padx=8, pady=(0, 8)
    )

    membership_plan_lbl.grid(
        row=2, column=0, columnspan=2, sticky="w", padx=8, pady=(0, 1)
    )
    payment_plan_lbl.grid(
        row=2, column=2, columnspan=2, sticky="w", padx=8, pady=(0, 1)
    )
    member_plan_dropdown.grid(row=3, column=0, columnspan=2, sticky="ew", padx=8, pady=(0, 4))
    payment_plan_dropdown.grid(row=3, column=2, columnspan=2, sticky="ew", padx=8, pady=(0, 4))

    partial_search_check.grid(
        row=4, column=1, columnspan=2, pady=(8, 8)
    )
    search_results_table.pack(fill="both", expand=True, padx=8, pady=8)

    clear_form_btn.grid(row=5, column=1)
    search_form_btn.grid(row=5, column=2)

    # Select the first search option after the readonly dropdowns are placed.
    member_plan_dropdown.current(0)
    payment_plan_dropdown.current(0)

    back_button.pack()
    
    return search_frame

