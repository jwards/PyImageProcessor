from PIL import Image

def open_image(fd):
    img = Image.open(fd)
    #img.show()
    print(img.format)
    print(img.mode)
    return img

def convert_to_bayer(image):
    width, height = image.size
    bayer = Image.new("RGB",(width,height),0xFFFFFF)
    for x in range(width):
        for y in range(height):
            r, g, b = image.getpixel((x, y))
            if x % 2 and y % 2:
                bayer.putpixel((x,y),(0,0,b))
            elif x % 2 and not y % 2:
                bayer.putpixel((x, y), (0, g, 0))
            elif not x % 2 and not y % 2:
                bayer.putpixel((x, y), (r, 0, 0))
            elif not x % 2 and y % 2:


                bayer.putpixel((x, y), (0, g, 0))
    return bayer

def convert_from_bayer(image):
    width, height = image.size
    converted = Image.new("RGB", (width, height), 0xFFFFFF)
    for x in range(width-1):
        for y in range(height-1):
            r1, g1, b1 = image.getpixel((x, y))
            r2, g2, b2 = image.getpixel((x, y+1))
            r3, g3, b3 = image.getpixel((x+1, y))
            r4, g4, b4 = image.getpixel((x+1, y+1))
            rc,gc,bc = (0,0,0)
            if x % 2 and y % 2:
                rc = r4
                bc = b1
                gc = (g2+g3)/2
            elif x % 2 and not y % 2:
                rc = r3
                bc = b2
                gc = (g1 + g4) / 2
            elif not x % 2 and not y % 2:
                rc = r1
                bc = b4
                gc = (g2 + g3) / 2
            elif not x % 2 and y % 2:
                rc = r2
                bc = b3
                gc = (g1 + g4) / 2

            converted.putpixel((x, y),(rc,gc,bc))

    return converted


def matrix_multiply(rgb,cm):
    y = cm[0][0] * rgb[0] + cm[0][1] * rgb[1] + rgb[2] * cm[0][2] + 16
    cb= cm[1][0] * rgb[0] + cm[1][1] * rgb[1] + rgb[2] * cm[1][2] + 128
    cr = cm[2][0] * rgb[0] + cm[2][1] * rgb[1] + rgb[2] * cm[2][2] + 128
    return int(y),int(cb),int(cr)



def convert_to_ycbcr(image):
    m_ycbcr = [[0.183,0.614,0.062],[-0.101, -0.338, 0.439],[0.439, -0.399, -0.040]]
    width, height = image.size
    ycbcr = Image.new("RGB", (width, height), 0xFFFFFF)
    for x in range(width):
        for y in range(height):
            ycbcr.putpixel((x, y), matrix_multiply(image.getpixel((x,y)),m_ycbcr))
    return ycbcr


def main():
    img = open_image("apple.png")
    #bayer = convert_to_bayer(img)
    #converted = convert_from_bayer(bayer)
    ycbr = convert_to_ycbcr(img)

    ycbr.show()
    #bayer.save("bayer.bmp")
    ycbr.save("ycbr.bmp")
    #converted.save("orig_bayer_orig.bmp")
    #converted.show()

main()