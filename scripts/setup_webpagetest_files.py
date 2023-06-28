# -*- coding: utf-8 -*-

import os


webpagetest = '/home/pi/wptagent/internal/webpagetest.py'


def modifica_webpagetest() :
    with open(webpagetest, 'r') as file :
        lines = file.readlines()

    with open(webpagetest, 'w') as file:
        for line in lines:
            strippedLine = line.strip('\n')
            if "task['width'] = job['width']" in strippedLine:
                file.write(line.replace("task['width'] = job['width']", "task['width'] = 1920"))
            elif "task['height'] = job['height']" in strippedLine:
                file.write(line.replace("task['height'] = job['height']", "task['height'] = 1080"))
            else:
                file.write(line)


def main():
    modifica_webpagetest()


if __name__ == "__main__":
    main()

