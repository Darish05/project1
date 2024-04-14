from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
import pymysql
import subprocess

#functions
def login_user():
    if usernameE.get()=='' or pwE.get()=='':
        messagebox.showerror('Error','All fields are required')
    else:
        try:
            con = pymysql.connect(host='localhost', user='root', password='Darish149@5*')
            mycursor = con.cursor()
        except pymysql.Error as e:
            messagebox.showerror('Error', f'Connection error: {e}')
            return
        try:
            mycursor.execute('USE db')
            mycursor.execute('SELECT * FROM data WHERE username=%s AND password=%s', (usernameE.get(), pwE.get()))
            row = mycursor.fetchone()
            if row:
                messagebox.showinfo('Welcome', 'Login successful')
                ob.destroy()  # Close the login window
                subprocess.Popen(['python', 'notificationeg.py'])  # Run taskwithcalander.py as a separate process
            else:
                messagebox.showerror('Error', 'Invalid username or password')
        except pymysql.Error as e:
            messagebox.showerror('Error', f'Database error: {e}')
        finally:
            mycursor.close()
            con.close()
                
#fn for username entry
def on_enter(event):
    if usernameE.get()=='Username':
        usernameE.delete(0,END)
#fn for password entry
def pw_enter(event):
    if pwE.get()=='Password':
        pwE.delete(0,END)
#to change the eye img and to hide the password
def hide():
    openeye.config(file='closeye.png')
    pwE.config(show='*')
    eyebutton.config(command=show)
def show():
    openeye.config(file="openeye.png")
    pwE.config(show='')
    eyebutton.config(command=hide)
  
def signup_page():
    ob.destroy()
    import signup

def mainpg():
    import taskwithcalander
    

    
#GUI part
ob=Tk()
ob.resizable(0,0)
ob.title('Login Page')
ob.geometry('990x660+50+50')
bgimg=ImageTk.PhotoImage(file='img.png')
bglable=Label(ob,image=bgimg)
bglable.grid(row=0,column=0)
#text lable
heading=Label(ob,text='USER LOGIN',font=('Helvetica 16 bold italic',23,'bold'),bg ='#9b5de5',)
heading.place(x=100,y=85 )

#entry fields
#user name entry field
usernameE=Entry(ob,width=25,font=('Helvetica 16 bold italic',13),bd=0,fg='white',bg='#9b5de5')
usernameE.place(x=100,y=170)
usernameE.insert(0,'User name')
usernameE.bind('<FocusIn>',on_enter)
#for the line in the entry
frame1=Frame(ob,width=230,height=2).place(x=100,y=190)
#password entry field
pwE=Entry(ob,width=25,font=('Helvetica 16 bold italic',13),bd=0,fg='white',bg='#9b5de5')
pwE.place(x=100,y=220)
pwE.insert(0,'Password')
pwE.bind('<FocusIn>',pw_enter)
frame2=Frame(ob,width=230,height=2).place(x=100,y=240)
#eyebutton
openeye=PhotoImage(file='openeye.png')
eyebutton=Button(ob,image=openeye,bd=0,bg='#9b5de5',activebackground='firebrick1',cursor='hand2',command=hide)
eyebutton.place(x=302,y=220)
'''forget password button
forgetbutton=Button(ob,text='Forget Password',bd=0,bg='#9b5de5',activebackground='#9b5de5',cursor='hand2',font=('Helvetica 16 bold italic',9,'bold'),fg='white',activeforeground='red')
forgetbutton.place(x=265,y=255)'''
#login button
loginbutton=Button(ob,text='Login',font=('Open Sans',16,'bold'),fg='white',bg='red',activeforeground='#9b5de5',activebackground='white',cursor='hand2',bd=0,width=20,command=login_user).place(x=90,y=300)
#or lable 
orlable=Label(ob,text='-----------------OR-----------------',font=('Open Sans',16),fg='white',bg='#9b5de5').place(x=95,y=365)
#logos
google_logo=PhotoImage(file='google.png')
googlable=Label(ob,image=google_logo,bg='#9b5de5').place(x=175,y=420)
twitter_logo=PhotoImage(file='twitter.png')
twitlable=Label(ob,image=twitter_logo,bg='#9b5de5').place(x=240,y=420)
#create new one lable
signuplable=Label(ob,text='Dont have an account?',font=('Open Sans',10,'bold underline'),fg='white',bg='#9b5de5').place(x=120,y=470)
#sign up button

signupbutton=Button(ob,text='Sign Up',font=('Open Sans',10,'bold'),fg='white',bg='#9b5de5',activeforeground='blue',activebackground='white',cursor='hand2',bd=0,command=signup_page).place(x=280,y=470)

ob.mainloop()
