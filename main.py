#------------------------------------------
#BIT502 Assessment 3, Jorj Baigent, 5132617
#------------------------------------------

#------------------------------------------
#IMPORTS
#------------------------------------------

import tkinter as tk
from tkinter import ttk


from colours import FROST_BLUE  #Variable holds hex code for frost blue
from styles import * #Custom styling
from member_repository import MemberRepository #Database

#Screens
from register_member import create_register_screen
from search_members import create_search_screen
from member_statistics import create_statistics_screen
from about import create_help_screen

#------------------------------------------
#TKINTER GUI SETUP
#------------------------------------------
 
root = tk.Tk()
root.geometry("400x300")
root.minsize(300, 250)
root.title("The Aurora Archive")
root.config(bg=FROST_BLUE)

#Apply styles globally
apply_global_styles()

#The repository creates the supplied schema if the database file is absent
repository = MemberRepository()

#Container for all screens
container = tk.Frame(root, bg=FROST_BLUE)
container.pack(fill="both", expand=True)

#------------------------------------------
#NAVIGATION FUNCTION
#------------------------------------------
def show_screen(screen):
    for widget in container.winfo_children():
        widget.pack_forget()

    #Resizing root for specific frames
    if screen is register_frame:
        root.geometry("500x650")
    elif screen is search_frame:
        root.geometry("500x500")
    elif screen is statistics_frame:
        root.geometry("500x500")
    else:
        root.geometry("400x300")

    screen.pack(fill="both", expand=True)
    if screen is statistics_frame:
        statistics_frame.refresh()


#------------------------------------------
#MAIN MENU FRAME
#------------------------------------------

main_menu_frame = tk.Frame(container, bg=FROST_BLUE)
main_menu_frame.pack(fill="both", expand=True)


#------------------------------------------
#MAIN MENU WIDGETS
#------------------------------------------

#Heading
title_label = ttk.Label(main_menu_frame, text="The Aurora Archive", style="Heading.TLabel")

title_label.pack(pady=(60, 5))


#Subtitle
subtitle_label = ttk.Label(main_menu_frame, text="Membership Management System", style="Subtitle.TLabel")
subtitle_label.pack()


#Instruction
instruction_label = ttk.Label(main_menu_frame, text="Please select an option from the menu above.", style="Instruction.TLabel")
instruction_label.pack(pady=(20,40))

#Exit Button
exit_button = ttk.Button(main_menu_frame, text="Exit Program", command=root.quit, style="Secondary.TButton")
exit_button.pack(pady=(20, 0))

#------------------------------------------
#OTHER SCREEN FRAMES
#------------------------------------------

#Register Member Screen
register_frame = create_register_screen(container, show_screen, main_menu_frame, repository)

#Search Members Screen
search_frame = create_search_screen(container, show_screen, main_menu_frame, repository)

#Member Statistics Screen
statistics_frame = create_statistics_screen(container, show_screen, main_menu_frame, repository)

#Help Screen
help_screen = create_help_screen(root)

#------------------------------------------
#MENU BAR
#------------------------------------------

menu_bar = tk.Menu(root)

#Display Menu Bar
root.config(menu=menu_bar)


#------------------------------------------
#FILE MENU
#------------------------------------------
file_menu = tk.Menu(menu_bar, tearoff=0)

file_menu.add_command(label="Main Menu", command=lambda: show_screen(main_menu_frame))

file_menu.add_command(label="Exit", command=root.quit)


menu_bar.add_cascade(label="File", menu=file_menu)


#------------------------------------------
#MEMBERS MENU
#------------------------------------------
members_menu = tk.Menu(menu_bar, tearoff=0)

members_menu.add_command(label="Register Member", command=lambda: show_screen(register_frame))

members_menu.add_command(label="Search Members", command=lambda: show_screen(search_frame))

menu_bar.add_cascade(label="Members", menu=members_menu)


#------------------------------------------
#VIEW MENU
#------------------------------------------
view_menu = tk.Menu(menu_bar, tearoff=0)

view_menu.add_command(label="Member Statistics", command=lambda: show_screen(statistics_frame))

menu_bar.add_cascade(label="View", menu=view_menu)


#------------------------------------------
#HELP MENU
#------------------------------------------
help_menu = tk.Menu(menu_bar, tearoff=0)

help_menu.add_command(label="About...", command=help_screen.deiconify)

menu_bar.add_cascade(label="Help", menu=help_menu)


#------------------------------------------
#MAIN GUI INTERFACE
#------------------------------------------




#Run program
if __name__ == "__main__":
    root.mainloop()
