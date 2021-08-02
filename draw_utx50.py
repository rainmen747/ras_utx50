import tkinter 
import time
import subprocess



proc = subprocess.Popen(['sudo','./rain_fx3'],stdout=subprocess.PIPE)

window=tkinter.Tk()

window.title("Rainmen")
window.geometry("1200x600+100+100")
window.resizable(True,True)
myCanvas = tkinter.Canvas(window, bg="white", height=400, width=1020)
myCanvas.pack() 

x=0
 
while True:
    output_str = proc.stdout.readline()
    s=output_str.decode("utf-8")
    mylist = s.split(" ")
    for ix in range(1,1000,1):
        myCanvas.create_line(ix,20+int(mylist[ix]),ix+1,20+int(mylist[ix+1]),fill="Blue")
    myCanvas.update()
    time.sleep(0.001)
    myCanvas.delete("all")
    
    
    
    
    
window.mainloop()

