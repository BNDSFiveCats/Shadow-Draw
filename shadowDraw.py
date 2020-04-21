import os 
from cv2 import cv2 as cv 
import numpy as np
import copy

def mkdir(path):
    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        print (path+' 文件夹创建成功')
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print (path+' 目录已存在')
        return False

#设置分层层数
layer = int(input("层数 layer: "))
col = 255*(layer-1)//layer
colorRange_list = []
for lay in range(1,layer+1): 
    colorRange_list.append([256*(lay-1)//layer,256*lay//layer-1])
#print(colorRange_list)

# 图片格式
format_list = ["png","jpg","jpeg"]
# 读取图片文件名
path = os.getcwd() 
obj_list = os.listdir(path)
photo_list = []
folder_list = []
for file in obj_list:
    fileSli = file.split(".")
    if fileSli[-1] in format_list:
        photo_list.append(file)
    if len(fileSli) == 1:
        folder_list.append(file)
del file,fileSli
#print(photo_list)
#print(folder_list)

finishedPhoto_list = []
unfinishedPhoto_list = []
# 筛选为操作图片
for photo in photo_list:
    if photo.split(".")[0]+"_layer"+str(layer)+"_" in folder_list: # 对于有两个"."的文件会出现问题
        finishedPhoto_list.append(photo)
    else:
        unfinishedPhoto_list.append(photo)
del photo
#print(unfinishedPhoto_list)

# 读取图片 制作图层
for photo in unfinishedPhoto_list:
    print(photo)
    imgbulticolor = cv.imread(photo,cv.IMREAD_COLOR)
    img = cv.imread(photo,cv.IMREAD_GRAYSCALE)
    #print(img)
    lenx = len(img[0])
    leny = len(img)
    # 创建图片
    imgOri = np.zeros((leny,lenx),int)
    for y in range(leny):
        for x in range(lenx):
            imgOri[y][x] = 255
    img_list = []
    for i in range(layer):
        print("start layer "+ str(i))
        optImg = imgOri
        for y in range(leny):
            for x in range(lenx):
                if img[y][x] <= colorRange_list[i][0]:
                    optImg[y][x] = col
        img_list.append(copy.deepcopy(optImg))

    mkdir(os.path.join(path,photo.split(".")[0]+"_layer"+str(layer)+"_")+"\\")
    num = 0
    for pho in img_list:
        num += 1
        filname = "P"+str(num)+".jpg"
        cv.imwrite(
            os.path.join(
                path,photo.split(".")[0]+"_layer"+str(layer)+"_",filname
            ),pho
        )
    cv.imwrite(
        os.path.join(path,photo.split(".")[0]+"_layer"+str(layer)+"_",photo.split(".")[0]+".jpg"),imgbulticolor
    )