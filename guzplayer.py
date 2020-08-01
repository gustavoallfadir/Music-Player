from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askopenfile
from tkinter import messagebox
from pygame import mixer
import os
import pickle

#init mixer
mixer.init()
#seting home directory
home_dir=os.getenv("HOME")
os.chdir(home_dir)


#----------Revisar si existe librería y crear si no existe----

try:
    libreria=open("libreria","rb")
    libreria.close()

except:
    empty=list()
    libreria=open("libreria","wb")
    pickle.dump(empty,libreria)
    libreria.close()

#------------File Finder-----------------------------

def find_file(name, path):
    
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


#----------------------Root y frames------------------
root=Tk()
root.title("Guzblack Music Player")
root.config(bg="#0B0B3B")
root.geometry("600x500+300+50")
root.minsize(400,400)
root.maxsize(800,600)
root.resizable(1,1)



frame=Frame(root,bg="#0B0B3B")
frame.pack(padx=20,pady=10, fill="both",expand="true")

statusframe=Frame(root,bg="#0B0B3B")
statusframe.pack()

buttonframe=Frame(root, bg="#0B0B3B")
buttonframe.pack(side="bottom",pady=20)


#-----------------------Variables-------------------
playlist=list()
listdir=StringVar()
trackVar=StringVar()
status=StringVar()
paused=bool()



#-----------------------Funciones--------------------
def opendir():
    directorio=askdirectory()

    canciones = os.listdir(directorio)
    
    #preparando para actualizar libreria
    archivo=open("libreria", "rb")
    temp=pickle.load(archivo)

    # insertar canciones en el Playlist
    for track in canciones:
        if track.endswith('.mp3'):

            playlistbox.insert(END,track) #inserta en lista actual
            temp.append(track) #inserta en libreria

    archivo.close()
    
    archivo=open("libreria","wb")
    pickle.dump(temp,archivo)
    archivo.close()

    


def openfile():
    file=askopenfilename(filetypes =[('Audio mp3', '*.mp3')])
    
    track = os.path.basename(file)

    playlistbox.insert(END, track)

    #actualizar librería
    archivo=open("libreria", "rb")
    temp=pickle.load(archivo)
    temp.append(track)

    archivo.close()

    archivo=open("libreria","wb")
    pickle.dump(temp, archivo)
    archivo.close()


def removefile():
    
    target=playlistbox.get(ACTIVE)
    playlistbox.delete(ACTIVE)

    #actualizar librería
    archivo=open("libreria", "rb")
    temp=pickle.load(archivo)
    temp.remove(target)

    archivo.close()

    archivo=open("libreria","wb")
    pickle.dump(temp, archivo)
    archivo.close()



def play():
    global paused

    if paused == True:

        mixer.music.unpause()

        status.set("Playing")

        paused=False
    
    else:
        path=find_file(playlistbox.get(ACTIVE),".")

        mixer.music.load(path)

        mixer.music.play()

        trackVar.set(playlistbox.get(ACTIVE))

        status.set("Playing")

        paused=False


def stop():
    mixer.music.stop()

    trackVar.set("")
    status.set("")

def pause():
    global paused

    if paused == True:

        mixer.music.unpause()

        status.set("Playing")

        paused=False

    else:

        mixer.music.pause()
        status.set("Paused")

        paused=True


def playnext():
    pass

def playprev():
    pass

def salir():
    root.destroy()


def acerca_de():
    messagebox.showinfo("Guzblack Music Player","Creado por Gustavo Allfadir\nTodos los derechos reservados.\n©2020")

#-----------------------Menus------------------------

#Setup

barramenu=Menu(root, fg="white", bg="#0B0B3B")
root.config(menu=barramenu)

#Comandos menu

menuarchivo=Menu(barramenu, tearoff=0, fg="white", bg="#0B0B3B")
menuarchivo.add_command(label="Agregar carpeta",command=lambda:opendir())
menuarchivo.add_command(label="Agregar archivo", command=lambda:openfile())
menuarchivo.add_command(label="Quitar archivo", command=lambda:removefile())
menuarchivo.add_command(label="Salir",command=lambda:salir())


menuayuda=Menu(barramenu,tearoff=0, fg="white", bg="#0B0B3B")
menuayuda.add_command(label="Acerca de...", command=acerca_de)


#Cascadas del menu
barramenu.add_cascade(label="Archivo", menu=menuarchivo)
barramenu.add_cascade(label="Ayuda", menu=menuayuda)


#-----------------------Playlist---------------------


playlistbox=Listbox(frame,font=18,fg="white", bg="black", selectmode="single")
playlistbox.pack(side="left",expand="true", fill="both")
#playlistbox.grid(row=0,column=0, padx=10,pady=10)

scrollvert=Scrollbar(frame, command=playlistbox.yview) #agregar un scroll bar y anclarla a la caja de texto
scrollvert.pack(side="right",fill="y")
#scrollvert.grid(row=0, column=1,sticky="nsw",pady=10, padx=10)


#----------------------Status------------------------

tracktxt=Label(statusframe, textvariable=trackVar,fg="white", bg="#0B0B3B")
tracktxt.pack(side="bottom")

statustxt=Label(statusframe, textvariable=status,fg="white", bg="#0B0B3B")
statustxt.pack(side="top")


#-----------------------Botones----------------------
'''
previousbutton=Button(buttonframe, font=18,text="prev",fg="white", bg="#0B0B3B")
previousbutton.grid(row=1,column=0, pady=10)
'''

playbutton=Button(buttonframe, text="▶",font=18,fg="white", bg="#0B0B3B", command=lambda:play())
playbutton.grid(row=1,column=1, pady=10)

'''
nextbutton=Button(buttonframe, text="next",font=18,fg="white", bg="#0B0B3B", command=lambda:playnext())
nextbutton.grid(row=1,column=2, pady=10)
'''

pausebutton=Button(buttonframe, text="pause",font=19,fg="white", bg="#0B0B3B", command=lambda:pause())
pausebutton.grid(row=1,column=3, pady=10)

stopbutton=Button(buttonframe, text="stop",font=19,fg="white", bg="#0B0B3B", command=lambda:stop())
stopbutton.grid(row=1,column=4, pady=10)

#-----------------------biblioteca-------------------

try:
    archivo=open("libreria","rb")
    libreria=pickle.load(archivo)
    
    for track in libreria:
            
        playlistbox.insert(END,track)

    archivo.close()

except:
    pass



#------------------------MAINLOOP--------------------

root.mainloop()     