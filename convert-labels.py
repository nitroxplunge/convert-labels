import xml.etree.cElementTree as ET
import os
from PIL import Image
import argparse

parser = argparse.ArgumentParser(description='Convert label files between datatypes.')
parser.add_argument('directory', metavar='d', type=str, nargs='+',
                    help='The directory of the dataset')
parser.add_argument('-r', action='store_true',
                    default=False, help='Replace the existing label files')
parser.add_argument('-v', action='store_true',
                    default=False, help='Print actions')
args = parser.parse_args()

# Returns a 2D array of lines
def readKITTI(filename):
    arr_out = []
    try:
        f = open(filename, 'r')
    except IOError:
        f = open(filename, 'w')
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            linearr = line.rstrip().split(" ")
            arr_out.append(linearr)
    return arr_out

def KITTItoVOC(data, filename, args):
    dir_arr = filename.split("/")

    f_xml = ET.Element("annotation")

    ET.SubElement(f_xml, "folder").text = dir_arr[-2]
    ET.SubElement(f_xml, "filename").text = dir_arr[-1]
    ET.SubElement(f_xml, "path").text = filename

    e_source = ET.SubElement(f_xml, "source")
    ET.SubElement(e_source, "database").text="Unknown"

    img_size = getImgDimensionsForLabel(filename)
    e_size = ET.SubElement(f_xml, "size")
    ET.SubElement(e_size, "width").text = str(img_size[0])
    ET.SubElement(e_size, "height").text = str(img_size[1])
    ET.SubElement(e_size, "depth").text = "3"

    ET.SubElement(f_xml, "segmented").text = "0"

    for line in data:
        e_object = ET.SubElement(f_xml, "object")
        ET.SubElement(e_object, "name").text = line[0]
        ET.SubElement(e_object, "pose").text = "Frontal"
        ET.SubElement(e_object, "truncated").text = line[1]
        ET.SubElement(e_object, "difficult").text = "0"
        ET.SubElement(e_object, "occluded").text = line[2]
        
        e_bndbox = ET.SubElement(e_object, "bndbox")
        ET.SubElement(e_bndbox, "xmin").text = line[4]
        ET.SubElement(e_bndbox, "xmax").text = line[6]
        ET.SubElement(e_bndbox, "ymin").text = line[5]
        ET.SubElement(e_bndbox, "ymax").text = line[7]

    tree = ET.ElementTree(f_xml)
    dir_name = dir_arr[0:-1]
    dir_name = "/".join(dir_name)
    tree.write(dir_name + "/" + dir_arr[-1].split(".")[0] + ".xml")
    if (args.v):
        print ("Created " + dir_arr[-1].split(".")[0] + ".xml")
    if (args.r):
        os.remove(filename)
        if (args.v):
            print ("Removed " + dir_arr[-1])

def getImgDimensionsForLabel(filename):
    imgname = filename.split("/")[-1].split(".")[0] + ".jpg"
    fullimgname = filename.split("/")[0:-2]
    fullimgname.append(imgname)
    fullimgname = "/".join(fullimgname)
    img = Image.open(fullimgname)
    return img.size

dir_list = os.listdir(os.path.realpath(args.directory[0] + "/labels"))

for f in dir_list:
    filename = os.path.realpath(args.directory[0] + "/labels/" + f)
    KITTItoVOC(readKITTI(filename), filename, args)