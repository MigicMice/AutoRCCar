__author__ = 'zhengwang'

import numpy as np
import cv2
import sys
import pygame
from pygame.locals import *
import socket
import time
import os


class CollectTrainingData(object):
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((400, 400))

        self.server_socket = socket.socket()
        self.server_socket.bind(('192.168.1.100', 8000))
        self.server_socket.listen(0)

        self.BUF_SIZE = 1024
        self.server_addr = ('192.168.1.103',8888)

        try:
            self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        except socket.error,msg:
            print "Creating Socket Failure. Error Code : " + str(msg[0]) + " Message : " + msg[1]
            sys.exit()
        self.client.connect(self.server_addr)
        self.forward = "Forward"
        self.backward = "Backward"
        self.left = "Left"
        self.right = "Right"
        #Trick = "Trick"


        #-------
        # accept a single connection
        self.connection = self.server_socket.accept()[0].makefile('rb')



        # create labels
        self.k = np.zeros((4, 4), 'float')
        for i in range(4):
            self.k[i, i] = 1
        self.temp_label = np.zeros((1, 4), 'float')


        self.collect_image()

    def collect_image(self):

        saved_frame = 0
        total_frame = 0

        # collect images for training
        print 'Start collecting images...'
        e1 = cv2.getTickCount()
        image_array = np.zeros((1, 38400))
        label_array = np.zeros((1, 4), 'float')

        # stream video frames one by one
        try:
            stream_bytes = ' '
            frame = 1
            while self.send_inst:
                stream_bytes += self.connection.read(1024)
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
                    
                    #cv2.imshow('roi_image', roi)
                    cv2.imshow('image', image)
                    
                    # reshape the roi image into one row array
                    temp_array = roi.reshape(1, 38400).astype(np.float32)
                    
                    frame += 1
                    total_frame += 1

                    # get input from human driver
                    for event in pygame.event.get():
                        if event.type == KEYDOWN:
                            key_input = pygame.key.get_pressed()
                            if key_input[K_ESCAPE]:
                                sys.exit()

                            # simple orders
                            elif key_input[pygame.K_UP]:
                                print("Forward")
                                saved_frame += 1
                                image_array = np.vstack((image_array, temp_array))
                                label_array = np.vstack((label_array, self.k[2]))
                                self.client.sendall(self.forward)

                            elif key_input[pygame.K_DOWN]:
                                print("Reverse")
                                saved_frame += 1
                                image_array = np.vstack((image_array, temp_array))
                                label_array = np.vstack((label_array, self.k[3]))
                                self.client.sendall(self.backward)
                            
                            elif key_input[pygame.K_RIGHT]:
                                print("Right")
                                image_array = np.vstack((image_array, temp_array))
                                label_array = np.vstack((label_array, self.k[1]))
                                saved_frame += 1
                                self.client.sendall(self.right)

                            elif key_input[pygame.K_LEFT]:
                                print("Left")
                                image_array = np.vstack((image_array, temp_array))
                                label_array = np.vstack((label_array, self.k[0]))
                                saved_frame += 1
                                self.client.sendall(self.left)


                                break
                                    


            # save training images and labels
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
            self.connection.close()
            self.server_socket.close()

if __name__ == '__main__':
    CollectTrainingData()
