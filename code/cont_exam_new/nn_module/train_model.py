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

from .SimplySimilarityNet import SimplySimilarityNet

if __name__ == '__main__':
    m = SimplySimilarityNet(300, 750)

    m.save("../data/SimilarityNet_no_clause.pth")
    model = torch.load("../data/SimilarityNet_no_clause.pth")
    model.eval()
    print(model)
