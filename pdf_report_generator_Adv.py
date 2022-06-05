# -*- coding: utf-8 -*-
"""
Created on Wed Jan  1 00:54:05 2020

@author: a0485645
"""
from tkinter import filedialog
import tkinter as tk
import os
from fpdf import FPDF
import threading


def folder_button():
    global folder_path
    folderbox.delete("1.0",tk.END)
    foldername = filedialog.askdirectory()
    folder_path.set(foldername)
    folderbox.insert(tk.END,foldername)
    folderbox.see(tk.END)
    outbox_msg(foldername)
    return None


def file_button():
    global file_path
    filebox.delete("1.0",tk.END)
    filename = filedialog.asksaveasfilename()
    file_path.set(filename)
    filebox.insert(tk.END,filename)
    filebox.see(tk.END)
    outbox_msg(filename)
    return None

def outbox_msg(msg):
    outbox.configure(state="normal")
    outbox.insert(tk.END,msg+'\n')
    outbox.see(tk.END)
    outbox.configure(state="disable")
    root.update()
    return None

thread_flag=False
stop_flag=False
def runbutton():
    global t,stop_flag
#    foldername=folderbox.get("1.0",'end-1c')
#    filename=filebox.get("1.0",'end-1c')
    if runscript.cget('text')=='RUN':
        # print("pre pdf gen run scritp")
        runscript.configure(text="Stop",bg="Red")
        stop_flag=False
        print("stop_flag set to:",stop_flag)
        # root.after(10,pdf_gen(folderbox,filebox))
        t=threading.Thread(target=pdf_gen,args=(folderbox,filebox))
        t.start()
        print("started a thread")
    else:
        stop_flag=True
        print("stop_flag set to:",stop_flag)
        runscript.configure(text="wait...",bg="yellow")
        # print("post pdf gen run scritp")
    return None

def pdf_gen(folder,file):
    global thread_flag,stop_flag
    thread_flag=False
    # stop_flag=False
    status.configure(text="Running")
    status['background']='red'
    processes['background']='red'
    foldername=folder.get("1.0",'end-1c') ## extract input directory
    filename=file.get("1.0",'end-1c')   ## extract output pdf file name
    pdf = FPDF('L',unit='pt',format='legal') # create an A4-size pdf document
    pdf.set_font('Arial', 'B', 11)

    try:
        os.chdir(foldername)
        try:                ### see if ReadMe.txt file there or not
            with open("ReadMe.txt", "r") as f:
                data = f.read().split("\n")
                pdf.add_page()
            for i in data:
                pdf.cell(100)
                pdf.cell(ln=1, h=15.0, align='L', w=0, txt=i, border=0)
        except:
            msg="No ReadMe.txt file found !"
            outbox_msg(msg)

        for root, dirs, files in os.walk(foldername, topdown = True):
            for image in files:
                rel_dir = os.path.relpath(root,foldername)
                path = os.path.join(rel_dir, image)
#               path=os.path.join(root,image)
                outbox_msg(path)
#               root.update()

                if (image[-3:]=='png') or (image[-3:]=='PNG'):
                    try:
                        pdf.add_page()
                        pdf.cell(0,0, path)
                        pdf.image(path,40,40,0,500)
                    except:
                        print("Error !! PNG encoding error ):")
                else:
                    outbox_msg("Skipped")

                # print("flag in loop:",stop_flag)
                if stop_flag==True:
                    print('break inner loop')
                    outbox_msg("------Aborted--------")
                    status.configure(text="Done (｡◕‿◕｡)",bg="yellow green")
                    processes['background']='yellow'
                    thread_flag=True
                    print("thread flag set to:",thread_flag)
                    runscript.configure(text="RUN",bg="deep sky blue")
                    return

            # if stop_flag==True:
            #     print('break outer loop')
            #     break


        outbox_msg("----------------Generating pdf May take some time------------")
        status.configure(text="Generating pdf")
        pdf.output(filename,"F")
        # folderbox.delete("1.0",tk.END)
        # filebox.delete("1.0",tk.END)
        outbox_msg("Done! (◕‿◕)           |")
        outbox_msg("      <) (>           |")
        outbox_msg("      _/ \_  ʕ •ᴥ•ʔ   !")
        outbox_msg("```````````````````````")

    except:
        outbox_msg("No such directory {:~(")
#        print("dir not available")
    status.configure(text="Done (｡◕‿◕｡)")
    processes['background']='yellow'
    status['background']='yellow green'
    thread_flag=True
    print("thread flag set to:",thread_flag)
    runscript.configure(text="RUN",bg="deep sky blue")

    return None

root = tk.Tk()
root.geometry("1000x600+100+50")
root.resizable(0,0)
root.title('Report Generator')
#### Variables to store foldername and filename
folder_path = tk.StringVar()
file_path=tk.StringVar()
## frame for show actions
frame00=tk.Frame(root,bg="#5FA8A8",bd=2,relief=tk.SUNKEN)
frame00.place(relx=0.75,rely=0.5, anchor="center",relwidth=0.5,relheight=1)
## frame for intractions
frame0=tk.Frame(root,bg="#87A4B3",bd=2)
frame0.place(relx=0.25,rely=0.5, anchor="center",relwidth=0.5,relheight=1)
## frames
frame1=tk.Frame(frame0,bg="#87A4B3",bd=5)
frame1.pack(side=tk.TOP,fill=tk.BOTH,expand=True)
frame2=tk.Frame(frame0,bg="#87A4B3",bd=5)
frame2.pack(side=tk.TOP,fill=tk.BOTH,expand=True)
frame3=tk.Frame(frame0,bg="#87A4B3",bd=5)
frame3.pack(side=tk.TOP,fill=tk.BOTH,expand=True)

tk.Grid.columnconfigure(frame1,0, weight=1) ## equal weight to all the columns
tk.Grid.columnconfigure(frame1,1, weight=1)
tk.Grid.columnconfigure(frame1,2, weight=1)

## button to browse folder
in_dir=tk.Button(frame1,text='Select Dir.',font='Helvetica 11 bold',height=2,
                 relief=tk.RAISED,bd=5,command=folder_button)
in_dir.grid(row=1,column=0,sticky="ew",padx=5,pady=5)

in_label=tk.Label(frame1, text="Input Dir.",font='Helvetica 11 bold')
in_label.grid(row=0,column=1,sticky="w",padx=1,pady=1)

folderbox = tk.Text(frame1,width=10,height=5,bd=5,relief=tk.SUNKEN)
folderbox.grid(row=1,column=1,columnspan=2,sticky="ew",padx=1,pady=1)
folderbox.grid_propagate(False)

tk.Grid.columnconfigure(frame2,0, weight=1) ## equal weight to all the columns
tk.Grid.columnconfigure(frame2,1, weight=1)
tk.Grid.columnconfigure(frame2,2, weight=1)

## button to output folder
out_dir=tk.Button(frame2,text='Output Dir.',font='Helvetica 11 bold',height=2,
                  relief=tk.RAISED,bd=5,command=file_button)
out_dir.grid(row=1,column=0,sticky="ew",padx=5,pady=5)

in_label=tk.Label(frame2, text="Output file",font='Helvetica 11 bold')
in_label.grid(row=0,column=1,sticky="w",padx=1,pady=1)

filebox = tk.Text(frame2,width=10,height=5,bd=5,relief=tk.SUNKEN)
filebox.grid(row=1,rowspan=2,column=1,columnspan=2,sticky="ew",padx=1,pady=1)
filebox.grid_propagate(False)

# t=threading.Thread(target=pdf_gen,args=(folderbox,filebox))

if thread_flag==True:
    t.join()
    stop_flag=True
    runscript.configure(text="RUN",bg="deep sky blue")
    print("thread is closed")

runscript=tk.Button(frame3,text='RUN',font='Helvetica 11 bold',width=10,height=2,
        relief=tk.RAISED,bg="deep sky blue",bd=5,command=lambda: runbutton() )#pdf_gen(folderbox,filebox))#runbutton)
runscript.pack(side=tk.RIGHT)
runscript["activebackground"] = 'red'



sts="Not Running"
status=tk.Label(frame3, text=sts,font='Helvetica 11 bold',bd=5,bg='yellow green',width=10,height=2)
status.pack(side=tk.RIGHT,padx=5,pady=5)
processes=tk.Label(frame00, text="---Processings---",bd=5,bg='yellow')
processes.pack(side=tk.TOP,fill=tk.X)
outbox = tk.Text(frame00)
outbox.pack(side=tk.TOP,fill=tk.BOTH,expand=True,padx=1,pady=1)


tk.mainloop()




