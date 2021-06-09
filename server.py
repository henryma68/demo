'''
GRPC Server for Image Upload
Image Upload v1
proto:ImageUpload.proto
'''
from threading import Thread
from concurrent import futures

import grpc
import ImageUpload_pb2
import ImageUpload_pb2_grpc

import time
from PIL import Image
from PIL import ImageDraw
import numpy as np

from pycoral.adapters import common
from pycoral.adapters import detect
from pycoral.utils.dataset import read_label_file
from pycoral.utils.edgetpu import make_interpreter

threshold = 0.4

import os

import Lib
import ImageProcess
#pic_count = 0

class ImageUploadSrvService(ImageUpload_pb2_grpc.ImageUploadSrvServicer):
    def analyze(self, request_iterator, context):
        start_time_server=time.time()
        print("--------------Calling Function Analyzeing--------------")
        for req in request_iterator:
            #pic_count= pic_count+1 #picture number
            print("--------------Uploading--------------")
            cam=req.camera
            img=req.pic            
            t=req.elapsed_time #Image Sending Time
            file_name=req.name          
            
            image=Lib.byte_array_to_image(img) #Trasfer bytes to PIL Image
            file_name=ImageProcess.obj_dect(interpreter,image,file_name,labels)
            #file_name=Lib.write_image(image,file_name)
            print("Image Location:"+file_name)            
            
        # Time Calculation
        end_time = time.time()
        end_time=end_time-start_time_server
        response = ImageUpload_pb2.Result(result="Upload Finished",process_time=end_time)
        return response    

def model_init():    
    # model loading
    global labels 
    labels = read_label_file("./src/coco_labels.txt") 
    print(labels)
    #if labels else {}
    global interpreter
    interpreter = make_interpreter("./src/ssd_mobilenet_v2_coco_quant_postprocess_edgetpu.tflite")
    print(interpreter)
    interpreter.allocate_tensors()
    print("--------------SSD Mobilenet v2 Model Completed !--------------")



def serve():
    MAX_MESSAGE_LENGTH = 512*1024*1024  

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10),options=[
               ('grpc.max_send_message_length', MAX_MESSAGE_LENGTH),
               ('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH),
               ])
    ImageUpload_pb2_grpc.add_ImageUploadSrvServicer_to_server(ImageUploadSrvService(),server)
    
    server.add_insecure_port('[::]:8080')

    model_init()
    
    print("--------------starting Image server--------------")   
    # #  interpreter global var

    server.start()
    server.wait_for_termination()    


if __name__ == '__main__':
    
    serve()
