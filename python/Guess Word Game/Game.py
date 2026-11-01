import tkinter as tk
from tkinter import messagebox
import random
import os

class GuessWordGame:
    # 1.Initialization
    # ============================================================
    def __init__(self, root):
        self.root = root                                      
        self.root.title("猜單字遊戲")                              
        
        w_width = root.winfo_screenwidth()                    
        w_height = root.winfo_screenheight()                  
        width = 680                                           
        height = 500                                          
        left = int((w_width - width)/2)                       
        top = int((w_height - height)/2)                      
        root.geometry(f'{width}x{height}+{left}+{top}')       

        self.data_file = "data.txt"                   

        self.word_data = {}                                   
        self.secret_word = ""                                 
        self.guessed_letters = set()                          
        self.lives = 0                                        
        self.buttons = {}                                     
        
        self.create_ui()                                      
        self.start_game("中等")
        
    def create_ui(self):
        control = tk.Frame(self.root)
        control.pack(pady=20)
        
        tk.Label(control, text="新遊戲難度:", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        
        tk.Button(control, text="簡單 (12次)", command=lambda: self.start_game("簡單"), bg="#90EE90").pack(side=tk.LEFT, padx=2)
        tk.Button(control, text="中等 (9次)", command=lambda: self.start_game("中等"), bg="#FFD700").pack(side=tk.LEFT, padx=2)
        tk.Button(control, text="困難 (6次)", command=lambda: self.start_game("困難"), bg="#FF6347").pack(side=tk.LEFT, padx=2)

        info_frame = tk.Frame(self.root)
        info_frame.pack(pady=10)
        
        self.lbl_category = tk.Label(info_frame, text="提示:", font=("Arial", 16))
        self.lbl_category.pack(side=tk.LEFT, padx=20)
        
        self.lbl_lives = tk.Label(info_frame, text="剩餘機會: ", font=("Arial", 16, "bold"))
        self.lbl_lives.pack(side=tk.LEFT, padx=20)

        self.word = tk.Text(self.root, height=1, width=20, font=("Arial", 40, "bold"), bd=0, bg=self.root.cget("bg"), cursor="arrow")
        self.word.pack(pady=20)
        
        self.word.tag_config("center", justify='center')
        self.word.tag_config("blue", foreground="blue")
        self.word.tag_config("red", foreground="red")
        self.word.tag_config("black", foreground="#333")
        
        self.word.config(state="disabled")

        self.keyboard = tk.Frame(self.root)
        self.keyboard.pack(pady=10, padx=10)
        
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for i, char in enumerate(letters):
            btn = tk.Button(self.keyboard, text=char, width=4, height=2, font=("Arial", 10, "bold"), command=lambda c=char: self.guess(c))
            row = i // 13
            col = i % 13
            btn.grid(row=row, column=col, padx=3, pady=3)
            self.buttons[char] = btn

    # 2.Loading Data
    # ============================================================
    def data(self):
        default_content = """水果: APPLE, BANANA, ORANGE, GRAPE, MANGO
動物: TIGER, LION, ZEBRA, PANDA, KOALA
國家: TAIWAN, JAPAN, KOREA, CANADA, FRANCE"""             # 若無檔案時的預設資料

        if not os.path.exists(self.data_file):                
            with open(self.data_file, "w", encoding="utf-8") as f:  # 若無則建立檔案
                f.write(default_content)                      

        data = {}                                             
        with open(self.data_file, "r", encoding="utf-8") as f:      
            for line in f:                                    
                if ":" in line:                               
                    parts = line.split(":")                   # 用冒號切割類別
                    category = parts[0].strip()               # 取得類別名稱並去空白
                    words_raw = parts[1].split(",")           # 用逗號切割單字
                    #將單字去空白、轉大寫，並去空白
                    words_clean = [w.strip().upper() for w in words_raw if w.strip()]
                    
                    if words_clean:                           # 如果該類別有有效單字
                        data[category] = words_clean          
        
        return data                                           
    # 3.Start Game
    # ============================================================
    def start_game(self, difficulty):
        self.word_data = self.data()                

        if not self.word_data:                                
            messagebox.showerror("錯誤", "題庫檔案是空的")      
            return                                            

        if difficulty == "簡單":                               
            self.lives = 12                                   
        elif difficulty == "中等":                            
            self.lives = 9                                    
        else:                                               
            self.lives = 6                                    
            
        category = random.choice(list(self.word_data.keys())) # 隨機抽選一個類別
        word_choice = random.choice(self.word_data[category]) # 從該類別隨機選單字
        
        self.secret_word = word_choice                        
        self.guessed_letters = set()                          # 清空已猜字母紀錄
        
        self.lbl_category.config(text=f"提示: {category}")     
        self.lbl_lives.config(text=f"剩餘機會: {self.lives}")  
        
        for btn in self.buttons.values():                     
            btn.config(state="normal", bg="#f0f0f0")          
            
        self.update_word()
    
    def update_word(self):
        self.word.config(state="normal")
        self.word.delete("1.0", "end")
        
        for char in self.secret_word:
            if char in self.guessed_letters:
                self.word.insert("end", char + " ", ("center", "black"))
            else:
                self.word.insert("end", "_ ", ("center", "black"))
        
        self.word.config(state="disabled")

        if all(char in self.guessed_letters for char in self.secret_word):
            self.game_over(True)

    def guess(self, letter):
        if letter in self.guessed_letters or self.lives <= 0:
            return

        self.guessed_letters.add(letter)
        btn = self.buttons[letter]
        
        if letter in self.secret_word:
            btn.config(bg="#90EE90", state="disabled")
            self.update_word()
        else:
            btn.config(bg="#FF6347", state="disabled")
            self.lives -= 1
            self.lbl_lives.config(text=f"剩餘機會: {self.lives}")
            
            if self.lives == 0:
                self.game_over(False)

    def game_over(self, won):
        for btn in self.buttons.values():
            btn.config(state="disabled")
            
        if won:
            messagebox.showinfo("恭喜", f"太厲害了！答案就是 {self.secret_word}")
        else:
            self.word.config(state="normal")
            self.word.delete("1.0", "end")
            
            for char in self.secret_word:
                if char in self.guessed_letters:
                    self.word.insert("end", char + " ", ("center", "blue"))
                else:
                    self.word.insert("end", char + " ", ("center", "red"))
            
            self.word.config(state="disabled")
            messagebox.showinfo("遊戲結束", "真可惜！看看正確答案吧。")

if __name__ == "__main__":
    root = tk.Tk()
    game = GuessWordGame(root)
    root.mainloop()