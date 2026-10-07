#------------------------------------------
#BIT502 Assessment 3, Jorj Baigent, 5132617
#------------------------------------------
#Stores the code for the About box

#------------------------------------------
#IMPORTS
#------------------------------------------
import tkinter as tk
from tkinter import ttk
from colours import FROST_BLUE

#------------------------------------------
#FUNCTIONS
#------------------------------------------
#Creates frames storing information about program
def create_info_frame(parent, label, content):

    #Creates a frame
    info_frame = ttk.Frame(parent, style="Info.TFrame")

    #Creates label for heading
    info_label = ttk.Label(info_frame, text=label, style="Info.TLabel", anchor="center")

    #Creates a label for content
    info_content = ttk.Label(info_frame, text=content, style="InfoText.TLabel", anchor="nw", justify="left", wraplength=240)

    #Positioning
    info_label.pack(fill="x", padx=5, pady=5)
    info_content.pack(fill="x", padx=5, pady=5)

    return info_frame

#------------------------------------------
#MAIN FUNCTION
#------------------------------------------
#Imported and called in main.py to create a help screen
def create_help_screen(parent):

    #Creates TopLevel window 
    help_box = tk.Toplevel(parent, bg=FROST_BLUE)
    help_box.title("Help")
    help_box.resizable(False, False)
    help_box.geometry("300x400")
    help_box.withdraw()

    #Frame and canvas to support a scrollbar
    help_frame = tk.Frame(help_box, bg=FROST_BLUE)
    canvas = tk.Canvas(help_frame, bg=FROST_BLUE, highlightthickness=0)

    #Creating scrollbar
    scrollbar = ttk.Scrollbar(help_frame, orient="vertical", command=canvas.yview)

    #Setting scrollbar to canvas
    canvas.configure(yscrollcommand=scrollbar.set)

    #Footer to hold 'OK' Button - so it is always visible without scrolling
    footer = tk.Frame(help_box, bg=FROST_BLUE)

    #Placing widgets
    footer.pack(side="bottom", fill="x")
    help_frame.pack(side="top", fill="both", expand=True)
    canvas.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")

    #Configuring columns to avoid empty space
    help_frame.rowconfigure(0, weight=1)
    help_frame.columnconfigure(0, weight=1)

    #Frame to place content
    content_frame= tk.Frame(canvas, bg=FROST_BLUE)


    #Adds widgets to top level
    help_lbl1 = ttk.Label(content_frame, text="About this program", style="Heading.TLabel")
    help_box.protocol("WM_DELETE_WINDOW", help_box.withdraw)

    #Labels and content to be placed on screen
    frame_labels = ["Application Overview:", "Searching for Members:", "Registering Members:", "Membership Options:", "Viewing Statistics:", "Troubleshooting:", "Navigation:"]
    frame_content = [
        ("This is a membership management application for The Aurora Archive "
         "to manage members and their details. Use the application to search "
         "for existing members, register new members, and view membership statistics."
         ),
         (
          "Use the Search Members screen to search for existing members. Enter "
          "the relevant member information into the search fields and select "
          "the search option to view matching members and their membership details."
          ), 
          (
            "Use the Register Member screen to register a new member. Enter all "
           "required member details, select membership options and extras, and "
           "then submit the registration. The application will automatically "
           "calculate the membership costs."
           ), 
           (
            "Select the membership type and payment plan that applies to the "
            "member. Library cards and optional extras can also be selected. "
            "Any applicable discounts are automatically applied when calculating "
            "membership costs."
            ), 
            (
                "Use the Member Statistics screen to view an overview of the current "
             "membership information. Statistics include membership types, payment "
             "plans, library cards, extras, and expected monthly income."
             ),
             ( 
             "If a member cannot be found, check that the search information has "
             "been entered correctly and try again. If a registration cannot be "
             "submitted, check that all required fields have been completed. If a "
             "calculated total appears incorrect, check the membership options and "
             "extras that have been selected."
             ), 
             (
                "Use the menu at the top of the application to move between screens. "
                "Select the appropriate option to access membership management, "
                "statistics, or help. Use the return option provided on each screen "
                "to return to the main menu."
                )
                ]

    #Creates heading
    help_lbl1.pack(pady=5, padx=5)

    #Creates and places frames with information in them using the frame_labels and frame_content lists
    for i in range(len(frame_labels)):
        info_frame = create_info_frame(content_frame, frame_labels[i], frame_content[i])
        info_frame.pack(fill="x" , pady=5, padx=5)


    #Button to exit help screen
    button_ok = ttk.Button(footer, text="OK", command=help_box.withdraw, style="Secondary.TButton")
    button_ok.pack(pady=5)

    #Window to hold the content frame
    content_window = canvas.create_window((0,0), window=content_frame, anchor="nw")
    content_frame.bind(
        "<Configure>",
        lambda _: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    #Resizing content for formatting
    def resize_content(event):
        canvas.itemconfigure(content_window, width=event.width)
        wraplength = max(120, event.width - 40)
        for info_frame in content_frame.winfo_children():
            for widget in info_frame.winfo_children():
                if (
                    isinstance(widget, ttk.Label)
                    and widget.cget("style") == "InfoText.TLabel"
                ):
                    widget.configure(wraplength=wraplength)

    canvas.bind(
        "<Configure>",
        resize_content
    )

    return help_box