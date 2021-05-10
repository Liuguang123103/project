import os
import numpy
from yolo3.yolo import YOLO
from PIL import Image
import cv2
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

input_path ='data/VOC2007/JPEGImages'
output_path = 'output'
os.makedirs(output_path,exist_ok=True)

detector = YOLO()

name_list = []
for file in os.listdir(input_path):
    if file.endswith(".jpg"):
        name_list.append(file)

for name in name_list:
# for name in name_list[:2]:#test code
    img_path = os.path.join(input_path, name)
    output_img_path = os.path.join(output_path, name)
    image = Image.open(img_path)
    detecte_image,[b,s,c],_ = detector.detect_image(image)
    detecte_image= numpy.array(detecte_image)
    cv2.imwrite(output_img_path, detecte_image[:,:,::-1])
    print(img_path,'is ok~')
detector.close_session()

print('ok')
