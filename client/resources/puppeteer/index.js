const puppeteer = require('puppeteer-extra')

const args = process.argv.slice(2);

if (args.length === 0) {
    console.log('Please provide a URL');
    return;
}

(async () => {
    const extensao_coleta = '/app/resources/extensions/ATF-chrome-plugin/'
    let timeoutDuration = 18000; // Timeout duration in milliseconds

    const browser = await puppeteer.launch({
        headless: false,
        args: [
            `--start-maximized`,
            `--disable-extensions-except=${extensao_coleta}`,
            `--load-extension=${extensao_coleta}`,
            '--user-data-dir=/data/chrome',
            '--profile-directory=data_gathering_agent',
            '--disable-dev-shm-usage',
            '--no-sandbox',
            '--verbose',
        ],
        ignoreDefaultArgs: ["--disable-extension", "--enable-automation"],
        executablePath: '/usr/bin/chromium',
    });

    const page = await browser.newPage();
    await page.setViewport({ width: 1920, height: 1080 });

    let logFound = false;

    let resultLog = '';

    page.on('console', (msg) => {
        if (msg.text().length > 0) {
            if (msg.text.includes('Version:')) {
                resultLog = msg.text();
                logFound = true;
            }
        }
    });

    await page.goto(args[0]);

    const waitForLog = async () => {
        if (logFound) {
            await page.close();
            await browser.close();
            console.log(resultLog);
        }

        if (timeoutDuration <= 0) {
            await page.close();
            await browser.close();
            console.log(resultLog);
        }

        setTimeout(async () => {
            timeoutDuration -= 100; // Reduce the timeout duration by 100 ms
            waitForLog();
        }, 100); // Check again after 100 ms
    };

    waitForLog();
})()
