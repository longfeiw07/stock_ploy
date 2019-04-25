# -*- coding: utf-8 -*-
from utils.reptile import Reptile
import argparse
def main():
    parser = argparse.ArgumentParser(description='读取CSV文件')
    parser.add_argument('-s', dest='start',  help='开始日期', default='')
    parser.add_argument('-e', dest='end',  help='结束日期', default='')
    args = parser.parse_args()
    if args.start != '' and args.end != '':
        rep = Reptile(args.start, args.end)
        rep.getAllDatas()

if __name__ == "__main__":
    main()