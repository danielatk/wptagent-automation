# -*- coding: utf-8 -*-

import os


chrome_desktop = '/home/pi/wptagent/internal/chrome_desktop.py'
webpagetest = '/home/pi/wptagent/internal/webpagetest.py'


def modifica_chrome_desktop() :
    with open(chrome_desktop, 'r') as file :
        lines = file.readlines()

    hasChecked = False

    with open(chrome_desktop, 'w') as file:
        for line in lines:
            strippedLine = line.strip('\n')
            if strippedLine == "]" and hasChecked == False:
                file.write("    #'--load-extension=/home/pi/wptagent-automation/extensions/adblock'\n")
                file.write(line)
                hasChecked = True
            else:
                file.write(line)


def modifica_webpagetest() :
    with open(webpagetest, 'r') as file :
        lines = file.readlines()

    with open(webpagetest, 'w') as file:
        for line in lines:
            strippedLine = line.strip('\n')
            if "task['width'] = job['width']" in strippedLine:
                file.write(line.replace("task['width'] = job['width']", "task['width'] = 1366"))
            elif "task['height'] = job['height']" in strippedLine:
                file.write(line.replace("task['height'] = job['height']", "task['height'] = 768"))
            else:
                file.write(line)


def main():
    modifica_chrome_desktop()
    modifica_webpagetest()


if __name__ == "__main__":
    main()

