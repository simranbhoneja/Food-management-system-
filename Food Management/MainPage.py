from BackgroundPage import *
from tkinter import messagebox
from Components.ButtonComponent import GrayButton
from DatabaseHelper import *
from Components.MessageComponent import WhiteMessage
from SignUpWindowPage import *
from LoginWindowPage import *


class MainPage(BackgroundPage):
    def __init__(self, root):
        # Calls the parent BackgroundPage and now MainPage adds its own widgets using add_widgets()
        super().__init__(root)
        self.root.geometry('900x600')
        # this is the reverse of 'zoomed' effect in AdminPage
        self.root.state('normal')
        self.add_widgets()

    def add_widgets(self):
        # Add 2 buttons-> Admin and user
        # Add 1 button-> new user
        # Add contact details
        self.admin_button = GrayButton(self.panel, "Admin login", lambda: Login("Admin", self))
        self.admin_button.place(x=450, y=150)
        self.user_button = GrayButton(self.panel, "User login", lambda: Login("User", self))
        self.user_button.place(x=620, y=150)
        self.new_user_button = GrayButton(self.panel, "New user? Sign up here", SignUp, borderwidth=2, relief=RIDGE)
        self.new_user_button.place(x=550, y=220)

        self.contact = WhiteMessage(self.f, text="Contact Details Here!")
        self.contact_detail = WhiteMessage(self.f,
                                           text=" Foodzapp Services,\n 221B Baker Street\n London\n +44 20 7234 3456",
                                           font=("Times New Roman", 15, "bold", "italic"))
        self.contact.place(x=500, y=320)
        self.contact.bind("<Button-1>", self.show_contact_details)

    def show_contact_details(self, event):
        self.contact_detail.place(x=500, y=400)

    def redirect_to_page(self, result, login_type):
        self.f.destroy()
        if login_type == "Admin":
            import AdminHomePage as admin
            admin.AdminHomePage(self.root, result)
        elif login_type == "User":
            import CustomerHomePage
            CustomerHomePage.CustomerHomePage(self.root, result)


if (__name__ == "__main__"):
    root = Tk()
    m = MainPage(root)
    root.mainloop()
