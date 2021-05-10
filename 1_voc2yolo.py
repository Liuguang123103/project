import os
import xml.etree.ElementTree as ET

datapath = 'data/VOC2007'
savepath = 'model_data/trainlist.txt'
classes = ["palte"]

def convert_annotation( image_id, list_file):
    xml_path = os.path.join(datapath,'Annotations/%s.xml'%(image_id))
    in_file = open(xml_path)
    tree=ET.parse(in_file)
    root = tree.getroot()

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), int(xmlbox.find('xmax').text), int(xmlbox.find('ymax').text))
        list_file.write(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))

txt = os.path.join(datapath,'ImageSets/Main/trainval.txt')
image_ids = open(txt).read().strip().split()
list_file = open(savepath, 'w')
for image_id in image_ids:
    file_path = os.path.join(datapath,'JPEGImages/%s.jpg'%(image_id))
    list_file.write(file_path)
    convert_annotation(image_id, list_file)
    list_file.write('\n')
list_file.close()

txt = os.path.join(datapath,'ImageSets/Main/test.txt')
image_ids = open(txt).read().strip().split()
list_file = open('model_data/test.txt', 'w')
for image_id in image_ids:
    file_path = os.path.join(datapath,'JPEGImages/%s.jpg'%(image_id))
    list_file.write(file_path)
    convert_annotation(image_id, list_file)
    list_file.write('\n')
list_file.close()

print('ok')
