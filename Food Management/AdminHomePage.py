from BackgroundPage import *
from Components.ButtonComponent import WhiteButton
from DatabaseHelper import *
from Components.table import SimpleTable
from Components.MessageComponent import WhiteMessage
from tkinter import messagebox
from AdminAnalytics import Analytics
from Queries.Admin import *


class AdminHomePage(BackgroundPage):
    def __init__(self, root, admin_details):
        print("Admin home page called")
        super().__init__(root)
        self.root.state('zoomed')  # Maximize the screen
        # Dict received from DATABASE. Eg=> {id:2, name:'Ritesh', password:'SGT', email:'riteshagicha@gmail.com', photo:'RiteshPic3.jpg'}
        self.details = admin_details
        # Dictionary to store the pending order checkbox IntVars
        self.dct_IntVar = {}

        self.admin_page = WhiteMessage(self.f, text="Admin Page")
        self.admin_page.place(x=320, y=20)
        self.add_admin_details()
        self.add_buttons()

    def add_admin_details(self):
        # Add image of admin
        # Add Name of admin as Message
        # Add email of admin as Message
        print(self.details)
        self.admin_raw_image = Image.open('images/' + self.details.get("AdminPhoto"))
        self.admin_raw_image.resize((100, 180))
        self.profile_pic = ImageTk.PhotoImage(self.admin_raw_image)
        # ensure this size is same as image size, also we can use label instead of this
        self.c = Canvas(self.f, width=100, height=180)
        # give the starting cordinates wrt canvas i.e 0,0
        self.canvas_pic = self.c.create_image(0, 0, image=self.profile_pic, anchor=NW)
        self.c.place(x=40, y=100)
        # message that displays admin's name
        self.admin_name = WhiteMessage(self.f, text="Name= " + self.details["AdminName"], width=200)
        self.admin_name.place(x=40, y=300)
        # message that displays admin's email address
        self.admin_email = WhiteMessage(self.f, text="Email " + self.details["AdminEmail"], width=300)
        self.admin_email.place(x=40, y=350)

    def add_buttons(self):
        # Add 3 buttons
        # View pending order
        # View recently completed order
        # logout

        # doesn't matter, you can add to the frame or panel(Label- for image)
        self.pending_button = WhiteButton(self.f, "View Pending Orders", self.view_pending_orders)
        self.pending_button.place(x=400, y=90)
        self.completed_button = WhiteButton(self.f, "View Recent Completed Orders", self.view_completed_orders)
        self.completed_button.place(x=600, y=90)
        self.logout = WhiteButton(self.f, "Logout", self.admin_logout, width=10)
        self.logout.place(x=800, y=20)
        self.b_analytics = WhiteButton(self.f, "Analytics", Analytics)
        self.b_analytics.place(x=50, y=500)

    def view_completed_orders(self):
        # same as pending orders, only diff is we dont need checkbutton here
        query = Query.RECENTLY_COMPLETED_ORDERS
        result = DatabaseHelper.get_all_data(query)
        self.orders_table = SimpleTable(self.f, rows=len(result), columns=len(result[0]), height=500, width=660)
        self.orders_table.place(x=500, y=200)
        self.orders_table.grid_propagate(0)

        for r in range(len(result)):  # r  in range(4)--> r=0,1,2,3
            for c in range(len(result[0])):  # c in range(2) c-> 0,1
                self.orders_table.set(row=r, column=c, value=result[r][c])

    def execute_order(self):
        selected_items = []
        for key, value in self.dct_IntVar.items():
            if (value.get() == 1):
                selected_items.append(key)
                value.set(0)
        print(selected_items)
        if (len(selected_items) == 0):
            messagebox.showwarning("No order", "Please select atleast one food order to execute")
        else:
            query = Query.EXECUTE_ORDERS
            DatabaseHelper.execute_all_data_multiple_input(query, selected_items)
            messagebox.showinfo("Success", f"Order Id(s) {selected_items} executed")
            self.view_pending_orders()

    def view_pending_orders(self):
        # Add execute button
        # Add table that shows pending orders with checkbutton
        self.execute_button = WhiteButton(self.f, "Execute Order", self.execute_order)
        self.execute_button.place(x=500, y=150)
        query = Query.PENDING_ORDERS
        result = DatabaseHelper.get_all_data(query)
        print(result)

        self.orders_table = SimpleTable(self.f, rows=len(result), columns=len(result[0]), height=500, width=650)
        self.orders_table.place(x=500, y=200)
        self.orders_table.grid_propagate(0)
        self.text_font = ("MS Serif", 12)
        # (('FoodOrderId', 'CustomerName', 'FoodDetails', 'FoodTotal', 'OrderDate'),
        #  (19, 'Agicha', 'Pizza,Cheese Pizza,Chunky Basil Pasta', 1150, datetime.date(2020, 4, 12)),
        #  (20, 'Agicha', 'Sizzling brownie,Vanilla,Waffles,Triple trouble', 800, datetime.date(2020, 4, 12)),
        #  (21, 'Agicha', 'Pizza', 350, datetime.date(2020, 4, 12)),
        #  (22, 'Agicha', 'Vanilla,Waffles,Triple trouble', 600, datetime.date(2021, 5, 8)),
        #  (23, 'Agicha', 'Vanilla,Waffles,Triple trouble', 600, datetime.date(2021, 5, 8)),
        #  (24, 'Agicha', 'Pizza,Cheese Pizza', 800, datetime.date(2021, 5, 8)))

        for i in range(1, len(result)):
            # store FoodOrderID as key and a checkbutton variable as value
            self.dct_IntVar[result[i][0]] = IntVar()

        for r in range(len(result)):
            for c in range(len(result[0])):
                if (c == 0 and r != 0):
                    # Put checkbutton in the all first column apart from the first row
                    check_b = Checkbutton(self.orders_table, text=result[r][c], font=self.text_font,
                                          variable=self.dct_IntVar[result[r][c]])
                    self.orders_table.set(row=r, column=c, value=result[r][c], widget=check_b)
                else:
                    self.orders_table.set(row=r, column=c, value=result[r][c])

    def admin_logout(self):
        import MainPage as main
        self.f.destroy()
        main.MainPage(self.root)


if (__name__ == "__main__"):
    root = Tk()
    admin_details = {'AdminId': 2, 'AdminName': 'Ritesh', 'AdminPassword': 'SGT',
                     'AdminEmail': 'riteshagicha@gmail.com',
                     'AdminPhoto': 'RiteshPic3.jpg'}
    a = AdminHomePage(root, admin_details)
    root.mainloop()

# 19,20
# mapping = {
# 19: IntVar(),
# 20:IntVar()
# }
# parameters= []
# c1=Checkbutton(variable=mapping[19])
# c2=Checkbutton(variable=mapping[20])
#
# for key in mapping:# 19,20
#     value = mapping[key]
#     if value.get()==1:
#         parameters.append(key)
