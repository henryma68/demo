# publilc function
from PIL import Image
import io


 
def image_to_byte_array(image):
    #use PIL open image first then call
    #this function trasfer image to bytes

    im = Image.open(image)    
    imgByteArr = io.BytesIO()
    im.save(imgByteArr, format=im.format)
    imgByteArr = imgByteArr.getvalue()

    return imgByteArr

def byte_array_to_image(bytes):
    #convert bytes array to image 
       
    image = Image.open(io.BytesIO(bytes))

    return image


    

def write_image(image,savepath):
    #pass image file name savepath:./results/1.jpg
    #bytes bytes array

    savepath=savepath.replace("./1/","./results/")    
    image.save(savepath)

    return savepath