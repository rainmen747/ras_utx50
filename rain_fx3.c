// NOTE: when running the example, it must be run with root privileges in order to access the USB device.
// usblink_AD100 usb 3.0 fx3 
// orientndt jw.kim 2021.7.25
//
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <errno.h>
#include <string.h>

// libusb library must be available. It can be installed on Debian/Ubuntu using apt-get install libusb-1.0-0-dev
#include <libusb-1.0/libusb.h>

#define VENDOR_ID      0x32e9  // Ontrak vendor ID. This should never change
#define PRODUCT_ID     0xfff1  // AD200 product ID. Set this product ID to match your device.
 

#define TRANSFER_SIZE    16*1024     // 

// Write a command to an ADU device with a specified timeout
int write_to_adu( libusb_device_handle * _device_handle, const char * _cmd, int _timeout )
{
    const int command_len = strlen( _cmd ); // Get the length of the command string we are sending

    int bytes_sent = 0;

    // Buffer to hold the command we will send to the ADU device.
    // Its size is set to the transfer size for low or full speed USB devices (ADU model specific - see defines at top of file)
    unsigned char buffer[ TRANSFER_SIZE ]; 

    if ( command_len > TRANSFER_SIZE )
    {
        printf( "Error: command is larger than our limit of %i\n", TRANSFER_SIZE );
        return -1;
    }

    memset( buffer, 0, TRANSFER_SIZE ); // Zero out buffer to pad with null values (command buffer needs to be padded with 0s)

    buffer[0] = 0x01; // First byte of the command buffer needs to be set to a decimal value of 1

    // Copy the command ASCII bytes into our buffer, starting at the second byte (we need to leave the first byte as decimal value 1)
    memcpy( &buffer[1], _cmd, command_len ); 

    // Attempt to send the command to the OUT endpoint (0x01) with the use specified millisecond timeout
    int result = libusb_interrupt_transfer( _device_handle, 0x01, buffer, TRANSFER_SIZE, &bytes_sent, _timeout );
    printf( "Write '%s' result: %i, Bytes sent: %u\n", _cmd, result, bytes_sent );

    if ( result < 0 ) // Was the interrupt transfer successful?
    {
        printf( "Error sending interrupt transfer: %s\n", libusb_error_name( result ) );
    }

    return result; // Returns 0 on success, a negative number specifying the libusb error otherwise
}

// Read a command from an ADU device with a specified timeout
int read_from_fx3( libusb_device_handle * _device_handle, unsigned char * buffer, int _read_len, int _timeout )
{
  	    
   int read_data;
   
   libusb_bulk_transfer(_device_handle,0x81,buffer,_read_len,&read_data,_timeout);

    return read_data; // returns 0 on success, a negative number specifying the libusb error otherwise
}


int main( int argc, char **argv )
{
    struct libusb_device_handle * device_handle = NULL; // Our ADU's USB device handle
	int result;
    unsigned char buffer[16*2*1024];
    memset(buffer,0,16*2*1024);
    
    // Initialize libusb
    result = libusb_init( NULL );
    if ( result < 0 )
    {
        printf( "Error initializing libusb: %s\n", libusb_error_name( result ) );
        exit( -1 );
    }

    // Set debugging output to max level
    libusb_set_option( NULL, LIBUSB_OPTION_LOG_LEVEL, LIBUSB_LOG_LEVEL_WARNING );

    // Open our ADU device that matches our vendor id and product id
    device_handle = libusb_open_device_with_vid_pid( NULL, VENDOR_ID, PRODUCT_ID );
    if ( !device_handle )
    {
        printf( "Error finding USB device\n" );
        libusb_exit( NULL );
        exit( -2 );
    }

    libusb_set_auto_detach_kernel_driver( device_handle, 1 );

    // Claim interface 0 on the device
    result = libusb_claim_interface( device_handle, 0 );
    if ( result < 0 )
    {
        printf( "Error claiming interface: %s\n", libusb_error_name( result ) );
        if ( device_handle )
        {
            libusb_close( device_handle );
        }

        libusb_exit( NULL );
        exit( -3 );
    }

	//printf("pulse off ");
	for(int qq=0;qq<5;qq++)	
	libusb_control_transfer(device_handle,0x40,0x21,0x20,0,0,0,1000);
    
    	
    int i;
 
    while(1)    {
        read_from_fx3(device_handle,buffer,TRANSFER_SIZE,200);
        //printf("%d  %d------------------------------------\n",ix,ret);
        for (i=0;i<1020;i++) printf("%d ",buffer[i+2000]);
        printf("\n");
    }
    printf("Ok closing....\n");

    // We are done with our device and will now release the interface we previously claimed as well as the device
    libusb_release_interface( device_handle, 0 );
    libusb_close( device_handle );

    // Shutdown libusb
    libusb_exit( NULL );

    return 0;
}


char *testgood(char *mess)
{
        return mess;
}

int add(int a,int b)
{
        return a+b;
}


