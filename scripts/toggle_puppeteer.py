# -*- coding: utf-8 -*-

import os
import sys


extensao_coleta = '/home/pi/wptagent-automation/extensions/ATF-chrome-plugin/'


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


def main():
    args = sys.argv

    if (len(args) != 2) :
        print('inform if puppeteer is being used')
        return

    toggle_puppeteer(args[1])


if __name__ == "__main__":
    main()
