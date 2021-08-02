import tkinter 
import time
#import subprocess
import usb.core
import usb.util



def pulseON():
    for i in range(1,5):
        ret=dev.ctrl_transfer(0x40,0x21, 0x21, 0x0, "pulseON",1000)
        time.sleep(0.5)
    

def pulseOFF():
    for i in range(1,5):
        ret=dev.ctrl_transfer(0x40,0x21, 0x20, 0x0, "pulseOFF",1000)
        time.sleep(0.5)
    
    
dev = usb.core.find(idVendor=0x32e9, idProduct=0xfff1)
if dev is None:
    raise ValueError('Device is not found')
# device is found :-)
#print(dev)

#dev.set_configuration()

usb.util.claim_interface(dev, 0)



window=tkinter.Tk()

window.title("Rainmen")
window.geometry("1000x480+100+100")
window.resizable(True,True)
myCanvas = tkinter.Canvas(window, bg="white", height=400, width=1020)

scrollbar=tkinter.Scrollbar(window)
scrollbar=tkinter.Scrollbar(orient=tkinter.HORIZONTAL)

scrollbar.pack(side="bottom", fill="x")
scrollbar.config(command=myCanvas.xview)
myCanvas.pack() 

bt_pulseon = tkinter.Button(window, text="pulse ON",overrelief="solid", width=15, command=pulseON, repeatdelay=1000, repeatinterval=1000)
bt_pulseon.pack() 
 
bt_pulseoff = tkinter.Button(window, text="pulse OFF",overrelief="solid", width=15, command=pulseOFF, repeatdelay=1000, repeatinterval=1000)
bt_pulseoff.pack() 

#ret=dev.ctrl_transfer(0x40,0x21, 0x20, 0x0, "pulseOFF")


while True:
    data= dev.read(0x81,1024*16,100)
    line_array = [(n, 20+data[n+1000]) for n in range(1,1000)]
    myCanvas.create_line(line_array,fill="Blue")

    #for ix in range(1,500,1):
        #myCanvas.create_line(ix*2,20+(data[ix+200]),ix*2+2,20+(data[ix+1+200]),fill="Blue")
    myCanvas.update()
    time.sleep(0.1)
    myCanvas.delete("all")
    



    
    
window.mainloop()


    
