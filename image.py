# coding='utf-8'
import cv2 as cv
import PyQt5
import random
import sys
from math import *
import numpy as np
def nothing(x):
	pass
temp_img = 0
img = 0
ori_img = 0
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
def skyRegion():
	Low = np.array([100,43,46])
	High = np.array([124, 255, 255])
	global img, ori_img
	temp_img = img.copy()
	temp_img = cv.cvtColor(temp_img, cv.COLOR_BGR2HSV)
	h,s,v = cv.split(temp_img)
	v = cv.equalizeHist(v)
	hsv = cv.merge((h,s,v))
	imgThresholded = cv.inRange(hsv, Low, High)
	imgThresholded = cv.medianBlur(imgThresholded,9)
	kernel = np.ones((5,5),np.uint8)
	imgThresholded = cv.morphologyEx(imgThresholded, cv.MORPH_OPEN, kernel, iterations = 10)
	imgThresholded = cv.medianBlur(imgThresholded,9)
	cv.imwrite("temp_mask.jpg", imgThresholded)
def seamClone(skyname):
	skyimg = cv.imread(skyname)
	global img, ori_img
	mask = cv.imread("temp_mask.jpg", 0)
	mask0 = cv.imread("temp_mask.jpg")
	contours = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
	cnt = contours[0]
	x,y,w,h = cv.boundingRect(cnt)
	if w == 0 or h == 0:
		return img
	dst_x = len(img[0])
	dst_y = len(img[1])
	src_x = len(img[0])
	src_y = len(img[1])
	scale_x = w * 1.0 / src_x
	# print(img.shape[0], img.shape[1])
	skyimg = cv.resize(skyimg, (img.shape[1], img.shape[0]), interpolation = cv.INTER_CUBIC)
	center = (int((x + w) / 2), int((y + h / 2)))
	img = cv.seamlessClone(skyimg, img, mask0, center, cv.NORMAL_CLONE)
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
def findPos(des):
	t_x = int(des[1] / 4)
	t_y = int(des[2] / 4)
	t_b = int(des[0] / 4)
	b_x = int(t_b / 8) * 64
	b_y = int(t_b % 8) * 64
	t_x += b_x
	t_y += b_y
	return [t_x, t_y]
def seka(seka_name):
	global img, ori_img
	img = ori_img.copy()
	new = cv.imread(seka_name)
	for i in range(len(img)):
		for j in range(len(img[0])):
			# pos = np.where(ori == img[i][j])
			pos = findPos(img[i][j])
			# print(pos)
			img[i][j] = new[pos[0]][pos[1]]
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
img = cv.imread(src_image)
if img is None:
	print("读取源文件失败")
	sys.exit()
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
	elif(func_code == 'u'):
		ori_img = img.copy()
		input("""按1-8来切换不同种类滤镜:
			1:怀旧风
			2:连环画
			3:浮雕
			4:毛玻璃
			5.素描
			6.你的名字
			7.美食
			""")
		while(1):
			cv.namedWindow('image', cv.WINDOW_AUTOSIZE)
			cv.imshow('image', img)
			k=cv.waitKey(1)&0xFF
			if k==27:
				init_stat()
				break
			elif k==ord('8'):
				img = ori_img
				skyRegion()
				img = cv.imread('temp_mask.jpg')
				seamClone("sky4.jpg")
			elif k==ord('7'):
				seka("meishi_seka.jpg")
			elif k==ord('6'):
				img = ori_img
				skyRegion()
				seka("your_name_seka.jpg")
				seamClone("sky3.jpg")
			elif k==ord('5'):
				t1 = cv.Sobel(ori_img, cv.CV_16S, 1, 0)
				t2 = cv.Sobel(ori_img, cv.CV_16S, 0, 1)
				abst1 = cv.convertScaleAbs(t1)
				abst2 = cv.convertScaleAbs(t2)
				dst = cv.addWeighted(abst1, 0.5, abst2, 0.5, 0)
				dst = cv.cvtColor(dst, cv.COLOR_BGR2GRAY)
				dst = 255 - dst
				img = dst.copy()
				# gray0 = cv.cvtColor(ori_img, cv.COLOR_BGR2GRAY)
				# gray1 = cv.addWeighted(gray0, -1, None, 0, 255)
				# gray1 = cv.GaussianBlur(gray1, (11,11), 0)
				# temp_img = ori_img.copy()
				# for i in range(0, temp_img.shape[0]):
				# 	for j in range(0, temp_img.shape[1]):
				# 		tmp0 = float(gray0[i][j])
				# 		tmp1 = float(gray1[i][j])
				# 		if (tmp0 + (tmp0 * tmp1) / (256 - tmp1)) > 255:
				# 			temp_img[i][j] = 255
				# 		else:
				# 			temp_img[i][j] = (tmp0 + (tmp0 * tmp1) / (256 - tmp1))
				# img = temp_img
			elif k==ord('4'):
				temp_img = ori_img.copy()
				place = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 0], [0, 1], [1, -1], [1, 0], [1, 1]]
				for i in range(0, temp_img.shape[0] - 1):
					for j in range(0, temp_img.shape[1] - 1):
						for k in range(0, 3):
							place_num = random.randint(0, 8)
							temp_img[i][j][k] = ori_img[i + place[place_num][0]][j + place[place_num][1]][k]
				img = temp_img
			elif k==ord('3'):
				temp_img = ori_img.copy()
				for i in range(0, temp_img.shape[0] - 1):
					for j in range(0, temp_img.shape[1] - 1):
						for k in range(0, 3):
							tmp0 = int(int(ori_img[i + 1][(j + 1)][k]) - int(ori_img[i - 1][(j - 1)][k]) + 128)
							if tmp0 < 0:
								temp_img[i][j][k] = 0
							elif tmp0 > 255:
								temp_img[i][j][k] = 255
							else:
								temp_img[i][j][k] = tmp0
				img = temp_img
			elif k==ord('2'):
				temp_img = ori_img.copy()
				for i in temp_img:
					for j in i:
						nR = abs(float(float(j[1]) - float(j[0]) + float(j[1]) + float(j[2]))) * (float(j[2]) / 256)
						nG = abs(float(float(j[0]) - float(j[1]) + float(j[0]) + float(j[2]))) * (float(j[2]) / 256)
						nB = abs(float(float(j[0]) - float(j[1]) + float(j[0]) + float(j[2]))) * (float(j[1]) / 256)
						# print(abs(j[1] - j[0] + j[1] + j[2]), j[2], abs(j[1] - j[0] + j[1] + j[2]) * j[2], nR)
						if nR > 255:
							nR = 255
						if nB > 255:
							nB = 255
						if nG > 255:
							nG = 255
						j[0] = nB
						j[1] = nG
						j[2] = nR
				temp_img = cv.cvtColor(temp_img, cv.COLOR_BGR2GRAY)
				img = temp_img
			elif k==ord('r'):
				img = ori_img.copy()
			elif k==ord('s'):
				try:
					cv.imwrite(des_image, img)
				except:
					print("文件写入失败，请检查目标路径是否正确")
			elif k==ord('1'):
				temp_img = img.copy()
				for i in temp_img:
					for j in i:
						nR = 0.393 * j[2] + 0.769 * j[1] + 0.189 * j[0]
						nG = 0.349 * j[2] + 0.686 * j[1] + 0.168 * j[0]
						nB = 0.272 * j[2] + 0.534 * j[1] + 0.131 * j[0]
						if nR > 255:
							nR = 255
						if nB > 255:
							nB = 255
						if nG > 255:
							nG = 255
						j[0] = nB
						j[1] = nG
						j[2] = nR
				img = temp_img
		cv.destroyWindow('image')
	elif(func_code == 't'):
		temp_img = img.copy()
		text = input("请输入你要加的文字：")
		font = cv.FONT_HERSHEY_SIMPLEX
		while(1):
			font_num = input("""请输入序号选择字体：
				1:FONT_HERSHEY_SIMPLEX -               正常大小无衬线字体. 
				2:FONT_HERSHEY_PLAIN -                 小号无衬线字体.
				3:FONT_HERSHEY_DUPLEX -                正常大小无衬线字体比 CV_FONT_HERSHEY_SIMPLEX 更复杂) 
				4:FONT_HERSHEY_COMPLEX -               正常大小有衬线字体.
				5:FONT_HERSHEY_TRIPLEX -               正常大小有衬线字体 (  比 CV_FONT_HERSHEY_COMPLEX更复杂) 
				6:FONT_HERSHEY_COMPLEX_SMALL -          CV_FONT_HERSHEY_COMPLEX 的小译本.
				7:FONT_HERSHEY_SCRIPT_SIMPLEX -         手写风格字体.
				8:FONT_HERSHEY_SCRIPT_COMPLEX -         比 CV_FONT_HERSHEY_SCRIPT_SIMPLEX 更复杂
				""")
			try:
				int(font_num)
			except:
				print("请输入正确的字体序号")
				continue
			if 1 <= int(font_num) and 8 >= int(font_num):
				if(int(font_num) == 1):
					font = cv.FONT_HERSHEY_SIMPLEX
				elif(int(font_num) == 2):
					font = cv.FONT_HERSHEY_PLAIN
				elif(int(font_num) == 3):
					font = cv.FONT_HERSHEY_DUPLEX
				elif(int(font_num) == 4):
					font = cv.FONT_HERSHEY_COMPLEX
				elif(int(font_num) == 5):
					font = cv.FONT_HERSHEY_TRIPLEX
				elif(int(font_num) == 6):
					font = cv.FONT_HERSHEY_COMPLEX_SMALL
				elif(int(font_num) == 7):
					font = cv.FONT_HERSHEY_SCRIPT_SIMPLEX
				elif(int(font_num) == 8):
					font = cv.FONT_HERSHEY_SCRIPT_COMPLEX
				break
			else:
				print("请输入正确的字体序号")
		input("拖动滑条改变文字颜色和大小，按a,s,d,w来改变文字位置, 按enter进行保存")
		cv.namedWindow('image')
		cv.createTrackbar('R','image',0,255,nothing)
		cv.createTrackbar('G','image',0,255,nothing)
		cv.createTrackbar('B','image',0,255,nothing)
		cv.createTrackbar('char_size','image',1,10,nothing)
		ix, iy = 0, 100
		while(1):
			img = temp_img.copy()
			r=cv.getTrackbarPos('R','image')
			g=cv.getTrackbarPos('G','image')
			b=cv.getTrackbarPos('B','image')
			color=(b,g,r)
			size=cv.getTrackbarPos('char_size','image')
			cv.putText(img, text, (ix, iy), font, int(size), color, lineType = cv.LINE_AA)
			cv.imshow('image', img)
			k=cv.waitKey(1)&0xFF
			if k==27:
				init_stat()
				break
			elif k==ord('\r'):
				try:
					cv.imwrite(des_image, img)
				except:
					print("文件写入失败，请检查目标路径是否正确")
			elif k== ord('a'):
				if(ix >= 1):
					ix -= 1
			elif k== ord('w'):
				if(iy >= 1):
					iy -= 1
			elif k==ord('s'):
				iy += 1
			elif k==ord('d'):
				ix += 1
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
