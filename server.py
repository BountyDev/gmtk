import asyncore
import socket
from packet import Packet
from match import Match
import threading
import random
import time
import struct

def server(port):
    random.seed(time.time())
    outgoing = []
    BS = 10024
    ids = {}
    conns = {}
    queue = []
    arr = {}
    games = {}
    un = {}

    #Constants
    BIT = 0
    BYTE = 1
    STRING = 2
    INT = 3
    DOUBLE = 4
    FLOAT = 5
    SHORT = 6
    USHORT = 7
    def readstring(mess):
        global mes
        s=""
        p=""
        while(p!="\x00"):
            p=struct.unpack('s', mess[:1])[0].decode("utf-8")
            mess=mess[1:]
            s+=p
        mes = mess
        return s[:-1]

    def readint(mess):
        global mes
        old = mess
        mes = mess[4:]
        return struct.unpack('i', old[:4])[0]

    def rec(message):
      global mes
      mes = message
      packet = Packet()
      arr[0] = readstring(mes)

      if arr[0] == "queue":
          pid = readint(mes)
          queue.append(pid)
          print("Entered Queue")

          if len(queue) == 2:
              print("Match found")
              new = {}
              num = 0
              for i in queue:
                new[num] = i
                packet.clear()
                packet.write(2, 'queue')
                packet.write(3, len(games))
                packet.write(3, num)
                packet.send(ids[i], packet)
                num+=1
              queue.clear()
              games["game" + str(len(games))] = Match(new[0], new[1], ids[new[0]], ids[new[1]])


      if arr[0] == "leave":
          pid = readint(mes)
          queue.remove(pid)

      if arr[0] == "move":
          xx = readint(mes)
          yy = readint(mes)
          pid = readint(mes)
          match = readint(mes)
          pn = readint(mes)
          #xs = readint(mes)

          cur = games["game" + str(match)]
          cur.update(xx,yy,pn)

          send = cur.grab(pn)

          packet.clear()
          packet.write(2, 'move')
          packet.write(3, xx)
          packet.write(3, yy)
          packet.send(send, packet)

      if arr[0] == "hit":
          game = readint(mes)
          pn = readint(mes)

          cur = games["game" + str(game)]
          chck = cur.hit(pn)

          players = cur.list()

          if chck:
              for i in players:
                  packet.clear()
                  packet.write(2, 'end')
                  packet.send(i, packet)
              games.pop("game"+str(game))

      if arr[0] == "shoot":
          xx = readint(mes)
          yy = readint(mes)
          dir = readint(mes)
          match = readint(mes)
          pn = readint(mes)

          cur = games["game" + str(match)]

          send = cur.grab(pn)

          packet.clear()
          packet.write(2, 'shoot')
          packet.write(3, xx)
          packet.write(3, yy)
          packet.write(3, dir)
          packet.send(send, packet)

    class MainServer(asyncore.dispatcher):
      def __init__(self, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(('127.0.0.1', port))
        self.listen(10)
        print("Server is up")
      def handle_accept(self):
        conn, addr = self.accept()
        print ('Connection address:' + addr[0] + " " + str(addr[1]))
        conn.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)
        outgoing.append(conn)
        playerid = len(ids)+1
        conns[conn] = playerid
        update = ['id update', playerid]
        ids[playerid] = conn
        username = 'user' + str(random.randint(1,999))
        un[playerid] = username
        packet = Packet()
        packet.clear()
        packet.write(2, 'init')
        packet.write(2, username)
        packet.write(3, playerid)
        packet.send(conn, packet)
        Run(conn, playerid)

    class Run(asyncore.dispatcher_with_send):
      def __init__(self, cd, pi):
          self.pi = pi
          threading.Thread.__init__(self)
          asyncore.dispatcher_with_send.__init__(self, cd)

      def handle_read(self):
        recievedData = self.recv(BS)
        if recievedData:
          rec(recievedData)
        else:
            player_id = self.pi
            ids.pop(player_id)
            un.pop(player_id)

            packet = Packet()

            self.close()


    MainServer(port)
    asyncore.loop()

server(4000)
