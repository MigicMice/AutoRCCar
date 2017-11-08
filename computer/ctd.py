# -*- coding:utf-8 -*-
import sys
import numpy as np
import socket
import cv2
import pygame
from pygame.locals import *

# ----------vision
server_socket.bind(('192.168.1.102', 8000))
server_socket.listen(0)
connection = self.server_socket.accept()[0].makefile('rb')
k = np.zeros((4, 4), 'float')
for i in range(4):
    k[i, i] = 1
temp_label = np.zeros((1, 4), 'float')
# ----------------
pygame.init()
screem = pygame.display.set_mode((400, 400))

BUF_SIZE = 1024  # 设置缓冲区的大小
server_addr = ('192.168.1.102', 8888)  # IP和端口构成表示地址
try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 返回新的socket对象
except socket.error, msg:
    print "Creating Socket Failure. Error Code : " + str(msg[0]) + " Message : " + msg[1]
    sys.exit()
client.connect(server_addr)  # 要连接的服务器地址

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
Trick = "Trick"
# --------v
saved_frame = 0
total_frame = 0
print 'Start collecting images...'
e1 = cv2.getTickCount()
image_array = np.zeros((1, 38400))
label_array = np.zeros((1, 4), 'float')
try:
    stream_bytes = ' '
    frame = 1
    while send_inst:
        stream_bytes += connection.read(1024)
    first = stream_bytes.find('\xff\xd8')
    last = stream_bytes.find('\xff\xd9')
    if first != -1 and last != -1:
        jpg = stream_bytes[first:last + 2]
        stream_bytes = stream_bytes[last + 2:]
        image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.CV_LOAD_IMAGE_GRAYSCALE)

        # select lower half of the image
        roi = image[120:240, :]

        # save streamed images
        cv2.imwrite('training_images/frame{:>05}.jpg'.format(frame), image)

        # cv2.imshow('roi_image', roi)
        cv2.imshow('image', image)

        # reshape the roi image into one row array
        temp_array = roi.reshape(1, 38400).astype(np.float32)

        frame += 1
        total_frame += 1

        while True:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    key_input = pygame.key.get_pressed()
                    if key_input[K_ESCAPE]:
                        sys.exit()
                    elif key_input[K_UP]:
                        print forward
                        saved_frame += 1
                        image_array = np.vstack((image_array, temp_array))
                        label_array = np.vstack((label_array, k[2]))
                        client.sendall(forward)
                    elif key_input[K_DOWN]:
                        print backword
                        saved_frame += 1
                        image_array = np.vstack((image_array, temp_array))
                        label_array = np.vstack((label_array, k[3]))
                        client.sendall(backword)
                    elif key_input[K_LEFT]:
                        print left
                        image_array = np.vstack((image_array, temp_array))
                        label_array = np.vstack((label_array, k[0]))
                        saved_frame += 1
                        client.sendall(left)
                    elif key_input[K_RIGHT]:
                        print right
                        image_array = np.vstack((image_array, temp_array))
                        label_array = np.vstack((label_array, k[1]))
                        saved_frame += 1
                        client.sendall(right)
                    elif key_input[K_t]:
                        client.sendall(Trick)
        client.close()

train = image_array[1:, :]
train_labels = label_array[1:, :]

# save training data as a numpy file
file_name = str(int(time.time()))
directory = "training_data"
if not os.path.exists(directory):
    os.makedirs(directory)
try:
    np.savez(directory + '/' + file_name + '.npz', train=train, train_labels=train_labels)
except IOError as e:
    print(e)

e2 = cv2.getTickCount()
# calculate streaming duration
time0 = (e2 - e1) / cv2.getTickFrequency()
print 'Streaming duration:', time0

print(train.shape)
print(train_labels.shape)
print 'Total frame:', total_frame
print 'Saved frame:', saved_frame
print 'Dropped frame', total_frame - saved_frame
finally:
connection.close()
server_socket.close()

