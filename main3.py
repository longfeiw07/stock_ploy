# -*- coding: utf-8 -*-
# from utils.reptile import Reptile
from utils.reptile import Reptile
import argparse
from utils.network import NeuralNetworks
def main():
    parser = argparse.ArgumentParser(description='读取CSV文件')
    parser.add_argument('-s', dest='start',  help='开始日期', default='2019-06-12')
    parser.add_argument('-e', dest='end',  help='结束日期', default='2019-06-25')
    parser.add_argument('-i', dest='isappend',  help='是否追加', default='no')
    args = parser.parse_args()
    if Reptile.is_valid(args.start, args.end):
        rep = Reptile(args.start, args.end, args.isappend)
        rep.StartReptile()

if __name__ == "__main__":
    # main()
        network = NeuralNetworks()
        network.NeuralNetwork()