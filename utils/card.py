import os
import time
from lxml import etree

from constants import COORDINATES

CARD_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "cards"))
TEMPLATE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "templates"))
FONT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "fonts"))
sbLight = os.path.join(FONT_PATH, "Sarabun-Light.ttf")
sbMedium = os.path.join(FONT_PATH, "Sarabun-Medium.ttf")
sbRegular = os.path.join(FONT_PATH, "Sarabun-Regular.ttf")

def make_timestamp_element(timestamp):
    tag = etree.Element(
        "text",
        x = str(COORDINATES['timestamp']['x']),
        y = str(COORDINATES['timestamp']['y'])
    )
    tag.set("text-anchor", "start")
    tag.set("class", "subtext black")
    tag.text = timestamp
    return tag

def make_train_name_element(trainName):
    tag = etree.Element(
        "text",
        x = str(COORDINATES['train_name']['x']),
        y = str(COORDINATES['train_name']['y'])
    )
    tag.set("text-anchor", "middle")
    tag.set("class", "head1")
    if len(trainName) > 28:
        # Exceeding max trainName length (28 characters)
        formatted = ""
        for wrd in list(trainName.split(" ")):
            if (len(formatted) + len(wrd) + 1) < 28:
                formatted = formatted + " " + wrd
                print(formatted)
        tag.text = formatted
    else:
        tag.text = trainName
    return tag

def make_train_number_element(trainNumber):
    tag = etree.Element(
        "text",
        x = str(COORDINATES['train_number']['x']),
        y = str(COORDINATES['train_number']['y'])
    )
    tag.set("text-anchor", "middle")
    tag.set("class", "head1")
    tag.text = str(trainNumber)
    return tag

def make_loco_number_element(locoNumber):
    tag = etree.Element(
        "text",
        x = str(COORDINATES['loco_number']['x']),
        y = str(COORDINATES['loco_number']['y'])
    )
    tag.set("text-anchor", "middle")
    tag.set("class", "title black")
    tag.text = str(locoNumber)
    return tag

def make_loco_shed_element(locoShed):
    tag = etree.Element(
        "text",
        x = str(COORDINATES['loco_shed']['x']),
        y = str(COORDINATES['loco_shed']['y'])
    )
    tag.set("text-anchor", "start")
    tag.set("class", "head1")
    tag.text = locoShed
    return tag

def make_loco_class_element(locoClass):
    tag = etree.Element(
        "text",
        x = str(COORDINATES['loco_class']['x']),
        y = str(COORDINATES['loco_class']['y'])
    )
    tag.set("text-anchor", "end")
    tag.set("class", "head1")
    tag.text = locoClass
    return tag

def make_location_element(location):
    tag = etree.Element(
        "text",
        x = str(COORDINATES['location']['x']),
        y = str(COORDINATES['location']['y'])
    )
    tag.set("text-anchor", "end")
    tag.set("class", "subtext black")
    if len(location) > 14:
        # Exceeding max location length (14 characters)
        formatted = ""
        for wrd in list(location.split(" ")):
            if (len(formatted) + len(wrd) + 1) < 14:
                formatted = formatted + " " + wrd
        tag.text = formatted
    else:
        tag.text = location
    return tag

def make_username_element(username):
    tag = etree.Element(
        "text",
        x = str(COORDINATES['username']['x']),
        y = str(COORDINATES['username']['y'])
    )
    tag.set("text-anchor", "middle")
    tag.set("class", "subtext white")
    tag.text = username
    return tag

def create_spotting_svg(data):
    if not data or not {'username', 'timestamp', 'spotting_category', '_id'}.issubset(data):
        return None

    try:
        with open(os.path.join(TEMPLATE_PATH, "{}.svg".format(data['loco_class'])), 'r') as file:
            template = file.read()

        xml = etree.XML(template)

        outputFile = os.path.abspath(os.path.join(CARD_PATH, "{}.svg".format(data['_id'])))

        styleTag = etree.Element("style")
        styleTag.text = "@font-face {"+"font-family: \"Sarabun\"; src:url({});".format(sbRegular)+"}"+\
        "@font-face {"+"font-family: \"Sarabun Medium\"; src:url({});".format(sbMedium)+"}"+\
        "@font-face {"+"font-family: \"Sarabun Light\"; src:url({});".format(sbLight)+"}"+\
        ".title { font-family: \"Sarabun Medium\", sans-serif; font-size: 25px; fill: #FFF}\
        .black { fill: #000 }\
        .white { fill: #FFF }\
        .head1 { font-family: Sarabun, sans-serif; font-size: 20px; fill: #FFF }\
        .head2 { font-family: Sarabun, sans-serif; font-size: 18px; fill: #FFF }\
        .head3 { font-family: Sarabun, sans-serif; font-size: 16px; fill: #FFF }\
        .subtext { font-family: Sarabun Light, sans-serif; font-size: 14px; }\
        .center { text-align: center }"

        xml.append(styleTag)

        if "loco_number" in data:
            xml.append(make_loco_number_element(data['loco_number']))
        if "loco_shed" in data:
            xml.append(make_loco_shed_element(data['loco_shed']))
        if "loco_class" in data:
            xml.append(make_loco_class_element(data['loco_class']))
        if "train_number" in data:
            xml.append(make_train_number_element(data['train_number']))
        if "train_name" in data:
            xml.append(make_train_name_element(data['train_name']))
        if "spotting_location" in data:
            xml.append(make_location_element(data['spotting_location']))

        xml.append(make_username_element(data['username']))
        timestamp = time.strftime("%b %d, %Y %H:%M", time.localtime(data['timestamp']))
        xml.append(make_timestamp_element(timestamp))

        with open(outputFile, 'w') as file:
            file.write(etree.tostring(xml).decode('utf-8'))

        return outputFile

    except Exception as e:
        print("Exception @ create_spotting_svg\n{}".format(e))
        return None