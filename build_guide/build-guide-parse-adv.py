import os
import sys
import re
import random
from PIL import Image, ImageFilter, ImageOps

javascript = '''
if(imgPixel.red > imgPixel.blue && imgPixel.red > imgPixel.green) {
    imgDNA += 'R'
} else if((imgPixel.red > imgPixel.blue && imgPixel.red < imgPixel.green) || (imgPixel.red < imgPixel.blue && imgPixel.red > imgPixel.green)) {
    imgDNA += 'r'
} else {
    imgDNA += 'X'
}

if(imgPixel.green > imgPixel.red && imgPixel.green > imgPixel.blue) {
    imgDNA += 'G'
} else if((imgPixel.green > imgPixel.red && imgPixel.green < imgPixel.blue) || (imgPixel.green < imgPixel.red && imgPixel.green > imgPixel.blue)) {
    imgDNA += 'g'
} else {
    imgDNA += 'X'
}

if(imgPixel.blue > imgPixel.red && imgPixel.blue > imgPixel.green) {
    imgDNA += 'B'
} else if((imgPixel.blue > imgPixel.red && imgPixel.blue < imgPixel.green) || (imgPixel.blue < imgPixel.red && imgPixel.blue > imgPixel.green)) {
    imgDNA += 'b'
} else {
    imgDNA += 'X'
}

if(imgPixel.red == imgPixel.blue == imgPixel.green <= 30) {
    imgDNA += '*'
} else if(imgPixel.red == imgPixel.blue == imgPixel.green) {
    imgDNA += '='
} else {
    imgDNA += '-'
}
'''

import json
f = open('./build_guide/build-seed-pixels.json')
brutePixels = json.load(f)

def getPixel(img, pixel):
    data = img.getdata()[img.width*pixel[1]+pixel[0]]
    # This doesn't make sense, should be 0, 1, 2, 3...
    pixel = {
        "red": data[0],
        "green": data[2],
        "blue": data[1],
        "alpha": data[3]
    }
    return pixel

def extractDNA(img, seedPixels):
    imgDNA = ''
    for pixelToGet in seedPixels:
        pixelToGet = (int(pixelToGet[0]/2), int(pixelToGet[1]/2))
        imgPixel = getPixel(img, pixelToGet)
        
        if imgPixel['red'] > imgPixel['green'] and imgPixel['red'] > imgPixel['blue']:
            imgDNA += 'R'
        elif (imgPixel['red'] > imgPixel['green'] and imgPixel['red'] < imgPixel['blue']) or (imgPixel['red'] < imgPixel['green'] and imgPixel['red'] > imgPixel['blue']):
            imgDNA += 'r'
        else:
            imgDNA += 'X'
        
        if imgPixel['green'] > imgPixel['red'] and imgPixel['green'] > imgPixel['blue']:
            imgDNA += 'G'
        elif (imgPixel['green'] > imgPixel['red'] and imgPixel['green'] < imgPixel['blue']) or (imgPixel['green'] < imgPixel['red'] and imgPixel['green'] > imgPixel['blue']):
            imgDNA += 'g'
        else:
            imgDNA += 'X'

        if imgPixel['blue'] > imgPixel['red'] and imgPixel['blue'] > imgPixel['green']:
            imgDNA += 'B'
        elif (imgPixel['blue'] > imgPixel['red'] and imgPixel['blue'] < imgPixel['green']) or (imgPixel['blue'] < imgPixel['red'] and imgPixel['blue'] > imgPixel['green']):
            imgDNA += 'b'
        else:
            imgDNA += 'X'
        
        if imgPixel['red'] == imgPixel['green'] == imgPixel['blue'] <= 30:
            imgDNA += '*'
        elif imgPixel['red'] == imgPixel['green'] == imgPixel['blue']:
            imgDNA += '='
        else:
            imgDNA += '-'

    return imgDNA

def testSeed(imgs, seedPixels):
    prints = {}
    for img in images:
        dna = extractDNA(img, seedPixels)

        if dna not in prints:
            prints[dna] = re.sub('.png$', '', re.sub(r'^.*\\', '', img.filename))
        else:
            print(f"FAIL ON {img.filename} and {prints[dna]}")
            return None 

    return prints

images = []
for filename in os.listdir("./build_guide/perks"):
    image = Image.open(os.path.join("./build_guide/perks", filename))
    images.append(image)

result = testSeed(images, brutePixels)

print(result)