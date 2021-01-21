#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import threading as th
from threading import Thread
import time 
import client
import socket 
class GUI(tk.Frame,Thread):

    
    
    def __init__(self,master,title,size,resizable,ikon):
        super().__init__(master)
        master.wm_title(title)
        master.geometry(size)
        master.resizable(resizable,resizable)
        master.iconbitmap(ikon)
        master.config(bg="ghost white")
        self.state=False

    def setFirstWindow(self,master):
        tk.Label(master, text= "Server İp",bg="ghost white").grid(row=0, column=0)
        tk.Label(master, text="Port",bg="ghost white").grid(row=1, column=0)
        self.serverip=tk.StringVar()
        self.port=tk.StringVar()
        tk.Entry(master, textvariable=self.serverip).grid(row=0, column=1)
        tk.Entry(master, textvariable=self.port,show='*').grid(row=1, column=1)

    def getValue(self):
        return self.serverip.get(),self.port.get()


    def startchat(self,master,ip,port):
        soket,addr,karsininpubi=self.handshake(ip,port,master)
        self.labels=[]
        self.send_button=tk.Button(master,text="Send",width=-1,height=-1,command=lambda:self.sendMessage(master,soket,addr,karsininpubi)).pack(ipady=5,side="bottom",fill=tk.X)
        self.user_text=tk.Text(master,width=-1,height=-1)
        self.user_text.pack(ipady=35,side="bottom",fill=tk.X)
        
        for i in range(0,22):
            label = tk.Label(master,bg="ghost white")
            label.place(x=0,y=20*i)
            self.labels.append(label)
        
        self.create_menu(master,soket,karsininpubi)
        
    def handshake(self,ip,port,master):
        try:    
            sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
            addr, karsininpubi = client.ilkBaglanti(sock, ip, port)
        except ConnectionResetError:
            messagebox.showerror("warning","Connect failed")
            master.destroy()
        return sock , addr , karsininpubi


    def sendMessage(self,master,soket,addr,karsininpubi):
        metin=self.user_text.get("1.0","end")
        self.user_text.delete("1.0", "end")
        metin=metin[:-1]
        state=self.show_message("admin",metin)
        if state==True:
            self.verici(metin,soket,addr,karsininpubi)
        
        
    
    def show_message(self,who,metin):
        text=""
        for i in range(0,21):
            index=self.labels[i+1].cget("text")
            index2=self.labels[i+1].cget("bg")
            self.labels[i].config(text=index)
            self.labels[i].config(bg=index2)

        if who=="admin":
            if len(metin)>145:
                messagebox.showerror("warning","Max text size 145")
                return False
            else:
                text+="Admin : "
                text+=metin
                text=text.replace("\n" , " ")
                text=text.replace("  " , " ")
                self.labels[21].config(text=text,bg="gainsboro")
                return True
        if who=="guest":
            text+="Guest : "
            text+=metin[1:]
            text=text.replace("\n" , " ")
            text=text.replace("  " , " ")
            self.labels[21].config(text=text,bg="ghost white")

    def create_menu(self,master,soket,karsininpubi):
        menu_bar=tk.Menu(master)
        theme=tk.Menu(menu_bar,tearoff=0)
        theme.add_command(label="Secret Mode",command=lambda:self.secretMode(master))
        theme.add_command(label="Normal Mode",command=lambda:self.normalMode(master))
        menu_bar.add_cascade(label="Settings",menu=theme)
        out=tk.Menu(menu_bar,tearoff=0)
        out.add_command(label="EXİT",command=lambda:self.kapat(master,soket))
        menu_bar.add_cascade(label="EXİT",menu=out)

        master.config(menu=menu_bar)
        self.start_connection(soket,karsininpubi)

    def kapat(self,master,soket):
        soket.close()
        master.destroy()

    def secretMode(self,master):
        for i in range(0,22):
            self.labels[i].config(bg="white",fg="gray85")
    
    def normalMode(self,master):
        for i in range(0,22):
            self.labels[i].config(bg="ghost white",fg="black")
        
    def start_connection(self,soket,karsininpubi):
        al=th.Thread(target=lambda:self.alici(soket,karsininpubi))
        al.start()

    def alici(self,sock,karsininpubi):
        while True:
            text=client.recv_msg(sock,karsininpubi)
            time.sleep(0.5)
            if(len(text)>0):
                self.show_message("guest",text)
                text=""
            print(text)
    def verici(self,text,sock,addr,karsininpubi):
        client.send_msg(sock, addr, karsininpubi,text)



if __name__ == "__main__":
    master=tk.Tk()
    arayüz=GUI(master,"Connect","220x75",False,"ikon.ico")
    arayüz.setFirstWindow(master)
    tk.Button(master, text="Connect",command=lambda:master.destroy()).grid(row=2, column=0)
    arayüz.mainloop()
    ip,port=arayüz.getValue()
    print("ip=",ip,"\nport=",port)
    port=int(port)
    root=tk.Tk()
    chatting=GUI(root,"Ayşe Tatile Çıksın","1200x600",False,"ikon.ico")
    chatting.startchat(root,ip,port)
    chatting.mainloop()
    print("Screen close")
else:
   tk.messagebox.showerror("Fatal error","warning program has fatal error pleace connect us deneme@deneme.com")
