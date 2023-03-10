# -*- coding: utf-8 -*-

import random
import os
import pandas as pd
import sys


extensao_coleta = '/home/pi/wptagent-automation/extensions/ATF-chrome-plugin/'
arquivo_controle_mudanca = '/home/pi/wptagent-automation/mac_change'
arquivo_mac = '/home/pi/wptagent-automation/mac'
arquivo_porta_node = '/home/pi/wptagent-automation/collection_server_node_port'
arquivo_url_servidor = '/home/pi/wptagent-automation/collection_server_url'
alexa_top_100_brasil = '/home/pi/wptagent-automation/top_100_brasil.csv'
alexa_top_100 = '/home/pi/wptagent-automation/top-100'


def modifica_extensao() :
    with open(arquivo_mac, 'r') as f:
        mac = f.read().rstrip()
    with open(arquivo_porta_node, 'r') as f:
        porta_node = f.read().rstrip()
    with open(arquivo_url_servidor, 'r') as f:
        url_servidor = f.read().rstrip()

    for filename in os.listdir(extensao_coleta):
        f = os.path.join(extensao_coleta,filename)
        if os.path.isfile(f):
            with open(f, 'rb') as file :
                filedata = file.read()

                filedata = filedata.replace(b'00:00:00:00:00:00', bytes(mac, 'UTF-8'))
                filedata = filedata.replace(b'0.0.0.0', bytes(url_servidor, 'UTF-8'))
                filedata = filedata.replace(b'65535', bytes(porta_node, 'UTF-8'))

            with open(f, 'wb') as file:
                file.write(filedata)


def toggle_adblock(adblock_usado) :
    f = os.path.join(extensao_coleta,'atfindex.js')
    if os.path.isfile(f):
        with open(f, 'rb') as file :
            filedata = file.read()

            if adblock_usado :
                filedata = filedata.replace(b'stats.adblock = false;', b'stats.adblock = true;')
            else :
                filedata = filedata.replace(b'stats.adblock = true;', b'stats.adblock = false;')

        with open(f, 'wb') as file:
            file.write(filedata)


def toggle_puppeteer(puppeteer_usado) :
    f = os.path.join(extensao_coleta,'atfindex.js')
    if os.path.isfile(f):
        with open(f, 'rb') as file :
            filedata = file.read()

            if puppeteer_usado == 'False' :
                filedata = filedata.replace(b'stats.puppeteer = true;', b'stats.puppeteer = false;')
            else :
                filedata = filedata.replace(b'stats.puppeteer = false;', b'stats.puppeteer = true;')

        with open(f, 'wb') as file:
            file.write(filedata)


def toggle_resolution(resolution_type) :
    f = os.path.join(extensao_coleta,'atfindex.js')
    if os.path.isfile(f):
        with open(f, 'rb') as file :
            filedata = file.read()

            if resolution_type == 1 :
                filedata = filedata.replace(b'stats.resolution_type = 2;', b'stats.resolution_type = 1;')
            elif resolution_type == 2 :
                filedata = filedata.replace(b'stats.resolution_type = 1;', b'stats.resolution_type = 2;')

        with open(f, 'wb') as file:
            file.write(filedata)


def writeToTop100(domain_list) :
    with open(alexa_top_100, 'w') as f :
        for i in range(0, len(domain_list)) :
            if i == 0:
                f.write(domain_list[i])
            else:
                f.write('\n{}'.format(domain_list[i]))


def readFromTop100() :
    with open(alexa_top_100, 'r') as f :
        lines = f.readlines()
        lines = [line.rstrip() for line in lines]
        return lines


def chooseAtRandom(domain_list) :
    index = random.randint(0, len(domain_list)-1)
    domain = domain_list[index]
    domain_list.remove(domain)
    return domain, domain_list


def main():
    args = sys.argv

    if (len(args) != 2) :
        print('inform if puppeteer is being used')
        return

    toggle_puppeteer(args[1])

    foi_modificado = os.path.exists(arquivo_controle_mudanca)

    # controle para saber se o mac j?? foi substitu??do na extens??o
    if (not foi_modificado) :
        modifica_extensao()
        with open(arquivo_controle_mudanca, 'w') as f:
            f.write('ok!')

    # uso ou n??o de adblock
    adblock_usado = False
    if random.random() < 0.5 :
        adblock_usado = True

    toggle_adblock(adblock_usado)

    resType = 1
    if random.random() >= 0.5 :
        resType = 2

    toggle_resolution(resType)

    # choose domain to perform experiment
    if os.path.isfile(alexa_top_100):
        domain_list = readFromTop100()
    else:
        domain_list = []

    if (len(domain_list) == 0) :
        # reset top 100 list
        df = pd.read_csv(alexa_top_100_brasil)
        df.columns = ['rank', 'domain', 'monthly traffic', 'pages per visit', 'time on site']
        domain_list = df['domain'].tolist()
        writeToTop100(domain_list)

    domain, domain_list = chooseAtRandom(domain_list)

    writeToTop100(domain_list)

    print('http://www.{} {} {}'.format(domain, adblock_usado, resType))


if __name__ == "__main__":
    main()

