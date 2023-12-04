import socket
import threading
import tkinter as tk

is_name = False
name = ""
client_messages = []

def client_log(path): 
    global client_messages

    with open(path, '+wt') as f:
        header = "name,message"
        f.write(header + "\n") 

    for log in client_messages:
        with open(path, "a") as f:
            f.write(log + "\n")

host = "127.0.0.1"
port = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

chat_frame = tk.Tk()
chat_frame.title("Chat")
chat_frame.geometry("800x500")

bottom_frame = tk.Frame(chat_frame, height=50, background="grey")
bottom_frame.pack(fill="x", padx=10, pady=10, side="bottom")

frame = tk.Frame(chat_frame, background="lightgrey")
frame.pack(side="left", fill="both", expand=True)

msgs_frame = tk.Canvas(frame, background="lightgrey", bd=0, highlightthickness=0)

scrollbary = tk.Scrollbar(frame, orient="vertical", command=msgs_frame.yview)
scrollbary.pack(side="right", fill="y")

msgs_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
msgs_frame.configure(yscrollcommand=scrollbary.set)

row = 0

def add_msg_box(message, name=""):
    global row
    if message:
        msg_box = tk.Frame(msgs_frame, background="white", padx=5, pady=5)
        
        if name:
            user_name = tk.Label(msg_box, text=name, background="white", font=("Helvetica", 10, "bold"))
            user_name.pack(anchor="w")
            msgs_frame.create_window((0, row * 60), window=msg_box, anchor="w", tags=f"message_{row}")
            
        elif name == "":
            msgs_frame.create_window((0, row * 60), window=msg_box, anchor="w", tags=f"message_{row}")

        user_msg = tk.Label(msg_box, text=message, background="white", justify="center")
        user_msg.pack(anchor="w")

        row += 1
        msgs_frame.update_idletasks()
        msgs_frame.config(scrollregion=msgs_frame.bbox("all"))

input = tk.Entry(bottom_frame)
input.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

bottom_frame.grid_rowconfigure(0, weight=1)
bottom_frame.grid_columnconfigure(0, weight=3)
bottom_frame.grid_columnconfigure(1, weight=1)
# Отримання повідомлення
def get_message():
    global client_messages
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            double = message.split("\n")
            print(double)
            split = message.split(": ")
            if message[-4:] == "quit":
                client.close()
                break
            else:
                if len(split) == 2:
                    add_msg_box(split[1], split[0])
                    client_messages.append(f"{split[0]},{split[1]}")
                elif len(double) == 3:
                    for i in double:
                        add_msg_box(i)
                else:
                    add_msg_box(message)
        except:
            client.close()
            break
#Читання введеного тексту 
def read_message():
    input_text = input.get()
    global is_name
    global name
    if input_text != "" and is_name is True:
        input.delete(0, tk.END)
        message = f"{name}: " + input_text
        client.send(message.encode("utf-8"))
    elif input_text != "" and is_name is False:
        input.delete(0, tk.END)
        is_name = True
        name = input_text
        client.send(name.encode("utf-8"))
        btn.configure(text="Send message")
#Кнопка для відправки повідомлпень 
btn = tk.Button(bottom_frame, text="Type your name", command=read_message)
btn.grid(row=0, column=1, sticky='nsew', padx=(0, 10), pady=10)

receive_t = threading.Thread(target=get_message)
receive_t.start()

chat_frame.mainloop()

client_log("D:/IT STEP/2CS/1 semester/Python/Python/Доздача/Task 10/logs/client_messages.csv")