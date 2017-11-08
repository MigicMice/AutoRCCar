# -*- coding:utf-8 -*-
import sys
import socket
import pygame
from pygame.locals import *

#----------vision

#----------------
pygame.init()
screem = pygame.display.set_mode((400,400))

BUF_SIZE = 1024  #设置缓冲区的大小
server_addr = ('192.168.1.103', 8888)  #IP和端口构成表示地址
try : 
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #返回新的socket对象
except socket.error, msg :
    print "Creating Socket Failure. Error Code : " + str(msg[0]) + " Message : " + msg[1]
    sys.exit()
client.connect(server_addr)  #要连接的服务器地址

'''
while True:
    data = raw_input("Please input some string > ")  
    if not data :
        print "input can't empty, Please input again.."
        continue
    client.sendall(data)  #发送数据到服务器
    data = client.recv(BUF_SIZE)  #从服务器端接收数据
    print data
'''
forward = "Forward"
backword = "Backward"
left = "Left"
right = "Right"



while True:
	for event in pygame.event.get():
		if event.type == KEYDOWN:
			key_input = pygame.key.get_pressed()
			if key_input[K_ESCAPE]:
				sys.exit()
			elif key_input[K_UP]:
				print forward
				client.sendall(forward)
			elif key_input[K_DOWN]:
				print backword
				client.sendall(backword)
			elif key_input[K_LEFT]:
				print left		
				client.sendall(left)
			elif key_input[K_RIGHT]:
				print right
				client.sendall(right)
client.close()				

			
			