#from PIL import Image
import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, filedialog

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
        tree = ttk.Treeview(self, columns=columns, show="headings", height=20)
        tree.place(x=210, y=135)
        
        for col in columns:
            tree.heading(col, text=col.capitalize() )
            tree.column(col, width=130)

        scroll_y = tk.Scrollbar(self, orient=tk.VERTICAL, command=tree.yview)
        scroll_y.place(x=975, y=170, height=265)
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





class ReportMissingItemFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.place(relwidth=1, relheight=1)


        ctk.CTkFrame(self, width=800, height=70, fg_color="#2b9348", corner_radius=0).place(x=201, y=0)
        ctk.CTkFrame(self, width=200, height=330, fg_color="#2b9348", corner_radius=0).place(x=0, y=275)
        ctk.CTkLabel(self, font=("Poppins", 20, "bold"),text="Lost and Found System", fg_color="#2b9348", ).place(x=230, y=17)

        ctk.CTkFrame(self, width=500, height=440, fg_color="#6c757d").place(x=350, y=130)

        ctk.CTkLabel(self, font=("Poppins", 15, "bold"),text="Item Name", fg_color="#6c757d", text_color="White").place(x=370, y=140)
        ctk.CTkEntry(self, fg_color="#f8f9fa", width=460, height=30 , text_color="black", placeholder_text="Name of Item", corner_radius=7).place(x=370, y=165)
        ctk.CTkLabel(self, font=("Poppins", 15, "bold"),text="Landmark", fg_color="#6c757d", text_color="White").place(x=370, y=200)
        ctk.CTkEntry(self, fg_color="#f8f9fa", width=460, height=30 , text_color="black", placeholder_text="Enter Landmark", corner_radius=7).place(x=370, y=225)
        ctk.CTkLabel(self, font=("Poppins", 15, "bold"),text="Date Found", fg_color="#6c757d", text_color="White").place(x=370, y=260)
        ctk.CTkEntry(self, fg_color="#f8f9fa", width=460, height=30 , text_color="black", placeholder_text="dd/mm/yyyy", corner_radius=7).place(x=370, y=285)
        ctk.CTkLabel(self, font=("Poppins", 15, "bold"),text="Time Found", fg_color="#6c757d", text_color="White").place(x=370, y=320)
        ctk.CTkEntry(self, fg_color="#f8f9fa", width=460, height=30 , text_color="black", placeholder_text="--:-- --", corner_radius=7).place(x=370, y=345)
        ctk.CTkLabel(self, font=("Poppins", 15, "bold"),text="Description", fg_color="#6c757d", text_color="White").place(x=370, y=380)
        ctk.CTkEntry(self, fg_color="#f8f9fa", width=460, height=30 , text_color="black", placeholder_text="e.g. Color: Blue Cotton, with money inside", corner_radius=7).place(x=370, y=405)
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

        ctk.CTkButton(
            self,
            text="Submit",
            font=("Poppins", 13, "bold"),
            height=15,
            width=460,
            fg_color="#2b9348",
            corner_radius=5,
            border_width=0,
            #command=browse_image
        ).place(x=370, y=520)


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






if __name__ == "__main__":
    app = App()
    app.mainloop()



