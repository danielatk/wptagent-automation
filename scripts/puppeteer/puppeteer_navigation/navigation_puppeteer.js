const puppeteer = require('puppeteer-extra');

const args = process.argv.slice(2);

if (args.length === 0) {
    console.log('Please provide a URL');
    return;
}

(async () => {
    const extensao_coleta = '/home/pi/wptagent-automation/extensions/ATF-chrome-plugin/';
    const logToWaitFor = 'Data sent to collection server.';
    let timeoutDuration = 60000; // Timeout duration in milliseconds
    let timeoutScroll = 10000; // Scroll timeout duration in milliseconds

    const browser = await puppeteer.launch({
        headless: false,
        args: [
            `--start-maximized`,
            `--disable-extensions-except=${extensao_coleta}`,
            `--load-extension=${extensao_coleta}`,
        ],
        ignoreDefaultArgs: ["--disable-extension", "--enable-automation"],
        executablePath: '/usr/bin/chromium-browser',
    });

    const page = await browser.newPage();
    await page.setViewport({ width: 1920, height: 1080 });

    let logFound = false;

    page.on('console', (msg) => {
        if (msg.text().includes(logToWaitFor)) {
            logFound = true;
        }
    });

    await page.goto(args[0]);

    const waitForLog = async () => {
        if (logFound) {
            await page.close();
            await browser.close();
            return;
        }

        if (timeoutDuration <= 0) {
            await page.close();
            await browser.close();
            return;
        }

        setTimeout(async () => {
            timeoutDuration -= 100; // Reduce the timeout duration by 100 ms
            waitForLog();
        }, 100); // Check again after 100 ms
    };

    async function autoScroll(timeoutScroll){
        await page.evaluate(async (timeoutScroll) => {
            await new Promise((resolve) => {
                var totalHeight = 0;
                var distance = 100;
                var timer = setInterval(() => {
                    var scrollHeight = document.body.scrollHeight;
                    window.scrollBy(0, distance);
                    totalHeight += distance;
                    timeoutScroll -= 100

                    if(totalHeight >= scrollHeight - window.innerHeight || timeoutScroll <= 0){
                        console.log('reached');
                        clearInterval(timer);
                        resolve();
                    }
                }, 100);
            });
        }, timeoutScroll);  // pass maxScrolls to the function
    }

    waitForLog();
    autoScroll(timeoutScroll);
})();