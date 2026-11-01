import tkinter as tk
from tkinter import filedialog, messagebox

the_most='A'
number=0
decode=''
encode=''
#
root = tk.Tk()
root.title("凱撒加密")
window_width = root.winfo_screenwidth()    # 取得螢幕寬度
window_height = root.winfo_screenheight()  # 取得螢幕高度
width = 520
height = 400
left = int((window_width - width)/2)       
top = int((window_height - height)/2) 
root.geometry(f'{width}x{height}+{left}+{top}')  # 定義視窗的尺寸和位置
#
def analyze_textfile(file_path):
    global char_count,content
    try:
        with open(file_path, 'r', encoding='UTF-8') as file:
            content=file.read()
            char_count=len(content)
            if char_count==0:
                messagebox.showinfo("查找","文件為空。")
    except FileNotFoundError:
        messagebox.showerror("查找","找不到文件。")
#
def select_file():
    global file_path
    file_path=filedialog.askopenfilename(filetypes=[("文本文件", ".txt")])
    analyze_textfile(file_path)
    file_label.config(text=f"已選擇文件: {file_path}")
#
def encrypt_decrypt_crack():
    global encode,decode,content,x,number,the_most,k,file_path
    action=selected_action.get()
    
    if action==1:    #---------------------------------------------------------------------Encrypt
        try:
            k=int(shift_entry.get())
        except ValueError:
            messagebox.showerror("錯誤","請輸入位移數")
        for i in range (char_count):
            if ord(content[i])>64 and ord(content[i])<91:
                encode=encode+chr((ord(content[i])+k -ord("A"))%26 + ord("A"))
            elif  ord(content[i])>96 and ord(content[i])<123:
                encode=encode+chr((ord(content[i])+k -ord("a"))%26 + ord("a"))
            else:
                encode=encode+chr(ord(content[i]))

        with open("encrypted_file.txt", 'w', encoding='UTF-8') as file:
            file.write(encode)
            file.close()
            messagebox.showinfo("加密完成","encrypted_file已寫入文件夾。")
        
    elif action==2:    #---------------------------------------------------------------------Decrypt
        try:
            k=int(shift_entry.get())
        except ValueError:
            messagebox.showerror("錯誤","請輸入位移數")
        for i in range (char_count):
            if ord(content[i])>64 and ord(content[i])<91:
                decode=decode+chr((ord(content[i])-k -ord("A"))%26 + ord("A"))
            elif  ord(content[i])>96 and ord(content[i])<123:
                decode=decode+chr((ord(content[i])-k -ord("a"))%26 + ord("a"))
            else:
                decode=decode+chr(ord(content[i]))
                
        with open("decrypted_file.txt", 'w', encoding='UTF-8') as file:
            file.write(decode)
            file.close()
            messagebox.showinfo("解密完成","decrypted_file已寫入文件夾。")
    elif action==3:#---------------------------------------------------------------------Crack
        k=0
        with open(file_path, 'r', encoding='UTF-8') as file:
            content=file.read()
            file_path=content.upper()
  
        for i in range (ord("A"),(ord("Z")+1)):
            x=file_path.count(chr(i))
            if x>number:
                number=x
                the_most=chr(i)
        if ord(the_most)!=ord('E'):
            k=ord(the_most)-ord('E')
            for i in range (char_count):
                if ord(content[i])>64 and ord(content[i])<91:
                    decode=decode+chr((ord(content[i])-k -ord("A"))%26 + ord("A"))
                elif  ord(content[i])>96 and ord(content[i])<123:
                    decode=decode+chr((ord(content[i])-k -ord("a"))%26 + ord("a"))
                else:
                    decode=decode+chr(ord(content[i]))
        shifting=(f"位移數:{k}\n")
        with open("cracked_file.txt", 'w', encoding='UTF-8') as file:
            file.write(shifting)
            file.write(decode)
            file.close()
            messagebox.showinfo("破解完成","carcked_file已寫入文件夾。")
    else:
        try:
            shifting=(f"位移數:{k}\n")
        except NameError:
            messagebox.showerror("錯誤","請選擇模式")
# GUI
file_label=tk.Label(root,text="已選擇文件: ")
file_label.pack()

select_file_button = tk.Button(root, text="選擇文件",command=select_file)
select_file_button.pack()

shift_label=tk.Label(root,text="輸入位移數:")
shift_label.pack()

shift_entry=tk.Entry(root)
shift_entry.pack()

button_frame=tk.Frame(root)
button_frame.pack()
selected_action=tk.IntVar()
encrypt_radio=tk.Radiobutton(button_frame,text="加密",variable=selected_action,value=1)
encrypt_radio.pack(side=tk.LEFT)
crack_radio=tk.Radiobutton(button_frame,text="破解",variable=selected_action,value=3)
crack_radio.pack(side=tk.RIGHT)
decrypt_radio=tk.Radiobutton(button_frame,text="解密",variable=selected_action,value=2)
decrypt_radio.pack(side=tk.RIGHT)

action_button=tk.Button(root, text="執行",command=encrypt_decrypt_crack)
action_button.pack()

root.mainloop()
