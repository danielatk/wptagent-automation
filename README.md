# wptagent-automation

## Description:

This is the client-side part of a a data collection automation project. This should be deployed at a dedicated machine.

The following tests are currently supported:
* WebPageTest jobs with video reproductions or webpage visits, which are scheduled via the server-side part of this project (https://github.com/danielatk/wptagent-control)
* webpage visits via Chromedriver, with ATF estimation plugin
* webpage visits via puppeteer, with ATF estimation plugin
* NDT tests (with optional traceroute)

For the webpage visits and video reproductions two factors are varied:
* viewport resolution (1920x1080 or  1366x768)
* adblock use

For webpage visits a list of top 100 webpages visited in Brazil is used. For videos a list of 147 videos with 4K option is given. These can be easily customized.

The NDT and traceroute results are sent via SSH and the ATF estimation plugin results are sent via XML to a node server.

## Deployment:

To setup the environment variables and the WebPageTest agent, download the initial setup script with the following command:
`curl https://raw.githubusercontent.com/danielatk/wptagent-automation/main/scripts/first_setup.sh > first_setup.sh`
To run the script execute the following command:
`sh first_setup.sh`

Note that this first setup script sets the WebPageTest agend id as the MAC address of the device. This must correspond with the the value given in the WebPageTest server `locations.ini` file or else the WPT agent will not be able to get jobs from the WPT server. Once this script has been executed, reboot the system. After this download and run the automation setup script:
```
curl https://raw.githubusercontent.com/danielatk/wptagent-automation/main/scripts/automation_setup.sh > automation_setup.sh
sh automation_setup.sh
```

After this the client should be running the automated experiments and receiving the WPT jobs.