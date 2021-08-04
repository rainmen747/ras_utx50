#
# branch _1_
#
import tkinter 
import time
import subprocess
import usb.core
import usb.util

count=0;



def pulseON():
    for i in range(1,5):
        ret=dev.ctrl_transfer(0x40,0x21, 0x21, 0x0, "pulseON",1000)
        time.sleep(0.5)
    

def pulseOFF():
    for i in range(1,5):
        ret=dev.ctrl_transfer(0x40,0x21, 0x20, 0x0, "pulseOFF",1000)
        time.sleep(0.5)
    

def countUP():
    global count
    lb_count.config(text=str(count))
    
dev = usb.core.find(idVendor=0x32e9, idProduct=0xfff1)
if dev is None:
    raise ValueError('Device is not found')
# device is found :-)
#print(dev)

#dev.set_configuration()

usb.util.claim_interface(dev, 0)



window=tkinter.Tk()

window.title("Rainmen")
window.geometry("1080x600+100+100")
window.resizable(True,True)


ScopeImage = tkinter.PhotoImage(file = "./scope.gif")

myCanvas = tkinter.Canvas(window, bg='#ffffff', height=270, width=1020)
myCanvas.place(x=0,y=10)
myCanvas.pack()
scrollbar=tkinter.Scrollbar(window)
scrollbar=tkinter.Scrollbar(orient=tkinter.HORIZONTAL)

scrollbar.pack(side="bottom", fill="x")
scrollbar.config(command=myCanvas.xview)
myCanvas.pack() 

bt_pulseon = tkinter.Button(window, text="pulse ON", width=15, fg="Brown",command=pulseON).place(x=10,y=450)
bt_pulseoff = tkinter.Button(window, text="pulse OFF", width=15,fg="Yellow",bg="gray", command=pulseOFF).place(x=10,y=480)



lb_count = tkinter.Label(window, text="0",fg="red")
lb_count.pack()
lb_count.place(x=10,y=410)

#ret=dev.ctrl_transfer(0x40,0x21, 0x20, 0x0, "pulseOFF")

#pen.color:=rgb($00,$ff,$ff);
       

while True:
    data= dev.read(0x81,1024*16,10)
    if ((count % 4)==0):
        line_array = [(n, 10+data[n+1020]) for n in range(1,1000)]
        myCanvas.delete("all")
        #myCanvas.create_image(0, 0, anchor = tkinter.NW, image = ScopeImage)

        #myCanvas.create_line(line_array,fill='#00ffff')
        myCanvas.create_line(line_array,fill='Blue')
        myCanvas.create_line((0,135),(1020,135),fill='#888888')
        
        myCanvas.update()
        countUP();
    count+=1
    #for ix in range(1,500,1):
        #myCanvas.create_line(ix*2,20+(data[ix+200]),ix*2+2,20+(data[ix+1+200]),fill="Blue")
    #time.sleep(0.1)
    
   



    
    
window.mainloop()


    
