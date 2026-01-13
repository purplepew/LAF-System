#from PIL import Image
import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, filedialog

# IMPORT FROM BACKEND
from backend.lib.queries.items import get_all_items
from backend.lib.mutations.items import create_new_item
from backend.lib.queries.items import get_all_items
from backend.lib.utils import ensure_tables

# make sure database is set up
ensure_tables()



ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

def browse_image():
    filename = filedialog.askopenfilename(
        title="Select Image",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif *.bmp")]
    )
    if filename:
        image_var.set(filename)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Frame Switching")
        self.geometry("1000x600")
        self.resizable(False,False)

        # Create frames
        self.login_frame = LoginFrame(self)
        self.signup_frame = SignupFrame(self)
        self.userprofile_frame = UserProfileFrame(self)
        self.dashboard_frame = DashboardFrame(self)
        self.viewlostitem_frame = ViewLostItemFrame(self)
        self.reportmissingitem_frame = ReportMissingItemFrame(self)

        # self.login_frame.grid(row=0, column=0, sticky="nsew")
        # self.signup_frame.grid(row=0, column=0, sticky="nsew")
        # self.dashboard_frame.grid(row=0, column=0, sticky="nsew")

        # Show login first
        self.show_frame(self.login_frame)

    def show_frame(self, frame):
        frame.tkraise()

         # Check if the frame has a "load_data" function
        # If yes, run it to refresh the table
        if hasattr(frame, "load_data"):
            frame.load_data()


class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.place(relwidth=1, relheight=1)

        ctk.CTkLabel(self, font=("Poppins", 40, "bold"),text="Lost and Found System", fg_color="transparent").pack( pady=50)

        ctk.CTkLabel(self, font=("Poppins", 25,"bold"),text="Login", fg_color="transparent").pack()

        loginUsername = ctk.CTkEntry(self, font=("Poppins", 15),width=240, height=40,placeholder_text="Username")
        loginUsername.pack(pady=8)

        loginPassword = ctk.CTkEntry(self, font=("Poppins", 15),width=240, height=40,placeholder_text="Password")
        loginPassword.pack(pady=8)

        # Use CTkButton instead of tkinter Button
        button = ctk.CTkButton(master=self, font=("Poppins", 15), fg_color="#2b9348", width=240, height=40, hover=True, text="Login", command=lambda: parent.show_frame(parent.dashboard_frame))
        button.pack(pady=8)

        button = ctk.CTkButton(master=self, font=("Poppins", 15), fg_color="#2b9348", width=240, height=40, hover=True, text="Sign Up", command=lambda: parent.show_frame(parent.signup_frame))
        button.pack(pady=8)

        # ctk.CTkButton(
        #     self,
        #     text="Login",
        #     command=lambda: 
        # ).pack()








class SignupFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.place(relwidth=1, relheight=1)

        ctk.CTkLabel(self, font=("Poppins", 40, "bold"),text="Lost and Found System", fg_color="transparent").pack(pady=50)
        ctk.CTkLabel(self, font=("Poppins", 23,"bold"),text="Create an Account", fg_color="transparent").pack()
        signupUsername = ctk.CTkEntry(self, font=("Poppins", 15),width=240, height=40,placeholder_text="Username")
        signupUsername.pack(pady=8)
        signupPassword = ctk.CTkEntry(self, font=("Poppins", 15),width=240, height=40, placeholder_text="Password")
        signupPassword.pack(pady=8)
        signupEmail = ctk.CTkEntry(self, font=("Poppins", 15),width=240, height=40,placeholder_text="Email")
        signupEmail.pack(pady=8)
        button = ctk.CTkButton(master=self, font=("Poppins", 15),width=240, height=40, hover=True, text="Register", command=lambda: parent.show_frame(parent.login_frame))
        button.pack(pady=10)

        ctk.CTkButton(
            self,
            text="Logout",
            command=lambda: parent.show_frame(parent.login_frame)
        ).pack()





























class DashboardFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.place(relwidth=1, relheight=1)

        #title
        ctk.CTkFrame(self, width=800, height=70, fg_color="#2b9348", corner_radius=0).place(x=201, y=0)
        ctk.CTkFrame(self, width=200, height=330, fg_color="#2b9348", corner_radius=0).place(x=0, y=275)

        ctk.CTkLabel(self, font=("Poppins", 20, "bold"),text="Lost and Found System", fg_color="#2b9348", ).place(x=230, y=17)
        
        #Dashboard
        ctk.CTkLabel(self, font=("Poppins", 15, "bold"),text="Dashboard", fg_color="transparent", ).place(x=220, y=85)

        ctk.CTkFrame(self, width=240, height=150, fg_color="#ffadad").place(x=220, y=130)

        ctk.CTkLabel(
            self, 
            font=("Poppins", 30, "bold"),
            text="12", 
            fg_color="#ffadad",
            #text_color="black", 
            ).place(x=235, y=135)
        
        ctk.CTkLabel(
            self, 
            font=("Poppins", 13, "bold"),
            text="Your Claimed Items", 
            fg_color="#ffadad",
            #text_color="black", 
            ).place(x=235, y=175)
        
        ctk.CTkFrame(self, width=240, height=150, fg_color="#cdb4db").place(x=480, y=130)

        ctk.CTkLabel(
            self, 
            font=("Poppins", 30, "bold"),
            text="55", 
            fg_color="#cdb4db",
            #text_color="black", 
            ).place(x=495, y=135)
        
        ctk.CTkLabel(
            self, 
            font=("Poppins", 13, "bold"),
            text="Users Claimed Items", 
            fg_color="#cdb4db",
            #text_color="black", 
            ).place(x=495, y=175)


        ctk.CTkFrame(self, width=240, height=150, fg_color="#a2d2ff").place(x=740, y=130)
        
        ctk.CTkLabel(
            self, 
            font=("Poppins", 30, "bold"),
            text="17", 
            fg_color="#a2d2ff",
            #text_color="black", 
            ).place(x=755, y=135)
        
        ctk.CTkLabel(
            self, 
            font=("Poppins", 13, "bold"),
            text="View Pending Claims", 
            fg_color="#a2d2ff",
            #text_color="black", 
            ).place(x=755, y=175)

        #TABLE
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="#2b9348", font=("Poppins", 10, "bold"), foreground="white")
        #style.configure("Treeview", background="#2b9348")
        
        columns = ("Item Name", "Landmark", "Date Found", "Time Found")
        tree = ttk.Treeview(self, columns=columns, show="headings", height=20)
        tree.place(x=210, y=300)
        
        for col in columns:
            tree.heading(col, text=col.capitalize() )
            tree.column(col, width=195)

        # --- ADDED CODE START ---
        items = get_all_items()

        for item in items:
            # We only need the first 4 items: Name, Landmark, Date, Time
            # item[0] is Name, item[1] is Landmark, etc.
            row_data = (item[0], item[1], item[2], item[3])
            
            tree.insert("", "end", values=row_data)
        # --- ADDED CODE END ---

        scroll_y = tk.Scrollbar(self, orient=tk.VERTICAL, command=tree.yview)
        scroll_y.place(x=975, y=335, height=265)
        tree.configure(yscrollcommand=scroll_y.set)

        ctk.CTkButton(
            self,
            text="MENU",
            font=("Poppins", 15, "bold"),
            height=70,
            width=200,
            fg_color="#2b9348",
            corner_radius=0,
            command=lambda: parent.show_frame(parent.login_frame)
        ).place(x=0, y=0)

        ctk.CTkButton(
            self,
            text="User Profile",
            font=("Poppins", 13, "bold"),
            height=50,
            width=200,
            fg_color="#2b9348",
            corner_radius=0,
            command=lambda: parent.show_frame(parent.userprofile_frame)
        ).place(x=0, y=71)

        ctk.CTkButton(
            self,
            text="Dashboard",
            font=("Poppins", 13, "bold"),
            height=50,
            width=200,
            fg_color="#2b9348",
            corner_radius=0,
            command=lambda: parent.show_frame(parent.dashboard_frame)
        ).place(x=0, y=122)

        ctk.CTkButton(
            self,
            text="View Lost Items",
            font=("Poppins", 13, "bold"),
            height=50,
            width=200,
            fg_color="#2b9348",
            corner_radius=0,
            command=lambda: parent.show_frame(parent.viewlostitem_frame)
        ).place(x=0, y=173)

        ctk.CTkButton(
            self,
            text="Report Missing Items",
            font=("Poppins", 13, "bold"),
            height=50,
            width=200,
            fg_color="#2b9348",
            corner_radius=0,
            command=lambda: parent.show_frame(parent.reportmissingitem_frame)
        ).place(x=0, y=224)















class UserProfileFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.place(relwidth=1, relheight=1)


        ctk.CTkFrame(self, width=800, height=70, fg_color="#2b9348", corner_radius=0).place(x=201, y=0)
        ctk.CTkFrame(self, width=200, height=330, fg_color="#2b9348", corner_radius=0).place(x=0, y=275)
        ctk.CTkLabel(self, font=("Poppins", 20, "bold"),text="Lost and Found System", fg_color="#2b9348", ).place(x=230, y=17)

        #Frame
        ctk.CTkFrame(self, width=600, height=300, fg_color="#495057", corner_radius=20).place(x=300, y=150)

        ctk.CTkLabel(self, font=("Poppins", 25, "bold"), text="Lexter D. Silva", fg_color="#495057", ).place(x=320, y=230)

        ctk.CTkLabel(self, font=("Poppins", 15, "bold"), text="Name:", fg_color="#495057", ).place(x=320, y=300)
        ctk.CTkLabel(self, font=("Poppins", 15, "bold"), text="Email:", fg_color="#495057", ).place(x=320, y=340)
        ctk.CTkLabel(self, font=("Poppins", 15, "bold"), text="Password:", fg_color="#495057", ).place(x=320, y=380)
        
        ctk.CTkLabel(self, font=("Poppins", 15), text="Lexter Silva", fg_color="#495057", ).place(x=450, y=300)
        ctk.CTkLabel(self, font=("Poppins", 15), text="lextersilva@gmail.com", fg_color="#495057", ).place(x=450, y=340)
        ctk.CTkLabel(self, font=("Poppins", 15), text="********", fg_color="#495057", ).place(x=450, y=380)

        ctk.CTkButton(self, text="Edit", font=("Poppins", 15), width=50, height=15, fg_color="#2b9348", corner_radius=3).place(x=825,y=300)
        ctk.CTkButton(self, text="Edit", font=("Poppins", 15), width=50, height=15, fg_color="#2b9348", corner_radius=3).place(x=825,y=340)
        ctk.CTkButton(self, text="Edit", font=("Poppins", 15), width=50, height=15, fg_color="#2b9348", corner_radius=3).place(x=825,y=380)

        ctk.CTkButton(
            self,
            text="MENU",
            font=("Poppins", 15, "bold"),
            height=70,
            width=200,
            fg_color="#2b9348",
            corner_radius=0,
            command=lambda: parent.show_frame(parent.login_frame)
        ).place(x=0, y=0)

        ctk.CTkButton(
            self,
            text="User Profile",
            font=("Poppins", 13, "bold"),
            height=50,
            width=200,
            fg_color="#2b9348",
            corner_radius=0,
            command=lambda: parent.show_frame(parent.userprofile_frame)
        ).place(x=0, y=71)

        ctk.CTkButton(
            self,
            text="Dashboard",
            font=("Poppins", 13, "bold"),
            height=50,
            width=200,
            fg_color="#2b9348",
            corner_radius=0,
            command=lambda: parent.show_frame(parent.dashboard_frame)
        ).place(x=0, y=122)

        ctk.CTkButton(
            self,
            text="View Lost Items",
            font=("Poppins", 13, "bold"),
            height=50,
            width=200,
            fg_color="#2b9348",
            corner_radius=0,
            command=lambda: parent.show_frame(parent.login_frame)
        ).place(x=0, y=173)

        ctk.CTkButton(
            self,
            text="Report Missing Items",
            font=("Poppins", 13, "bold"),
            height=50,
            width=200,
            fg_color="#2b9348",
            corner_radius=0,
            command=lambda: parent.show_frame(parent.login_frame)
        ).place(x=0, y=224)







class ViewLostItemFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.place(relwidth=1, relheight=1)

        ctk.CTkFrame(self, width=800, height=70, fg_color="#2b9348", corner_radius=0).place(x=201, y=0)
        ctk.CTkFrame(self, width=200, height=330, fg_color="#2b9348", corner_radius=0).place(x=0, y=275)
        ctk.CTkLabel(self, font=("Poppins", 20, "bold"),text="Lost and Found System", fg_color="#2b9348", ).place(x=230, y=17)

        ctk.CTkLabel(self, font=("Poppins", 15, "bold"),text="View Lost Items", fg_color="transparent", ).place(x=220, y=85)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="#2b9348", font=("Poppins", 10, "bold"), foreground="white")
        #style.configure("Treeview", background="#2b9348")
        
        columns = ("Item Name", "Landmark", "Date Found", "Time Found", "Reported By", "Action")

        # We use self.tree so we can access it in other functions
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=20)
        self.tree.place(x=210, y=135)
        
        
        for col in columns:
            self.tree.heading(col, text=col.capitalize() )
            self.tree.column(col, width=130)

        scroll_y = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        scroll_y.place(x=975, y=170, height=265)
        self.tree.configure(yscrollcommand=scroll_y.set)

        # --- Load Initial Data ---
        self.load_data()

        ctk.CTkButton(
            self,
            text="MENU",
            font=("Poppins", 15, "bold"),
            height=70,
            width=200,
            fg_color="#2b9348",
            corner_radius=0,
            command=lambda: parent.show_frame(parent.login_frame)
        ).place(x=0, y=0)

        ctk.CTkButton(
            self,
            text="User Profile",
            font=("Poppins", 13, "bold"),
            height=50,
            width=200,
            fg_color="#2b9348",
            corner_radius=0,
            command=lambda: parent.show_frame(parent.userprofile_frame)
        ).place(x=0, y=71)

        ctk.CTkButton(
            self,
            text="Dashboard",
            font=("Poppins", 13, "bold"),
            height=50,
            width=200,
            fg_color="#2b9348",
            corner_radius=0,
            command=lambda: parent.show_frame(parent.dashboard_frame)
        ).place(x=0, y=122)

        ctk.CTkButton(
            self,
            text="View Lost Items",
            font=("Poppins", 13, "bold"),
            height=50,
            width=200,
            fg_color="#2b9348",
            corner_radius=0,
            command=lambda: parent.show_frame(parent.viewlostitem_frame)
        ).place(x=0, y=173)

        ctk.CTkButton(
            self,
            text="Report Missing Items",
            font=("Poppins", 13, "bold"),
            height=50,
            width=200,
            fg_color="#2b9348",
            corner_radius=0,
            command=lambda: parent.show_frame(parent.reportmissingitem_frame)
        ).place(x=0, y=224)

    def load_data(self):
        """Fetches fresh data from the database and updates the table."""
        # 1. Clear the current table
        for item in self.tree.get_children():
            self.tree.delete(item)

        # 2. Fetch new data
        try:
            items = get_all_items() # Returns list of tuples
            
            # 3. Insert data
            for item in items:
                # Our query returns: (name, landmark, date, time, type, description)
                # We only need the first 4 for this table
                row_values = (item[0], item[1], item[2], item[3], 'YSER 1', "pls Claim")
                self.tree.insert("", "end", values=row_values)
                
            print(f"Loaded {len(items)} items into the table.") # Debug message
            
        except Exception as e:
            print(f"Error loading data: {e}")



class ReportMissingItemFrame(ctk.CTkFrame):

    

    def __init__(self, parent):
        super().__init__(parent)

        self.place(relwidth=1, relheight=1)


        # --- Layout & Header ---
        ctk.CTkFrame(self, width=800, height=70, fg_color="#2b9348", corner_radius=0).place(x=201, y=0)
        ctk.CTkFrame(self, width=200, height=330, fg_color="#2b9348", corner_radius=0).place(x=0, y=275)
        ctk.CTkLabel(self, font=("Poppins", 20, "bold"),text="Lost and Found System", fg_color="#2b9348", ).place(x=230, y=17)
        ctk.CTkFrame(self, width=500, height=440, fg_color="#6c757d").place(x=350, y=130)

        # --- FIXED INPUTS ---
        
        # 1. Item Name
        ctk.CTkLabel(self, font=("Poppins", 15, "bold"),text="Item Name", fg_color="#6c757d", text_color="White").place(x=370, y=140)
        self.name_entry = ctk.CTkEntry(self, fg_color="#f8f9fa", width=460, height=30 , text_color="black", placeholder_text="Name of Item", corner_radius=7)
        self.name_entry.place(x=370, y=165)

        # 2. Landmark
        ctk.CTkLabel(self, font=("Poppins", 15, "bold"),text="Landmark", fg_color="#6c757d", text_color="White").place(x=370, y=200)
        self.landmark_entry = ctk.CTkEntry(self, fg_color="#f8f9fa", width=460, height=30 , text_color="black", placeholder_text="Enter Landmark", corner_radius=7)
        self.landmark_entry.place(x=370, y=225)

        # 3. Date Found
        ctk.CTkLabel(self, font=("Poppins", 15, "bold"),text="Date Found", fg_color="#6c757d", text_color="White").place(x=370, y=260)
        self.date_entry = ctk.CTkEntry(self, fg_color="#f8f9fa", width=460, height=30 , text_color="black", placeholder_text="dd/mm/yyyy", corner_radius=7)
        self.date_entry.place(x=370, y=285)

        # 4. Time Found
        ctk.CTkLabel(self, font=("Poppins", 15, "bold"),text="Time Found", fg_color="#6c757d", text_color="White").place(x=370, y=320)
        self.time_entry = ctk.CTkEntry(self, fg_color="#f8f9fa", width=460, height=30 , text_color="black", placeholder_text="--:-- --", corner_radius=7)
        self.time_entry.place(x=370, y=345)

        # 5. Description
        ctk.CTkLabel(self, font=("Poppins", 15, "bold"),text="Description", fg_color="#6c757d", text_color="White").place(x=370, y=380)
        self.desc_entry = ctk.CTkEntry(self, fg_color="#f8f9fa", width=460, height=30 , text_color="black", placeholder_text="e.g. Color: Blue Cotton, with money inside", corner_radius=7)
        self.desc_entry.place(x=370, y=405)

        # Image Button
        ctk.CTkLabel(self, font=("Poppins", 15, "bold"),text="Insert Image", fg_color="#6c757d", text_color="White").place(x=370, y=440)
        ctk.CTkButton(
            self,
            text="Browse",
            font=("Poppins", 13, "bold"),
            height=15,
            width=50,
            fg_color="#2b9348",
            corner_radius=5,
            border_width=0,
            command=browse_image
        ).place(x=370, y=465)

        # Submit Button
        ctk.CTkButton(
            self,
            text="Submit",
            font=("Poppins", 13, "bold"),
            height=15,
            width=460,
            fg_color="#2b9348",
            corner_radius=5,
            border_width=0,
            command=self.submit_form 
        ).place(x=370, y=520)


        # Belwo are the menus
        ctk.CTkButton(
            self,
            text="MENU",
            font=("Poppins", 15, "bold"),
            height=70,
            width=200,
            fg_color="#2b9348",
            corner_radius=0,
            command=lambda: parent.show_frame(parent.login_frame)
        ).place(x=0, y=0)

        ctk.CTkButton(
            self,
            text="User Profile",
            font=("Poppins", 13, "bold"),
            height=50,
            width=200,
            fg_color="#2b9348",
            corner_radius=0,
            command=lambda: parent.show_frame(parent.userprofile_frame)
        ).place(x=0, y=71)

        ctk.CTkButton(
            self,
            text="Dashboard",
            font=("Poppins", 13, "bold"),
            height=50,
            width=200,
            fg_color="#2b9348",
            corner_radius=0,
            command=lambda: parent.show_frame(parent.dashboard_frame)
        ).place(x=0, y=122)

        ctk.CTkButton(
            self,
            text="View Lost Items",
            font=("Poppins", 13, "bold"),
            height=50,
            width=200,
            fg_color="#2b9348",
            corner_radius=0,
            command=lambda: parent.show_frame(parent.viewlostitem_frame)
        ).place(x=0, y=173)

        ctk.CTkButton(
            self,
            text="Report Missing Items",
            font=("Poppins", 13, "bold"),
            height=50,
            width=200,
            fg_color="#2b9348",
            corner_radius=0,
            command=lambda: parent.show_frame(parent.reportmissingitem_frame)
        ).place(x=0, y=224)

    def submit_form(self):
        """Gets text from entries and saves to database."""
        # 1. Get the text from the inputs
        i_name = self.name_entry.get()
        i_landmark = self.landmark_entry.get()
        i_date = self.date_entry.get()
        i_time = self.time_entry.get()
        i_desc = self.desc_entry.get()

                # 2. Call the database function
                # We use '1' as a temporary user_id (1 is the user_id of Leeex lex@gmail.com)
                # We use 'LOST' as the default type (you can change this logic later)
        try:
            create_new_item(1, i_name, i_landmark, i_date, i_time, "LOST", i_desc)
            print("Item saved successfully!")
                    
                # Optional: Clear the boxes after submitting
            self.name_entry.delete(0, 'end')
            self.landmark_entry.delete(0, 'end')
                    # ... clear others ...
                    
        except Exception as e:
            print(f"Error saving: {e}")




if __name__ == "__main__":
    app = App()
    app.mainloop()



