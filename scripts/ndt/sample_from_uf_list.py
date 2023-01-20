# -*- coding: utf-8 -*-

import random

lista_ufs = '/home/pi/Documents/lista_ufs'

def readFromUFs() :
    with open(lista_ufs, 'r') as f :
        lines = f.readlines()
        lines = [line.rstrip() for line in lines]
        return lines

def chooseAtRandom(ufs) :
    index = random.randint(0, len(ufs)-1)
    uf = ufs[index]
    return uf

def main():
    ufs = readFromUFs()
    uf = chooseAtRandom(ufs)
    print(uf)

if __name__ == "__main__":
    main()

