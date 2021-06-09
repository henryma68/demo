# Obj Detection

#Library import
#import argparse
import time
from PIL import Image
from PIL import ImageDraw

from pycoral.adapters import common
from pycoral.adapters import detect
#from pycoral.utils.dataset import read_label_file
#from pycoral.utils.edgetpu import make_interpreter

threshold = 0.4
count = 1

def draw_objects(draw, objs, labels):
  """Draws the bounding box and label for each object."""
  for obj in objs:
    bbox = obj.bbox
    draw.rectangle([(bbox.xmin, bbox.ymin), (bbox.xmax, bbox.ymax)],
                   outline='red',width=5)
    draw.text((bbox.xmin + 10, bbox.ymin + 10),
              '%s\n%.2f' % (labels.get(obj.id, obj.id), obj.score),
              fill='red')

def obj_dect(interpreter,image_PIL,savepath,labels):
    # Obj Detection
    _, scale = common.set_resized_input(interpreter, image_PIL.size, lambda size: image_PIL.resize(size, Image.ANTIALIAS))

    print('----INFERENCE TIME----')
    print('Note: The first inference is slow because it includes',
        'loading the model into Edge TPU memory.')
    for _ in range(count):
        start = time.perf_counter()
        interpreter.invoke()
        inference_time = time.perf_counter() - start
        objs = detect.get_objects(interpreter, threshold, scale)
        print('%.2f ms' % (inference_time * 1000))

    print('-------RESULTS--------')
    if not objs:
        print('No objects detected')

    for obj in objs:
        print(labels.get(obj.id, obj.id))
        print('  id:    ', obj.id)
        print('  score: ', obj.score)
        print('  bbox:  ', obj.bbox)

    image_PIL = image_PIL.convert('RGB')
    draw_objects(ImageDraw.Draw(image_PIL), objs, labels)
    savepath=savepath.replace("./data/","./results/")
    image_PIL.save(savepath)
    #image.show()

    return savepath

