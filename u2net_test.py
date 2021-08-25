import os
from skimage import io, transform
import torch
import torchvision
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms#, utils
# import torch.optim as optim

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import glob
import sys
import time
import cv2 as cv

from data_loader import RescaleT
from data_loader import ToTensor
from data_loader import ToTensorLab
from data_loader import SalObjDataset

from model import U2NET # full size version 173.6 MB
from model import U2NETP # small version u2net 4.7 MB


def MAIN(imagelist):
    # normalize the predicted SOD probability map
    def normPRED(d):                                                # 归一化概率图d
        ma = torch.max(d)
        mi = torch.min(d)

        dn = (d-mi)/(ma-mi)

        return dn

    def save_output(image_name,pred,i_dir,d_dir):                         # 保存并输出图片

        predict = pred                                              # pred.size = [1,320,320]
        predict = predict.squeeze()                                 # 去除predict中的1维[1,320,320]->[320,320]
        predict_np = predict.cpu().data.numpy()                     # 将数据转化为numpy并转存到CPU中（之前位于GPU）

        im = Image.fromarray(predict_np*255).convert('RGB')         # 将array形式转化为图片形式，且转换为RGB模式（未转换前array数组为BGR格式）,predict_np仍为[320,320]
        img_name = image_name.split(os.sep)[-1]                     # 将文件路径（image_name）按照分隔符“\”全部切开（-1参数的作用），例：C:\Users\kilok\  ->  C: Users kilok
        image = io.imread(image_name)                               # 按路径读入图片，此处选用io.imread，故读取格式为RGB格式
    
        imo = im.resize((image.shape[1],image.shape[0]),resample=Image.BILINEAR)    # 对图像进行缩放处理，采用双线性采样方式缩放,缩放为原图大小
    
        origin_image = Image.open(i_dir)                            # origin_image 为PIL.JpegImageFile格式
        origin_image = origin_image.convert("RGB")                  # 舍弃透明度通道
        origin_image = np.array(origin_image)                       # 将origin_image转为数组形式以方便计算
    
        imo_norm = np.array(imo)/255                                # 将imo转为数组形式并将所有元素同除255，赋给imo_norm
        imo_norm_reverse = [1,1,1]-imo_norm
        colored_front_img_array = origin_image * imo_norm           # origin_image和imo_norm两者相乘
        colored_front_img = Image.fromarray(np.uint8(colored_front_img_array))  # 将上行变量转化为图片形式（.png）
        colored_back_img_array = origin_image * imo_norm_reverse    # 取背景操作
        colored_back_img = Image.fromarray(np.uint8(colored_back_img_array))

        pb_np = np.array(imo)                                       # 缩放后图片转化为array数组

        aaa = img_name.split(".")                                   # 按.切分路径
        bbb = aaa[0:-1]                                             # 按左起第0个元素直到倒数第一个元素-1进行切片
        imidx = bbb[0]                                              # 第一个切片，如C：
        for i in range(1,len(bbb)):
            imidx = imidx + "." + bbb[i]                            

        imo.save(d_dir+imidx+'.png')                                # 循环保存图片文件as.png
    
        class Temp:
            def __init__(self):
                self.Front = colored_front_img
                self.Back = colored_back_img
        def RETURN():
            return Temp()                                           # 通过定义的class类返回两张图片（一张前景一张背景）
        


    def main(img_name_list):

        # --------- 1. get image path and name ---------
        model_name='u2net'#u2netp
                                                                                                     # 只接收一个文件夹路径传入
        
            #os.path.join(os.getcwd(), 'test_data', 'test_images')                                   # 在当前程序路径加入test_data test_images
        prediction_dir = os.path.join(os.getcwd(), 'test_data', model_name + '_results' + os.sep)    # 模型预测结果的存放目录，我这里是C:\Users\......\U-2-Net\test_data\u2net_results
        model_dir = os.path.join(os.getcwd(), 'saved_models', model_name, model_name + '.pth')       # 学习到的模型参数文件所在目录
        
                                                                                                     # 测试文件夹下的图片路径列表
        print(img_name_list)                                                                        # img_name_list是一个列表形式C:\\Users\\......\\U-2-Net\\test_data\\u2net_results\\...

        # --------- 2. dataloader ---------
        #1. dataloader
        test_salobj_dataset = SalObjDataset(img_name_list = img_name_list,
                                            lbl_name_list = [],
                                            transform=transforms.Compose([RescaleT(320),
                                                                          ToTensorLab(flag=0)])
                                            )                                                       # 加载数据
        test_salobj_dataloader = DataLoader(test_salobj_dataset,
                                            batch_size=1,
                                            shuffle=False,
                                            num_workers=1)

        # --------- 3. model define ---------
        if(model_name=='u2net'):
            print("...load U2NET---173.6 MB")                                                       # 这两行打印可以去掉
            net = U2NET(3,1)
        elif(model_name=='u2netp'):
            print("...load U2NEP---4.7 MB")
            net = U2NETP(3,1)

        if torch.cuda.is_available():
            net.load_state_dict(torch.load(model_dir))
            net.cuda()                                                                              # 送入显卡处理或送入CPU处理
        else:
            net.load_state_dict(torch.load(model_dir, map_location='cpu'))
        net.eval()

        # --------- 4. inference for each image ---------

        for i_test, data_test in enumerate(test_salobj_dataloader):                                 # 同时遍历键与值

        
            print("inferencing:",img_name_list[i_test].split(os.sep)[-1])

            inputs_test = data_test['image']                                                        # 导入图片
            inputs_test = inputs_test.type(torch.FloatTensor)                                       # inputs_test为[1，3,320,320]格式

            if torch.cuda.is_available():
                inputs_test = Variable(inputs_test.cuda())
            else:
                inputs_test = Variable(inputs_test)

            d1,d2,d3,d4,d5,d6,d7= net(inputs_test)                                                  # 对输入图片送入模型处理

            # normalization
            pred = d1[:,0,:,:]                                                                      # 切片
            pred = normPRED(pred)                                                                   # 归一化得到的mask,pred是torch.tensor类型
        

            # save results to test_results folder
            if not os.path.exists(prediction_dir):
                os.makedirs(prediction_dir, exist_ok=True)
            save_output(img_name_list[i_test],pred,img_name_list[i_test],prediction_dir)                                  # 保存mask图到相应目录
            del d1,d2,d3,d4,d5,d6,d7
            input()
        print (str(len(img_name_list))+"个文件已处理")
    main(imagelist)


if __name__ == "__main__":
    MAIN(['C:\\Users\\kilok\\Desktop\\2021-02-02_15.08.54.png','C:\\Users\\kilok\\Desktop\\absfbsxt.jpg'])
