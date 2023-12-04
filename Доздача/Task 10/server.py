import socket
import threading
import tkinter as tk

clients = []
names = []
server_messages = []

def server_log(path): 
    global server_messages

    with open(path, '+wt') as f:
        header = "message"
        f.write(header + "\n") 

    for log in server_messages:
        with open(path, "a") as f:
            f.write(log + "\n")

host = "127.0.0.1"
port = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
#Створюємо нове вікно
server_frame = tk.Tk()
server_frame.title("Chat Server")
server_frame.geometry("800x500")
#Створюємо віджет всередині головно вікна
frame = tk.Frame(server_frame, background="lightgrey")
#Розміщеємо наш віджет(контейнер)
frame.pack(side="left", fill="both", expand=True)
#Створюємо полотно для фігури
msgs_frame = tk.Canvas(frame, background="lightgrey", bd=0, highlightthickness=0)
#Створюємо скролбар
scrollbary = tk.Scrollbar(frame, orient="vertical", command=msgs_frame.yview)
scrollbary.pack(side="right", fill="y")
#Розміщуємо
msgs_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
#Дозволить взаєиодіяти з скролбаром
msgs_frame.configure(yscrollcommand=scrollbary.set)
#Створюмо поле для вводу тексту
label_msg = tk.Label(frame, text="", background="lightgrey")
#Розміщуємо
label_msg.pack()

row = 0

def add_msg_box(message):
    global row
#Перевіряємо чи існує повідомлення
    if message:
        msg_box = tk.Frame(msgs_frame, background="white", padx=5, pady=5)
        user_msg = tk.Label(msg_box, text=message, background="white", justify="center", anchor="w")
#Розміщужмо.anchor="w" прив'язуваня до лівого краю
        user_msg.pack(anchor="w")
#Створюємо вікно в якому буде розміщено контейнер  msg_box
        msgs_frame.create_window((0, row * 40), window=msg_box, anchor="w", tags=f"message_{row}")

        row += 1
#Оновлюємо віджет 
        msgs_frame.update_idletasks()
#Налаштовуємо область прокрутки
        msgs_frame.config(scrollregion=msgs_frame.bbox("all"))
#Відпарвка повідомлення всім клієнтам які під'єднані до серевера 
def broadcast(message):
    for client in clients:
        client.send(message)
    #Обробка повідомлення від окремого клієнта 
def client_messages(conn, addr):
    print(f"Connected by {addr}")
    text = f"Connected by {addr}"
    add_msg_box(text)
    server_messages.append(text.replace(",",";"))
#Цмкл який буде обробляти повідомлення до поки не закриється сервер 
    while True:
        try:
            message = conn.recv(1024) 
            broadcast(message)
            text = f"Received from {addr}: {message}"
            add_msg_box(text)
            server_messages.append(text.replace(",",";"))
        except:
            conn.close()
            break
#Обробка нових підключень до сервера
def receive_message():
    global server_messages
    #Цикл який обробляє нові пвдключення 
    while True:
        conn, addr = server.accept()
        print(f"Connected with {str(addr)}".replace(",",";"))

        name = conn.recv(1024).decode("utf-8")
        names.append(name)
        clients.append(conn)

        text = f"{name} has joined the server"
        add_msg_box(text)
        broadcast(f"{name} has joined the chat\n".encode("utf-8"))
        conn.send(f"Connected to the server with {addr}\nYou can start texting".encode("utf-8"))
        server_messages.append(text)
        server_messages.append(f"{name} has joined the chat")
        server_messages.append(f"Connected to the server with {addr}".replace(",",";"))

        client_messages_thread = threading.Thread(target=client_messages, args=(conn, addr))
        client_messages_thread.start()

server_thread = threading.Thread(target=receive_message)
server_thread.start()

server_frame.mainloop()

server_log("D:/IT STEP/2CS/1 semester/Python/Python/Доздача/Task 10/logs/server_messages.csv")