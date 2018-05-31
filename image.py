# coding='utf-8'
import cv2 as cv
import PyQt5
import sys
from math import *
import numpy as np
def nothing(x):
	pass
temp_img = 0
drawing = False
L_button = False
R_button = False
mode = False
ix, iy = -1, -1
sx, sy = -1, -1
def rotate_image(event, x, y, flags, param):
	global ix, iy, temp_img, drawing
	if event == cv.EVENT_LBUTTONDOWN:
		drawing = True
		height,width=img.shape[:2]
		degree=270
		heightNew=int(width*fabs(sin(radians(degree)))+height*fabs(cos(radians(degree))))
		widthNew=int(height*fabs(sin(radians(degree)))+width*fabs(cos(radians(degree))))
		matRotation=cv.getRotationMatrix2D((width/2,height/2),degree,1)
		matRotation[0,2] +=(widthNew-width)/2  
		matRotation[1,2] +=(heightNew-height)/2  
		imgRotation=cv.warpAffine(img,matRotation,(widthNew,heightNew),borderValue=(255,255,255))
		temp_img = imgRotation.copy()
	elif event == cv.EVENT_RBUTTONDOWN:
		height,width=img.shape[:2]
		degree=90
		heightNew=int(width*fabs(sin(radians(degree)))+height*fabs(cos(radians(degree))))
		widthNew=int(height*fabs(sin(radians(degree)))+width*fabs(cos(radians(degree))))
		matRotation=cv.getRotationMatrix2D((width/2,height/2),degree,1)
		matRotation[0,2] +=(widthNew-width)/2  
		matRotation[1,2] +=(heightNew-height)/2  
		imgRotation=cv.warpAffine(img,matRotation,(widthNew,heightNew),borderValue=(255,255,255))
		temp_img = imgRotation.copy()
def init_stat():
	global drawing, mode, ix, iy, sx, sy
	drawing = False
	mode = False
	ix, iy = -1, -1
	sx, sy = -1, -1
def cut_image(event, x, y, flags, param):
	global drawing, mode, ix, iy, sx, sy
	if event == cv.EVENT_LBUTTONDOWN:
		ix, iy = x, y
		sx, sy = x, y
		drawing = True
	elif event == cv.EVENT_MOUSEMOVE:
		if drawing == True:
			sx, sy = x, y
	elif event == cv.EVENT_LBUTTONUP:
		sx, sy = x, y
		drawing = False
def change_position():
	global ix, sx
	ix -= 1
	sx -= 1
def draw_circle(event,x,y,flags,param):
	r=cv.getTrackbarPos('R','image')
	g=cv.getTrackbarPos('G','image')
	b=cv.getTrackbarPos('B','image')
	size=cv.getTrackbarPos('brush_size','image')
	color=(b,g,r)
	global ix,iy,drawing,mode
	if event==cv.EVENT_LBUTTONDOWN:
		drawing=True
		ix,iy=x,y
	elif event==cv.EVENT_MOUSEMOVE and flags==cv.EVENT_FLAG_LBUTTON:
		if drawing==True:
			if mode==True:
				cv.rectangle(img,(ix,iy),(x,y),color,-1, lineType = cv.LINE_AA)
			else:
				cv.circle(img,(x,y),size,color,-1, lineType = cv.LINE_AA)
	elif event==cv.EVENT_LBUTTONUP:
		drawing=False
	global sx, sy
	if sx != -1 and sy != -1 and drawing==True:
		cv.line(img,(sx, sy),(x, y),color,2 * size, lineType = cv.LINE_AA)
	sx = x
	sy = y
print("欢迎使用图像处理程序")
src_image = input("请输入你要处理的文件路径：")
des_image = input("请输入你要存放目标文件的路径：")
try:
	img = cv.imread(src_image)
except:
	print("读取源文件失败")
while True:
	init_stat()
	func_code = input("""请输入你需要对目标图像进行的操作：
		c: 图片裁剪
		r: 图片旋转
		p: 人像美容
		t: 添加文字
		w: 用画笔进行自由绘画
		u: 滤镜
		q: 退出
		""")
	if(func_code == 'w'):
		input("完成编辑后按s进行保存，按esc退出，拖动滑条改变RGB值来确定画笔颜色。")
		cv.namedWindow('image')
		cv.createTrackbar('R','image',0,255,nothing)
		cv.createTrackbar('G','image',0,255,nothing)
		cv.createTrackbar('B','image',0,255,nothing)
		cv.createTrackbar('brush_size','image',1,10,nothing)
		cv.setMouseCallback('image',draw_circle)
		while(1):
			cv.imshow('image',img)
			k=cv.waitKey(1)&0xFF
			if k==27:
				init_stat()
				break
			if k==ord('s'):
				try:
					cv.imwrite(des_image, img)
				except:
					print("文件写入失败，请检查目标路径是否正确")
		cv.destroyWindow('image')

	elif(func_code == 'c'):
		input("""按住鼠标左键并拖动来确定你要裁剪的区域，选好之后可以用a,s,d,w移动所选区域，
			用1,2,3,4,5,6,7,8来分别向各个方向移动你选中区域的各条边
			按enter进行保存
			按esc退出""")
		cv.namedWindow('image')
		cv.setMouseCallback('image',cut_image)
		temp_img = img.copy()
		while(1):
			img = temp_img.copy()
			cv.rectangle(img, (ix, iy), (sx, sy), (255,0,0), 1, lineType = cv.LINE_AA)
			cv.imshow('image',img)
			k=cv.waitKey(1)&0xFF
			if k==27:
				init_stat()
				break
			elif k==ord('a'):
				if ix >= 1 and sx >= 1:
					ix -= 1
					sx -= 1
			elif k==ord('s'):
				iy += 1
				sy += 1
			elif k==ord('d'):
				ix += 1
				sx += 1
			elif k==ord('w'):
				if iy >= 1 and sy >=1:
					iy -= 1
					sy -= 1
			elif k == ord('1'):
				if(ix >= 1):
					ix -= 1
			elif k == ord('2'):
				ix += 1
			elif k == ord('3'):
				if(sx >= 1):
					sx -= 1
			elif k == ord('4'):
				sx -+ 1
			elif k == ord('5'):
				if(iy >= 1):
					iy -= 1
			elif k == ord('6'):
				iy += 1
			elif k == ord('7'):
				if(sy >= 1):
					sy -= 1
			elif k == ord('8'):
				sy += 1
			elif k == ord('\r'):
				roiImg = temp_img[iy:sy,ix:sx]
				# print(ix, iy, sx, sy)
				cv.imwrite(des_image, roiImg)
				temp_img = roiImg.copy()
				ix, iy, sx, sy = -1,-1,-1,-1
		cv.destroyWindow('image')
	elif(func_code == 'r'):
		input("按鼠标左键顺时针旋转，按鼠标右键逆时针旋转，按s保存，按esc退出")
		cv.namedWindow('image')
		cv.setMouseCallback('image',rotate_image)
		temp_img = img.copy()
		while(1):
			img = temp_img.copy()
			cv.imshow('image', img)
			k=cv.waitKey(1)&0xFF
			if k==27:
				init_stat()
				break
			elif k == ord('s'):
				cv.imwrite(des_image, img)
		cv.destroyWindow('image')
	elif(func_code == 'q'):
		break
	else:
		print("请输入正确的功能码！")
