import usb.core
import usb.util

# find our device
dev = usb.core.find(idVendor=0x32e9, idProduct=0xfff1)

# was it found?
if dev is None:
    raise ValueError('Device not found')

# configuration will be the active one
#dev.set_configuration()
usb.util.claim_interface(dev, 0)
print("Device found!")
print(dev)

ret=dev.ctrl_transfer(0x40,0x21, 0x20, 0x0, "pulseOFF")
   