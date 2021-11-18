# 2021-fall-cs160-team-wanda
## Selenium Test Automation
### Downloading & Configuring the Driver
1. Go to Chrome, click Settings > Help > About Google Chrome to check what version your Chrome browser is at.
2. Download the chromedriver that matches the version of your browser: https://chromedriver.chromium.org/downloads <br>
3. Make sure you have selenium installed: https://www.selenium.dev/documentation/getting_started/installing_selenium_libraries/ ( in command line: ```pip install selenium``` <br>
4. Add the driver to your system path
If you have a Mac, you can add the driver to your system by opening Terminal, then typing ```sudo nano /etc/paths```. Type in the path to the folder that contains the webdriver.<br>
### Running the Test
1. Open the project folder and navigate to 2021-fall-cs160-team-wanda/tutor4points. Run the command
```python manage.py test```<br>
2. You should see the driver being activated, the chrome window opening, and buttons being pressed automatically. The test results will be shown after the script is ran<br>

