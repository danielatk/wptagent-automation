const puppeteer = require('puppeteer-extra')

const { DEFAULT_INTERCEPT_RESOLUTION_PRIORITY } = require('puppeteer')
const AdblockerPlugin = require('puppeteer-extra-plugin-adblocker')

const args = process.argv.slice(2);

if (args.length !== 3) {
    console.log('inform url, adblock use and resolution type');
    return;
}

/*
first argument is the url to be navigated to
second argument is if adblock should be used
third argument is the viewport resolution (1 or 2)
*/

(async () => {
    const extensao_coleta = '/home/pi/wptagent-automation/extensions/ATF-chrome-plugin/'
    const extensao_adblock = '/home/pi/wptagent-automation/extensions/adblock/'

    var extensoes = extensao_coleta;
    if(args[1] == 'True') {
        // add adblock extension
        puppeteer.use(
            AdblockerPlugin({
                // Optionally enable Cooperative Mode for several request interceptors
                interceptResolutionPriority: DEFAULT_INTERCEPT_RESOLUTION_PRIORITY
            })
        )
    }
    const browser = await puppeteer.launch(
    {
        headless: false,
        args: [
            `--start-maximized`,
            `--disable-extensions-except=${extensoes}`,
            `--load-extension=${extensoes}`,
        ],
        ignoreDefaultArgs: ["--disable-extension", "--enable-automation"],
        executablePath: '/usr/bin/chromium-browser',
    });
    const page = await browser.newPage();
    if (args[2] == 1) {
        await page.setViewport({
            width: 1920,
            height: 1080
        });
    } else if (args[2] == 2) {
        await page.setViewport({
        width: 1366,
        height: 768
        });
    }
    await page.goto(args[0]);
    await new Promise(r => setTimeout(r, 18000));
    await page.close();
    await browser.close();
})()
