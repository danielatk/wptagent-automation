# -*- coding: utf-8 -*-

import os


extensao_coleta = '/home/pi/wptagent-automation/extensions/ATF-chrome-plugin/'
arquivo_status = '/home/pi/wptagent-automation/status'
arquivo_chrome = '/home/pi/wptagent/internal/chrome_desktop.py'
arquivo_webpagetest = '/home/pi/wptagent/internal/webpagetest.py'


def toggle_adblock(adblock_usado) :
    f = os.path.join(extensao_coleta,'atfindex.js')
    if os.path.isfile(f):
        with open(f, 'rb') as file :
            filedata = file.read()

            if adblock_usado == 'False':
                filedata = filedata.replace(b'stats.adblock = true;', b'stats.adblock = false;')
            else :
                filedata = filedata.replace(b'stats.adblock = false;', b'stats.adblock = true;')

        with open(f, 'wb') as file:
            file.write(filedata)


def toggle_puppeteer(puppeteer_usado) :
    f = os.path.join(extensao_coleta,'atfindex.js')
    if os.path.isfile(f):
        with open(f, 'rb') as file :
            filedata = file.read()

            if puppeteer_usado :
                filedata = filedata.replace(b'stats.puppeteer = false;', b'stats.puppeteer = true;')
            else :
                filedata = filedata.replace(b'stats.puppeteer = true;', b'stats.puppeteer = false;')

        with open(f, 'wb') as file:
            file.write(filedata)


def toggle_resolution(resolution_type) :
    f = os.path.join(extensao_coleta,'atfindex.js')
    if os.path.isfile(f):
        with open(f, 'rb') as file :
            filedata = file.read()

            if resolution_type == '1' :
                filedata = filedata.replace(b'stats.resolution_type = 2;', b'stats.resolution_type = 1;')
            elif resolution_type == '2' :
                filedata = filedata.replace(b'stats.resolution_type = 1;', b'stats.resolution_type = 2;')

        with open(f, 'wb') as file:
            file.write(filedata)


def modifica_chrome(use_adblock) :
    with open(arquivo_chrome, 'rb') as file :
        filedata = file.read()

        if (use_adblock == 'True') :
            # add adblock extension
            filedata = filedata.replace(b'#\'--load-extension', b'\'--load-extension')
        else :
            # remove adblock extension
            filedata = filedata.replace(b'#\'--load-extension', b'\'--load-extension')
            filedata = filedata.replace(b'\'--load-extension', b'#\'--load-extension')

    with open(arquivo_chrome, 'wb') as file:
        file.write(filedata)


def modifica_webpagetest(resolution_type) :
    # resolução da tela (https://gs.statcounter.com/screen-resolution-stats/desktop/worldwide)
    res1 = [1920, 1080]
    res2 = [1366, 768]

    width_string1 = 'task[\'width\'] = {}'.format(res1[0])
    height_string1 = 'task[\'height\'] = {}'.format(res1[1])
    width_string2 = 'task[\'width\'] = {}'.format(res2[0])
    height_string2 = 'task[\'height\'] = {}'.format(res2[1])

    with open(arquivo_webpagetest, 'rb') as file :
        filedata = file.read()

        if (resolution_type == '1') :
            filedata = filedata.replace(bytes(width_string2,'UTF-8'), bytes(width_string1, 'UTF-8'))
            filedata = filedata.replace(bytes(height_string2,'UTF-8'), bytes(height_string1, 'UTF-8'))
        elif (resolution_type == '2') :
            filedata = filedata.replace(bytes(width_string1,'UTF-8'), bytes(width_string2, 'UTF-8'))
            filedata = filedata.replace(bytes(height_string1,'UTF-8'), bytes(height_string2, 'UTF-8'))

    with open(arquivo_webpagetest, 'wb') as file:
        file.write(filedata)


def main():

    with open(arquivo_status, 'r') as file:
        lines = file.readlines()

        content = lines[0].strip().split()

        if content[0] == 'puppeteer' or content[0] == 'webdriver':
            toggle_puppeteer(content[0] == 'puppeteer')
            toggle_adblock(content[1])
            toggle_resolution(content[2])

        if content[0] == 'wpt':
            modifica_chrome(content[2])
            modifica_webpagetest(content[3])


if __name__ == "__main__":
    main()

