# -*- coding: utf-8 -*-

import random
import os
import pandas as pd


extensao_coleta = '/home/pi/wptagent-automation/extensions/ATF-chrome-plugin/'
arquivo_controle_mudanca = '/home/pi/wptagent-automation/mac_change'
arquivo_mac = '/home/pi/wptagent-automation/mac'
arquivo_porta_node = '/home/pi/wptagent-automation/collection_server_node_port'
arquivo_url_servidor = '/home/pi/wptagent-automation/collection_server_url'
navigation_list = '/home/pi/wptagent-automation/navigation_list.csv'
navigation_sample_list = '/home/pi/wptagent-automation/navigation_sample_list'


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


def writeToList(domain_list) :
    with open(navigation_sample_list, 'w') as f :
        for i in range(0, len(domain_list)) :
            if i == 0:
                f.write(domain_list[i])
            else:
                f.write('\n{}'.format(domain_list[i]))


def readFromList() :
    with open(navigation_sample_list, 'r') as f :
        lines = f.readlines()
        lines = [line.rstrip() for line in lines]
        return lines


def chooseAtRandom(domain_list) :
    index = random.randint(0, len(domain_list)-1)
    domain = domain_list[index]
    domain_list.remove(domain)
    return domain, domain_list


def main():
    foi_modificado = os.path.exists(arquivo_controle_mudanca)

    # controle para saber se o mac já foi substituído na extensão
    if (not foi_modificado) :
        modifica_extensao()
        with open(arquivo_controle_mudanca, 'w') as f:
            f.write('ok!')

    # choose domain to perform experiment
    if os.path.isfile(navigation_sample_list):
        domain_list = readFromList()
    else:
        domain_list = []

    if (len(domain_list) == 0) :
        # reset navigation list
        df = pd.read_csv(navigation_list)
        df.columns = ['rank', 'domain', 'monthly traffic', 'pages per visit', 'time on site']
        domain_list = df['domain'].tolist()
        writeToList(domain_list)

    domain, domain_list = chooseAtRandom(domain_list)

    writeToList(domain_list)

    print('http://www.{}'.format(domain))


if __name__ == "__main__":
    main()

