from tkinter import *
from tkinter import messagebox
from DatabaseHelper import *


class Login:
    def __init__(self, login_type, main_page):
        # Creates a temporary window to login
        # 2 labels-> username,password
        # 2 entry-> take username, password
        # 2 Button-> submit, reset
        self.login_window = Toplevel()
        self.login_type = login_type
        self.login_window.title(login_type)
        self.main_page = main_page
        f = Frame(self.login_window, height=200, width=400)
        l1 = Label(f, width=20, text="Enter username: ")
        # storing this inside self because we need this later to get data
        self.e_username = Entry(f, width=30, fg='black', bg='white')
        # activative the cursor here
        self.e_username.focus_set()
        self.e_password = Entry(f, width=30, fg='black', bg='white', show='*')
        l2 = Label(f, width=20, text="Enter password: ")
        l1.grid(row=1, column=1, padx=10, pady=10)
        l2.grid(row=2, column=1, padx=10, pady=10)
        self.e_username.grid(row=1, column=4, padx=10, pady=10)
        self.e_password.grid(row=2, column=4, padx=10, pady=10)
        b1 = Button(f, text="Submit", height=2, width=10, command=self.validate)
        # # Whenever enter is pressed anywhere on this temporary root, call my validate function.
        # self.login_window.bind('<Return>', lambda event: self.validate())
        b1.grid(row=3, column=1, padx=10, sticky='e')
        b2 = Button(f, text="Reset", height=2, width=10, command=self.reset)
        b2.grid(row=3, column=4, padx=10, sticky='w')
        f.pack()
        f.grid_propagate(0)

    def reset(self):
        self.e_username.delete(0, END)
        self.e_password.delete(0, END)

    def validate(self):
        username = self.e_username.get()
        pwd = self.e_password.get()
        if (self.login_type == "Admin"):
            query = "Select * from world.Admin where AdminName= %s and AdminPassword=%s"
        else:
            query = "Select * from world.Customer where CustomerName= %s and CustomerPassword=%s"
        parameters = (username, pwd)
        result = DatabaseHelper.get_data(query, parameters)
        print(username)
        print(pwd)
        if (result is None):
            messagebox.showerror("Login Failed", "Incorrect credentials")
            self.login_window.tkraise()
            self.reset()
            self.e_username.focus()
        else:
            messagebox.showinfo('Login Success', "Login successfuly completed")

            # Destorying the temporary window created for login
            self.login_window.destroy()
            self.main_page.redirect_to_page(result, self.login_type)
            # self.f.destroy()
            # the type of login was admin so go to adminhomepage
