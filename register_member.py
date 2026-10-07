#------------------------------------------
#BIT502 Assessment 3, Jorj Baigent, 5132617
#------------------------------------------
#------------------------------------------
#IMPORTS
#------------------------------------------
#Imports tkinter and sqlite3
import tkinter as tk
import sqlite3
from tkinter import messagebox, ttk

from colours import FROST_BLUE #Imports background colour

#Imports member calculation functions
from member_calculations import (
    calculate_annual_discount,
    calculate_extras_cost,
    calculate_library_discount,
    calculate_totals,
    get_membership_cost
)

#Imports membership options and prices
from member_options import (
    EXTRAS,
    MEMBERSHIP_PLANS,
    PAYMENT_PLANS,
    PLAN_MONTHLY,
    PLAN_STANDARD,
)


#------------------------------------------
#MAIN FUNCTION
#------------------------------------------

#Imported and called in main.py to create a member registration screen
def create_register_screen(parent, show_screen, main_menu_frame, repository):

    #Creates a frame to hold the canvas and scrollbar 
    register_frame = tk.Frame(parent, bg=FROST_BLUE)

    #Creates a canvas and a scrollbar
    canvas = tk.Canvas(register_frame, bg=FROST_BLUE, highlightthickness=0)
    scrollbar = ttk.Scrollbar(register_frame, orient="vertical", command=canvas.yview)

    #Setting the scrollbar to canvas
    canvas.configure(yscrollcommand=scrollbar.set)

    #Placing canvas and scrollbar
    canvas.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")

    #Configuring rows and columns of register frame to avoid empty space
    register_frame.rowconfigure(0, weight=1)
    register_frame.columnconfigure(0, weight=1)

    #Frame to hold the content
    content_frame = tk.Frame(canvas, bg=FROST_BLUE)

    #Variable to hold user input
    first_name = tk.StringVar(register_frame)
    last_name = tk.StringVar(register_frame)
    address = tk.StringVar(register_frame)
    mobile = tk.StringVar(register_frame)
    membership_plan = tk.StringVar(register_frame, PLAN_STANDARD)
    payment_plan = tk.StringVar(register_frame, PLAN_MONTHLY)
    library_number = tk.StringVar(register_frame)
    has_library_card = tk.BooleanVar(register_frame, False)
    selected_extras = {
        name: tk.BooleanVar(register_frame, False) for name in EXTRAS
    }

    #Heading label
    title_label = ttk.Label(
        content_frame, text="New Member Registration Form",
        style="Heading.TLabel", anchor="center"
    )

    #Label to indicate required fields
    required_label = ttk.Label(content_frame, text="* Required fields", style="Hint.TLabel")

    #Frames to hold different categories of content

    #Holds entries for users personal details
    personal_frame = ttk.LabelFrame(
        content_frame, text="Personal Details:",
        style="Generic.TLabelframe"
    )

    #Holds entries for membership details
    membership_frame = ttk.LabelFrame(
        content_frame, text="Membership and Payment:",
        style="Generic.TLabelframe"
    )

    #Holds entries for library card and ID
    library_frame = ttk.LabelFrame(
        content_frame, text="Library Card Details:",
        style="Generic.TLabelframe"
    )

    #Holds labels that display total calculations
    totals_frame = ttk.LabelFrame(
        content_frame, text="Totals:",
        style="Primary.TLabelframe"
    )

    #Sets the columns sizes
    for column in range(2):
        personal_frame.columnconfigure(column, weight=1)
        membership_frame.columnconfigure(column, weight=1)
        library_frame.columnconfigure(column, weight=1)
        totals_frame.columnconfigure(column, weight=1)


    warnings = {}

    #Function to add entries and warning labels
    def add_field(frame, row, label_text, variable, warning_key, column=0, width=24):
        ttk.Label(frame, text=f"* {label_text}", style="Field.TLabel").grid(
            row=row, column=column, sticky="w", padx=8, pady=(5, 1)
        )
        entry = ttk.Entry(frame, textvariable=variable, width=width, style="Form.TEntry")
        entry.grid(row=row + 1, column=column, sticky="ew", padx=8, pady=(0, 1))
        warning = ttk.Label(frame, text="", style="Warning.TLabel")
        warning.grid(row=row + 2, column=column, sticky="w", padx=8)
        warnings[warning_key] = warning

    #Adding personal details entries
    add_field(personal_frame, 0, "First Name:", first_name, "first_name")
    add_field(personal_frame, 0, "Last Name:", last_name, "last_name", column=1)
    add_field(personal_frame, 3, "Address:", address, "address")
    add_field(personal_frame, 3, "Mobile:", mobile, "mobile", column=1)

    #Membership plan selection label
    ttk.Label(membership_frame, text="* Membership Plan:", style="Field.TLabel").grid(
        row=0, column=0, columnspan=2, sticky="w", padx=8, pady=(5, 1)
    )

    #Creates radio buttons for membership plan selection
    for column, plan in enumerate(MEMBERSHIP_PLANS):
        ttk.Radiobutton(
            membership_frame, text=plan, value=plan, variable=membership_plan,
            command=lambda: update_totals(), style="Form.TRadiobutton",
        ).grid(row=1, column=column, sticky="w", padx=8)

    #Payment plan selection label
    ttk.Label(membership_frame, text="* Payment Plan:", style="Field.TLabel").grid(
        row=2, column=0, columnspan=2, sticky="w", padx=8, pady=(7, 1)
    )

    #Creates radio buttons for payment period selection
    for column, plan in enumerate(PAYMENT_PLANS):
        ttk.Radiobutton(
            membership_frame, text=plan, value=plan, variable=payment_plan,
            command=lambda: update_totals(), style="Form.TRadiobutton",
        ).grid(row=3, column=column, sticky="w", padx=8)

    #Extras selection label
    ttk.Label(membership_frame, text="Extras (Optional):", style="Field.TLabel").grid(
        row=4, column=0, columnspan=2, sticky="w", padx=8, pady=(7, 1)
    )

    #Creates checkboxes for optional extras selection
    for index, (name, variable) in enumerate(selected_extras.items()):
        ttk.Checkbutton(
            membership_frame, text=name, variable=variable,
            command=lambda: update_totals(), style="Form.TCheckbutton",
        ).grid(row=5 + index // 2, column=index % 2, sticky="w", padx=8)

    #Library card label
    ttk.Label(library_frame, text="* Do you have a library card?", style="Field.TLabel").grid(
        row=0, column=0, columnspan=2, sticky="w", padx=8, pady=(5, 1)
    )

    #Adds radio buttons for library card
    ttk.Radiobutton(
        library_frame, text="Yes", value=True, variable=has_library_card,
        command=lambda: update_library_card(), style="Form.TRadiobutton",
    ).grid(row=1, column=0, sticky="w", padx=8)

    ttk.Radiobutton(
        library_frame, text="No", value=False, variable=has_library_card,
        command=lambda: update_library_card(), style="Form.TRadiobutton",
    ).grid(row=1, column=1, sticky="w", padx=8)

    #Adds label that pops up if user selects yes to having a library card
    library_number_label = ttk.Label(library_frame, text="* Library Card Number:", style="Field.TLabel")
    library_number_label.grid(row=2, column=0, sticky="w", padx=8, pady=(5, 1))

    #Adds entry for library card ID that pops up if user selects yes to having library card
    library_number_entry = ttk.Entry(library_frame, textvariable=library_number, style="Form.TEntry")
    library_number_entry.grid(row=2, column=1, sticky="ew", padx=8, pady=(5, 1))

    #Adds warning label for the library card section
    warnings["library_card"] = ttk.Label(library_frame, text="", style="Warning.TLabel")
    warnings["library_card"].grid(row=3, column=0, columnspan=2, sticky="w", padx=8)

    #Removes the library card ID label and entry
    library_number_label.grid_remove()
    library_number_entry.grid_remove()


    total_labels = {}
    total_rows = (
        ("Membership Cost:", "membership"),
        ("Extra Charges:", "extras"),
        ("Monthly Cost:", "monthly"),
        ("Weekly Cost:", "weekly"),
        ("Total Discount:", "discount"),
        ("Total Cost:", "total"),
    )

    #Adds labels for total labels and values
    for row, (label_text, key) in enumerate(total_rows):

        #Sets styles for each label
        total_style = "TotalCost.TLabel" if key == "total" else "Totals.TLabel"
        ttk.Label(totals_frame, text=label_text, style=total_style).grid(
            row=row, column=0, sticky="w", padx=8, pady=2
        )
        total_labels[key] = ttk.Label(totals_frame, text="--", style=total_style)
        total_labels[key].grid(row=row, column=1, sticky="e", padx=8, pady=2)

    #Updates the totals shown in the totals frame
    def update_totals():

        membership_cost = get_membership_cost(membership_plan.get()) #Gets membership cost

        #Gets extras cost and chosen extras
        extras_cost, _ = calculate_extras_cost(
            {name: variable.get() for name, variable in selected_extras.items()}
        )

        monthly_price = membership_cost + extras_cost #Calculates monthly cost

        library_discount = calculate_library_discount(monthly_price, has_library_card.get()) #Calculates library discount

        #Calculates annual discount
        annual_discount = calculate_annual_discount(
            membership_cost, has_library_card.get(), payment_plan.get()
        )

        #Calculates totals
        monthly_total, discount, total, weekly, period = calculate_totals(
            membership_cost, extras_cost, library_discount, annual_discount, payment_plan.get()
        )

        #Values to be entered into totals frame
        values = {
            "membership": membership_cost,
            "extras": extras_cost,
            "monthly": monthly_total,
            "weekly": weekly,
            "discount": discount,
            "total": f"{total:.2f} {period}"
        }

        #Placing values inside frame
        for key, value in values.items():
            total_labels[key].configure(text=value if key == "total" else f"${value:.2f}")
        return membership_cost, extras_cost, discount, monthly_total, weekly, total

    #Validates text entered by user
    def validate_text_field(key, value, empty_message, invalid_message=None, digits_only=False, phone_number=False):
        value = value.strip() #Strips empty space 

        message = ""

        if not value: #Value left empty

            message = empty_message

        elif digits_only and not value.isdigit(): #A digit only field with non digits entered

            message = invalid_message

        elif phone_number and (
            not any(char.isdigit() for char in value)
            or any(not (char.isdigit() or char in " +-()") for char in value)
        ): #If field is for a phone number and non-digit characters or characters that aren't +-() are entered
            
            message = invalid_message

        elif ( 
            not digits_only and not phone_number and invalid_message
            and any(char.isdigit() for char in value)
        ): #If a non-digit field contains any digit and an invalid message is provided
            
            message = invalid_message

        #Adds warning messages     
        warnings[key].configure(text=message)

        return not message

    #Validates the library card
    def validate_library_card():

        #Gets the library card number field
        card_number = library_number.get().strip()
        card_message = ""

        if has_library_card.get() and not card_number: #Selected yes for library card but hasn't entered ID

            card_message = "Library card number is required."

        elif has_library_card.get() and (
            not card_number.isdigit() or len(card_number) != 5
        ): #Library card number entered contains non-digit characters or more/less than 5 characters
            
            card_message = "Library card number must contain exactly 5 digits."

        elif not has_library_card.get() and card_number: #In case function doesn't remove library card ID entry

            card_message = "Please select Yes to apply the library card discount."

        #Adds library card warnings   
        warnings["library_card"].configure(text=card_message)

        return not card_message

    #Validates all necessary fields
    def validate_fields():

        #Validates first name
        valid = validate_text_field(
            "first_name", first_name.get(), "First name is required.",
            "First name cannot contain numbers."
        )

        #Validates last name
        valid = validate_text_field(
            "last_name", last_name.get(), "Last name is required.",
            "Last name cannot contain numbers."
        ) and valid #Ensures first name is valid too

        #Validates address
        valid = validate_text_field(
            "address", address.get(), "Address is required."
        ) and valid #Ensures previous fields are valid too

        #Validates mobile 
        valid = validate_text_field(
            "mobile", mobile.get(), "Mobile number is required.",
            "Mobile number can only contain digits.", digits_only=True, phone_number=True
        ) and valid #Ensures previous fields are valid too

        return valid and validate_library_card() #Validates library card

    #Function to attach validation function to each entry so that validation is automated
    def watch_text_field(
            key, variable, empty_message, invalid_message=None, phone_number=False
    ):
        variable.trace_add(
            "write",
            lambda *_: validate_text_field(
                key,
                variable.get(),
                empty_message,
                invalid_message,
                phone_number=phone_number
            )
        )

    #Attaching validation to text fields
    #First name
    watch_text_field(
        "first_name", first_name, "First name is required.", "First name cannot contain numbers."
    )

    #Last name
    watch_text_field(
        "last_name", last_name, "Last name is required.", "Last name cannot contain numbers."
    )

    #Address
    watch_text_field(
        "address", address, "Address is required."
        )

    #Mobile
    watch_text_field(
        "mobile", mobile, "Mobile number is required.", "Mobile number can only contain digits.", phone_number=True
    )

    #Attaches library card validation to library card ID entry
    library_number.trace_add("write", lambda *_: validate_library_card())

    #Function to show/hide library card ID entry 
    def update_library_card():
        if has_library_card.get():
            library_number_label.grid()
            library_number_entry.grid()
        else:
            library_number.set("")
            library_number_label.grid_remove()
            library_number_entry.grid_remove()

        #Revalidates and updates totals
        validate_fields()
        update_totals()

    #Resets the form to its original state
    def reset_form(confirm=True):

        #Confirms user wants to reset the form if they press the reset button on screen
        if confirm and not messagebox.askyesno("Confirm Reset", "Reset the registration form?"):

            return False

        #Sets all entries to be blank
        for variable in (first_name, last_name, address, mobile, library_number):
            variable.set("")

        #Sets membership plan radio buttons to be set to Standard Plan
        membership_plan.set(PLAN_STANDARD)

        #Sets payment plan radio buttons to be set to Monthly Payment
        payment_plan.set(PLAN_MONTHLY)

        #Sets library card radio buttons to false
        has_library_card.set(False)

        #Removes library card ID label and entry
        library_number_label.grid_remove()
        library_number_entry.grid_remove()

        #Unchecks any selected extras
        for variable in selected_extras.values():
            variable.set(False)

        #Clears warning labels
        for warning in warnings.values():
            warning.configure(text="")

        #Resets total labels
        for label in total_labels.values():
            label.configure(text="--")
        return True

    #Runs when Submit button is pressed to save details to the database
    def submit():

        #Shows warning if submit is pressed with invalid fields
        if not validate_fields():

            messagebox.showwarning("Invalid Details", "Please correct the highlighted fields.")
            return False

        #Gets total costs
        membership_cost, extras_cost, discount, monthly_total, weekly, total = update_totals()

        #Gets membership details entered
        details = {
            "first_name": first_name.get().strip(),
            "last_name": last_name.get().strip(),
            "address": address.get().strip(),
            "mobile": mobile.get().strip(),
            "membership_plan": membership_plan.get(),
            "extras": [name for name, value in selected_extras.items() if value.get()],
            "payment_plan": payment_plan.get(),
            "has_library_card": has_library_card.get(),
            "library_id": library_number.get().strip(),
            "membership_cost": membership_cost,
            "extras_cost": extras_cost,
            "total_discount": discount,
            "monthly_cost": monthly_total,
            "weekly_cost": weekly,
            "payment_due": total,
        }

        #Attempts to save membership information to the database
        try:

            repository.add_member(details)

        except sqlite3.Error as error: #Shows an error message if saving was unsuccessful

            messagebox.showerror("Database Error", f"Could not save the member.\n{error}")
            return False

        #Shows success message if details were saved
        messagebox.showinfo("Success", "Member details saved successfully")

        #Resets form without triggering confirmation box
        reset_form(False)

        return True

    #Placing title and frames
    title_label.grid(row=0, column=0, columnspan=3, pady=(10, 0))
    required_label.grid(row=1, column=0, columnspan=3, sticky="w", padx=8)
    personal_frame.grid(row=2, column=0, columnspan=3, sticky="ew", padx=8, pady=4)
    membership_frame.grid(row=3, column=0, columnspan=3, sticky="ew", padx=8, pady=4)
    library_frame.grid(row=4, column=0, columnspan=3, sticky="ew", padx=8, pady=4)
    totals_frame.grid(row=5, column=0, columnspan=3, sticky="ew", padx=8, pady=4)

    #Creating buttons 
    #Navigates to main menu
    ttk.Button(
        content_frame, text="Main Menu",
        command=lambda: show_screen(main_menu_frame), style="Secondary.TButton",
    ).grid(row=6, column=0, sticky="ew", padx=(8, 4), pady=8)

    #Resets form to its original state
    ttk.Button(
        content_frame, text="Reset", command=reset_form, style="Secondary.TButton",
    ).grid(row=6, column=1, sticky="ew", padx=4, pady=8)

    #Submits details to be saved to the database
    ttk.Button(
        content_frame, text="Submit", command=submit, style="Submit.TButton",
    ).grid(row=6, column=2, sticky="ew", padx=(4, 8), pady=8)

    #Configuring content frame columns to eliminate empty space
    content_frame.columnconfigure(0, weight=1)
    content_frame.columnconfigure(1, weight=1)
    content_frame.columnconfigure(2, weight=1)

    #Creates a window for the content_frame
    content_window = canvas.create_window((0, 0), window=content_frame, anchor="nw")

    content_frame.bind(
        "<Configure>",
        lambda _: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.bind(
        "<Configure>",
        lambda event: canvas.itemconfigure(content_window, width=event.width)
    )
    
    return register_frame
