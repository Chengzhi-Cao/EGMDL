import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn import Softmax

class Self_Attn(nn.Module):
    """ Self attention Layer"""
    def __init__(self,in_dim,activation):
        super(Self_Attn,self).__init__()
        self.chanel_in = in_dim
        self.activation = activation
 
        self.query_conv = nn.Conv2d(in_channels = in_dim , out_channels = in_dim//8 , kernel_size= 1)
        self.key_conv = nn.Conv2d(in_channels = in_dim , out_channels = in_dim//8 , kernel_size= 1)
        self.value_conv = nn.Conv2d(in_channels = in_dim , out_channels = in_dim , kernel_size= 1)
        self.gamma = nn.Parameter(torch.zeros(1))
 
        self.softmax  = nn.Softmax(dim=-1)
 
    def forward(self,x):
        """
        inputs :
            x : input feature maps (B X C X W X H)
        returns :
            out : self attention value + input feature
            attention: B X N X N (N is Width*Height)
        """
        
        
        m_batchsize,C,width ,height = x.size()
        proj_query = self.query_conv(x).view(m_batchsize, -1, width*height).permute(0,2,1) # B X CX(N)
        proj_key = self.key_conv(x).view(m_batchsize, -1, width*height) # B X C x (*W*H)
        energy = torch.bmm(proj_query, proj_key) # transpose check
        attention = self.softmax(energy) # BX (N) X (N)
        proj_value = self.value_conv(x).view(m_batchsize, -1, width*height) # B X C X N
 
        out = torch.bmm(proj_value,attention.permute(0, 2, 1) )
        out = out.view(m_batchsize, C, width, height)
 
        out = self.gamma * out + x
 
        return out,attention


#!usr/bin/env python
# -*- coding:utf-8 _*-
# @author: ycy
# @contact: asuradayuci@gmail.com
# @time: 2019/9/7 下午2:53
import torch
from torch import nn
import torch.nn.functional as F
#!usr/bin/env python
# -*- coding:utf-8 _*-
# @author: ycy
# @contact: asuradayuci@gmail.com
# @time: 2019/9/7 下午2:53
import torch
from torch import nn


def weights_init_kaiming(m):
    classname = m.__class__.__name__
    if classname.find('Linear') != -1:
        nn.init.kaiming_uniform_(m.weight, mode='fan_out')
        nn.init.constant_(m.bias, 0.0)
    elif classname.find('Conv') != -1:
        nn.init.kaiming_normal_(m.weight, a=0, mode='fan_in')
        if m.bias is not None:
            nn.init.constant_(m.bias, 0.0)
    elif classname.find('BatchNorm') != -1:
        if m.affine:
            nn.init.constant_(m.weight, 1.0)
            nn.init.constant_(m.bias, 0.0)


def weights_init_classifier(m):
    classname = m.__class__.__name__
    if classname.find('Linear') != -1:
        nn.init.normal_(m.weight, std=0.001)
        # if m.bias:
        #     nn.init.constant_(m.bias, 0.0)
        nn.init.constant_(m.bias, 0.0)


class Siamese(nn.Module):

    def __init__(self, input_num, output_num, class_num):
        super(Siamese, self).__init__()

        self.input_num = input_num
        self.output_num = output_num
        self.class_num = class_num
        self.feat_num = input_num
        # linear_Q
        self.featQ = nn.Linear(self.input_num, self.output_num)
        self.featQ_bn = nn.BatchNorm1d(self.output_num)
        self.featQ.apply(weights_init_kaiming)
        self.featQ_bn.apply(weights_init_kaiming)

        # linear_K
        self.featK = nn.Linear(self.input_num, self.output_num)
        self.featK_bn = nn.BatchNorm1d(self.output_num)
        self.featK.apply(weights_init_kaiming)
        self.featK_bn.apply(weights_init_kaiming)

        # linear_V
        self.featV = nn.Linear(self.input_num, self.output_num)
        self.featV_bn = nn.BatchNorm1d(self.output_num)
        self.featV.apply(weights_init_kaiming)
        self.featV_bn.apply(weights_init_kaiming)

        # Softmax
        self.softmax = nn.Softmax(dim=-1)

        # BCE classifier
        self.classifierBN = nn.BatchNorm1d(self.feat_num)
        self.classifierlinear = nn.Linear(self.feat_num, self.class_num)
        self.classifierBN.apply(weights_init_kaiming)
        self.classifierlinear.apply(weights_init_classifier)


    def self_attention(self, input):
        input = torch.zeros(8,3,128,64)
        size = input.size()
        print('input_size=',size)
        batch = size[0]
        len = size[1]

        Qs = input.view(batch * len, -1)
        # print('Qs=',Qs.shape)
        Qs = self.featQ(Qs)
        Qs = self.featQ_bn(Qs)
        Qs = Qs / Qs.norm(2, 1).unsqueeze(1).expand_as(Qs)
        Qs = Qs.contiguous().view(batch, len, -1)

        K = input.view(batch*len, -1)
        K = self.featK(K)
        K = self.featK_bn(K)
        K = K / K.norm(2, 1).unsqueeze(1).expand_as(K)
        K = K.view(batch, len, -1)

        weights = torch.matmul(Qs, K.transpose(-1, -2))
        weights = self.softmax(weights)

        V = input.view(batch, len, -1)
        pool_input = torch.matmul(weights, V)

        # pool_input = pool_input.sum(1)
        # pool_input = pool_input / pool_input.norm(2, 1).unsqueeze(1).expand_as(pool_input)
        # pool_input = pool_input.squeeze(1)
        pool_input = pool_input.view(size)
        print('pool_input=',pool_input.shape)
        return pool_input

    def forward(self, x):
        
        xsize = x.size()
        sample_num = xsize[0]

        if sample_num % 2 != 0:
            raise RuntimeError("the batch size should be even number!")

        seq_len = x.size()[1]  # 8
        x = x.view(int(sample_num/2), 2, seq_len, -1)

        probe_x = x[:, 0, :, :]
        probe_x = probe_x.contiguous()
        gallery_x = x[:, 1, :, :]
        gallery_x = gallery_x.contiguous()

        pooled_probe = self.self_attention(probe_x)
        pooled_gallery = self.self_attention(gallery_x)

        siamese_out = torch.cat((pooled_probe, pooled_gallery))
        probesize = pooled_probe.size()
        gallerysize = pooled_gallery.size()
        probe_batch = probesize[0]
        gallery_batch = gallerysize[0]

        pooled_gallery = pooled_gallery.unsqueeze(0)
        pooled_probe = pooled_probe.unsqueeze(1)

        diff = pooled_probe - pooled_gallery
        diff = torch.pow(diff, 2)
        diff = diff.view(probe_batch * gallery_batch, -1).contiguous()
        diff = self.classifierBN(diff)
        cls_encode = self.classifierlinear(diff)
        cls_encode = cls_encode.view(probe_batch, gallery_batch, -1)

        return cls_encode, siamese_out



my_model = Siamese(input_num=8192,output_num=512,class_num=2)

_input = torch.zeros(8,3,128,64)
_output,_ = my_model(_input)
print('_output=',_output.shape)