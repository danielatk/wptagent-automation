# NAVIGATION FILE
import time
import sys
import subprocess
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException, WebDriverException

EXTENSAO_COLETA = '/app/resources/extensions/ATF-chrome-plugin/'
EXTENSAO_ADBLOCK_CRX = '/app/resources/extensions/adblock.crx'

def setup_chrome(use_adblock, resolution_type):
    # opções do chrome
    chrome_options = Options()
    extensoes = EXTENSAO_COLETA
    if use_adblock:
        # add adblock extension
        chrome_options.add_extension(EXTENSAO_ADBLOCK_CRX)
    chrome_options.add_argument(f'--load-extension={extensoes}')
    # browser log
    d = DesiredCapabilities.CHROME
    d['goog:loggingPrefs'] = { 'browser':'ALL' }
    driver = webdriver.Chrome(desired_capabilities=d, options = chrome_options)
    driver.execute_cdp_cmd("Network.setCacheDisabled", {"cacheDisabled":True})
    # resolução da tela (https://gs.statcounter.com/screen-resolution-stats/desktop/worldwide)
    resolution = {
        '1': [1920, 1080],
        '2': [1366, 768],
    }
    driver.set_window_size(resolution[resolution_type][0], resolution[resolution_type][1], driver.window_handles[0])
    if use_adblock: # adblock use
        window = driver.current_window_handle
        for w in driver.window_handles:
            if w != window:
                driver.switch_to.window(w)
    return driver

def navigation(url, use_adblock, resolution_type):
    driver = setup_chrome(use_adblock, resolution_type)
    driver.get(url)
    result = "navigation WEBDRIVER -> test begun successfully\nnavigation WEBDRIVER -> browser log:"
    for entry in driver.get_log('browser'):
        result += str(entry) + '\n\n'    
    time.sleep(18)
    driver.quit()
    return result


def reproduction(url, use_adblock, resolution_type):
    driver = setup_chrome(use_adblock, resolution_type)
    driver.get(url)

    beginning = datetime.timestamp(datetime.now())

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
    time.sleep(1)
    driver.quit()
    return json_stats_for_nerds
