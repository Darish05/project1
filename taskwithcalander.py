from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime, timedelta
from PIL import Image, ImageTk
from tkcalendar import DateEntry

# Declare tasks as global
tasks = []

def list_update():  
    clear_list()  
    
    cursor.execute('SELECT title, due_date, due_time FROM tasks')
    for task in cursor.fetchall():  
        task_listbox.insert('end', f"{task[0]} (Due: {task[1]} {task[2]})")  

def delete_task():  
    global tasks  # Declare tasks as global
    try:  
        selected_index = task_listbox.curselection()
        if not selected_index:  
            messagebox.showinfo('Error', 'No Task Selected. Cannot Delete.')
            return

        task_name = task_listbox.get(selected_index).split(" (Due: ")[0]

        tasks = [task for task in tasks if task[0] != task_name]

        cursor.execute('DELETE FROM tasks WHERE title = %s', (task_name,))
        mydb.commit()

        list_update()

    except Exception as e:  
        messagebox.showinfo('Error', f'Error deleting task: {e}')

def delete_all_tasks():  
    global tasks  
    message_box = messagebox.askyesno('Delete All', 'Are you sure?')  
    
    if message_box == True:  
        tasks.clear()
        cursor.execute('DELETE FROM tasks')
        mydb.commit()
        list_update()  

def clear_list():  
    task_listbox.delete(0, 'end')  

def close():  
    global tasks  
    print(tasks)  
    guiWindow.destroy() 
    

def add_task():  
    global tasks  
    task_string = task_field.get()  
    due_date = due_date_entry.get_date()
    due_time_str = due_time_entry.get()

    try:
        due_time = datetime.strptime(due_time_str, '%I:%M %p').strftime('%H:%M:%S')
    except ValueError:
        messagebox.showinfo('Error', 'Invalid time format. Please use HH:MM AM/PM format.')
        return
    
    if len(task_string) == 0 or due_date is None or len(due_time) == 0:
        messagebox.showinfo('Error', 'Fields are Empty.')  
    else:  
        tasks.append((task_string, due_date, due_time))  
        cursor.execute('INSERT INTO tasks (title, due_date, due_time) VALUES (%s, %s, %s)', (task_string, due_date, due_time))
        mydb.commit()
        list_update()  
        task_field.delete(0, 'end')  
        due_date_entry.set_date(datetime.now())  
        due_time_entry.set('')  

if __name__ == "__main__":  
    guiWindow = Tk()  
    guiWindow.title("Task Manager App")  
    guiWindow.geometry('990x660+50+50')
    guiWindow.configure(bg='#8338ec')
    
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Darish149@5*",
        database="db"
    )

    cursor = mydb.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS tasks (title VARCHAR(255), due_date DATE, due_time TIME)')  

    tasks = []  

    functions_frame = Frame(guiWindow,bg='#8338ec') 
    functions_frame.grid(row=0, column=0, sticky="nsew")

    task_label = Label(functions_frame,text="Enter Task:",bg='#8338ec', font=("arial", "14", "bold"))  
    task_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")  
    
    task_field = Entry(functions_frame, font=("Arial", "14"), width=30)  
    task_field.grid(row=0, column=1, padx=10, pady=10)  

    due_date_label = Label(functions_frame, text="Due Date:",bg='#8338ec', font=("arial", "14", "bold"))  
    due_date_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")  
    
    due_date_entry = DateEntry(functions_frame, font=("Arial", "14"), width=15, date_pattern='yyyy-mm-dd')  
    due_date_entry.grid(row=1, column=1, padx=10, pady=10)  

    due_time_label = Label(functions_frame, text="Due Time:",bg='#8338ec', font=("arial", "14", "bold"))  
    due_time_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")  
    
    due_time_entry = ttk.Combobox(functions_frame, font=("Arial", "14"), width=15, values=['08:00 AM', '09:00 AM', '10:00 AM', '11:00 AM', '12:00 PM', '01:00 PM', '02:00 PM', '03:00 PM', '04:00 PM', '05:00 PM', '06:00 PM', '07:00 PM', '08:00 PM', '09:00 PM'])  
    due_time_entry.grid(row=2, column=1, padx=10, pady=10)  

    add_button =Button(functions_frame, text="Add Task", width=15, bg='#90a955', fg="white", font=("arial", "14", "bold"), command=add_task)  
    add_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)  

    del_button = Button(functions_frame, text="Delete Task", width=15,bg='#90a955', fg="white", font=("arial", "14", "bold"), command=delete_task)  
    del_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)  

    del_all_button = Button(functions_frame, text="Delete All Tasks", width=15, font=("arial", "14", "bold"),bg='#90a955', fg="white", command=delete_all_tasks)  
    del_all_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)  

    exit_button = Button(functions_frame, text="Exit", width=52, bg='#90a955', fg="white", font=("arial", "14", "bold"), command=close)  
    exit_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)  
    
    task_listbox = Listbox(functions_frame, width=60, height=10, font=("bold", 12), selectmode='SINGLE',bg='#8338ec', fg='white')  
    task_listbox.grid(row=0, column=2, rowspan=7, padx=20, pady=10, sticky="ns")  

    guiWindow.mainloop()  

    cursor.close()
    mydb.close()  





   



