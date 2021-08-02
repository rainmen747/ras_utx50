CFLAGS := -O2 -std=c99 -Wall

adu_example: rain_fx3.o
	$(CC) -o rain_fx3 rain_fx3.o -lusb-1.0

default: rain_fx3

clean:
	rm rain_fx3 rain_fx3.o
