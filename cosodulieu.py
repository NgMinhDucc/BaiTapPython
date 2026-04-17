import customtkinter as ctk
from tkinter import ttk
import sqlite3

def create_database():
    conn = sqlite3.connect("university.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS university
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            major TEXT,
            gpa REAL
        )
    """)
    
    conn.commit()
    conn.close()

class Database(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Students")
        self.geometry("700x400")
        self.resizable(True, True)
        
        self.entries = {}
        
        self.create_style()
        self.create_table()
        self.create_button()
        self.create_input_form()
        
        self.load_data("SELECT * FROM university")
            
    def create_style(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2b2b2b", foreground="white", fieldbackground="#2b2b2b", rowheight=30)
        style.configure("Treeview.Heading", background="#333333", foreground="white", font=("Arial", 15, "bold"))
        style.map("Treeview", background=[('selected', '#1f538d')])
        
    def create_table(self):
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        # tao cot
        tags = ["id", "name", "major", "gpa"]
        self.tree = ttk.Treeview(self.table_frame, columns=tags, show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("major", text="Major")
        self.tree.heading("gpa", text="GPA")
        
        self.tree.column("id", width=100, anchor="w")
        self.tree.column("name", width=100, anchor="w")
        self.tree.column("major", width=100, anchor="w")
        self.tree.column("gpa", width=100, anchor="w")
        
        self.tree.pack(fill="both", expand=True)
        
    def create_input_form(self):
        self.form_frame = ctk.CTkFrame(self)
        self.form_frame.pack(padx=10, pady=10, fill="both", side="bottom")
        
        inner_form = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        inner_form.pack(padx=20, pady=20)
        
        fields = ["ID", "Name", "Major", "GPA"]
        for field in fields:
            self.label = ctk.CTkLabel(inner_form, text=field)
            self.label.pack(padx=5, pady=20, side="left")
            
            self.entry = ctk.CTkEntry(inner_form, width=110)
            self.entry.pack(padx=5, pady=20, side="left")
            
            self.entries[field] = self.entry
            
    def create_button(self):
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(padx=5, pady=(0,10), fill="both", side="bottom")
        
        inner_form = ctk.CTkFrame(self.button_frame, fg_color="transparent")
        inner_form.pack(padx=20, pady=20)
        
        add = ctk.CTkButton(inner_form, text="ADD", command=self.button_add)
        add.pack(padx=5, pady=20, side="left")
        
        search = ctk.CTkButton(inner_form, text="SEARCH", command=self.button_search)
        search.pack(padx=5, pady=20, side="left")
        
        update = ctk.CTkButton(inner_form, text="UPDATE", command=self.button_update)
        update.pack(padx=5, pady=20, side="left")
        
        delete = ctk.CTkButton(inner_form, text="DELETE", command=self.button_delete)
        delete.pack(padx=5, pady=20, side="left")
        
        reset = ctk.CTkButton(inner_form, text="RESET", command=self.button_reset)
        reset.pack(padx=5, pady=20, side="left")
            
    # ham tai lai du lieu bang
    def load_data(self, query, parameters=()):
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        conn = sqlite3.connect("university.db")
        cursor = conn.cursor()
        cursor.execute(query, parameters)
        rows = cursor.fetchall()
        
        for row in rows:
            self.tree.insert("", "end", values=row)
        
        conn.commit()
        conn.close()
        
    def button_add(self):
        # id = self.entries["ID"].get()
        name = self.entries["Name"].get()
        major = self.entries["Major"].get()
        gpa = self.entries["GPA"].get()
        gpa = float(gpa)
        
        conn = sqlite3.connect("university.db")
        cursor = conn.cursor()
        
        cursor.execute("INSERT INTO university (name, major, gpa) VALUES (?,?,?)", (name, major, gpa))

        conn.commit()
        conn.close()
        
        self.load_data("SELECT * FROM university")
        
    def button_search(self):
        gpa = self.entries["GPA"].get()
        gpa = float(gpa)
        
        self.load_data("SELECT * FROM university WHERE gpa > ?", (gpa,))
        
    def button_update(self):
        id = self.entries["ID"].get()
        gpa = self.entries["GPA"].get()
        gpa = float(gpa)
        
        conn = sqlite3.connect("university.db")
        cursor = conn.cursor()
        
        cursor.execute("UPDATE university SET gpa = ? WHERE id = ?", (gpa, id))
        
        conn.commit()
        conn.close()
        
        self.load_data("SELECT * FROM university")
        
    def button_delete(self):
        conn = sqlite3.connect("university.db")
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM university WHERE gpa < 2.0")
        
        conn.commit()
        conn.close()
        
        self.load_data("SELECT * FROM university")
    
    def button_reset(self):
        self.load_data("SELECT * FROM university")

        
if __name__ == "__main__":
    create_database()
    app = Database()
    app.mainloop()