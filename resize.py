## Resize Image

import os 
from PIL import Image


file=("./data/")
allFileList = os.listdir(file)
dist=("./ImageResized/")
number=0

for f in allFileList:
    
    f=file+f
    image = Image.open(f)
    image = image.convert('RGB')
    image = image.resize((300, 300),Image.ANTIALIAS)    
    resize=dist+str(number)+".jpg"
    print(resize)
    number+=1
    image.save(resize)