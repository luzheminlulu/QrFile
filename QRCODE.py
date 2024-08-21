#!/usr/bin/python3

from PIL import Image
import qrcode
import cv2
import numpy as np
import base64
import math
import time
import os
from datetime import datetime
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f","--FileName",type=str,default="./QRCODE.py",help="文件名.")
parser.add_argument("-s","--STEP"    ,type=int,default=400          ,help="单次传输容量(Byte).")
args=parser.parse_args()
FileName=args.FileName
Step    =args.STEP

cv2.namedWindow("QRCODE",cv2.WINDOW_NORMAL)
cv2.resizeWindow('QRCODE',800,900)

	


def main():


	with open(FileName,'rb') as f:
		DataBase64 = base64.b64encode(f.read()).decode('utf-8')
		#DataBase64 = f.read()
	
	#image_data = base64.b64decode(DataBase64)
	#with open('./result.gif','wb') as fw:
	#	fw.write(image_data)
	
	BaseName = os.path.basename(FileName)
	
	DataSize = len(DataBase64)

	QrSize   = math.ceil(DataSize/Step)
	
	print('数据量:',DataSize,'Byte, 单次传输:',Step,'Byte, 传输次数:',QrSize,'次',)
	

	waitTime  = 80
	waitTimed = waitTime
	
	returnFlag=0
	
	pause_k = -1
	t1 = datetime.now().timestamp()
	fps= 0
	
	
	qr = qrcode.QRCode(
		#	version=10,
			error_correction=qrcode.constants.ERROR_CORRECT_H,
		#	box_size=8,
		#	border=4
		)
	#version：值为1~40的整数，控制二维码的大小（最小值是1，是个21×21的矩阵）
	#error_correction：控制二维码的错误纠正功能。qrcode.constants.ERROR_CORRECT_X可取值下列4个常量： 
	#1. X=L 7% 2. X=M（默认）15% 3. X=Q 25% 4. X=H 大约30%或更少的错误能被纠正。
	#box_size：控制二维码中每个小格子包含的像素数。
	#border：控制边框（二维码与图片边界的距离）包含的格子数（默认为4)	
	
	
	while(1):
		k=0
		while(k < QrSize):
			if(pause_k>=0):
				i = pause_k
			else:
				i = k
				k+=1
			
			qr.clear()
			
			#print(i,'/',QrSize)
			OneQrData = DataBase64[Step*i:Step*(i+1)]
			qr.add_data(f'{BaseName}:{i}:{QrSize}:{OneQrData}')

			qr.make(fit=True)
			img = qr.make_image()
		
		
			#cv_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
			img = img.convert('RGB')
			img = img.resize((800, 800))
			#cv_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
			
			new_frame = Image.new("RGB", (800,900), (255, 255, 255))
			
			new_frame.paste(img, (0, 100 ))
			new_frame = cv2.cvtColor(np.array(new_frame), cv2.COLOR_RGB2BGR)
			
			if(waitTimed<waitTime):
				infoadd='(speed down)'
			elif(waitTimed>waitTime):
				infoadd='(speed up)'
			else:
				infoadd=''
			waitTimed=waitTime
			info = f"{i}/{QrSize-1} {'{:.2f}'.format(fps)}fps {'{:.2f}'.format(Step*fps/1000)}KB/s "+infoadd
			cv2.putText(new_frame, info, (150, 80), cv2.FONT_HERSHEY_COMPLEX, 1.0, (100, 200, 200), 2)
			
			cv2.imshow("QRCODE", new_frame)
			
			key = cv2.waitKeyEx(waitTime)
			
			#print(key)
			if(key==ord(' ')):
				if(pause_k<0):
					pause_k = k
				else:
					k=pause_k
					pause_k = -1
			
			if(key>=ord('0') and key<=ord('9')):
				
				if(pause_k<0 or returnFlag):
					pause_k=0
					returnFlag=0
				
				pause_k = pause_k*10 + int(key - ord('0'))
				if(pause_k>=QrSize):
					pause_k = int(key - ord('0'))
				if(pause_k>=QrSize):
					pause_k = QrSize-1
				#print(pause_k)
			if(key==27):
				cv2.destroyAllWindows()
				return
			if(key==2490368 or key==65362 ): #上
				waitTime -= 1
				if(waitTime<1):
					waitTime = 1
				#print('帧间延迟:',waitTime,'ms')
			if(key==2621440 or key==65364 ): #下
				waitTime += 1
				#print('帧间延迟:',waitTime,'ms')
			if(key==2424832 or key==65361 ): #左
				if(pause_k<0):
					pause_k=k
				pause_k -= 1
				if(pause_k<0):
					pause_k=0
				#print(pause_k)
			if(key==2555904 or key==65363 ): #右
				if(pause_k<0):
					pause_k=k
				pause_k += 1
				if(pause_k>=QrSize):
					pause_k = QrSize-1
				#print(pause_k)
			if(key==13):
				returnFlag = 1
				
			
			t2 = t1
			t1 = datetime.now().timestamp()
			fps = 1/(t1-t2)
			#print(fps,'fps')
			
		
	
	

 
main()  #调用main()函数