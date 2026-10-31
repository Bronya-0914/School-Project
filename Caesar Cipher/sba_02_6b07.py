import tkinter as tk
from tkinter import filedialog, messagebox

the_most='A'
number=0
decode=''
encode=''
#
root = tk.Tk()
root.title("?望???")
window_width = root.winfo_screenwidth()    # ???Ｗ?撖砍漲
window_height = root.winfo_screenheight()  # ???Ｗ?擃漲
width = 520
height = 400
left = int((window_width - width)/2)       
top = int((window_height - height)/2) 
root.geometry(f'{width}x{height}+{left}+{top}')  # 摰儔閬??偕撖詨?雿蔭
#
def analyze_textfile(file_path):
    global char_count,content
    try:
        with open(file_path, 'r', encoding='UTF-8') as file:
            content=file.read()
            char_count=len(content)
            if char_count==0:
                messagebox.showinfo("?交","?辣?箇征??)
    except FileNotFoundError:
        messagebox.showerror("?交","?曆??唳?隞嗚?)
#
def select_file():
    global file_path
    file_path=filedialog.askopenfilename(filetypes=[("??辣", ".txt")])
    analyze_textfile(file_path)
    file_label.config(text=f"撌脤??隞? {file_path}")
#
def encrypt_decrypt_crack():
    global encode,decode,content,x,number,the_most,k,file_path
    action=selected_action.get()
    
    if action==1:    #---------------------------------------------------------------------Encrypt
        try:
            k=int(shift_entry.get())
        except ValueError:
            messagebox.showerror("?航炊","隢撓?乩?蝘餅")
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
            messagebox.showinfo("??摰?","encrypted_file撌脣神?交?隞嗅冗??)
        
    elif action==2:    #---------------------------------------------------------------------Decrypt
        try:
            k=int(shift_entry.get())
        except ValueError:
            messagebox.showerror("?航炊","隢撓?乩?蝘餅")
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
            messagebox.showinfo("閫??摰?","decrypted_file撌脣神?交?隞嗅冗??)
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
        shifting=(f"雿宏??{k}\n")
        with open("cracked_file.txt", 'w', encoding='UTF-8') as file:
            file.write(shifting)
            file.write(decode)
            file.close()
            messagebox.showinfo("?渲圾摰?","carcked_file撌脣神?交?隞嗅冗??)
    else:
        try:
            shifting=(f"雿宏??{k}\n")
        except NameError:
            messagebox.showerror("?航炊","隢?芋撘?)
# GUI
file_label=tk.Label(root,text="撌脤??隞? ")
file_label.pack()

select_file_button = tk.Button(root, text="?豢??辣",command=select_file)
select_file_button.pack()

shift_label=tk.Label(root,text="頛詨雿宏??")
shift_label.pack()

shift_entry=tk.Entry(root)
shift_entry.pack()

button_frame=tk.Frame(root)
button_frame.pack()
selected_action=tk.IntVar()
encrypt_radio=tk.Radiobutton(button_frame,text="??",variable=selected_action,value=1)
encrypt_radio.pack(side=tk.LEFT)
crack_radio=tk.Radiobutton(button_frame,text="?渲圾",variable=selected_action,value=3)
crack_radio.pack(side=tk.RIGHT)
decrypt_radio=tk.Radiobutton(button_frame,text="閫??",variable=selected_action,value=2)
decrypt_radio.pack(side=tk.RIGHT)

action_button=tk.Button(root, text="?瑁?",command=encrypt_decrypt_crack)
action_button.pack()

root.mainloop()
