# -*- coding: utf-8 -*-

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys

extensao_coleta = '/home/pi/Documents/extensions/ATF-chrome-plugin/'
extensao_adblock = '/home/pi/Documents/extensions/adblock/'
extensao_adblock_crx = '/home/pi/Documents/extensions/adblock.crx'
arquivo_log = '/home/pi/Documents/log_webdriver'

def main():
    args = sys.argv

    if (len(args) != 4) :
        print('inform url, adblock use and resolution type')
        return

    # first argument is the url to be navigated to
    # second argument is if adblock should be used
    # third argument is the viewport resolution (1 or 2)

    # opções do chrome
    chrome_options = Options()
    chrome_options.add_argument("--kiosk")
    extensoes = extensao_coleta
    if (args[2] == 'True') :
        # add adblock extension
        chrome_options.add_extension(extensao_adblock_crx)
    chrome_options.add_argument('--load-extension={}'.format(extensoes))
    driver = webdriver.Chrome(options = chrome_options)

    # resolução da tela (https://gs.statcounter.com/screen-resolution-stats/desktop/worldwide)
    res1 = [1920, 1080]
    res2 = [1366, 768]
    if (args[3] == '1') :
        driver.set_window_size(res1[0], res1[1], driver.window_handles[0])
    elif (args[3] == '2') :
        driver.set_window_size(res2[0], res2[1], driver.window_handles[0])

    if (args[2] == 'True'): # adblock use
        window = driver.current_window_handle
        for w in driver.window_handles:
            if w != window:
                driver.switch_to.window(w)

    driver.get(args[1])

    with open(arquivo_log, 'a') as file :
        file.write("navigation WEBDRIVER -> test begun successfully")

    time.sleep(18)

    driver.quit()


if __name__ == "__main__":
    main()

