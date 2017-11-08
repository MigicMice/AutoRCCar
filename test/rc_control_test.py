#coding=utf-8
__author__ = 'zhengwang'
import sys
import socket
import pygame
import threading
import struct
from pygame.locals import *
#Receive message
class Receiver(threading.Thread):
    def __init__(self,threadName,window):
        threading.Thread.__init__(self)
        self.threadName = threadName
        self.window = window
        self.timeToQuit = threading.Event()
        self.timeToQuit.clear()
        #连接服务器
        # Create a socket (SOCK_STREAM means a TCP socket)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # Connect to server and send data
            self.sock.connect((self.window.host, self.window.port))
            self.window.LogMessage("连接服务器成功...\n")
            self.runT = True
        except Exception:
            self.window.LogMessage("连接服务器失败...\n")
            self.sock.close()

    def stop(self):
        self.window.LogMessage("关闭Socket连接...\n")
        self.sock.close()
        self.runT = False
        self.timeToQuit.set()

    def sendMsg(self,msg):
        logMsg = (u"发送：%s\n" % (msg))
        self.window.LogMessage(logMsg)
        self.sock.sendall(msg)

    def run(self):
        try:
            while self.runT:
                data = self.sock.recv(4)
                if data:
                    dataLen, = struct.unpack_from("i",data)
                    wx.CallAfter(self.window.LogMessage,(u"返回数据长度:%s\n" % (dataLen)))
                    wx.CallAfter(self.window.LogMessage,(u"返回数据:%s\n" % (self.sock.recv(dataLen))))
        except Exception:
            pass

class RCTest(object):

    def __init__(self):
        


        pygame.init()
        screen = pygame.display.set_mode((500, 500))
        self.send_inst = True
        self.steer()

    def steer(self):

        while self.send_inst:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    key_input = pygame.key.get_pressed()

                    if key_input[K_ESCAPE]:
                        sys.exit()
                    # simple orders
                    if key_input[pygame.K_UP]:
                        print("Forward")
                        #self.forward()
                        #self.ser.write(chr(1))

                    elif key_input[pygame.K_DOWN]:
                        print("Reverse")
                        #self.back()
                        #self.ser.write(chr(2))

                    elif key_input[pygame.K_RIGHT]:
                        print("Right")
                        #self.right()
                        #self.ser.write(chr(3))

                    elif key_input[pygame.K_LEFT]:
                        print("Left")
                        #self.left()
                        #self.ser.write(chr(4))
                    elif event.type == QUIT:
                        sys.exit()

                        


    def forward(self,event):
        self.thread.sendMsg("forward")

    def back(self,event):
        self.thread.sendMsg("back")

    def left(self,event):
        self.thread.sendMsg("left")

    def right(self,event):
        self.thread.sendMsg("right")

    def stop(self,event):
        self.thread.sendMsg("stop")
                    



if __name__ == '__main__':
    #Receiver()
    RCTest()
