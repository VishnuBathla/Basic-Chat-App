import socket
import threading
import tkinter
import time
import tkinter.scrolledtext
from tkinter import simpledialog

host="127.0.0.1"
port=9090

class Client:
    def __init__(self,host,port):
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.connect((host,port))
        msg=tkinter.Tk()
        msg.withdraw()
        self.name=simpledialog.askstring('Name','Please choose your Name',parent=msg)
        self.gui_done=False
        self.running=True
        gui_thread=threading.Thread(target=self.gui_loop)
        receive_thread=threading.Thread(target=self.receive)
        gui_thread.start()
        time.sleep(1)
        receive_thread.start()

    def gui_loop(self):
        self.wind=tkinter.Tk()
        self.wind.configure(bg='white')

        self.chat_label=tkinter.Label(self.wind,text='Chat:',bg='lightgray')
        self.chat_label.config(font=('Arial',14))
        self.chat_label.pack(padx=20,pady=5)
        
        self.text_area=tkinter.scrolledtext.ScrolledText(self.wind)
        self.text_area.pack(padx=20,pady=5)
        self.text_area.config(state='disabled')
        
        self.msg_label=tkinter.Label(self.wind,text='Message:',bg='lightgray')
        self.msg_label.config(font=('Arial',14))
        self.msg_label.pack(padx=20,pady=5)
        
        self.input_area=tkinter.Text(self.wind,height=3)
        self.input_area.pack(padx=20,pady=5)

        self.send_button=tkinter.Button(self.wind,text='Send',command=self.write)
        self.send_button.config(font=('Arial',14))
        self.send_button.pack(padx=20,pady=5)

        self.gui_done=True

        self.wind.protocol('WM_DELETE_WINDOW',self.stop)
        
        self.wind.mainloop()

    def write(self):
        msg=f"{self.name}:{self.input_area.get('1.0','end')}"
        self.sock.send(msg.encode('utf-8'))
        self.input_area.delete('1.0','end')
    
    def stop(self):
        self.running=False
        self.wind.destroy()
        self.sock.close()
        exit(0)

    def receive(self):
        while self.running:
            try:
                message=self.sock.recv(1024).decode('utf-8')
                if message =='Name':
                    self.sock.send(self.name.encode('utf-8'))
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end',message)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')
            except ConnectionAbortedError:
                break
            except:
                self.sock.close()
                break
client=Client(host,port)
