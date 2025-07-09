import socket, threading
import tkinter as tk
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 9999))

with open("keys/private.pem", "rb") as priv_file:
    private_key = RSA.import_key(priv_file.read())
with open("keys/public.pem", "rb") as pub_file:
    public_key = RSA.import_key(pub_file.read())

cipher_rsa = PKCS1_OAEP.new(public_key)
decipher_rsa = PKCS1_OAEP.new(private_key)

def receive():
    while True:
        try:
            enc_msg = client.recv(4096)
            msg = decipher_rsa.decrypt(enc_msg).decode()
            chat.insert(tk.END, "Friend: " + msg + "\n")
        except:
            break

def send():
    msg = entry.get()
    enc_msg = cipher_rsa.encrypt(msg.encode())
    client.send(enc_msg)
    chat.insert(tk.END, "You: " + msg + "\n")
    entry.delete(0, tk.END)

app = tk.Tk()
app.title("Secure Chat")

chat = tk.Text(app)
chat.pack()

entry = tk.Entry(app)
entry.pack()

send_btn = tk.Button(app, text="Send", command=send)
send_btn.pack()

thread = threading.Thread(target=receive)
thread.daemon = True
thread.start()

app.mainloop()
