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
        self.create_input_form()
        self.create_button()
        
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
        self.form_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        fields = ["ID", "Name", "Major", "GPA"]
        for field in fields:
            self.label = ctk.CTkLabel(self.form_frame, text=field)
            self.label.pack(padx=5, pady=20, side="left", expand=True)
            
            self.entry = ctk.CTkEntry(self.form_frame)
            self.entry.pack(padx=5, pady=20, side="left", expand=True)
            
            self.entries[field] = self.entry
            
    def create_button(self):
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(padx=5, pady=10, fill="both", expand=True)
        
        add = ctk.CTkButton(self, text="ADD", command=self.button_add)
        add.pack(padx=5, pady=20, side="left", expand=True)
        
        search = ctk.CTkButton(self, text="SEARCH", command=self.button_search)
        search.pack(padx=5, pady=20, side="left", expand=True)
        
        update = ctk.CTkButton(self, text="UPDATE", command=self.button_update)
        update.pack(padx=5, pady=20, side="left", expand=True)
        
        delete = ctk.CTkButton(self, text="DELETE", command=self.button_delete)
        delete.pack(padx=5, pady=20, side="left", expand=True)
        
        reset = ctk.CTkButton(self, text="RESET", command=self.button_reset)
        reset.pack(padx=5, pady=20, side="left", expand=True)
            
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
        gpa = self.entries["GPA"].get()
        gpa = float(gpa)
        
        conn = sqlite3.connect("university.db")
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM university WHERE gpa = ?", (gpa,))
        
        conn.commit()
        conn.close()
        
        self.load_data("SELECT * FROM university")
    
    def button_reset(self):
        self.load_data("SELECT * FROM univeristy")

        
if __name__ == "__main__":
    create_database()
    app = Database()
    app.mainloop()