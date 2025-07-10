import io
from typing import List, Tuple, Union
from deskew import determine_skew
import cv2
from fastapi import FastAPI, UploadFile

from pdf2image import convert_from_path

import os

import imutils

import pytesseract

from pytesseract import Output
import base64

import re

app = FastAPI()

def file_to_base64(file_path):
    try:
        with open(file_path, "rb") as file:
            # Read the file content in binary mode
            file_content = file.read()
            # Encode the binary content to Base64
            encoded_content = base64.b64encode(file_content)
            # Decode the Base64 bytes to a UTF-8 string
            base64_string = encoded_content.decode("utf-8")
            return base64_string
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None



def image_orientation_corrector(image_path):
    print(image_path)
    angle_rotate = None
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"The image at path {image_path} could not be found.")
        
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # image_to_osd function is used to extract the orientation detail of an image
    results = pytesseract.image_to_osd(rgb, config='--psm 0 -c min_characters_to_try=5',output_type=Output.DICT)
    
    # Display the orientation information
    print("[INFO] detected orientation: {}".format(results["orientation"]))
    print("[INFO] rotate by {} degrees to correct".format(results["rotate"]))
    print("[INFO] detected script: {}".format(results["script"]))

    if results["script"] == 'Han':
        angle_rotate=180

    elif results["script"] == 'Bengali':
        angle_rotate=0
    else:
        angle_rotate=results["rotate"]
    
    # Rotate the image to correct the orientation
    rotated = imutils.rotate_bound(image, angle=angle_rotate)
    cv2.imwrite(image_path, rotated)


def convertPDFToImages(path_file):
    path_img = path_file.split('/')
    doc_name = path_img[1].split('.')
    doc_name = doc_name[0]
    path_img = path_img[0]

    path_images = []
    
    images = convert_from_path(path_file,poppler_path=r'C:\Program Files\poppler-24.08.0\Library\bin')
    os.makedirs('{}/{}/img'.format(path_img,doc_name), exist_ok=True)
    for i in range(len(images)):
        images[i].save(path_img+'/'+doc_name+'/img/page'+ str(i) +'.jpg', 'JPEG')
        image_orientation_corrector(path_img+'/'+doc_name+'/img/page'+ str(i) +'.jpg')
        path_images.append(path_img+'/'+doc_name+'/img/page'+ str(i) +'.jpg')
    
    return path_images





@app.post("/files/{id_customer}")
async def file_contents(files: List[UploadFile],id_customer:str):
    results=None
    for file in files:
        if file.content_type=='application/pdf':
            os.makedirs(id_customer, exist_ok=True)
            file_location = f"{id_customer}/{file.filename}"
            with open(file_location, "wb+") as file_object:
                file_object.write(file.file.read())
            results=convertPDFToImages(file_location)

    print(results)
    return {"images": [file_to_base64(i) for i in results]}