'''
GRPC client for Testing Network Latency
Image Upload v1
proto:ImageUpload.proto
'''
from __future__ import print_function
import grpc
import ImageUpload_pb2
import ImageUpload_pb2_grpc

import time
import os 

import numpy as np
import Lib

Path = './data/'
allFileList = os.listdir(Path)
camera_num ="1"

def generaterequest(stub):
    print("--------------Call Image Analyzing Begin--------------")
    start_time = time.time()
    print("Start Time:%f S" % (start_time))

    def stream():
        for file in allFileList:
                        
            file=Path+file
            print(file)
            print(type(file))
            img_str=Lib.image_to_byte_array(file)                        
            print(type(img_str))
            print('--------------Start Transmition--------------')            
            request=ImageUpload_pb2.Image(camera=camera_num,pic=img_str,elapsed_time=start_time,name=file)
            yield request

    response = stub.analyze(stream())
    end_time = time.time()
    end_time = end_time - start_time
    print(response.result)
    print("Process Time:%f S" % (response.process_time))
    print("NetWork Latency:%f S" % (end_time))

def run():  
    channel_opt = [('grpc.max_send_message_length', 512 * 1024 * 1024), ('grpc.max_receive_message_length', 512 * 1024 * 1024)]
    channel = grpc.insecure_channel('localhost:8080',  channel_opt)
    stub = ImageUpload_pb2_grpc.ImageUploadSrvStub(channel)
    generaterequest(stub)

if __name__ == '__main__':    
    run()
