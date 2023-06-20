######################       IMPORT NECESSARY MODULES       ####################################################################################

import contextlib
import os
import tkinter as tk
from datetime import datetime
from tkinter import Toplevel, messagebox, ttk

import customtkinter as ctk
import tkcalendar as tkc
from customtkinter import CTkImage
from PIL import Image
from plyer import notification
from tkcalendar import Calendar
from tktimepicker import AnalogPicker, AnalogThemes, constants
from tktooltip import ToolTip
############################################################################################################################################
# Selecting GUI theme - dark, light , system (for system default)
ctk.set_appearance_mode("dark")
# Selecting color theme - blue, green, dark-blue
ctk.set_default_color_theme("blue")
# Make the window completely transparent except for grey pixels
my_file = "medication_data.txt"
# Check if the file exists, and create a new one if not
if not os.path.exists(my_file):
    with open(my_file, 'w'):
        pass
# Create empty medication data to store it in the list widget
saved_data_medication = []
# Define the take_care_of_file to search for any errors and save data into it
################################## ##########################################################################################################

def take_care_of_file():
    with contextlib.suppress(FileNotFoundError):
        with open(my_file, "r") as f:
            for line in f:
                res = line.strip().split("|")
                if len(res) != 4:
                    raise ValueError("Invalid format in file")
                medication_name, dose_name, date_name, current_time = res
                if date_name:
                    try:
                        datetime.strptime(date_name, '%m/%d/%Y')
                    except ValueError:
                        continue
                current_time = current_time if current_time and current_time != 'None' else ''
                saved_data_medication.append(
                    (medication_name, dose_name, date_name, current_time))
take_care_of_file()
def save_information():
    medication_name = medication_entry.get()
    dose_name = dose_entry.get()
    date_name = date_entry.get()
    current_time = time_entry.get()

    if not all((medication_name, dose_name, date_name, current_time)):
        messagebox.showwarning("Warning", "Please fill out all fields!")
        return

    try:
        datetime.strptime(date_name, '%m/%d/%Y')
    except ValueError:
        messagebox.showwarning(
            "Warning", "Enter a valid date in the format MM/DD/YYYY!")
        return

    current_time = current_time if current_time and current_time != 'None' else ''
    saved_data_medication.append(
        (medication_name, dose_name, date_name, current_time))

    medication_entry.delete(0, tk.END)
    dose_entry.delete(0, tk.END)
    time_for_now = datetime.now().strftime('%I:%M %p')

    if current_time == time_for_now:
        remind_text_user = f"Medication Reminder\n\nIt's time to take your {medication_name} medication!"
        messagebox.showinfo("Medication Reminder", remind_text_user)
    listbox_updated()
    remind_schedule_user(medication_name, date_name, current_time)

    with open(my_file, "a") as f:
        f.write(f"{medication_name}|{dose_name}|{date_name}|{current_time}\n")

    var_for_date.set('')
    var_for_time.set('')
def reminder_show_up(medication_name):
    notification.notify(title="Medication Reminder", message=f"It's time to take your {medication_name} medication!")
def remind_schedule_user(medication_name, date_name, current_time):
    if not current_time or not date_name:
        return
    datetime_correct_format = datetime.combine(datetime.strptime(
        date_name, '%m/%d/%Y').date(), datetime.strptime(current_time, '%I:%M %p').time())
    time_for_now = datetime.now()
    if time_for_now < datetime_correct_format:
        my_app.after(int((datetime_correct_format-time_for_now).total_seconds()*1000), lambda: reminder_show_up(medication_name))
def clear_all_items():
    global saved_data_medication
    saved_data_medication = []
    update_medication_window.delete(*update_medication_window.get_children())
    with open(my_file, "w") as f:
        pass
def updateTime(time):
    var_for_time.set("{}:{} {}".format(*time))
def choose_time():
    top = tk.Toplevel(my_app)
    time_picker = AnalogPicker(top, type=constants.HOURS12)
    time_picker.pack(expand=True, fill="both")

    theme = AnalogThemes(time_picker)
    theme.setDracula()
    frame_color = frame['bg']
    ok_btn = tk.Button(top, text="OK", font=('Helvetica', 12), background=frame_color, width='50', foreground='white', command=lambda: (updateTime(time_picker.time()), time_entry.configure(state='readonly'), top.destroy()))
    ok_btn.pack()
def choose_date():
    # Create a new calendar window
    top = tk.Toplevel(my_app)
    cal = tkc.Calendar(top)

    # Wait for the user to choose a date and close the window
    cal.selection_clear()
    cal.configure(date_pattern="dd/MM/yyyy")
    cal.pack(expand=True, fill="both")

    def updateDate():
        # Get the chosen date and update the Date entry
        chosen_date = cal.selection_get().strftime("%m/%d/%Y")
        var_for_date.set(chosen_date)
        date_entry.configure(state='readonly')
        top.destroy()

    frame_color = frame['bg']
    ok_btn = tk.Button(top, text="OK", font=('Helvetica', 12), background=frame_color, width='50', foreground='white', command=updateDate)
    ok_btn.pack()
    cal.pack()
def listbox_updated():
    update_medication_window.delete(*update_medication_window.get_children())
    for medication_name, dose_name, date_name, current_time in saved_data_medication:
        correct_format_date = datetime.strptime(
            date_name, '%m/%d/%Y').strftime('%B %d, %Y') if date_name else '-'
        medication_name = medication_name if medication_name else '-'
        dose_name = dose_name if dose_name else '-'
        current_time = current_time if current_time and current_time != 'None' else '-'
        update_medication_window.insert("", "end", values=(
            medication_name, dose_name, current_time, correct_format_date))
def items_deleting():
    for piece in update_medication_window.selection():
        saved_data_medication.pop(int(update_medication_window.index(piece)))
        update_medication_window.delete(piece)
    with open(my_file, "w") as f:
        for medication_name, dose_name, date_name, current_time in saved_data_medication:
            f.write(f"{medication_name}|{dose_name}|{date_name}|{current_time}\n")
def clear_all_items():
    global saved_data_medication
    saved_data_medication = []
    update_medication_window.delete(*update_medication_window.get_children())
    with open(my_file, "w") as f:
        pass
def validate_medication_entry(new_value):
    return new_value.isalpha() if new_value else True
def validate_dose_entry(new_value):
    return new_value.isdigit() if new_value else True
def destroy_window():
    my_app.destroy()
def move_window(event):
    global pos_x, pos_y
    x, y = event.x_root, event.y_root
    if pos_x is not None and pos_y is not None:
        dx, dy = x - pos_x, y - pos_y
        x_pos, y_pos = my_app.winfo_x(), my_app.winfo_y()
        new_x, new_y = x_pos + dx, y_pos + dy
        if y_pos < event.y_root < y_pos + 30:
            my_app.geometry(f"+{new_x}+{new_y}")
    pos_x, pos_y = x, y
def stop_window_move(event):
    global pos_x, pos_y
    pos_x, pos_y = None, None
pos_x, pos_y = None, None

##################################################################################################################################################

my_app = ctk.CTk()
my_app.geometry("910x665")
my_app.resizable(False, False)
my_app.title("Medication Reminder")

my_app.wm_attributes('-transparentcolor', 'grey')
my_app.overrideredirect(1)

my_app.bind("<B1-Motion>", move_window)
my_app.bind("<ButtonRelease-1>", stop_window_move)

messagebox.showinfo("Welcome to Medication Reminder App!", "You can move the window by clicking and dragging the edge of the window.")

######################################        Frame #1 / CLOSE BUTTON          ################################################################
frame = ctk.CTkFrame(master=my_app, width=390, height=310)
frame.place(x=20, y=30)
frame_color = frame['bg']

####################  CLOSE BUTTON ICON #################################################
button_image = ctk.CTkImage(Image.open("icons\icon.png"), size=(88, 88))
image_button = ctk.CTkButton(master=my_app, hover_color=frame_color,command=destroy_window , text=None, image=button_image, width = 1, height = 1, fg_color=(frame_color))
image_button.place(x=810, y= 8)
###########################################################################################################################

medication = ctk.CTkLabel(master=frame, text='Medication')
medication.place(x=15, y=10)

medication_entry = ctk.CTkEntry(master=frame, placeholder_text="Medication Name")
medication_entry.place(x=90, y=10)
medication_entry.configure(validate="key", validatecommand=(medication_entry.register(validate_medication_entry), "%P"))

ToolTip(medication_entry, msg="Numbers are not allowed", follow=True, delay = 0, parent_kwargs={"bg": "#1c1c1c", "padx": 5, "pady": 5},
        fg="#ffffff", bg="#1c1c1c")
###########################################################################################################################
dose = ctk.CTkLabel(master=frame, text='Dose')
dose.place(x=25, y=50)

dose_entry = ctk.CTkEntry(master=frame, placeholder_text="Doses")
dose_entry.place(x=90, y=50)
dose_entry.configure(validate="key", validatecommand=(dose_entry.register(validate_dose_entry), "%P"))

ToolTip(dose_entry, msg="Only date is allowed", follow=True, delay = 0, parent_kwargs={"bg": "#1c1c1c", "padx": 5, "pady": 5},
        fg="#ffffff", bg="#1c1c1c")
###########################################################################################################################
time_label = ctk.CTkLabel(master=frame, text='Time')
time_label.place(x=25, y=90)

var_for_time = tk.StringVar()
time_entry = ctk.CTkEntry(master=frame,textvariable=var_for_time , state='readonly', placeholder_text="Time")
time_entry.place(x=90, y=90)

ToolTip(time_entry, msg="Numbers & String not allowed", follow=True, delay = 0, parent_kwargs={"bg": "#1c1c1c", "padx": 5, "pady": 5},
        fg="#ffffff", bg="#1c1c1c")

icon_img4 = Image.open("icons\icon_time.png")
# Define the button image
icon_size4 = (20, 20)
icon_img4 = icon_img4.resize(icon_size4)
button_image4 = ctk.CTkImage(icon_img4, size=(20, 20))

frame_color = frame['bg']
ticons\\icon.pngme_button = ctk.CTkButton(master=frame,image=button_image4, text='Time', width=130, fg_color=(frame_color), command=choose_time)
time_button.place(x=240, y=90)

time_button._image_label.place(x=17, y=3)
time_button._text_label.place(x=icon_size4[0] + 32, y=5)
################################################################################################################################################

date = ctk.CTkLabel(master=frame, text='Date')
date.place(x=25, y=130)

var_for_date = tk.StringVar()
date_entry = ctk.CTkEntry(master=frame, state='readonly', placeholder_text="Date", textvariable=var_for_date)
date_entry.place(x=90, y=130)
ToolTip(date_entry, msg="Only selecting date allowed", follow=True, delay = 0, parent_kwargs={"bg": "#1c1c1c", "padx": 5, "pady": 5},
        fg="#ffffff", bg="#1c1c1c")


icon_img5 = Image.open("icons\date_icon.png")
# Define the button image
icon_size5 = (20, 20)
icon_img5 = icon_img5.resize(icon_size5)
button_image5 = ctk.CTkImage(icon_img5, size=(20, 20))

date_button = ctk.CTkButton(master=frame,image=button_image5,width=130, text='Date', fg_color=(frame_color), command=choose_date)
date_button.place(x=240, y=130)
date_button._image_label.place(x=17, y=3)
date_button._text_label.place(x=icon_size4[0] + 32, y=5)
#######################################################################################################################################################

card_frame = ctk.CTkFrame(master=frame, width=270, height=100, border_width=2, border_color="#c9c9c9")
card_frame.place(x=30, y=186)

info = ctk.CTkLabel(master=card_frame, text=' Fill Out All The Fields\nUse The Time/Date Buttons\nTo Select The Date/Time', bg_color='transparent', text_color='#C8BBB7', font=('Helvetica', 17))
info.place(x=30, y=19)

#####################################      FRAME2             #####################################################################
frame2 = ctk.CTkFrame(master=my_app, width=200, height=140)
frame2.place(x=440, y=30)

#################################    SAVE BUTTON           ###########################################################################################################
# Load the image
icon_img = Image.open("icons\save_icon.png")
# Define the button image
icon_size = (20, 20)
icon_img = icon_img.resize(icon_size)
button_image = ctk.CTkImage(icon_img, size=(20, 20))

save_button = ctk.CTkButton(master=frame2, image=button_image, width=130, text='Save',fg_color=(frame_color), command=save_information)
save_button.place(x=30, y=10)
save_button._image_label.place(x=11, y=3)
save_button._text_label.place(x=icon_size[0] + 32, y=5)
###########################     DELETE BUTTON WITH ICON                      ###########################################################################################
icon_img1 = Image.open("icons\delete_icon.png")
icon_size1 = (20, 20)
icon_img1 = icon_img1.resize(icon_size1)
button_image1 = ctk.CTkImage(icon_img1, size=(25, 25))

delete_button = ctk.CTkButton(master=frame2, image=button_image1, width=130, text='Delete',fg_color=(frame_color), command=items_deleting)
delete_button.place(x=30, y=50)
delete_button._image_label.place(x=10, y=1)
delete_button._text_label.place(x=icon_size[0] + 32, y=5)

############################         CLEAR_ALL BUTTON AND ICON            #########################################################################################################
icon_img2 = Image.open("icons\clear_all.png")
# Define the button image
icon_size2 = (20, 20)
icon_img2 = icon_img2.resize(icon_size2)
button_image2 = ctk.CTkImage(icon_img2, size=(25, 25))

clear_all_button = ctk.CTkButton(master=frame2, image=button_image2, width=130, text='Clear All',fg_color=(frame_color), command=clear_all_items)
clear_all_button.place(x=30, y=90)
clear_all_button._image_label.place(x=13, y=1)
clear_all_button._text_label.place(x=icon_size[0] + 32, y=5)

############################################                    TREEVIEW                 ####################################################################

frame1 = ctk.CTkFrame(master=my_app, width=850, height=270)
frame1.place(x=20, y=370)

frame_color = frame['bg']
style = ttk.Style()
style.theme_use('clam')
style.map('Treeview', background=[('selected', '#2e2726')])
style.configure('Treeview', font=('Helvetica', 12), background = frame_color, 
                foreground= 'white', fieldbackground= frame_color ,rowheight=20, columnwidth=20)

update_medication_window = ttk.Treeview(frame1, columns=('Medication', 'Dose', 'Time', 'Date'), show='headings')
update_medication_window.heading('#1', text='Medication')
update_medication_window.heading('#2', text='Dose', anchor='center')
update_medication_window.heading('#3', text='Time', anchor='center')
update_medication_window.heading('#4', text='Date', anchor='center')
# Add the medication data to the treeview
for index, (medication_name, dose_name, date, time) in enumerate(saved_data_medication):
    date_obj = datetime.strptime(date, '%m/%d/%Y')
    date_str = date_obj.strftime('%B %d, %Y')
    update_medication_window.insert(parent='', index=index, values=(medication_name, dose_name, time, date_str))
# Center the text in all columns
update_medication_window.column('0', anchor='center')
update_medication_window.column('1', anchor='center')
update_medication_window.column('2', anchor='center')
update_medication_window.column('3', anchor='center')

# Add the treeview widget to the tkinter window
scrollbar = ttk.Scrollbar(frame1, orient='vertical', command=update_medication_window.yview)
scrollbar.place(x=820, y=20, height=230)
update_medication_window.configure(yscrollcommand=scrollbar.set)
update_medication_window.place(x=20, y=20)
#
# Update the listbox with the saved medication data
listbox_updated()
my_app.mainloop()


