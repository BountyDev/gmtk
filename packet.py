import socket
import asyncore
import select
import random
import pickle
import time
import json
import struct
import hashlib, binascii, os

class Packet():

    #Initialize the packet
    def __init__(self):

        #Buffer variables
        self.Buffer = -1
        self.BufferO = -1
        self.BufferWrite = []
        self.BufferWriteT = []
        #Constants
        self.BIT = 0
        self.BYTE = 1
        self.STRING = 2
        self.INT = 3
        self.DOUBLE = 4
        self.FLOAT = 5
        self.SHORT = 6
        self.USHORT = 7


    #Clear the packet
    def clear(self):

        #Clear the lists
        self.BufferWrite.clear()
        self.BufferWriteT.clear()


    #Write to the packet
    def write(self, buffer_type, value):

        #Check for buffer type
        if buffer_type == self.BIT:
            self.BufferWrite.append(value)
            self.BufferWriteT.append("?")
        elif buffer_type == self.BYTE:
            self.BufferWrite.append(value)
            self.BufferWriteT.append("B")
        elif buffer_type == self.STRING:
            self.BufferWriteT.append("{}s".format(len(value)+1))
            self.BufferWrite.append(value.encode("utf-8")+b'\x00')
        elif buffer_type == self.INT:
            self.BufferWrite.append(value)
            self.BufferWriteT.append("i")
        elif buffer_type == self.DOUBLE:
            self.BufferWrite.append(float(value))
            self.BufferWriteT.append("d")
        elif buffer_type == self.FLOAT:
            self.BufferWrite.append(value)
            self.BufferWriteT.append("f")
        elif buffer_type == self.SHORT:
            self.BufferWrite.append(value)
            self.BufferWriteT.append("h")
        elif buffer_type == self.USHORT:
            self.BufferWrite.append(value)
            self.BufferWriteT.append("H")


    #Read from the packet
    def read(self, buffer_type):

        #Check for buffer type
        if buffer_type == self.BIT:
            Buffer2=self.Buffer
            self.Buffer=self.Buffer[1:]
            return struct.unpack('?', Buffer2[:1])[0]
        elif buffer_type == self.BYTE:
            Buffer2=self.Buffer
            self.Buffer=self.Buffer[1:]
            return struct.unpack('B', Buffer2[:1])[0]
        elif buffer_type == self.STRING:
            s=""
            p=""
            while(p!="\x00"):
                p=struct.unpack('s', self.Buffer[:1])[0].decode("utf-8")
                self.Buffer=self.Buffer[1:]
                s+=p
            return s[:-1]
        elif buffer_type == self.INT:
            Buffer2=self.Buffer
            self.Buffer=self.Buffer[4:]
            return struct.unpack('i', Buffer2[:4])[0]
        elif buffer_type == self.DOUBLE:
            Buffer2=self.Buffer
            self.Buffer=self.Buffer[8:]
            return struct.unpack('d', Buffer2[:8])[0]
        elif buffer_type == self.FLOAT:
            Buffer2=self.Buffer
            self.Buffer=self.Buffer[4:]
            return struct.unpack('f', Buffer2[:4])[0]
        elif buffer_type == self.SHORT:
            Buffer2=self.Buffer
            self.Buffer=self.Buffer[2:]
            return struct.unpack('h', Buffer2[:2])[0]
        elif buffer_type == self.USHORT:
            Buffer2=self.Buffer
            self.Buffer=self.Buffer[2:]
            return struct.unpack('H', Buffer2[:2])[0]


    #Send the packet
    def send(self, client, pack, all = None):
        #Variables
        packet = pack
        types = ''.join(packet.BufferWriteT)
        length=struct.calcsize(types)
        if all == "all":
            for c in outgoing:
                c.send(struct.pack("="+types,*packet.BufferWrite))
        else:
            #Send
            if client != None:
                client.send(struct.pack("="+types,*packet.BufferWrite))
