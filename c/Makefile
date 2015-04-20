CFLAGS = -g -Wall

CP := cp

PREFIX := $(HOME)/sad

all: ux2mac mac2ux

ux2mac: ux2mac.o
	$(LINK.c) -o $@ $<

mac2ux: mac2ux.o
	$(LINK.c) -o $@ $<

ux2mac.o: x2y.c
	$(COMPILE.c) -DNAME=\"ux2mac\" -DFROM=0x0d -DTO=0x0a -o $@ $<

mac2ux.o: x2y.c
	$(COMPILE.c) -DNAME=\"mac2ux\" -DFROM=0x0a -DTO=0x0d -o $@ $<

install:
	$(CP) ux2mac $(PREFIX)/bin
	$(CP) mac2ux $(PREFIX)/bin

clean:
	-rm *.o ux2mac mac2ux

