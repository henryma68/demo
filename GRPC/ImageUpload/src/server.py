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
import cv2
import os

Path = './results/'
pic_count = 0


class ImageUploadSrvService(ImageUpload_pb2_grpc.ImageUploadSrvServicer):
    def analyze(self, request_iterator, context):
        start_time_server=time.time()
        print("--------------Calling Function Analyzeing--------------")
        for req in request_iterator:
            
            print("--------------Uploading--------------")
            cam=req.camera
            img=req.pic
            t=req.elapsed_time#Image Sending Time
            file_name=req.name

            file_name = Path+file_name
            print("Image Location:"+file_name)
            nparr = np.fromstring(img, np.uint8)
            picture = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            cv2.imwrite(file_name,picture)
            
        # Time Calculation
        end_time = time.time()
        end_time=end_time-start_time_server
        response = ImageUpload_pb2.Result(result="Upload Finished",process_time=end_time)
        return response    

def serve():
    MAX_MESSAGE_LENGTH = 512*1024*1024
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10),options=[
               ('grpc.max_send_message_length', MAX_MESSAGE_LENGTH),
               ('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH),
               ])
    ImageUpload_pb2_grpc.add_ImageUploadSrvServicer_to_server(ImageUploadSrvService(),server)
    
    server.add_insecure_port('[::]:50051')
    
    print("--------------starting Image server--------------")    
    

    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()