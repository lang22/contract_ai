#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time       : 2019/2/28 14:57
@Author     : jzs
@File       : train.py
@Software   : PyCharm
@Description: ......
"""
import torch

from ..nn_model.SimplySimilarityNet import SimplySimilarityNet

if __name__ == '__main__':
    m = SimplySimilarityNet(300, 150)
    m.save("../data/SimilarityNet_paras.pth")
    model = torch.load("../data/SimilarityNet_paras.pth")
    model.eval()
    print(model)
