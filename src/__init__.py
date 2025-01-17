import cv2
import numpy as np
from PIL import ImageFont,ImageDraw,Image
import os
import pandas as pd

# DRIVER CODE FOR DELETING OLD CERRTIFICATES
# USEFUL FOR TESTING 
def clean():
       x=input("enter folder name to clean: ")
       print("Cleaning {} folder ........".format(str(x)))
       for certificates in os.listdir("result/{}/".format(str(x))):
        os.remove("result/{}/{}".format(str(x),certificates))
       print("completed.......")

# FOR READING FROM TEXT FILE
def open_textfile():
    file=open("names.txt",'r')
    name_ls=file.read().split('\n')
    return name_ls

'''
GENERATION USING PILLOW MODULE
'''
def pillow(name_ls):
   # MAIN CODE FOR GENERTING CERTIFICATES
    def certificate_gen(name_ls):
        for name in name_ls:
            template=cv2.imread('certificate.jpg')
            '''
            When the image file is read with the OpenCV function imread(), the order of colors is BGR (blue, green, red),
            but where as in Pillow, the order of colors is assumed to be RGB (red, green, blue) (ik its bullshit)
            So..if you want to use both the Pillow function and the OpenCV function,
            you need to convert BGR and RGB.
            '''
            template_conv = cv2.cvtColor(template,cv2.COLOR_BGR2RGB)
            arr_img= Image.fromarray(template_conv)
            var_draw=ImageDraw.Draw(arr_img)
            pacifico=ImageFont.truetype("fonts/Pacifico.ttf",90)
            sofia_regular = ImageFont.truetype("fonts/Sofia-Regular.otf", 20) # CAN IMPLEMENT MORE THAN ONE FONT      
            var_draw.text((1253,660),name,font=pacifico,fill='grey') # DEFINING CO-ORDS NAME AND FONT-COLOR
            final_res=cv2.cvtColor(np.array(arr_img),cv2.COLOR_RGB2BGR) # RE-CONVERTING IMAGE FROM ARRAY INFO
            cv2.imwrite("result/pillow/{}.jpg".format(name), final_res) # TO SAVE THE FINAL OUTPUT
            print("{}'s certificate generated using PILLOW".format(name))
    open_textfile()
    certificate_gen(name_ls)
'''
GENERATION USING cv2 MODULE
'''
def cv_2(name_ls):
    for name in name_ls:
      template=cv2.imread('certificate.jpg')
      # Syntax: cv2.putText(image, text, org, font, fontScale, color[, thickness[, lineType[, bottomLeftOrigin]]])
      cv2.putText(template, name.strip(),(1123,795),cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 4, (128, 128, 128), 10)
      cv2.imwrite("result/cv2/{}.jpg".format(name.strip()),template)
      print("{}'s certificate generated using Open cv".format(name))
      
if __name__=="__main__":
    clean()

    print('Do you want to convert contents of a text file to a list or a csv file?\n1.names.txt\n2.names.csv')
    choice=int(input("Enter your choice: as (1) or (2): "))
    if(choice) == 1:
        try:
            name_ls=open_textfile()
        except:
            print("Error in opening the file")
    else:
        try:
            df = pd.read_csv('names.csv')
            name_ls = df['NAMES'].tolist()
        except:
            print("File not found")
            exit()
    pillow(name_ls)
    cv_2(name_ls)
    