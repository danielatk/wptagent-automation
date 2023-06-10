# -*- coding: utf-8 -*-

from datetime import datetime
import subprocess
import re
import time
import sys
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException, WebDriverException

extensao_adblock_crx = '/home/pi/wptagent-automation/extensions/adblock.crx'
arquivo_log = '/home/pi/wptagent-automation/log'
arquivo_mac = '/home/pi/wptagent-automation/mac'
arquivo_url_servidor = '/home/pi/wptagent-automation/collection_server_url'
arquivo_usuario_servidor = '/home/pi/wptagent-automation/collection_server_user'
arquivo_porta_ssh_servidor = '/home/pi/wptagent-automation/collection_server_ssh_port'

def main():
    args = sys.argv

    if (len(args) != 4) :
        print('inform url, adblock use and resolution type')
        return

    # first argument is the url to be reproduced
    # second argument is if adblock should be used
    # third argument is the viewport resolution (1 or 2)

    # opções do chrome
    chrome_options = Options()
    if (args[2] == 'True') :
        # add adblock extension
        chrome_options.add_extension(extensao_adblock_crx)
    
    # browser log
    d = DesiredCapabilities.CHROME
    d['goog:loggingPrefs'] = { 'browser':'ALL' }
    
    driver = webdriver.Chrome(desired_capabilities=d, options = chrome_options)
    driver.execute_cdp_cmd("Network.setCacheDisabled", {"cacheDisabled":True})
    
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

    beginning = datetime.timestamp(datetime.now())

    # with open(arquivo_log, 'a') as file :
    #     file.write("reproduction WEBDRIVER -> test begun successfully")
    #     file.write("reproduction WEBDRIVER -> browser log:")
    #     for entry in driver.get_log('browser'):
    #         file.write(str(entry))
    #         file.write('\n\n')

    while True:
        try:
            video = driver.find_element('id', 'ytd-player')
            break
        except NoSuchElementException:
            pass

    encontrou_botao = True
    try:
        play_btn = driver.find_element('xpath', "//div[@aria-label='Reproduzir (k)']/div[@class='ytp-play-button ytp-button'][text()='Reproduzir (k)']")
    except NoSuchElementException:
        encontrou_botao = not encontrou_botao
        pass
    if encontrou_botao:
        play_btn.click()

    begin_time = time.time()

    # autoplay_btn = driver.find_element('id', 'toggleButton')
    # autoplay_btn.click()

    while True:
        fullscreen = driver.find_elements('class name', 'ytp-fullscreen-button')
        fullscreen_btn = fullscreen[len(fullscreen)-1]
        while True:
            try:
                fullscreen_btn.click()
                break
            except WebDriverException:
                pass
        #if fullscreen_btn.is_displayed() and fullscreen_btn.is_enabled():
            #fullscreen_btn.click()
            #break
        break

    actionChains = ActionChains(driver)
    actionChains.context_click(video).perform()
    context_menu = driver.find_elements('class name', 'ytp-menuitem-content')
    stats_for_nerds = context_menu[len(context_menu)-1]
    stats_for_nerds.click()

    while True:
        stats_panel = driver.find_elements('class name', 'html5-video-info-panel-content')
        if len(stats_panel) > 0:
            break
    stats_panel = stats_panel[0]

    is_first_JSON = True

    # TODO(danielatk): write JSON with dict!
    json_stats_for_nerds = '{"st":'
    json_stats_for_nerds += str(beginning)
    # indicates file has SFN data
    json_stats_for_nerds += ',"SFN":1'
    json_stats_for_nerds += ',"vals":['

    while True:
        encontrou_video_res = True
        try:
            video_res = stats_panel.find_element('xpath', ".//span[contains(text(), '@')]")
        except NoSuchElementException:
            encontrou_video_res = not encontrou_video_res
        pass
        encontrou_connection_speed = True
        try:
            connection_speed = stats_panel.find_element('xpath', ".//span[contains(text(), 'Kbps')]")
        except NoSuchElementException:
            encontrou_connection_speed = not encontrou_connection_speed
        pass
        encontrou_viewport = True
        try:
            viewport_frames = stats_panel.find_element('xpath', ".//span[contains(text(), 'dropped')]")
        except NoSuchElementException:
            encontrou_viewport = not encontrou_viewport
        pass
        encontrou_codecs = True
        try:
            codecs = stats_panel.find_element('xpath', ".//span[contains(text(), ') /')]")
        except NoSuchElementException:
            encontrou_codecs = not encontrou_codecs
        pass
        encontrou_buffer = True
        try:
            buffer = stats_panel.find_element('xpath', ".//span[contains(text(), ' s')]")
        except NoSuchElementException:
            encontrou_buffer = not encontrou_buffer
        pass
        encontrou_network_activity = True
        try:
            network_activity = stats_panel.find_element('xpath', ".//span[contains(text(), ' KB')]")
        except NoSuchElementException:
            encontrou_network_activity = not encontrou_network_activity
        pass
        if is_first_JSON == False:
            json_stats_for_nerds += ','
        else:
            is_first_JSON = not is_first_JSON #is_first_JSON = True
        json_stats_for_nerds += '{"RES":'
        json_stats_for_nerds += '"' 
        if encontrou_video_res == True:
            json_stats_for_nerds += str(video_res.text)
        else:
            json_stats_for_nerds += 'NaN'
        json_stats_for_nerds += '"'
        json_stats_for_nerds += ',"CSP":'
        json_stats_for_nerds += '"'
        if encontrou_connection_speed == True:
            json_stats_for_nerds += str(connection_speed.text)
        else:
            json_stats_for_nerds += 'NaN'
        json_stats_for_nerds += '"'
        json_stats_for_nerds += ',"VFR":'
        json_stats_for_nerds += '"'
        if encontrou_viewport == True:
            json_stats_for_nerds += str(viewport_frames.text)
        else:
            json_stats_for_nerds += 'NaN'
        json_stats_for_nerds += '"'
        json_stats_for_nerds += ',"COD":'
        json_stats_for_nerds += '"'
        if encontrou_codecs == True:
            json_stats_for_nerds += str(codecs.text)
        else:
            json_stats_for_nerds += 'NaN'
        json_stats_for_nerds += '"'
        json_stats_for_nerds += ',"BUF":'
        json_stats_for_nerds += '"'
        if encontrou_buffer == True:
            json_stats_for_nerds += str(buffer.text)
        else:
            json_stats_for_nerds += 'NaN'
        json_stats_for_nerds += '"'
        json_stats_for_nerds += ',"NET":'
        json_stats_for_nerds += '"'
        if encontrou_network_activity == True:
            json_stats_for_nerds += str(network_activity.text)
        else:
            json_stats_for_nerds += 'NaN'
        json_stats_for_nerds += '"'
        timestamp = datetime.timestamp(datetime.now())
        json_stats_for_nerds += ',"ts":'
        json_stats_for_nerds += str(timestamp)
        json_stats_for_nerds += '}'
        # wait half a second between each sample
        time.sleep(0.5)

        #attrs = driver.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', progress_bar)
        #print(attrs)
        '''progress_bar = driver.find_elements('class name', 'ytp-progress-bar')
        progress_bar = progress_bar[0]
        progress = progress_bar.get_attribute('aria-valuenow')
        print(progress)
        if int(progress) >= 60:
            break'''

        if time.time() - begin_time >= 70:
            break

        indicator_end = driver.find_elements('class name', 'ytp-videowall-still-info-content')
        if len(indicator_end) > 0:
            break

    ending = datetime.timestamp(datetime.now())

    json_stats_for_nerds += '],"et":'
    json_stats_for_nerds += str(ending)
    json_stats_for_nerds += '}'

    with open(arquivo_mac, 'r') as f:
        mac = f.read().rstrip()

    index = args[1].find('watch?v=')
    video_id = args[1][index+8:]

    filename = '/home/pi/wptagent-automation/sfn_data/{}_{}_{}_webdriver_sfn.json'.format(video_id, mac, beginning)

    with open(filename, 'w') as outfile:
        outfile.write(json_stats_for_nerds)
        outfile.close

    time.sleep(1)

    driver.quit()

    with open(arquivo_url_servidor, 'r') as f:
        url_servidor = f.read().rstrip()
    with open(arquivo_usuario_servidor, 'r') as f:
        usuario_servidor = f.read().rstrip()
    with open(arquivo_porta_ssh_servidor, 'r') as f:
        porta_ssh_servidor = f.read().rstrip()

    command = 'scp -o StrictHostKeyChecking=no -P {} /home/pi/wptagent-automation/sfn_data/{}_{}_{}_webdriver_sfn.json {}@{}:~/wptagent-control/other_data'.format(porta_ssh_servidor, video_id, mac, beginning, usuario_servidor, url_servidor)
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output1, error1 = process.communicate()


if __name__ == "__main__":
    main()
