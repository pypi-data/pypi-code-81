import os
import site
import time
import tkinter as tk
from datetime import datetime
import pyperclip
valid_input_flag = False
print("copy the zoom link")
if "zoom.us" in pyperclip.paste():
    link_time = ""


    def function_for_time(key=None):
        def function_for_time1(key):
            global valid_input_flag
            try:
                current = str(datetime.now())[11:-10]
                starting_time = e2.get()
                current = current.split(":")
                if ":" in starting_time:
                    starting_time = starting_time.split(":")
                else:
                    starting_time = starting_time.split()
                current_total_minutes = int(current[0]) * 60 + int(current[1])
                total_minutes_time_to_start = int(starting_time[0]) * 60 + int(starting_time[1])
                minutes_to_start = total_minutes_time_to_start - current_total_minutes
                if minutes_to_start < 0 or len(starting_time[0]) > 2 or len(starting_time[1]) > 2 or int(starting_time[1]) > 60 or int(starting_time[0]) > 24:
                    link_detected_label.configure(text=f"wrong time input")
                    valid_input_flag = False
                    return
                link_detected_label.configure(text=f"opening in {minutes_to_start // 60} hours and {minutes_to_start % 60} minutes")
                valid_input_flag = True
            except:
                link_detected_label.configure(text=f"time format [HH:MM]")
                valid_input_flag = False

        master.after(1, function_for_time1, key)


    def get_text(args=None):
        global link_time
        link_time = e2.get()
        global link
        link = str(e1.get())
        global master
        global valid_input_flag
        if not valid_input_flag or not link_time:
            link_detected_label.configure(text=f"wrong time input")
            return

        master.destroy()


    master = tk.Tk()
    master.title('auto zoom join by snir')
    master.configure(background="#2A3240")
    master.iconbitmap(fr"{site.getsitepackages()[1]}\snirzoom\icon.ico")
    ok_button = tk.Button(master, text='OK', command=get_text, width=3, height=1, font=("Consolas", 35))
    ok_button.place(x=850, y=422)
    ok_button.configure(background="#3EDB14", activebackground="#33CC78")
    label_link = tk.Label(master, text="enter link:", height=5, font=("Consolas", 32))
    label_link.grid(row=0)
    label_link.configure(background="#2A3240")
    label_time = tk.Label(master, text="enter time:", height=5, font=("Consolas", 32))
    link_detected_label = tk.Label(master, text="", height=1, font=("Consolas", 26))
    link_detected_label.place(x=250, y=260)
    link_detected_label.configure(fg="#1AAFF9", background="#2A3240")
    label_time.grid(row=1)
    label_time.configure(background="#2A3240")
    e1 = tk.Entry(master, font=("Consolas", 32), width="30")
    e2 = tk.Entry(master, font=("Consolas", 32), width="30")
    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)
    e1.configure(background="#39455B")
    e2.configure(background="#39455B")
    link = pyperclip.paste()
    print("got the link from the clipboard:", link)
    link_detected_label.configure(text="detected link from clipboard")
    e1.delete(0, tk.END)
    e1.insert(0, pyperclip.paste())
    e2.bind("<Key>", function_for_time)
    e2.bind("<Return>", get_text)
    e2.focus()
    tk.mainloop()
    if link_time[1] == " ":
        link_time = "0" + link_time
    print("time:", link_time.replace(" ", ":"))

    while str(datetime.now())[11:-10] != link_time.replace(" ", ":"):
        time.sleep(1)


    os.system(f"start {link}")
    print("zoom meeting has started")
while pyperclip.waitForNewPaste():
    if "zoom.us" in pyperclip.paste():
        link_time = ""


    def function_for_time(key=None):
        def function_for_time1(key):
            global valid_input_flag
            try:
                current = str(datetime.now())[11:-10]
                starting_time = e2.get()
                current = current.split(":")
                if ":" in starting_time:
                    starting_time = starting_time.split(":")
                else:
                    starting_time = starting_time.split()
                current_total_minutes = int(current[0]) * 60 + int(current[1])
                total_minutes_time_to_start = int(starting_time[0]) * 60 + int(starting_time[1])
                minutes_to_start = total_minutes_time_to_start - current_total_minutes
                if minutes_to_start < 0 or len(starting_time[0]) > 2 or len(starting_time[1]) > 2 or int(starting_time[1]) > 60 or int(starting_time[0]) > 24:
                    link_detected_label.configure(text=f"wrong time input")
                    valid_input_flag = False
                    return
                link_detected_label.configure(text=f"opening in {minutes_to_start // 60} hours and {minutes_to_start % 60} minutes")
                valid_input_flag = True
            except:
                link_detected_label.configure(text=f"time format [HH:MM]")
                valid_input_flag = False

        master.after(1, function_for_time1, key)


    def get_text(args=None):
        global link_time
        link_time = e2.get()
        global link
        link = str(e1.get())
        global master
        global valid_input_flag
        if not valid_input_flag or not link_time:
            link_detected_label.configure(text=f"wrong time input")
            return

        master.destroy()



    master = tk.Tk()
    master.title('auto zoom join by snir')
    master.configure(background="#2A3240")
    master.iconbitmap(fr"{site.getsitepackages()[1]}\snirzoom\icon.ico")
    ok_button = tk.Button(master, text='OK', command=get_text, width=3, height=1, font=("Consolas", 35))
    ok_button.place(x=850, y=422)
    ok_button.configure(background="#3EDB14", activebackground="#33CC78")
    label_link = tk.Label(master, text="enter link:", height=5, font=("Consolas", 32))
    label_link.grid(row=0)
    label_link.configure(background="#2A3240")
    label_time = tk.Label(master, text="enter time:", height=5, font=("Consolas", 32))
    link_detected_label = tk.Label(master, text="", height=1, font=("Consolas", 26))
    link_detected_label.place(x=250, y=260)
    link_detected_label.configure(fg="#1AAFF9", background="#2A3240")
    label_time.grid(row=1)
    label_time.configure(background="#2A3240")
    e1 = tk.Entry(master, font=("Consolas", 32), width="30")
    e2 = tk.Entry(master, font=("Consolas", 32), width="30")
    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)
    e1.configure(background="#39455B")
    e2.configure(background="#39455B")
    link = pyperclip.paste()
    print("got the link from the clipboard:", link)
    link_detected_label.configure(text="detected link from clipboard")
    e1.delete(0, tk.END)
    e1.insert(0, pyperclip.paste())
    e2.bind("<Key>", function_for_time)
    e2.bind("<Return>", get_text)
    e2.focus()
    tk.mainloop()
    if link_time[1] == " ":
        link_time = "0" + link_time
    

    while str(datetime.now())[11:-10] != link_time.replace(" ", ":"):
        time.sleep(1)


    os.system(f"start {link}")
    print("zoom meeting has started")