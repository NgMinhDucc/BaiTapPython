import customtkinter as ctk

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class Calculator(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # ten va kich thuoc ban dau
        self.title("Calculator3000")
        self.geometry("300x400")
        self.resizable(True, True)
        
        self.equation = ""
        self.display_var = ctk.StringVar(value="")
        
        # tu dieu chinh kich thuoc theo kich thuoc cua so
        for i in range(4):
            self.grid_columnconfigure(i, weight=1)
        for i in range(6): # tinh ca man hinh la 6 hang
            self.grid_rowconfigure(i, weight=1)
            
        # tao man hinh
        self.display = ctk.CTkEntry(self, font=("Arial", 20), justify="right", textvariable=self.display_var)
        self.display.grid(row=0, column=0, columnspan=4, padx=5, pady=10, sticky="nsew")
        
        self.create_button()
    
    # tao cac phim
    def create_button(self):
        buttons = [
        ["AC", "DEL", "(", ")"],
        ["7", "8", "9", "*"],
        ["4", "5", "6", "/"],
        ["1", "2", "3", "+"],
        ["0", ".", "=", "-"]
        ]
        
        button_font = ctk.CTkFont(family="Arial", size=18, weight="bold")
        for i in range(len(buttons)):
            for j in range(len(buttons[i])):
                if buttons[i][j] == "AC" or buttons[i][j] == "DEL":
                    button = ctk.CTkButton(self, text=buttons[i][j], fg_color="#6FDF00", text_color="#000000", font=button_font, command=lambda val = buttons[i][j]: self.click_button(val))
                else:
                    button = ctk.CTkButton(self, text=buttons[i][j], fg_color="#42463E", font=button_font, command=lambda val = buttons[i][j]: self.click_button(val))
                button.grid(row=i+1, column=j, columnspan=1, padx=3, pady=3, sticky="nsew")
    
    # su kien cac phim
    def click_button(self, button):
        if button == "AC":
            self.equation = ""
        elif button == "DEL":
            self.equation = self.equation[:-1]
        elif button == "=":
            try:
                self.equation = str(eval(self.equation))
            except:
                self.equation = "Error"
        else:
            if self.equation == "Error":
                self.equation = ""
            else:
                self.equation += button
        self.update_display()
                
    def update_display(self):
        self.display_var.set(self.equation)
        
            
if __name__ == "__main__":
    app = Calculator()
    app.mainloop()
