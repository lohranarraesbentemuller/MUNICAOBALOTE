# -*- coding: utf-8 -*-
 
 
import cv2
import numpy as np
import pytesseract 
from PIL import Image
import face_recognition
import datetime

from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
import os
import unidecode
import mysql.connector
import datetime
import requests
import json
from pprint import pprint
from PIL import Image
import zbarlight
import random
from PIL import Image
import string
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import  CallbackQueryHandler

#pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Meu PC\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'


def same(image1,image2):


  im1 = Image.open(image1)
  im2 = Image.open(image2)

  if list(im1.getdata()) == list(im2.getdata()):
    #print "Identical"
    return True
  else:
    #print "Different"
    return False


    
def acha_placa(frame,canny_img):
   # canny_img=frame
    contours, hierarchy = cv2.findContours(canny_img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    try: hierarchy = hierarchy[0]
    except: hierarchy = []

    height, width = canny_img.shape[:2]
    min_x, min_y = width, height
    max_x = max_y = 0

# computes the bounding box for the contour, and draws it on the frame,
    for contour, hier in zip(contours, hierarchy):
      (x,y,w,h) = cv2.boundingRect(contour)
      min_x, max_x = min(x, min_x), max(x+w, max_x)
      min_y, max_y = min(y, min_y), max(y+h, max_y)
      if w > 80 and h > 80:
          cv2.rectangle(frame, (x,y), (x+w,y+h), (255, 0, 0), 2)

    #if max_x - min_x > 0 and max_y - min_y > 0:
    #  cv2.rectangle(frame, (min_x, min_y), (max_x, max_y), (255, 0, 0), 2)
   # cv2.imshow('a',frame)
   # cv2.waitKey(0)
class charclass:
    def __init__(self, _contour):
     self.contour=_contour
     self.boundingRect=cv2.boundingRect(self.contour)
     self.rect_x, self.rect_y, self.rect_w, self.rect_h = self.boundingRect
     #self.rect_x,self.rect_w=self.rect_h
     self.rect_area=self.rect_w*self.rect_h
     self.x_center=(self.rect_x+self.rect_x+self.rect_w)/2
     self.y_center=(self.rect_y+self.rect_y+self.rect_h)/2
     self.hypotenuse=np.sqrt((self.rect_w**2)+(self.rect_h**2))
     self.aspect_ratio=float(self.rect_w)/float(self.rect_h)
    
 
def getmatchingchars(char_cands):
    char_list=[]
    
    for char_cand in char_cands:
        ch_matches=[]
        for matching_candidate in char_cands:
            if matching_candidate == char_cand:
                 continue
            chardistance=np.sqrt((abs(char_cand.x_center - matching_candidate.x_center)**2)+(abs(char_cand.y_center - matching_candidate.y_center)**2))
            x=float(abs(char_cand.x_center - matching_candidate.x_center))
            y=float(abs(char_cand.y_center - matching_candidate.y_center))
            angle=np.rad2deg(np.arctan(y/x)if x !=0.0 else np.pi/2)
            
            deltaarea=float(abs(matching_candidate.rect_area - char_cand.rect_area)) / float(char_cand.rect_area)
            deltawidth=float(abs(matching_candidate.rect_w-char_cand.rect_w))/float(char_cand.rect_w)
            deltaheight=float(abs(matching_candidate.rect_h-char_cand.rect_h))/float(char_cand.rect_h)
            
            if(chardistance < (char_cand.hypotenuse*5.0) and angle<12.0 and deltaarea<0.5 and deltawidth <0.8 and deltaheight<0.2 ):
                ch_matches.append(matching_candidate)
                
        ch_matches.append(char_cand)
        if len(ch_matches)<3:
            continue
        
        char_list.append(ch_matches)
        
        for charlist in getmatchingchars(list(set(char_cands)-set(ch_matches))):
            char_list.append(charlist)
        break
    return char_list
def gray_tresh_img(input_image):
    h,w, _=input_image.shape
    grayimg = cv2.cvtColor(input_image,cv2.COLOR_BGR2HSV)[:,:,2]
    
    kernel=cv2.getStructuringElement(cv2.MORPH_RECT,(3,3)) 
    
    tophat=cv2.morphologyEx(grayimg,cv2.MORPH_TOPHAT, kernel)
    blackhat=cv2.morphologyEx(grayimg,cv2.MORPH_BLACKHAT,kernel)
    graytop=cv2.add(grayimg,tophat)
    countrastgray=cv2.subtract(graytop,blackhat)
    blurred=cv2.GaussianBlur(countrastgray,(5,5),0)
    thresholded=cv2.adaptiveThreshold(blurred,255.0,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,19,9)
    
    return grayimg,thresholded


def circula_placa(input_image):
 
 h,w= input_image.shape[:2]

 grayimg,thresholded=gray_tresh_img(input_image)
 contours = cv2.findContours(thresholded,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)[0]
 char_cands=[]
 plate_candidates=[]
  
 for index in range(0,len(contours)):
       char_cand=charclass(contours[index])
       if(char_cand.rect_area>80 and char_cand.rect_w>2 and char_cand.rect_h>8 and 0.25<char_cand.aspect_ratio and char_cand.aspect_ratio<1.0):
         char_cands.append(char_cand)

 x=0
 x_contour=list()
 y_contour=list()
 h_contour=list()
 w_contour=list()
 for ch_matches in getmatchingchars(char_cands):
    class blank: pass
    plate_candidate=blank()
    
    ch_matches.sort(key=lambda ch: ch.x_center)
    
    plate_w = int((ch_matches[len(ch_matches)-1].rect_x) + (ch_matches[len(ch_matches)-1].rect_w - ch_matches[0].rect_x))
    
    sum_char_h=0
    for ch in ch_matches:
         sum_char_h += ch.rect_h
         
    avg_char_h=sum_char_h/len(ch_matches)
    plate_h = int(avg_char_h*1.5)
    
    y=ch_matches[len(ch_matches)-1].y_center - ch_matches[0].y_center
    r=np.sqrt(abs(ch_matches[0].x_center - ch_matches[len(ch_matches)-1].x_center)**2 + (abs(ch_matches[0].y_center - ch_matches[len(ch_matches)-1].y_center)**2))
    
    rotate_angle=np.rad2deg(np.arcsin(y/r))
    
    platex=(ch_matches[0].x_center + ch_matches[len(ch_matches)-1].x_center)/2
    platey=(ch_matches[0].y_center + ch_matches[len(ch_matches)-1].y_center)/2
    plate_cent = platex,platey
    
    plate_candidate.plateloc=(tuple(plate_cent),(plate_w,plate_h),rotate_angle)
    
    rotationMatrix=cv2.getRotationMatrix2D(tuple(plate_cent),rotate_angle,1.0)
 
    rotated =cv2.warpAffine(input_image,rotationMatrix,tuple(np.flipud(input_image.shape[:2])))
    
    plate_candidate.plate_im=cv2.getRectSubPix(rotated,(plate_w,plate_h),tuple(plate_cent))
    
    if plate_candidate.plate_im is not None :
        plate_candidates.append(plate_candidate)
        #cv2.drawContours(input_image,ch_matches[2].contour,-1,(255,0,255),3)
        if(x==x):
            
         for xx in ch_matches:
          #cv2.drawContours(input_image,xx.contour,-1,(0,0,255),3)
          x_contour.append(xx.rect_x)
          y_contour.append(xx.rect_y)
          h_contour.append(xx.rect_h)
          w_contour.append(xx.rect_w)
          #cv2.rectangle(input_image, (xx.rect_x,xx.rect_y), (xx.rect_x+xx.rect_w,xx.rect_y+xx.rect_h), (255, 0, 0), 2)
          
    x=x+1
 x1=0
 x2=0
 y1=0
 y2=0
 try:
  min_x=min(x_contour)
  min_y=min(y_contour)
  max_x=max(x_contour)
  max_y=max(y_contour)
  min_w=min(w_contour)
  min_h=min(h_contour)
  max_w=max(w_contour)
  max_h=max(h_contour)
  x1=min_x
  x2=max_y
  y1=max_x+max_w
  y2=max_y+max_h
  #cv2.rectangle(input_image,(min_x,max_y),(max_x+max_w,max_y+max_h),(255, 0, 0), 2)
 except: pass

 text=""
 for plate_candidate in plate_candidates:
     plate_candidate.grayimg,plate_candidate.thresholded=gray_tresh_img(plate_candidate.plate_im)
     plate_candidate.thresholded=cv2.resize(plate_candidate.thresholded,(0,0),fx=1.6,fy=1.6)
     thresholdValue, plate_candidate.thresholded= cv2.threshold(plate_candidate.thresholded,0.0,255.0,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
     #cv2.imshow('a',plate_candidate.thresholded)
   # cv2.waitKey(0)
     #cv2.imwrite('C:/Users/Meu PC/Desktop/saida.jpg',plate_candidate.thresholded)
      
     text = pytesseract.image_to_string(plate_candidate.thresholded)
     #font= cv2.FONT_HERSHEY_DUPLEX
     text=repr(text)
     text=text.replace(chr(92)+'x0c','')
     text=text.replace(chr(92)+'n','')
     text=text.replace('-','')
     text=text.replace(' ','')
     text=text.replace('"','')
     text=text.replace("'",'')
     text=text.replace(":",'')
    # text.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]', '', text)
     #cv2.putText(input_image,repr(text),(min_x,max_y),font,0.5,(255,255,255),1)  
     #print(repr(text))
 
      
 return x1,x2,y1,y2,text 
 
#agora=datetime.datetime.now()
#webcam_video_stream=cv2.VideoCapture('placas.mp4')
#all_face_locations=[]

#input_image= cv2.imread('placa4.jpg')
#placas_ttexto=list()
#images=0
#while True:
#   try: 
 #     ret,input_image = webcam_video_stream.read()
      
 #     current_frame_double=cv2.resize(input_image,(0,0),fx=2,fy=2)
 #     current_frame_half=cv2.resize(input_image,(0,0),fx=0.5,fy=0.5)
 #     current_frame_small=cv2.resize(input_image,(0,0),fx=0.25,fy=0.25)
 #     current_frame_smaller=cv2.resize(input_image,(0,0),fx=0.125,fy=0.125)
      
 #     all_face_location=face_recognition.face_locations(current_frame_small,number_of_times_to_upsample=2,model="hog")
      #current_frame_small=circula_placa(current_frame_small)
 #     for index,current_face_location in enumerate(all_face_location):
 #       top_pos,right_pos,bottom_pos,left_pos=current_face_location
 #       top_pos=top_pos*4
 #       right_pos=right_pos*4
 #       bottom_pos=bottom_pos*4
 #       left_pos=left_pos*4
 #       cv2.rectangle(input_image,(left_pos,top_pos),(right_pos,bottom_pos),(0,0,255),2)      
      
  #    x1,x2,y1,y2,text=circula_placa(current_frame_half)
  #    if len(text)==7:
          
   #       x1=x1*2
   #       x2=x2*2
  #        y1=y1*2
   #       y2=y2*2         
    #      cv2.rectangle(input_image,(x1,x2),(y1,y2),(255, 0, 0), 2)
     #     placas_ttexto.append(text)
      #    font= cv2.FONT_HERSHEY_DUPLEX
       #   cv2.putText(input_image,repr(text),(x1,x2),font,2,(255,255,255),2)  
     # numero=str(images)
 

     # if len(numero)==1: numero='0000'+numero
     # if len(numero)==2: numero='000'+numero
     # if len(numero)==3: numero='00'+numero
     # if len(numero)==4: numero='0'+numero
# 
#      cv2.imwrite('C:/ProgramData/Anaconda3/code/placas/frame'+numero+'.jpg',input_image)    
#      images=images+1
      #    cv2.rectangle(input_image,(x1,x2),(y1,y2),(255, 0, 0), 2)
      #    font= cv2.FONT_HERSHEY_DUPLEX
      #    cv2.putText(input_image,repr(text),(x1,x2),font,0.5,(255,255,255),2)  
 #  except:break       
   #cv2.imshow("teste",input_image)
  # if cv2.waitKey(1) & 0xFF == ord('q'):
   #     break
    
#webcam_video_stream.release()
#cv2.destroyAllWindows()        
#print('placas identificadas')
#unicas=list(set(placas_ttexto))
#for i in unicas:
#    print (i + ' ' + str(placas_ttexto.count(i)))

#for i in placas_ttexto:
 #   print(i)
#import imageio

#images = []
#filenames=filter(lambda x: x.find('frame')!=-1,os.listdir('./'))
#for filename in filenames:
 #   images.append(imageio.imread(filename))
  #  os.remove(filename)
#imageio.mimsave('movie.gif', images)

#print(datetime.datetime.now()-agora)    

def maps(bot,update,args):
  print(args)
  print(len(args[0]))
  if(len(''.join(args))<6): return
  if(len(args)==0):
      bot.send_message(
      chat_id=update.message.chat_id,
      text="Você esqueceu de digitar a placa/nome"
    )
  mydb = mysql.connector.connect(
  host="localhost",
  user="USUARIO_DB",
  passwd="SENHA_DB",
  database="DB"
  )
  mycursor = mydb.cursor()

  hoje= (str(datetime.datetime.now()).split(" ")[0])
  saida=' '.join(args)
  saida=saida.replace('-'," ")
 
     
  print("select lat,lng,data,placa from localizacao_balote where placa like '%"+' '.join(args)+"%' order by data desc limit 5")
  mycursor.execute("select lat,lng,data,placa from localizacao_balote where placa like '%"+' '.join(args)+"%' order by data desc limit 5")
   
  
  myresult = mycursor.fetchall()
  escalados=list();
  for x in myresult:
     bot.send_message(
     chat_id=update.message.chat_id,
     #text="http://maps.google.com/?ie=UTF8&hq=&ll="+x[0]+","+x[1]+"&z=13"
     text="https://www.google.com/maps/?q="+x[0]+","+x[1]
     )
  print("select lat,lng,data,placa from localizacao_balote where placa like '%"+''.join(saida.split(" "))+"%' order by data desc limit 5")
  mycursor.execute("select lat,lng,data,placa from localizacao_balote where placa like '%"+''.join(saida.split(" "))+"%' order by data desc limit 5")
   
  
  myresult = mycursor.fetchall()
  escalados=list();
  for x in myresult:
     bot.send_message(
     chat_id=update.message.chat_id,
    # text="http://maps.google.com/?ie=UTF8&hq=&ll="+x[0]+","+x[1]+"&z=13"
    text="https://www.google.com/maps/?q="+x[0]+","+x[1]
     )

def ultima_localizacao_id(id,message):
    mydb = mysql.connector.connect(
          host="localhost",
          user="USUARIO_DB",
          passwd="SENHA_DB",
          database="DB"
          )
    mycursor = mydb.cursor()
    sql="select * from localizacao_balote where identificacao='"+str(id)+"' and data>=date_add(now(),interval -2 hour_minute) order by data asc limit 1"
    print(sql)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    resultado=""
    for x in myresult:
        resultado=x[0]
    #lohran arraes
    if resultado!="":
       try:
         sql="update localizacao_balote set placa='"+str(message.text)+"' where id="+str(resultado)
       except:
         sql="update localizacao_balote set placa='"+str(message)+"' where id="+str(resultado)
       print(sql)
       print("lohran")
       mycursor.execute(sql)
       mydb.commit()

#erro_humano




def contador_de_simbolo(simbolos,quantidade):
  s=""
  semelhantes=list()
  if(quantidade==0):
     for i in simbolos:
       semelhantes.append(i)
     return semelhantes
  else:
    #if(quantidade==1):
    #if True:
    try:
     for j in contador_de_simbolo(simbolos,quantidade-1):
        try:
          for i in simbolos:
            semelhantes.append(j+i)
        except RecursionError as re:
            return
    except RecursionError as re:
      return
       
    return(semelhantes)

def identifica_simbolo(simbolos,chave):
   locais=list()
   x=0
   for i in chave:
      if i in simbolos:
         locais.append(x)
      x=x+1
   return locais

def cria_substitutos(simbolos,chave,locais):
    lista=list()
    try:
     simbolos2=contador_de_simbolo(simbolos,len(locais)-1)
    except:
      return lista
    #x=0
    for j in simbolos2:
          x=0
          for i in locais:
            chave=chave[:i]+j[x]+chave[i+1:]
            lista.append(chave)
            x=x+1
    return(lista) 

def dicionario(placa):
  placa=placa.upper()
  substitutos1=["B","3","8"]
  substitutos2=["0","O","Q"]
  substitutos3=["1","I","T"]
  substitutos4=["J","U"]
  substitutos5=["M","N","W"]

  substitutosq=list()
  substitutosq.append(list(set(cria_substitutos(substitutos1,placa,identifica_simbolo(substitutos1,placa)))))
  substitutosw=list()
  for i in substitutosq:
     if(isinstance(i,str)):
        substitutosw=substitutosw+list(i)
     else:
       substitutosw=substitutosw+i
  substitutosq=substitutosw
  substitutosq2=list()
  for placa2 in substitutosq:
     try:
       substitutosq2.append(list(set(cria_substitutos(substitutos2,placa2,identifica_simbolo(substitutos2,placa2)))))
     except RecursionError as re:
       continue
     # print('Sorry but this maze solver was not able to finish '
       #     'analyzing the maze: {}'.format(re.args[0]))  
  
  for i in substitutosq2:
       substitutosw=substitutosw+i
       
  substitutosq=substitutosw
  substitutosq2=list()      
  
  
  for placa2 in substitutosw:   
     try:
       substitutosq2.append(list(set(cria_substitutos(substitutos3,placa2,identifica_simbolo(substitutos3,placa2)))))
     except RecursionError as re:
        continue
  
  for i in substitutosq2:
       substitutosw=substitutosw+i
  
  substitutosq=substitutosw
  substitutosq2=list()
        
  for placa2 in substitutosw:
     try:
        substitutosq2.append(list(set(cria_substitutos(substitutos4,placa2,identifica_simbolo(substitutos4,placa2)))))
     except RecursionError as re:
        continue
        
  for i in substitutosq2:
       substitutosw=substitutosw+i
       
  substitutosq=substitutosw
  substitutosq2=list()
  
  for placa2 in substitutosw:
     try:
        substitutosq2.append(list(set(cria_substitutos(substitutos5,placa2,identifica_simbolo(substitutos5,placa2)))))   
     except RecursionError as re:
        continue
  for i in substitutosq2:
      substitutosw=substitutosw+i
  substitutosq=substitutosw
  substitutosq2=list()    
  substitutosw.append(placa)
  return list(set(substitutosw))

#erro_humano

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    #print("Random string of length", length, "is:", result_str)
    return result_str
modo='QRCODE' 
#from conf.settings import BASE_API_URL, TELEGRAM_TOKEN
#TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
#BASE_API_URL = os.getenv("BASE_API_URL")
TELEGRAM_TOKEN='TELEGRAM_TOKEN'
BASE_API_URL='https://http.cat/'
#BASE_API_URL='http://www.cfo2019.com/MUNICAO_BALOTE/teste.php?teste='

#teste2
from google.cloud import vision
import os
import io
import time

def autentica(mensagem):
    mydb = mysql.connector.connect(
    host="localhost",
    user="USUARIO_DB",
    passwd="SENHA_DB",
    database="DB"
    )
    sql="select * from cadastro_balote where id_telegram='"+str(mensagem.from_user.id)+"'"
    mycursor=mydb.cursor()
    mycursor.execute(sql)
    myresult=  mycursor.fetchall()
    if(len(myresult)<1):
       return 0
    else:
       for x in myresult:
         return x[-1]    
    

def qrcode(bot,update):
    path=(str(update.message).split('file_id')[1].split("'")[2])
    url='https://api.telegram.org/bot1223754477:AAEmZcnHbCEBR_q52SimK_R8TTBx2YL0kLE/getFile?file_id='+path
    print(url)
    r=requests.get(url,allow_redirects=True)
    print(r.content)
    url='https://api.telegram.org/file/bot1223754477:AAEmZcnHbCEBR_q52SimK_R8TTBx2YL0kLE/'
    path=str(r.content).split('file_path')[1].split('"')[2]
    r = requests.get(url+path,allow_redirects=True)
    open('/home/wwcfo2/www/MUNICAO_BALOTE/src/temp.jpg','wb').write(r.content)

    file_path = '/home/wwcfo2/www/MUNICAO_BALOTE/src/temp.jpg'
    with open(file_path, 'rb') as image_file:
      image = Image.open(image_file)
      image.load()

    codes = zbarlight.scan_codes(['qrcode'], image)
    try:
     credencial = str(codes).split("id=")[1]
     credencial=credencial.split("'")[0]
    except:
      bot.send_message(
         chat_id=update.message.chat_id,
         text="ERRO DE LEITURA"
     )
      
    mydb = mysql.connector.connect(
    host="localhost",
    user="USUARIO_DB",
    passwd="SENHA_DB",
    database="DB"
    )
    
    
    mycursor=mydb.cursor()
    mycursor.execute("select * from credenciais where id="+credencial+"")
    myresult=  mycursor.fetchall()
    
    for x in myresult:
     response_message="Credencial: "+str(x[1])+chr(10)
     credencial1=str(x[1])
     response_message+="Posto: "+str(x[3])+chr(10)
     response_message+="Nome: "+str(x[4])+chr(10)
     response_message+="Matricula: "+str(x[5])+chr(10)
     response_message+="Placa e Veiculo: "+str(x[6])
    #response_message=credencial
    
    
    
    bot.send_message(
        chat_id=update.message.chat_id,
        text=response_message
    )
    mycursor=mydb.cursor()
    mycursor.execute("select * from registro where credencial='"+credencial1+"' order by id desc")
    myresult=  mycursor.fetchall()
    entrada_saida=""
    for x in myresult:
       entrada_saida=x[4]
    sql="insert into registro(credencial,data,temperatura,entrada_saida) values('"+credencial1+"','"+str(datetime.datetime.now()).split(".")[0]+"','"+"0"+"','"+entrada_saida+"')"
 ## print(sql)
    mycursor.execute(sql)
    mydb.commit()


def retorna_placa_google(path):
 
 with io.open(path, 'rb') as image_file:
        content = image_file.read()

 os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/wwcfo2/www/MUNICAO_BALOTE/src/client2_secrets.json"
 client = vision.ImageAnnotatorClient()

 image = vision.types.Image(content=content)


 response = client.text_detection(image=image,timeout=10)
 texts = response.text_annotations
 placa=""
 antes=time.time()
 for text in texts:
 
       # print(text)
        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])
        placa=placa+str(text)
 

 if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

 return placa
def retorna_placa(path):
 if False:
  with io.open(path, 'rb') as image_file:
        content = image_file.read()

  os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/wwcfo2/www/MUNICAO_BALOTE/src/client2_secrets.json"
  client = vision.ImageAnnotatorClient()

  image = vision.types.Image(content=content)


  response = client.text_detection(image=image,timeout=10)
  texts = response.text_annotations
  placa=""
  antes=time.time()
  for text in texts:
 
      #  print(text)
        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])
        placa=placa+str(text)
 

  if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

  return placa
 if True: 
    regions = ['br', 'it'] # Change to your country
    with open('.//home/wwcfo2/www/MUNICAO_BALOTE/src/temp.jpg', 'rb') as fp:
     response = requests.post(
         'https://api.platerecognizer.com/v1/plate-reader/',
         data=dict(regions=regions),  # Optional
         files=dict(upload=fp),
         headers={'Authorization': 'Token google_token'})
    placa=""
    #pprint(response.json())
   # print(response.json()['results'])    
    for i in (response.json()['results']):
      try:
        placa=i['plate']
        print(placa)
      except: 
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
   #break
   #for x in i['plate']:
   #  print x 
    return placa      
    #pprint(response.json()) 
 
 

#for i in os.listdir('./'):
#   if(i.find('.jpg')!=-1):
#      try:
#        placa=retorna_placa(i)
#        print(placa)
 
#      except:
#        print("ERRO NO FRAME"+i)
#        pass
 
 

#teste2
#teste
#current_frame_small=cv2.resize(input_image,(0,0),fx=0.25,fy=0.25)
def rosto_bent():


       mydb = mysql.connector.connect(
              host="localhost",
              user="USUARIO_DB",
              passwd="SENHA_DB",
              database="DB"
       )       
       sql="select * from rostos"
       mycursor = mydb.cursor()
       mycursor.execute(sql)
       myresult = mycursor.fetchall()
       vetor_fotos=list()
       nomes=list()
       identificados=list()
#i="KEVEN KENNY PEREIRA PASSO.jpg"
#a=face_recognition.load_image_file('/home/wwcfo2/public_html/MUNICAO_BALOTE/src/PEBAS/'+i)
       i=0
       for x in myresult:
 
           string=str(x[3]).split("[")[1].split("]")[0].strip()
 
           string=list(filter(lambda x: len(x)>2,string.split(" ")))
           string=list(map(lambda x: float(x),string))
 
           vetor_fotos.append(np.array(string,dtype=np.float128))
           nomes.append(str(x[1]))
   
       imagem='/home/wwcfo2/www/MUNICAO_BALOTE/src/temp.jpg'
 
       image_to_recognize=cv2.imread(imagem)
       all_face_location=face_recognition.face_locations(image_to_recognize,model="hog")
       all_face_encodings=face_recognition.face_encodings(image_to_recognize,all_face_location)
       
       fotos = list()
      # vetor_fotos = list()
      # nomes=list()
#       for i in os.listdir('/home/wwcfo2/public_html/MUNICAO_BALOTE/src/PEBAS'):
#         if len(i)>2:
#           try:
#            a=face_recognition.load_image_file('/home/wwcfo2/public_html/MUNICAO_BALOTE/src/PEBAS/'+i)
#            fotos.append(a)
        #    print(face_recognition.face_encodings(a)[0])#lixo
#            input()
#            vetor_fotos.append(face_recognition.face_encodings(a)[0])
#           except: print("foto " + str(i) + " falhou")
          # print(i)
#           nomes.append(i.split('.')[0])
       known_face_encodings= vetor_fotos  
       known_face_names =nomes
       for current_face_location,current_face_encoding in zip(all_face_location,all_face_encodings):
          top_pos,right_pos,bottom_pos,left_pos=current_face_location
          print('Found face at top {} right {} left {} down {}'. format(top_pos,right_pos,bottom_pos,left_pos))
          current_face_image=image_to_recognize[top_pos:bottom_pos,left_pos:right_pos]

          all_matches=face_recognition.compare_faces(known_face_encodings,current_face_encoding,tolerance=0.4)
          name="Desconhecido"
#          if True in all_matches:
#             print("AQUI")
#             first_match_index=all_matches.index(True)
#             name=known_face_names[first_match_index]
#             cv2.rectangle(image_to_recognize,(left_pos,top_pos),(right_pos,bottom_pos),(255,0,0),2)
          print(all_matches)
          for faces in all_matches:
             if faces:
                match_index=all_matches.index(faces)
                name=known_face_names[match_index]
                identificados.append(name)
                all_matches.pop(all_matches.index(faces))
           
      
#          font= cv2.FONT_HERSHEY_DUPLEX
#          cv2.putText(image_to_recognize,name,(left_pos,bottom_pos),font,0.5,(255,255,255),1)
#          print(name)
          #return name
          return identificados
          #cv2.imwrite('/home/wwcfo2/public_html/MUNICAO_BALOTE/src/',image_to_recognize)
          #cv2.imwrite(image_to_recognize,'/home/wwcfo2/public_html/MUNICAO_BALOTE/src/')
         
        
def placa_bent():
        
       imagem='/home/wwcfo2/www/MUNICAO_BALOTE/src/temp.jpg'
       input_image=cv2.imread(imagem)
       
       placas_ttexto=list()
       images=0
#while True:
       if True:
       #try: 
 #     ret,input_image = webcam_video_stream.read()
      
 #     current_frame_double=cv2.resize(input_image,(0,0),fx=2,fy=2)
 #     current_frame_half=cv2.resize(input_image,(0,0),fx=0.5,fy=0.5)
 #     current_frame_small=cv2.resize(input_image,(0,0),fx=0.25,fy=0.25)
 #     current_frame_smaller=cv2.resize(input_image,(0,0),fx=0.125,fy=0.125)
      
 
       #current_frame_small=circula_placa(input_image)
 
        x1,x2,y1,y2,text=circula_placa(input_image)
        #print('macaco louco')
        #print(x1)
        #print(x2)
        #print(y1)
        #print(y1)
        if len(text)==7:
          
          x1=x1*2
          x2=x2*2
          y1=y1*2
          y2=y2*2         
          cv2.rectangle(input_image,(x1,x2),(y1,y2),(255, 0, 0), 2)
          placas_ttexto.append(text)
          font= cv2.FONT_HERSHEY_DUPLEX
          cv2.putText(input_image,repr(text),(x1,x2),font,2,(255,255,255),2)  
        numero=str(images)
 

        if len(numero)==1: numero='0000'+numero
        if len(numero)==2: numero='000'+numero
        if len(numero)==3: numero='00'+numero
        if len(numero)==4: numero='0'+numero
# 
       
       
        images=images+1
        cv2.rectangle(input_image,(x1,x2),(y1,y2),(255, 0, 0), 2)
        font= cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(input_image,repr(text),(x1,x2),font,0.5,(255,255,255),2)  
        #cv2.imwrite('/home/wwcfo2/public_html/MUNICAO_BALOTE/src/',input_image)
       #except:print("erro")
   #cv2.imshow("teste",input_image)
  # if cv2.waitKey(1) & 0xFF == ord('q'):
   #     break
    
#webcam_video_stream.release()
#cv2.destroyAllWindows()        
       print('placas identificadas')
       unicas=list(set(placas_ttexto))
       for i in unicas:
          print(i)
      
           
       
def placa(bot, update):
    print(update.message)
    grupo=False
    if str(update.message.chat_id)[0]=='-':
       grupo = True
       return
    a=update.message
    

    
    cadastro=''
 
    
    if(autentica(update.message)>0):
    
      
      
       
      if(len(str(a.caption).upper().split('ENDERE'))>1 and len(str(a.caption).upper().split('MARCA'))>1 and len(str(a.caption).upper().split('PLACA'))>1  ):
 
       cadastro='ENDERE'+str(a.caption).upper().split('ENDERE')[1]
       cadastro=str(a.caption).upper().split('MARCA')[0]

      if(len(str(a.caption).upper().split('AVISO'))>1 and len(str(a.caption).upper().split('MARCA'))>1 and len(str(a.caption).upper().split('PLACA'))>1  ):
       cadastro='AVISO'+str(a.caption).upper().split('AVISO')[1]
       cadastro=str(a.caption).upper().split('MARCA')[0]

      if(len(str(a.caption).upper().split('ALERTA'))>1 and len(str(a.caption).upper().split('MARCA'))>1 and len(str(a.caption).upper().split('PLACA'))>1  ):
       print("aqui")
       cadastro='ALERTA'+str(a.caption).upper().split('ALERTA')[1]
       cadastro=str(a.caption).upper().split('MARCA')[0]

#teste
      print("O CADASTRO"+cadastro)
      if cadastro!='':
               mydb = mysql.connector.connect(
               host="localhost",
               user="USUARIO_DB",
               passwd="SENHA_DB",
               database="DB"
               )
               #cadastro=cadastro.split("TEXT':")[1]
               cadastro=cadastro.replace("'",'')
               cadastro=cadastro.replace('"','')
               cadastro=cadastro.replace(';','')
               cadastro=cadastro.replace('-','')
               
               #teste
               i=cadastro
               local=""
               placa=""
               data=""
               modelo=""
               try:
                  local=(i.upper().split('ENDEREÇO:\n')[1].split('\n')[0])
               except: 
                     try:
                           local=(i.upper().split('LOCAL')[1].split('\n')[0])
                     except:
                            try:
                               local=(i.upper().split('CIDADE')[1].split('\n')[0])
                            except: 
                               local=('')
               try:
                  placa=(i.upper().split('PLACA:')[1].split('\n')[0])
               except: 
                  placa=('')
               try: 
                  data=((i.upper().split('DATA')[1].split('\n')[0]))
               except: 
                  data=datetime.datetime.now()
               try: 
                  modelo=((i.upper().split('MODELO')[1].split('\n')[0]))
               except: 
                   try:
                        modelo=((i.upper().split('MARCA')[1].split('\n')[0]))
                   except:
                        modelo=('') 
               #teste               
               sql="insert into roubados(tudo,local,placa,data,modelo,data_postagem) values('"+cadastro+"','"+local+"','"+''.join(placa)+"','"+data+"','"+modelo+"','"+str(datetime.datetime.now()).split(' ')[0]+"')"
               print(sql)
               
             #  sql="insert into roubados(tudo) values('"+cadastro+"');"
               mycursor = mydb.cursor()
               mycursor.execute(sql)
               mydb.commit()
               if not grupo:
                 bot.send_message(
                    chat_id=update.message.chat_id,
                    text="Veículo cadastrado na base de dados"
                    
                     )
               return      


       
    
    autorizados=['140356417','1032658936','1244180790']
    usuario_id=str(update.message).split("'")
    a=list(filter(lambda x: usuario_id[8].find(x)!=-1,autorizados))
    b=update.message

    if(autentica(update.message)<2):
      
       return

    
    b2=0
    print(str(update.message))
    path=(str(update.message).split('file_id')[2].split("'")[2]) #se der problema troque o numero na frente de file_id para 1
    print ("lohran")
    print (path)
    url='https://api.telegram.org/bot_token/getFile?file_id='+path
   # print(url)
    r=requests.get(url,allow_redirects=True)
   # print(r.content)
    url='https://api.telegram.org/file/bot_token/'
    path=str(r.content).split('file_path')[1].split('"')[2]
    r = requests.get(url+path,allow_redirects=True)
    open('/home/wwcfo2/www/MUNICAO_BALOTE/src/temp.jpg','wb').write(r.content) 
    placa=""
    #placa=retorna_placa('/home/wwcfo2/www/MUNICAO_BALOTE/src/temp.jpg')
    #print(placa)
    #try:
    #  placa=retorna_placa('/home/wwcfo2/www/MUNICAO_BALOTE/src/temp.jpg')
    #except:
    #  if not grupo:
    #     bot.send_message(
    #                chat_id=update.message.chat_id,
    #                text="Não conseguimos identificar nenhuma placa na imagem. Tente reduzir a distância, diminuir a inclinação e melhorar a iluminação da foto, ou digite manualmente a placa. Ou você pode tentar enviar novamente essa mesma foto."
    #                 )
    #  return
    #if placa=="":
    if True:
       flag2=True
       print("AQUI")
       if True:
       #try:
          rosto=rosto_bent()
          #print("rosto abaixo")
          #print(rosto)
          #if rosto==None:
          #print("lohran arraes Bentemuller")
          #print(rosto)
          #if len(rosto)==0:
          
          if rosto==None:
            placa=retorna_placa_google('/home/wwcfo2/www/MUNICAO_BALOTE/src/temp.jpg') #API DO GOOGLE 
          
          #placa=placa_bent()
          else:
            if not grupo:
                   #if rosto !="Desconhecido":
                if(len(rosto)==0):
                  bot.send_message(
                     chat_id=update.message.chat_id,
                     text="Rosto não identificado na base de dados"
                  )
                for x in rosto:
                     #bot.send_message(
                     #chat_id=update.message.chat_id,
                     #text="Provável identificação: nome do rosto identificado:"+x
                      #)
                     bot.send_photo(chat_id=update.message.chat_id, photo=open('/home/wwcfo2/www/MUNICAO_BALOTE/src/PEBAS/'+x+'.jpg', 'rb'))
                     bot.send_message(
                     chat_id=update.message.chat_id,
                     text="Provável identificação: nome do rosto identificado:"+x + " passagem por furto de veículo"
                      )                     
                return
                   #if placa!="":  
                   #  bot.send_message(
                   # chat_id=update.message.chat_id,
                   # text="Rosto encontrado na foto CPF:"+rosto
                   #  )
                   #print("oi")
       #except:
       else:
          flag2=False
       if True:
       #try:
          placa=''.join(map(lambda x: x.split("\n")[0],placa.split('description:')[1]))
          placa=placa.split('"')[1]  
          print(placa)
       #except: flag2=False          
       else: 
          flag2=False
       if not grupo:
        if not flag2:
         bot.send_message(
                    chat_id=update.message.chat_id,
                    text="Não conseguimos identificar nenhuma placa na imagem. Tente reduzir a distância, diminuir a inclinação e melhorar a iluminação da foto, ou digite manualmente a placa. Ou você pode tentar enviar novamente essa mesma foto."
                     )
       if not flag2: return
       #return                      
    #placa=str(placa)
    #try:
    #  placa=''.join(map(lambda x: x.split("\n")[0],placa.split('description:')[1]))
    #except:
    #   if not grupo:
    #     bot.send_message(
    #                chat_id=update.message.chat_id,
    #                text="Não conseguimos identificar nenhuma placa na imagem. Tente reduzir a distância, diminuir a inclinação e melhorar a iluminação da foto, ou digite manualmente a placa"
    #                 )
    #   return      
 
    #placa=placa.split('"')[1]
    placa=placa.replace(chr(92)+'n',chr(10) )
    anterior=''
    placa2=''
    for i in placa.split(chr(10)):
       if(len(i)==0):continue
       #print(anterior)
       #print(i)
       
       #print(len(i))
       #print(len(anterior))
       if((len(i)==4) and (len(anterior)==3)):
         
           placa2=placa2+anterior+i+chr(10)  
       else:
           placa2=placa2+i+chr(10)
       anterior=i
    #placa2=placa
    placa=placa2
    print(placa)
    f=open('/home/wwcfo2/www/MUNICAO_BALOTE/src/total.txt','r')
    total=int(f.read())
    if(total==0):
      print("Acabaram as consultas")
      if not grupo:
         bot.send_message(
                   chat_id=update.message.chat_id,
                   text="Restam 0 consultas, contate o administrador do sistema"
                    )                
      return
    total=total-1
    print("restam "+str(total)+" consultas")
    
    mydb = mysql.connector.connect(
    host="localhost",
    user="USUARIO_DB",
    passwd="SENHA_DB",
    database="DB"
    )    

    if not grupo:
     pass
     # bot.send_message(
     #    chat_id=update.message.chat_id,
     #    text="restam "+str(total)+" consultas"
     #    )                
    f.close()
    f=open('/home/wwcfo2/www/MUNICAO_BALOTE/src/total.txt','w')
    f.write(str(total))
    f.close()
    #placa=placa.replace('\n',chr(10))
   # placa=' '.join(split("\n"))
    if not grupo:
     bot.send_message(
        chat_id=update.message.chat_id,
        text=placa
     )

    placa=''.join(placa.split(" "))
    placa=placa.replace('-','')
    placa=placa.replace('%','')
    placa=placa.replace("'",'')
    placa=placa.replace('"','')
   # print(placa)
    
    if(cadastro==''):
        i=placa

     

        if(len(placa.split(chr(10)))==0):
         total_de_placas=0
         encontrado=False
         for i in dicionario(placa):
 
          #print("entrou Aqui")
          #sql="select * from roubados where tudo like '%"+i[:3]+"%"+i[-4:]+"%'"
          sql="select * from roubados where tudo like '%"+i[:3]+""+i[-4:]+"%' union all select * from roubados where tudo like '%"+i[:3]+" "+i[-4:]+"%' union all select * from roubados where tudo like '%"+i[:3]+"-"+i[-4:]+"%'"
          mycursor = mydb.cursor()
          mycursor.execute(sql)
          myresult = mycursor.fetchall()
          if(len(myresult)==0):
             pass
             #print(total_de_placas)
             if total_de_placas>199:break
           #   print("Placa "+placa+" não encontrada na base dados")          
              #if not grupo:
              #  bot.send_message(
              #     chat_id=update.message.chat_id,
              #     text="Placa "+placa+" não encontrada na base de dados"
              #      )   
                #sql2="insert into balote_auditoria(id_telegram,mensagem,resposta,data) values("+str(update.message.from_user.id)+",'imagem: "+str(placa)+"','"+"Placa não encontrada na base de dados"+"','"+str(datetime.datetime.now())+"');"
                #mycursor = mydb.cursor()
                #mycursor.execute(sql2)
                #mydb.commit()      
                #print(sql2)                
                #break                
              #return
          #print(len(myresult))     
          else:
           for x in myresult:
              if not grupo:
                bot.send_message(
                   chat_id=update.message.chat_id,
                   text=str(x[-3]).replace("<BR>",chr(10))
                    )
                sql2="insert into balote_auditoria(id_telegram,mensagem,resposta,data) values("+str(update.message.from_user.id)+",'imagem: "+str(placa)+"','"+str(x[-1]).replace("<BR>",chr(10))+"','"+str(datetime.datetime.now())+"');"
                #print(sql2)
                ultima_localizacao_id(update.message.from_user.id,"imagem " +str(placa))
                mycursor = mydb.cursor()
                mycursor.execute(sql2)
                mydb.commit()
                    #if(encontrado):
 
                update.message.reply_text(encontrado_menu_message(update.message.from_user.id,str(placa)),
                reply_markup=encontrado_menu_keyboard())
           return
          total_de_placas=total_de_placas+1             
         if not grupo:
             bot.send_message(
                 chat_id=update.message.chat_id,
                 text=str(total_de_placas)+" variações da placa pesquisadas e nenhum resultado encontrado na base de dados, clique em /historico para saber mais detalhas"
                 )
             sql2="insert into balote_auditoria(id_telegram,mensagem,resposta,data) values("+str(update.message.from_user.id)+",'imagem: "+str(placa)+"','"+"Placa não encontrada na base de dados"+"','"+str(datetime.datetime.now())+"');"
             #print(sql2)
             ultima_localizacao_id(update.message.from_user.id,"imagem "+ str(placa))
             mycursor = mydb.cursor()
             mycursor.execute(sql2)
             mydb.commit()
             update.message.reply_text(encontrado_menu_message(update.message.from_user.id,update.message.text),
             reply_markup=encontrado_menu_keyboard())             
             return
        else:
         #print("entrou la")
         total_de_placas=0
         for i in placa.split(chr(10)):
          if(len(i)!=7):continue
          print(total_de_placas)
          if total_de_placas>200: break 
          for j in dicionario(i):
           sql="select * from roubados where tudo like '%"+i[:3]+""+i[-4:]+"%' union all select * from roubados where tudo like '%"+i[:3]+" "+i[-4:]+"%' union all select * from roubados where tudo like '%"+i[:3]+"-"+i[-4:]+"%'"
           mycursor = mydb.cursor()
           mycursor.execute(sql)
           myresult = mycursor.fetchall()
           if(len(myresult)==0):
             pass
            # print(total_de_placas)
             if total_de_placas>199:break             
            #  print("Placa "+placa+" não encontrada na base dados")          
            #   if not grupo:
            #     bot.send_message(
            #        chat_id=update.message.chat_id,
            #        text="Placa "+str(i)+" não encontrada na base dados"
            #         ) 
            #     sql2="insert into balote_auditoria(id_telegram,mensagem,resposta,data) values("+str(update.message.from_user.id)+",'imagem: "+str(placa)+"','"+"Placa não encontrada na base de dados"+"','"+str(datetime.datetime.now())+"');"
            #     mycursor = mydb.cursor()
            #     mycursor.execute(sql2)
            #     mydb.commit()                     
            #   return
         #print(placa)
         #print(sql)
         #if(len(placa)!=7): return
           else:         
             for x in myresult:
               if not grupo:
                 bot.send_message(
                    chat_id=update.message.chat_id,
                    text=str(x[-3]).replace("<BR>",chr(10))
                     )
                 sql2="insert into balote_auditoria(id_telegram,mensagem,resposta,data) values("+str(update.message.from_user.id)+",'imagem: "+str(placa)+"','"+str(x[-1]).replace("<BR>",chr(10))+"','"+str(datetime.datetime.now())+"');"
                 ultima_localizacao_id(update.message.from_user.id,"imagem "+ str(placa))
                 mycursor = mydb.cursor()
                 mycursor.execute(sql2)
                 mydb.commit()  
                 update.message.reply_text(encontrado_menu_message(update.message.from_user.id,update.message.text),
                 reply_markup=encontrado_menu_keyboard())
                 return
           total_de_placas=total_de_placas+1
          if not grupo:
             bot.send_message(
                 chat_id=update.message.chat_id,
                 text=str(total_de_placas)+" variações da placa pesquisadas e nenhum resultado encontrado na base de dados, clique em /historico para saber mais detalhes"
                 )
             sql2="insert into balote_auditoria(id_telegram,mensagem,resposta,data) values("+str(update.message.from_user.id)+",'imagem: "+str(placa)+"','"+"Placa não encontrada na base de dados"+"','"+str(datetime.datetime.now())+"');"
             ultima_localizacao_id(update.message.from_user.id,"imagem "+ str(placa)) 
             print (sql2)
             mycursor = mydb.cursor()
             mycursor.execute(sql2)
             mydb.commit()                   
             #return         


def start(bot, update):
    response_message = "Bot criado pelo Cad Bentemuller"
    bot.send_message(
        chat_id=update.message.chat_id,
        text=response_message
    )

def escala(bot,update,args):
  #print(update.message)
  return
  if(len(args)==0):
      bot.send_message(
      chat_id=update.message.chat_id,
      text="Você esqueceu de digitar a turma"
    )
  mydb = mysql.connector.connect(
  host="localhost",
  user="USUARIO_DB",
  passwd="SENHA_DB",
  database="DB"
  )
  mycursor = mydb.cursor()

  hoje= (str(datetime.datetime.now()).split(" ")[0])
  mycursor.execute("select cadetes,matricula_pmdf,escala from (select cadetes,escala,antiguidade from (select * from cadetes_servico)t1 inner join (select * from escala where escala="+args[0]+" and data='"+hoje+"')t2 on t1.id=t2.id_cadete)q1 inner join (select * from informacoes1) q2 on q1.antiguidade=q2.matricula_esfo")

  myresult = mycursor.fetchall()
  escalados=list();
  for x in myresult:
 #escalados.append(' '.join(x))
   a=x[0]+' ' +x[1]+ ' '+str(x[2])
   escalados.append(a) 
  escalados='\n'.join(escalados)  
  if(len(myresult)!=0):  
    bot.send_message(
      chat_id=update.message.chat_id,
      text="os escalados de hoje sao\n"+escalados
    )
  else:
    bot.send_message(
      chat_id=update.message.chat_id,
      text="Não foi encontrada escala para essa turma"
    )     

def http_cats(bot, update, args):
    #bot.sendPhoto(
    #    chat_id=update.message.chat_id,
    #    photo=BASE_API_URL + args[0]
    #)
    return
    bot.send_message(
        chat_id=update.message.chat_id,
        text=BASE_API_URL+args[0]        
    )


def spam(bot, update,args):
   if(autentica(update.message)>2): 
     mydb = mysql.connector.connect(
     host="localhost",
     user="USUARIO_DB",
     passwd="SENHA_DB",
     database="DB"
     )
    # print(''.join(args))
    # return
     mycursor = mydb.cursor()
     sql="select * from cadastro_balote where nivel >=2"
     #sql="select * from cadastro_balote where nivel=0 or nivel=3"
     print(sql)
     mycursor.execute(sql)
     myresult = mycursor.fetchall()
     mensagem = ' '.join(args)
     for x in myresult:
       print(x)
       print(int(list(x)[1]))
       try:
        bot.send_message(
          chat_id=int(list(x)[1]),
          text=mensagem
        )
      #  remote_photo_url="http://www.cfo2019.com/MUNICAO_BALOTE/src/audio.jpg"
      #  bot.sendPhoto(chat_id=int(list(x)[1]), photo=remote_photo_url,caption="Nova funcionalidade para o bot. Agora você pode fazer suas consultas por audio, bastando clicar no microfone destacado na imagem e falar as letras pelo padrão de codificação fonética internacional e falar os números normalmente")     
       except:continue
    
       
   return
    

def unknown(bot, update):
    return
    response_message = "Retransmita"
    bot.send_message(
        chat_id=update.message.chat_id,
        text=response_message
    )

#def placa(bot,update):
 #   print(update.file_id)
def gerar_senha(bot,update):
   if(autentica(update.message)>2):
    senha=  get_random_string(8)
    bot.send_message(
        chat_id=update.message.chat_id,
        text=senha
      )   
    mydb = mysql.connector.connect(
    host="localhost",
    user="USUARIO_DB",
    passwd="SENHA_DB",
    database="DB"
    )
    mycursor = mydb.cursor()
    sql="update senha_secreta set senha=Sha2('"+str(senha)+"',224) where 1=1"
    print(sql)
    mycursor.execute(sql)
    mydb.commit()
          
      
def registro(bot,update,args):
    print(update.message)
    print(args)
    mydb = mysql.connector.connect(
    host="localhost",
    user="USUARIO_DB",
    passwd="SENHA_DB",
    database="DB"
    )
    
    mycursor = mydb.cursor()
    sql="select * from senha_secreta where senha=Sha2('"+args[-1]+"',224)"
    print(sql)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    total=list()
    for x in myresult:
       total.append(x)
    print(total)
    if(len(total)>0):
       sql="insert into cadastro_balote (id_telegram,nome,batalhao,nivel) values('"+str(update.message.from_user.id)+"','"+str(args[0])+"','"+str(args[1])+"',2)"
       mycursor = mydb.cursor()
       mycursor.execute(sql)
       mydb.commit()
       text2="Usuario cadastrado com sucesso\n"
       text2=text2+"Estamos testando uma nova ferramenta e precisamos da sua participação.\n"
       text2=text2+"Analisamos que muitos carros roubados ou furtados são deixados em locais públicos.\n"
       text2=text2+"Por isso o objetivo é usar a ferramenta para levantamento em massa de grande número de veículos como estacionamentos abertos, estações de metrô, pontos de bloqueio, setores de oficinas ou vias muito movimentadas.\n"
       text2=text2+"O sistema informa a situação do carro em 1,62 segundos após você apertar o botão enter. Dessa forma é possível procurar com maior rapidez os veículos com restrição.\n"
       text2=text2+"É importante lembrar que a busca não ocorre em uma base nacional de veículos, então o sistema não vai trazer informações detalhadas sobre ele, mas vai informar se ele está em uma lista de veículos de interesse para nós.\n"
       text2=text2+"Caso o sistema forneça informações sobre o veículo é indicativo que ele já constou com alguma pendência, então pesquise no Gênesis para ter mais informações e saber se já foi restituído ou acabou a pendência.\n"
       text2=text2+"O objetivo agora é procurar problemas na ferramenta, ela não é a versão final e novos recursos estão sendo adicionados lentamente.\n"
       text2=text2+"Inicialmente, para fazer um teste, digite a placa de um veículo com restrição na última semana ou há dois meses e veja quais mensagens são apresentadas. Digite também a placa de um veículo sem restrições e veja a mensagem que aparece.\n"
       text2=text2+"digite apenas 1 placa por vez\n"
       text2=text2+"Dessa forma, precisamos saber quais dificuldades e problemas você encontrou durante o uso. Solicite meu contato e me informe para que possamos tentar corrigir e melhorar a ferramenta.\n"
       text2=text2+"Para ver esse texto novamente basta digitar /help\n"       
       text2="Funcionalidades do aplicativo:\n"
       text2+="<b>reconhecimento de placas por foto:</b> Envie várias fotos de placas de veículo e o BOT responderá se alguma delas"
       text2+="\n"
       text2+="consta como produto de furto/roubo na base de dados."
       text2+="\n"
       text2+="<b>reconhecimento facial:</b> Envie uma foto de um rosto e o BOT responderá com os dados cadastrados na plataforma."
       text2+="\n"
       text2+="<b>Busca de mandados de prisão em aberto:</b> Digita um nome e um sobrenome e o BOT buscará na base de dados do portal BNMP os nomes compatíveis com mandado de prisão em aberto."
       text2+="\n"
       text2+="<b>Pesquisa de placas por texto:</b> Digite uma placa e o BOT responderá se o veículo consta ou não na base de dados como produto de furto/roubo."
       text2+="\n"
       text2+="<b>Demarcação de locais:</b> Envie sua localização em tempo real para o bot e toda pesquisa realizada demarcará a latitude e longitude do texto digitado."
       text2+="\n"
       text2+="<b>Recuperação de locais demarcados:</b> Para recuperar a localização dos locais demarcados, basta digitar o comando /maps +termo_procurado e ele retornará os resultados."
       text2+="\n"
       text2+="Por exemplo, digite '/maps lava jato' e ele retornará todas as localizações demarcadas como lava jatos."
       text2+="\n"
       text2+="<b>Cadastro de veículos produtos de roubo/furto</b>: digite o comando /cadastro e o bot retornará o padrão de preenchimento, preencha os dados solicitados e envie para o bot"
       text2+="\n"
       text2+="ele então cadastrará o veículo na base. Todas as mensagens enviadas por usuários tem registro de data e hora e de quem enviou, portanto cadastre apenas os veículos que tiver"
       text2+="\n"
       text2+="certeza. O registro de usuários tem validade de 15 dias. Caso o veículo já tenha sido recuperado, reenvie a mensagem de cadastro com a informação RECUPERADO logo após a palavra HISTÓRICO."
       text2+="\n"
       text2+="\n"
       text2+="<b>ajuda:</b> Digite o comando /help para visualizar essa mensagem novamente"  
       text2+="\n"  
       
       
       
       bot.send_message(
        chat_id=update.message.chat_id,
        text=text2
       )
    else:
       bot.send_message(
        chat_id=update.message.chat_id,
        text="Senha incorreta"
       )
    
    pass

def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu
    
def historico(bot,update):
   if(autentica(update.message)<1):
      print("saiu")
      return
   grupo=False
   if str(update.message.chat_id)[0]=='-':
       grupo = True
   if grupo:return


   usuario=update.message.from_user.id
   mydb = mysql.connector.connect(
   host="localhost",
   user="USUARIO_DB",
   passwd="SENHA_DB",
   database="DB" )  
   sql="select * from balote_auditoria where id_telegram="+str(usuario)+" order by data desc limit 1"
   mycursor = mydb.cursor()
   mycursor.execute(sql)
   myresult = mycursor.fetchall()
   bot.send_message(
             chat_id=update.message.chat_id,
             text="Relação de ultima placa pesquisada"
            )
   texto_total="Relações de variações da placa ultima placa pesquisada\n"   
   for x in myresult:
         print(x)
      #for i in str(x[2]).split(chr(10)):
         if str(x[2]).find("texto")!=-1:
         
            bot.send_message(
             chat_id=update.message.chat_id,
             text="Ultima placa pesquisada "+str(x[2])
            )
            return
         else:
            if str(x[2]).find('imagem')!=-1:
               texto=str(x[2]).split('imagem')[1]
               texto=''.join(texto.split(" "))
               texto=texto.replace(":","")
               #texto=texto.split('\n')[0]
               for i in texto.split(chr(10)):
                  print(i)
                  print(len(i))
                  if(len(i)!=7):continue
                  total_de_placas=0
                  for j in dicionario(i):
                     if(total_de_placas>199): break
                     texto_total=texto_total+j+"\n"
                     #bot.send_message(
                     #  chat_id=update.message.chat_id,
                     #  text=j
                     #  )
                     total_de_placas=total_de_placas+1  
   bot.send_message(
       chat_id=update.message.chat_id,
       text=texto_total
       )   
def cadastro(bot,update):
   grupo=False
   if(autentica(update.message)<1):
      print("saiu")
      return
   if str(update.message.chat_id)[0]=='-':
      grupo=True


   text2=""
   text2+="🚨ALERTA DE VEÍCULO ROUBADO/FURTADO🚨\n"
   text2+="DATA: XX/XX/XXXX\n"
   text2+="LOCAL: CIDADE\n"
   text2+="HORÁRIO: XX:XX\n"
   text2+="PLACA: XXX0000\n"
   text2+="MARCA/MODELO/COR/ANO: MARCA/MODELO COR ANO\n"
   text2+="HISTÓRICO: FURTADO/ROUBADO\n"
   if not grupo:   
     bot.send_message( 
        chat_id=update.message.chat_id,
        text=text2
       )  
   
def help(bot,update):
   grupo=False
   if(autentica(update.message)<1):
      print("saiu")
      return
   if str(update.message.chat_id)[0]=='-':
       grupo = True
   text2=""
   text2=text2+"Estamos testando uma nova ferramenta e precisamos da sua participação.\n"
   text2=text2+"Analisamos que muitos carros roubados ou furtados são deixados em locais públicos.\n"
   text2=text2+"Por isso o objetivo é usar a ferramenta para levantamento em massa de grande número de veículos como estacionamentos abertos, estações de metrô, pontos de bloqueio, setores de oficinas ou vias muito movimentadas.\n"
   text2=text2+"O sistema informa a situação do carro em 1,62 segundos após você apertar o botão enter. Dessa forma é possível procurar com maior rapidez os veículos com restrição.\n"
   text2=text2+"É importante lembrar que a busca não ocorre em uma base nacional de veículos, então o sistema não vai trazer informações detalhadas sobre ele, mas vai informar se ele está em uma lista de veículos de interesse para nós.\n"
   text2=text2+"Caso o sistema forneça informações sobre o veículo é indicativo que ele já constou com alguma pendência, então pesquise no Gênesis para ter mais informações e saber se já foi restituído ou acabou a pendência.\n"
   text2=text2+"O objetivo agora é procurar problemas na ferramenta, ela não é a versão final e novos recursos estão sendo adicionados lentamente.\n"
   text2=text2+"Inicialmente, para fazer um teste, digite a placa de um veículo com restrição na última semana ou há dois meses e veja quais mensagens são apresentadas. Digite também a placa de um veículo sem restrições e veja a mensagem que aparece.\n"
   text2=text2+"digite apenas 1 placa por vez\n"
   text2=text2+"Dessa forma, precisamos saber quais dificuldades e problemas você encontrou durante o uso. Solicite meu contato e me informe para que possamos tentar corrigir e melhorar a ferramenta.\n"
   text2=text2+"Para ver esse texto novamente basta digitar /help\n"   
   
   text2="<b>Funcionalidades do aplicativo:</b>\n"
   text2+="<b>reconhecimento de placas por foto:</b> Envie várias fotos de placas de veículo e o BOT responderá se alguma delas"
   text2+="\n"
   text2+="consta como produto de furto/roubo na base de dados."
   text2+="\n"
   text2+="<b>reconhecimento facial:</b> Envie uma foto de um rosto e o BOT responderá com os dados cadastrados na plataforma."
   text2+="\n"
   text2+="<b>Busca de mandados de prisão em aberto:</b> Digita um nome e um sobrenome e o BOT buscará na base de dados do portal BNMP os nomes compatíveis com mandado de prisão em aberto."
   text2+="\n"
   text2+="<b>Pesquisa de placas por texto:</b> Digite uma placa e o BOT responderá se o veículo consta ou não na base de dados como produto de furto/roubo."
   text2+="\n"
   text2+="<b>Demarcação de locais:</b> Envie sua localização em tempo real para o bot e toda pesquisa realizada demarcará a latitude e longitude do texto digitado."
   text2+="\n"
   text2+="<b>Recuperação de locais demarcados:</b> Para recuperar a localização dos locais demarcados, basta digitar o comando /maps +termo_procurado e ele retornará os resultados."
   text2+="\n"
   text2+="Por exemplo, digite '/maps lava jato' e ele retornará todas as localizações demarcadas como lava jatos."
   text2+="\n"
   text2+="<b>Cadastro de veículos produtos de roubo/furto</b>: digite o comando /cadastro e o bot retornará o padrão de preenchimento, preencha os dados solicitados e envie para o bot"
   text2+="\n"
   text2+="ele então cadastrará o veículo na base. Todas as mensagens enviadas por usuários tem registro de data e hora e de quem enviou, portanto cadastre apenas os veículos que tiver"
   text2+="\n"
   text2+="certeza. O registro de usuários tem validade de 15 dias. Caso o veículo já tenha sido recuperado, reenvie a mensagem de cadastro com a informação RECUPERADO logo após a palavra HISTÓRICO."
   text2+="\n"
   text2+="\n"
   text2+="<b>ajuda:</b> Digite o comando /help para visualizar essa mensagem novamente"  
   text2+="\n"   
   if not grupo:   
     bot.send_message( 
        chat_id=update.message.chat_id,
        text=text2,parse_mode="html"
       )
     time.sleep(3)
     after=int(str(update.message).split("':")[1].split(",")[0])+1
     bot.deleteMessage(update.message.chat_id,int(str(update.message).split("':")[1].split(",")[0]))
     bot.deleteMessage(update.message.chat_id,after)
     if same('/home/wwcfo2/www/MUNICAO_BALOTE/src/teste.jpg','/home/wwcfo2/www/MUNICAO_BALOTE/src/teste.jpg'):
        print("foto ja postada")
     #remote_photo_url="https://pt.wikipedia.org/wiki/Capivara#/media/Ficheiro:Capybara_(Hydrochoerus_hydrochaeris).JPG"
   #  remote_photo_url="http://www.cfo2019.com/MUNICAO_BALOTE/src/audio.jpg"
   #  bot.sendPhoto(chat_id=update.message.chat_id, photo=remote_photo_url,caption="teste")     

def principal_texto(bot,update):
    print(update.message)
    print(update.message.chat_id)    
    grupo=False
    print(str(update.message.chat_id)[0])
    
    #if str(update.message.chat_id).startswith('-'): 
    if str(update.message.chat_id)[0]=='-':
       grupo = True
       
    autorizados=['674285145','687722997','140356417','1032658936','1244180790']
    b=update.message
    #print(str(b))
    #print(b.chat_id)
    #print(b.text)
    #print(b.from_user.id)
    #print(b.from_user.first_name)
    
    #if(str(b.chat_id) not in autorizados):
    #if(str(b.from_user.id) not in autorizados):  
    if(autentica(update.message)<1):
      print("saiu")
      return
   
    ultima_localizacao_id(update.message.chat_id,update.message)
    telefone=False
    if(update.message.text.split(" ")[-1].isnumeric()):
       if(int(update.message.text.split(" ")[-1])> 1000000 and int(update.message.text.split(" ")[-1])<= 999999999):
         telefone=True
    print("telefone "+ str(telefone))
    print( str(update.message.text)[-1].isnumeric())
    if str(update.message.text).upper().find('PLACA')==-1: 
     if not str(update.message.text)[-1].isnumeric():
       print("entrou")
       mydb = mysql.connector.connect(
       host="localhost",
       user="USUARIO_DB",
       passwd="SENHA_DB",
       database="DB"
       )
       if len(str(update.message.text)) < 8: return
       nome=str(update.message.text).replace(";","")
       nome=str(nome).replace(",","")
       nome=str(nome).replace(".","")
       nome=str(nome).replace(":","")
       nome=str(nome).replace("(","")
       nome=str(nome).replace(")","")
       nome=nome.upper()
       nome=unidecode.unidecode(nome)
       nome=' '.join(nome.split(" "))
       sql="select * from mandados_abertos where nome like '%"+nome+"%';"
       sql="select * from mandados_abertos where nome like '%"+nome.split(" ")[0]+"%' and nome like '%"+nome.split(" ")[1]+"%';"
       print(sql)
       mycursor = mydb.cursor()
       mycursor.execute(sql)
       texto_total=list()
       myresult = mycursor.fetchall()
       
       if len(myresult)==0:
           if not grupo:
                    bot.send_message(
                    chat_id=update.message.chat_id,
                    text="sem passagens para "+nome
                    
                     )
       for x in myresult:
          print(x)
          texto2=""
          texto2=texto2+"Nome:"+str(x[1])+"\n"
          texto2=texto2+"Alcunha:"+str(x[2])+"\n"
          texto2=texto2+"Nome da mãe:"+str(x[3])+"\n"
          texto2=texto2+"Nome do pai:"+str(x[4])+"\n"
          texto2=texto2+"Data de nascimento:"+str(x[5])+"\n"
          texto2=texto2+"Situacao:"+str(x[6])+"\n"
          texto2=texto2+"Data do mandado:"+str(x[7])+"\n"
          texto2=texto2+"Orgão:"+str(x[8])+"\n"
          texto2=texto2+"Peça:"+str(x[9])+"\n"
          texto_total.append(texto2)
       if not grupo:
                 for i in texto_total:
                    bot.send_message(
                    chat_id=update.message.chat_id,
                    text=i
                     )
       return
    cadastro=''
    if(len(str(b.text).upper().split('ENDERE'))>1 and len(str(b.text).upper().split('MARCA'))>1 and len(str(b.text).upper().split('PLACA'))>1  ):
       cadastro=str(b.text)

    if(len(str(b.text).upper().split('AVISO'))>1 and len(str(b.text).upper().split('MARCA'))>1 and len(str(b.text).upper().split('PLACA'))>1  ):
       cadastro=str(b.text)
       
    if(len(str(b.text).upper().split('ALERTA'))>1 and len(str(b.text).upper().split('MARCA'))>1 and len(str(b.text).upper().split('PLACA'))>1  ):
       cadastro=str(b.text)    
    
    letras=list()
    letras.append(["A","ALPHA","ALFA"])
    letras.append(["B","BRAVO"])
    letras.append(["C","CHARLES","CHARLIE","CHARLI"])
    letras.append(["D","DELTA"])
    letras.append(["E","ECO","ECCO","ECHO"])
    letras.append(["F","FOX"])
    letras.append(["G","GOLF","GOLFE"])
    letras.append(["H","HOTEL"])
    letras.append(["I","ÍNDIA","INDIAN","INDIA"])
    letras.append(["J","JULIET","JULIETE"])
    letras.append(["K","KILO","QUILO"])
    letras.append(["L","LIMA"])
    letras.append(["M","MIKE"])
    letras.append(["N","NOVEMBER"])
    letras.append(["O","OSCAR","OSCA"])
    letras.append(["P","PAPA"])
    letras.append(["Q","QUEBEC","QUEBÉC"])
    letras.append(["R","ROMEU","ROMEO"])
    letras.append(["S","SIERRA"])
    letras.append(["T","TANGO"])
    letras.append(["U","UNIFORM","UNIFORME"])
    letras.append(["V","VICTER","VICTOR"])
    letras.append(["W","WHISKY","WHISKEY"])
    letras.append(["X","X-RAY","X REI","SUEI","XINGU","CHINGU"])
    letras.append(["Y","YANKEE","YANQUE","IANQUE"])
    letras.append(["Z","ZULU"])
    placa = str(b.text)
    placa=placa.upper()
    for i in letras:
       x=0
       for j in i[1:]:
          if placa.find(j)!=-1:
             placa=placa.replace(j,i[0])
             #placa=placa[:placa.find(j)]+i[0]+placa[placa.find(j)+len(j):]
             
    #placa = str(b.text)
    print(placa)
    placa=placa.replace('-','')
    placa=placa.replace(' ','')
    placa=placa.replace('%','')
    placa=placa.replace("'",'')
    placa=placa.replace('"','')    
    
    mydb = mysql.connector.connect(
    host="localhost",
    user="USUARIO_DB",
    passwd="SENHA_DB",
    database="DB"
    )
    print("O CADASTRO "+cadastro)           
    if cadastro!='':
               cadastro=cadastro.replace("'",'')
               cadastro=cadastro.replace('"','')
               cadastro=cadastro.replace(';','')
               cadastro=cadastro.replace('-','')
               #teste
               i=cadastro
               local=""
               placa=""
               data=""
               modelo=""
               try:
                  local=(i.upper().split('ENDEREÇO:\n')[1].split('\n')[0])
               except: 
                     try:
                           local=(i.upper().split('LOCAL')[1].split('\n')[0])
                     except:
                            try:
                               local=(i.upper().split('CIDADE')[1].split('\n')[0])
                            except: 
                               local=('')
               try:
                  placa=(i.upper().split('PLACA:')[1].split('\n')[0])
               except: 
                  placa=('')
               try: 
                  data=((i.upper().split('DATA')[1].split('\n')[0]))
               except: 
                  data=datetime.datetime.now()
               try: 
                  modelo=((i.upper().split('MODELO')[1].split('\n')[0]))
               except: 
                   try:
                        modelo=((i.upper().split('MARCA')[1].split('\n')[0]))
                   except:
                        modelo=('') 
               #teste               
               sql="insert into roubados(tudo,local,placa,data,modelo,data_postagem) values('"+cadastro+"','"+local+"','"+''.join(placa)+"','"+data+"','"+modelo+"','"+str(datetime.datetime.now()).split(' ')[0]+"')"               
              # print(sql)
              # exit()
               #sql="insert into roubados(tudo) values('"+cadastro+"');"
               mycursor = mydb.cursor()
               mycursor.execute(sql)
               mydb.commit()
               if not grupo:
                 bot.send_message(
                    chat_id=update.message.chat_id,
                    text="Veículo cadastrado na base de dados"
                     )
               return


    autorizados=['140356417','1032658936','1244180790']
    

    #if(str(b.from_user.id) not in autorizados): #se o usuario nao esta autorizado a pesquisar placas
    if(autentica(update.message)<2):
       return
    if not grupo:
       if telefone:
          bot.send_message(
             chat_id=update.message.chat_id,
             text="Estabelecimento cadastrado com sucesso"
             )
          return
    if(len(placa)!=7 and cadastro==''):
        if not grupo:
         #if not telefone:
          bot.send_message(
             chat_id=update.message.chat_id,
             text="Padrão de placa não encontrado, em caso de dúvidas digite /help"
             )

        return
    encontrado=False
    if(cadastro==''):
        i=placa


     

        if(len(placa.split(chr(10)))==0):
          #sql="select * from roubados where tudo like '%"+i[:3]+"%"+i[-4:]+"%'"
          sql="select * from roubados where tudo like '%"+i[:3]+""+i[-4:]+"%' union all select * from roubados where tudo like '%"+i[:3]+" "+i[-4:]+"%' union all select * from roubados where tudo like '%"+i[:3]+"-"+i[-4:]+"%'"
          mycursor = mydb.cursor()
          mycursor.execute(sql)
          myresult = mycursor.fetchall()
          if(len(myresult)==0):
              #print("Placa "+placa+" não encontrada na base dados")          
              if not grupo:
                bot.send_message(
                   chat_id=update.message.chat_id,
                   text="Placa "+placa+" não encontrada na base dados"
                    )
                sql2="insert into balote_auditoria(id_telegram,mensagem,resposta,data) values("+str(update.message.from_user.id)+",'texto: "+str(placa)+"','"+"Placa não encontrada na base de dados"+"','"+str(datetime.datetime.now())+"');"
                ultima_localizacao_id(update.message.from_user.id,str(placa))
                mycursor = mydb.cursor()
                mycursor.execute(sql2)
                mydb.commit()                      
              return
          #print(len(myresult))     
          for x in myresult:
              bot.send_message(
                   chat_id=update.message.chat_id,
                   text=str(x[-3]).replace("<BR>",chr(10))
                    )
              sql2="insert into balote_auditoria(id_telegram,mensagem,resposta,data) values("+str(update.message.from_user.id)+",'imagem: "+str(placa)+"','"+str(x[-1]).replace("<BR>",chr(10))+"','"+str(datetime.datetime.now())+"');"
              ultima_localizacao_id(update.message.from_user.id,"imagem " +str(placa))
              mycursor = mydb.cursor()
              mycursor.execute(sql2)
              mydb.commit()                      
              encontrado=True
        else:
         for i in placa.split(chr(10)):
          #sql="select * from roubados where tudo like '%"+i[:3]+"%"+i[-4:]+"%'"
          sql="select * from roubados where tudo like '%"+i[:3]+""+i[-4:]+"%' union all select * from roubados where tudo like '%"+i[:3]+" "+i[-4:]+"%' union all select * from roubados where tudo like '%"+i[:3]+"-"+i[-4:]+"%'"
          mycursor = mydb.cursor()
          mycursor.execute(sql)
          myresult = mycursor.fetchall()
          if(len(myresult)==0):
              print("Placa "+str(i)+" não encontrada na base dados")          
              if not grupo:
                bot.send_message(
                   chat_id=update.message.chat_id,
                   text="Placa "+str(i)+" não encontrada na base dados"
                    )
                sql2="insert into balote_auditoria(id_telegram,mensagem,resposta,data) values("+str(update.message.from_user.id)+",'texto: "+update.message.text+"','Placa não encontrada na base de dados','"+str(datetime.datetime.now())+"');"
                ultima_localizacao_id(update.message.from_user.id,"texto " +str(placa))
                mycursor = mydb.cursor()
                mycursor.execute(sql2)
                mydb.commit()
               
              return
              
         for x in myresult:
              if not grupo:
                bot.send_message(
                   chat_id=update.message.chat_id,
                   text=str(x[-3]).replace("<BR>",chr(10))
                    )
                sql2="insert into balote_auditoria(id_telegram,mensagem,resposta,data) values("+str(update.message.from_user.id)+",'texto: "+update.message.text+"','"+str(x[-1]).replace("<BR>",chr(10))+"','"+str(datetime.datetime.now())+"');"
                ultima_localizacao_id(update.message.from_user.id,"texto " +str(placa))
                mycursor = mydb.cursor()
                mycursor.execute(sql2)
                mydb.commit()                    
                encontrado=True
     
    if(encontrado):
 
      update.message.reply_text(encontrado_menu_message(update.message.from_user.id,update.message.text),
      reply_markup=encontrado_menu_keyboard())
 
def location(bot, update):
    message = None
    
    if update.edited_message:
        message = update.edited_message
    else:
        message = update.message
    current_pos = (message.location.latitude, message.location.longitude)
    
 
    mydb = mysql.connector.connect(
          host="localhost",
          user="USUARIO_DB",
          passwd="SENHA_DB",
          database="DB"
          )
    mycursor = mydb.cursor()
    sql="insert into localizacao_balote(identificacao,lat,lng,data) values('"+str(message.chat_id)+"','"+str(current_pos[0])+"','"+str(current_pos[1])+"','"+str(datetime.datetime.now()).split(".")[0]+"')"
 
    mycursor.execute(sql)
    mydb.commit()    
    

 
def principal_backup(bot,update):
    print(update.message)
    print(update.message.text)
    autorizados=['674285145','687722997','140356417','1032658936','1244180790']
    #674285145 adm do atena
    #687722997 adm do atena
    #1001465334485 adm do atena dentro do grupo
    usuario_id=str(update.message).split("'")
    print(usuario_id)
    print(usuario_id[8])
    print(usuario_id[42])
    a=list(filter(lambda x: usuario_id[8].find(x)!=-1,autorizados))
    b=update.message
    if(str(b.from_user.id) not in autorizados):
       print(str(b.from_user.id)+ ' saiu')
       return
    #if(len(a)<1):
    #   a=list(filter(lambda x: usuario_id[42].find(x)!=-1,autorizados))
    #   for i in autorizados:
    #     if(str(update.message).find(i)!=-1):
    #        a.append('a')
   # if(len(a)<1):
       #bot.send_message(
       # chat_id=update.message.chat_id,
       # text='Você não tem autorização para o uso desse módulo'
       #)
    #   print("saiu")
     #  return
    cadastro=''
    #print(len(str(update.message).upper().split('$QRCODE')))
    if(len(str(update.message).upper().split('ENDERE'))>1 and len(str(update.message).upper().split('MARCA'))>1 and len(str(update.message).upper().split('PLACA'))>1  ):
       #print str(update.message)
       cadastro='ENDERE'+str(update.message).upper().split('ENDERE')[1]
       cadastro=str(update.message).upper().split('MARCA')[0]

    if(len(str(update.message).upper().split('AVISO'))>1 and len(str(update.message).upper().split('MARCA'))>1 and len(str(update.message).upper().split('PLACA'))>1  ):
       cadastro='AVISO'+str(update.message).upper().split('AVISO')[1]
       cadastro=str(update.message).upper().split('MARCA')[0]

    if(len(str(update.message).upper().split('ALERTA'))>1 and len(str(update.message).upper().split('MARCA'))>1 and len(str(update.message).upper().split('PLACA'))>1  ):
       cadastro='ALERTA'+str(update.message).upper().split('ALERTA')[1]
       cadastro=str(update.message).upper().split('MARCA')[0]

           
    #if(len(str(update.message).upper().split('$QRCODE'))>1):
    #  modo='QRCODE'
    #  bot.send_message(
    #               chat_id=update.message.chat_id,
    #               text="Alterado para o modo QRCODE"
    #                )
    #  return                    
    #if(len(str(update.message).upper().split('$OCRPLACAS'))>1):
    #  modo='OCRPLACAS'
    #  bot.send_message(
    #               chat_id=update.message.chat_id,
    #               text="Alterado para o modo OCRPLACAS"
    #                )       
    #  return             
    #print(update.message)

    placa=str(update.message).split('text')[1].split('entities')[0].split("'")[2]
    #print(placa)
    #'text': 'PBU9473', 'entities'
    #return
    placa=''.join(placa.split(" "))
    placa=placa.replace('-','')
    placa=placa.replace('"','')
    placa=placa.replace("'",'')
    placa=placa.replace('%','')
    placa=placa.replace(';','')
    
    mydb = mysql.connector.connect(
    host="localhost",
    user="USUARIO_DB",
    passwd="SENHA_DB",
    database="DB"
    )
    print("O CADASTRO2 "+cadastro)           
    if cadastro!='':
               cadastro=cadastro.split("TEXT':")[1]
               cadastro=cadastro.replace("'",'')
               cadastro=cadastro.replace('"','')
               cadastro=cadastro.replace(';','')
               cadastro=cadastro.replace('-','')
               #teste
               i=cadastro
               local=""
               placa=""
               data=""
               modelo=""
               try:
                  local=(i.upper().split('ENDEREÇO:\n')[1].split('\n')[0])
               except: 
                     try:
                           local=(i.upper().split('LOCAL')[1].split('\n')[0])
                     except:
                            try:
                               local=(i.upper().split('CIDADE')[1].split('\n')[0])
                            except: 
                               local=('')
               try:
                  placa=(i.upper().split('PLACA:')[1].split('\n')[0])
               except: 
                  placa=('')
               try: 
                  data=((i.upper().split('DATA')[1].split('\n')[0]))
               except: 
                  data=datetime.datetime.now()
               try: 
                  modelo=((i.upper().split('MODELO')[1].split('\n')[0]))
               except: 
                   try:
                        modelo=((i.upper().split('MARCA')[1].split('\n')[0]))
                   except:
                        modelo=('') 
               #teste               
               sql="insert into roubados(tudo,local,placa,data,modelo,data_postagem) values('"+cadastro+"','"+placa+"','"+data+"','"+modelo+"','"+str(datetime.datetime.now())+"')"
              # print(sql)
              # print("placa"+placa)
              # print("data"+data)
              # print("modelo"+modelo)
              # print("tudo"+cadastro)
              # print("agora"+str(datetime.datetime.now()))
               #sql="insert into roubados(tudo) values('"+cadastro+"');"
               mycursor = mydb.cursor()
               mycursor.execute(sql)
               mydb.commit()
               #bot.send_message(
               #    chat_id=update.message.chat_id,
               #    text="Veículo cadastrado na base de dados"
               #     )
    autorizados=['140356417','1032658936','1244180790']
    a=list(filter(lambda x: usuario_id[8].find(x)!=-1,autorizados))

    if(len(a)<1): #se o usuario nao esta autorizado a pesquisar placas
       return                        
    if(len(placa)!=7 and cadastro==''):
        #bot.send_message(
        #    chat_id=update.message.chat_id,
        #    text="Padrão de placa não encontrado"
        #    )     
        return
    if(True):
        i=placa

     

        if(len(placa.split(chr(10)))==0):
          #sql="select * from roubados where tudo like '%"+i[:3]+"%"+i[-4:]+"%'"
          sql="select * from roubados where tudo like '%"+i[:3]+""+i[-4:]+"%' union all select * from roubados where tudo like '%"+i[:3]+" "+i[-4:]+"%' union all select * from roubados where tudo like '%"+i[:3]+"-"+i[-4:]+"%'"
          mycursor = mydb.cursor()
          mycursor.execute(sql)
          myresult = mycursor.fetchall()
          if(len(myresult)==0):
              #print("Placa "+placa+" não encontrada na base dados")      
              if not grupo:
                bot.send_message(
                   chat_id=update.message.chat_id,
                   text="Placa "+placa+" não encontrada na base dados"
                    )          
              return
          #print(len(myresult))     
          for x in myresult:
              if not grupo:
                bot.send_message(
                   chat_id=update.message.chat_id,
                   text=str(x[-1]).replace("<BR>",chr(10))
                    )
        else:
         for i in placa.split(chr(10)):
          #sql="select * from roubados where tudo like '%"+i[:3]+"%"+i[-4:]+"%'"
          sql="select * from roubados where tudo like '%"+i[:3]+""+i[-4:]+"%' union all select * from roubados where tudo like '%"+i[:3]+" "+i[-4:]+"%' union all select * from roubados where tudo like '%"+i[:3]+"-"+i[-4:]+"%'"
          mycursor = mydb.cursor()
          mycursor.execute(sql)
          myresult = mycursor.fetchall()
          if(len(myresult)==0):
              print("Placa "+placa+" não encontrada na base dados")          
              if not grupo:
                bot.send_message(
                   chat_id=update.message.chat_id,
                   text="Placa "+placa+" não encontrada na base dados"
                    )          
              return
              
         for x in myresult:
              if not grupo:
                bot.send_message(
                   chat_id=update.message.chat_id,
                   text=str(x[-1]).replace("<BR>",chr(10))
                    )

         
        
                    

#   print(update.message)
#   response_message="digite /escala <turma> para saber quem esta escalado hoje"
#   bot.send_message(
#    chat_id=update.message.chat_id,
#    text=response_message
#   )
def start2(bot, update):
  #update.message.reply_text(main_menu_message(),
  #reply_markup=main_menu_keyboard())
  update.message.reply_text(encontrado_menu_message(),
  reply_markup=encontrado_menu_keyboard())
  
  
  

def encontrado_menu_message(id_telegram,placa):
   return '['+str(id_telegram)+'] O veículo com placa <'+str(placa)+'> foi encontrado mesmo ou esse é apenas um teste?'

def encontrado_menu_keyboard():
  keyboard = [[InlineKeyboardButton('Sim, encontrei o veículo e digitei/fotografei a placa', callback_data='e1')],
              [InlineKeyboardButton('Foi apenas um teste de funcionalidade da ferramenta', callback_data='e2',request_location=True)]]
  return InlineKeyboardMarkup(keyboard)

def encontrado_menu(bot, update):
  #print(query.message.text)
  query = update.callback_query
  bot.edit_message_text(chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        text=encontrado_menu_message(),
                        reply_markup=encontrado_menu_keyboard())

def encontrado(bot,update):
          
          query = update.callback_query
          placa=str(query.message.text).split("<")[1].split(">")[0]
          id_telegram=str(query.message.text).split("[")[1].split("]")[0]
          #print(query.message.text)
          bot.send_message(
              chat_id=query.message.chat_id,
              text="Carro e usuário adicionados para o relatório de produtividade")
          mydb = mysql.connector.connect(
          host="localhost",
          user="USUARIO_DB",
          passwd="SENHA_DB",
          database="DB"
          )
    
    
          mycursor=mydb.cursor()    
          sql="insert into balote_encontrados(id_telegram,placa) values("+id_telegram+",'"+placa+"')"
          print(sql)     
          mycursor.execute(sql)
          mydb.commit()

def alarme_falso(bot,update):
           query=update.callback_query
           bot.send_message(
              chat_id=query.message.chat_id,
              text="Grato pelo feedback")
           print("não encontrado")        
           print (update.message.location.latitude + " " + update.message.location.longitude)
           
def encontrado_sim_message():
   return "Carro e usuário adicionados para o relatório de produtividade"           
def alarme_falso_message():
   return "Grato pelo feedback"           
def main_menu_message():
  return 'Choose the option in main menu:'
  
def main_menu_keyboard():
  keyboard = [[InlineKeyboardButton('Option 1', callback_data='m1')],
              [InlineKeyboardButton('Option 2', callback_data='m2')],
              [InlineKeyboardButton('Option 3', callback_data='m3')]]
  return InlineKeyboardMarkup(keyboard)

def first_menu_keyboard():
  keyboard = [[InlineKeyboardButton('Submenu 1-1', callback_data='m1_1')],
              [InlineKeyboardButton('Submenu 1-2', callback_data='m1_2')],
              [InlineKeyboardButton('Main menu', callback_data='main')]]
  return InlineKeyboardMarkup(keyboard)

def second_menu_keyboard():
  keyboard = [[InlineKeyboardButton('Submenu 2-1', callback_data='m2_1')],
              [InlineKeyboardButton('Submenu 2-2', callback_data='m2_2')],
              [InlineKeyboardButton('Main menu', callback_data='main')]]
  return InlineKeyboardMarkup(keyboard)
def first_menu_message():
  return 'Choose the submenu in first menu:'

def second_menu_message():
  return 'Choose the submenu in second menu:'
def main_menu(bot, update):
  query = update.callback_query
  bot.edit_message_text(chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        text=main_menu_message(),
                        reply_markup=main_menu_keyboard())
def first_menu_keyboard():
  keyboard = [[InlineKeyboardButton('Submenu 1-1', callback_data='m1_1')],
              [InlineKeyboardButton('Submenu 1-2', callback_data='m1_2')],
              [InlineKeyboardButton('Main menu', callback_data='main')]]
  return InlineKeyboardMarkup(keyboard)

def second_menu_keyboard():
  keyboard = [[InlineKeyboardButton('Submenu 2-1', callback_data='m2_1')],
              [InlineKeyboardButton('Submenu 2-2', callback_data='m2_2')],
              [InlineKeyboardButton('Main menu', callback_data='main')]]
  return InlineKeyboardMarkup(keyboard)
  
def first_menu(bot, update):
  query = update.callback_query
  bot.edit_message_text(chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        text=first_menu_message(),
                        reply_markup=first_menu_keyboard())

def second_menu(bot, update):
  query = update.callback_query
  bot.edit_message_text(chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        text=second_menu_message(),
                        reply_markup=second_menu_keyboard())  
def first_submenu(bot, update):
  pass

def second_submenu(bot, update):
  pass  
def main():
    updater = Updater(token=TELEGRAM_TOKEN)
    
    dispatcher = updater.dispatcher
    dispatcher.add_handler(
        CommandHandler('maps', maps, pass_args=True) 
    )
    dispatcher.add_handler(
        CommandHandler('escala', escala, pass_args=True) 
    )
    dispatcher.add_handler(
        CommandHandler('start', start)
    )
    dispatcher.add_handler(
        CommandHandler('start2', start2)
    )
    dispatcher.add_handler(
        CommandHandler('http', http_cats, pass_args=True) 
    )
    dispatcher.add_handler(
        CommandHandler('spam', spam, pass_args=True) 
    ) 
    dispatcher.add_handler(
        CommandHandler('gerar_senha', gerar_senha, pass_args=False) 
    )    
    dispatcher.add_handler(
        CommandHandler('registro', registro, pass_args=True) 
    )        
    dispatcher.add_handler(
        CommandHandler('help', help, pass_args=False) 
    )            
    dispatcher.add_handler(
        CommandHandler('cadastro', cadastro, pass_args=False) 
    )    
    dispatcher.add_handler(
        CommandHandler('historico', historico, pass_args=False) 
    )
    updater.dispatcher.add_handler(CallbackQueryHandler(encontrado, pattern='e1'))
    updater.dispatcher.add_handler(CallbackQueryHandler(alarme_falso, pattern='e2'))    
    updater.dispatcher.add_handler(CallbackQueryHandler(encontrado_menu, pattern='encontrado'))
    updater.dispatcher.add_handler(CallbackQueryHandler(main_menu, pattern='main'))
    updater.dispatcher.add_handler(CallbackQueryHandler(first_menu, pattern='m1'))
    updater.dispatcher.add_handler(CallbackQueryHandler(second_menu, pattern='m2'))
    updater.dispatcher.add_handler(CallbackQueryHandler(first_submenu,
                                                    pattern='m1_1'))
    updater.dispatcher.add_handler(CallbackQueryHandler(second_submenu,
                                                    pattern='m2_1'))   
    dispatcher.add_handler(
        MessageHandler(Filters.command, unknown)
    )
    dispatcher.add_handler(
        MessageHandler(Filters.text, principal_texto)
    )
    #if modo =='OCRPLACAS' :
    dispatcher.add_handler( 
        MessageHandler(Filters.photo,placa)
    )
    #if modo == 'QRCODE' :
     #   dispatcher.add_handler( 
      #  MessageHandler(Filters.photo,qrcode)
       # )
   # dispatcher.add_handler(MessageHandler(Filters.photo, self._msg_hook(PhotoMessageEvent)))
    location_handler = MessageHandler(Filters.location, location)
    dispatcher.add_handler(location_handler)
   
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    print("press CTRL + C to cancel.")
    main()
