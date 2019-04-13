# -*- coding: utf-8 -*-
from utils.reptile import Reptile
def main():
    rep = Reptile()
    datas = rep.writeCSV()
    print(datas)

if __name__ == "__main__":
    main()