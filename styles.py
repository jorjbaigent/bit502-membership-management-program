#------------------------------------------
#BIT502 Assessment 3, Jorj Baigent, 5132617
#------------------------------------------

#------------------------------------------
#IMPORTS
#------------------------------------------
from tkinter import ttk
from colours import NAVY_BLUE, FROST_BLUE, TEAL, WHITE, TURQUOISE

#------------------------------------------
#STYLING
#------------------------------------------
#Applies styles across screens
def apply_global_styles():
    style = ttk.Style()

    #Supports background colouring
    style.theme_use("clam")

#Custom Styles

    #Custom style button for main menu and reset
    style.configure(
        "Secondary.TButton",
        font=("Arial", 12),
        background=TURQUOISE,
        foreground=WHITE,
    )

    #Adding active/hover states
    style.map(
        "Secondary.TButton", 
        background=[("pressed", NAVY_BLUE), ("active", NAVY_BLUE)], 
        foreground=[("pressed", WHITE), ("active", WHITE)]
        )

    #Generic LabelFrame styles
    style.configure(
        "Generic.TLabelframe",
        background=WHITE,
        foreground=NAVY_BLUE,
        bordercolor=TURQUOISE,
        borderwidth=1,
        relief="solid",
        padding=10
    )

    #Generic Labelframe Label styles
    style.configure(
        "Generic.TLabelframe.Label",
        background=WHITE,
        foreground=NAVY_BLUE,
        font=("Arial", 11, "bold")
    )

#Primary LabelFrame styles
    style.configure(
        "Primary.TLabelframe",
        background=NAVY_BLUE,
        foreground=TEAL,
        bordercolor=TURQUOISE,
        borderwidth=0,
        relief="solid",
        padding=10
    )
    style.configure(
        "Primary.TLabelframe.Label",
        background=NAVY_BLUE,
        foreground=TEAL,
        font=("Arial", 11, "bold"),
    )

    #Styles for totals labels
    style.configure(
        "Totals.TLabel",
        background=NAVY_BLUE, 
        foreground=WHITE
        )

    #Style for the total cost label
    style.configure(
        "TotalCost.TLabel",
        background=NAVY_BLUE,
        foreground=TEAL,
        font=("Arial", 11, "bold"),
    )

    #Styles for field labels for entries
    style.configure(
        "Field.TLabel", 
        background=WHITE, 
        foreground=NAVY_BLUE
        )

    #Styles for frame titles
    style.configure(
        "FrameTitle.TLabel", 
        background=WHITE, 
        foreground=NAVY_BLUE
        )

    #Styles for the totals frame title
    style.configure(
        "TotalsFrameTitle.TLabel", 
        background=NAVY_BLUE, 
        foreground=TEAL
        )

    #Style for radiobuttons
    style.configure(
        "Form.TRadiobutton", 
        background=WHITE, 
        foreground=NAVY_BLUE,
        indicatorbackground=WHITE,
        indicatorcolor=NAVY_BLUE,
        bordercolor=NAVY_BLUE,
        lightcolor=NAVY_BLUE,
        darkcolor=NAVY_BLUE
        )

    style.map(
        "Form.TRadiobutton",
        indicatorbackground=[("selected", WHITE)],
        indicatorcolor=[("selected", NAVY_BLUE)],

        foreground=[("selected", NAVY_BLUE)],
        focuscolor=[("selected", NAVY_BLUE)]
    )

    #Styles for checkbuttons
    style.configure(
        "Form.TCheckbutton",
        background=WHITE,
        foreground=NAVY_BLUE,
        indicatorbackground=WHITE,
        indicatorcolor=NAVY_BLUE,
        bordercolor=NAVY_BLUE,
        lightcolor=NAVY_BLUE,
        darkcolor=NAVY_BLUE,
    )

    style.map(
        "Form.TCheckbutton",
        indicatorbackground=[("selected", WHITE)],
        indicatorcolor=[("selected", NAVY_BLUE)],
        foreground=[("selected", NAVY_BLUE)],
    )

    style.layout(
        "RightIndicator.TCheckbutton",
        [
            (
                "Checkbutton.padding",
                {
                    "sticky": "nswe",
                    "children": [
                        (
                            "Checkbutton.focus",
                            {
                                "side": "left",
                                "sticky": "w",
                                "children": [("Checkbutton.label", {"sticky": "nswe"})],
                            },
                        ),
                        ("Checkbutton.indicator", {"side": "right", "sticky": ""}),
                    ],
                },
            )
        ],
    )
    style.configure("RightIndicator.TCheckbutton", background=WHITE, foreground=NAVY_BLUE)
    style.map(
        "RightIndicator.TCheckbutton",
        indicatorbackground=[("selected", WHITE)],
        indicatorcolor=[("selected", NAVY_BLUE)],
        foreground=[("selected", NAVY_BLUE)],
    )

    #Styles for entry fields
    style.configure(
        "Form.TEntry",
        fieldbackground=FROST_BLUE,
        foreground=NAVY_BLUE,
        bordercolor=TURQUOISE,
        lightcolor=TURQUOISE,
        darkcolor=TURQUOISE,
        borderwidth=1,
    )

    #Styles for the search results table
    style.configure(
        "Search.Treeview",
        background=WHITE,
        fieldbackground=WHITE,
        foreground=NAVY_BLUE,
        rowheight=24,
        bordercolor=TURQUOISE,
        borderwidth=1,
        relief="solid",
    )

    #Styles for the search results table headings
    style.configure(
        "Search.Treeview.Heading",
        background=TURQUOISE,
        foreground=WHITE,
        font=("Arial", 10, "bold"),
    )

    #Styles for hint labels
    style.configure(
        "Hint.TLabel", 
        background=FROST_BLUE, 
        foreground=NAVY_BLUE
        )

    #Styles for warning labels
    style.configure(
        "Warning.TLabel", 
        background=WHITE, 
        foreground="#d9534f", 
        font=("Arial", 8)
    )

    #Styles for Submit/Search buttons
    style.configure(
        "Submit.TButton", 
        font=("Arial", 11),
        background=TEAL, 
        foreground=NAVY_BLUE
    )
    style.map(
        "Submit.TButton",
        background=[("pressed", TURQUOISE), ("active", NAVY_BLUE)],
        foreground=[("pressed", WHITE), ("active", WHITE)],
    )

    style.configure(
        "Search.TButton",
        font=("Arial", 11),
        background=TEAL,
        foreground=NAVY_BLUE,
    )
    style.map(
        "Search.TButton",
        background=[("pressed", TURQUOISE), ("active", NAVY_BLUE)],
        foreground=[("pressed", WHITE), ("active", WHITE)],
    )

    #Page Headings
    style.configure(
        "Heading.TLabel",
        background=FROST_BLUE,
        foreground=NAVY_BLUE,
        font=("Arial", 20, "bold")
    )

    #Subheading styles
    style.configure(
        "Subtitle.TLabel",
        background=FROST_BLUE,
        foreground=NAVY_BLUE,
        font=("Arial", 16)
    )

    #Instructions styles
    style.configure(
        "Instruction.TLabel",
        background=FROST_BLUE,
        foreground=TURQUOISE,
        font=("Arial", 14)
    )

    #Combobox styles
    style.configure(
        "Search.TCombobox",
        fieldbackground=FROST_BLUE,
        foreground=NAVY_BLUE,

        background=FROST_BLUE,
        arrowcolor=NAVY_BLUE,

        bordercolor=TURQUOISE,
        lightcolor=TURQUOISE,
        darkcolor=TURQUOISE,
        font=("Arial", 10)
    )

    style.map(
        "Search.TCombobox",
        fieldbackground=[("readonly", FROST_BLUE)],
        foreground=[("readonly", NAVY_BLUE)]
    )

    #Stats frame styles
    style.configure(
        "Stats.TFrame",
        background=FROST_BLUE
    )

    #Stats label styles
    style.configure(
        "StatsLabel.TLabel",
        background=FROST_BLUE,
        foreground=TURQUOISE,
        font=("Arial", 7, "bold")
    )

    #Stats values styles
    style.configure(
        "StatsValue.TLabel",
        background=FROST_BLUE,
        foreground=NAVY_BLUE,
        font=("Arial", 14, "bold")
    )

    #Styling for income table
    style.configure(
        "Income.Treeview",
        rowheight=23,
        font=("Arial", 8),
        background=WHITE,
        foreground=TURQUOISE
    )

    #Income table heading styles
    style.configure(
        "Income.Treeview.Heading",
        font=("Arial", 8, "bold"),
        background = FROST_BLUE,
        foreground=NAVY_BLUE
    )

    #Styling for info frames
    style.configure(
        "Info.TFrame",
        background=WHITE,
        padding=(10, 8)
    )

    #Styling for info labels
    style.configure(
        "Info.TLabel",
        background=WHITE,
        foreground=TURQUOISE,
        font=("Arial", 11, "bold")
    )

    #Styling for info content
    style.configure(
        "InfoText.TLabel",
        background=WHITE,
        foreground=NAVY_BLUE,
        font=("Arial", 10)
    )

    top_level = style.master
    top_level.option_add("*TCombobox*Listbox.background", FROST_BLUE)
    top_level.option_add("*TCombobox*Listbox.foreground", NAVY_BLUE)
    top_level.option_add("*TCombobox*Listbox.selectBackground", TURQUOISE)
    top_level.option_add("*TCombobox*Listbox.selectForeground", NAVY_BLUE)
    top_level.option_add("*TCombobox*Listbox.font", ("Arial", 10))


    return style