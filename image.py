# coding='utf-8'
import cv2 as cv
import sys
import numpy as np
def nothing(x):
	pass
drawing = False
mode = False
ix, iy = -1, -1
sx, sy = -1, -1
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
				cv.rectangle(img,(ix,iy),(x,y),color,-1)
			else:
				cv.circle(img,(x,y),size,color,-1)
	elif event==cv.EVENT_LBUTTONUP:
		drawing=False
	global sx, sy
	if sx != -1 and sy != -1 and drawing==True:
		cv.line(img,(sx, sy),(x, y),color,2 * size)
	sx = x
	sy = y
print("欢迎使用图像处理程序")
src_image = input("请输入你要处理的文件路径：")
des_image = input("请输入你要存放目标文件的路径：")
while True:
	func_code = input("""请输入你需要对目标图像进行的操作：
		c: 图片裁剪
		r: 图片旋转
		p: 人像美容
		t: 添加文字
		w: 用画笔进行自由绘画
		u: 滤镜
		q: 退出
		""")
	try:
		img = cv.imread(src_image)
	except:
		print("读取源文件失败")
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
				break
			if k==ord('s'):
				try:
					cv.imwrite(des_image, img)
				except:
					print("文件写入失败，请检查目标路径是否正确")
		cv.destroyWindow('image')
	elif(func_code == 'q'):
		break
