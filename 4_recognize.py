# -*- coding: utf-8 -*-
import os
from yolo3.card_seg import Cardseg
from yolo3.yolo import YOLO
from PIL import Image
import cv2

input_path ='data/VOC2007/JPEGImages'
output_path = 'outputs'
os.makedirs(output_path,exist_ok=True)

detector = YOLO()

name_list = []
for file in os.listdir(input_path):
    if file.endswith(".jpg"):
        name_list.append(file)

for name in name_list:
# for name in name_list[:2]:#test code
    img_path = os.path.join(input_path, name)
    # img_path = 'test_img/lLD9016.jpg'
    output_img_path = os.path.join(output_path, name)
    image = Image.open(img_path)
    _, _, palte = detector.detect_image(image)
    palte = cv2.cvtColor(palte, cv2.COLOR_RGB2BGR)
    try:
        _, _, pre_palte = Cardseg([palte],['blue'],None)
    except:
        pre_palte=''
    if not pre_palte:
        continue
    save_path = ''
    for s in pre_palte:
        save_path+=s
    save_path = os.path.join(output_path,save_path+'.jpg')
    cv2.imencode('.jpg', palte)[1].tofile(save_path)
    # cv2.imwrite(save_path, palte)
    print(img_path, 'is ok~')

detector.close_session()
print('ok')
