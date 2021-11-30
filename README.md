# 2021-fall-cs160-team-wanda

## Downloading Project Dependencies
1. Download python from https://www.python.org/downloads/. If you are a Mac user, it is likely that you already have python installed.
2. The best way to install other project dependencies is through pip. Instructions to install pip can be found here https://pip.pypa.io/en/stable/installation/
3. Install Pillow using ```pip install Pillow```
4. Install Crispy Forms using ```pip install django-crispy-forms```

## Cloning the Project
1. Using Terminal to navigate to the folder where you would like the project to be stored.
2. Copy the URL from the GitHub Repository
3. Clone the project by running the following command in Terminal: ```git clone <url>```

## Running the Project
1. Navigate into the tutor4points folder and run ```python3 maange.py migrate```
2. Run the pythong project setup script ```python3 setup_project.py```
3. Type ```python3 manage.py runserver```
4. Copy the address into your browser (usually it’s http://127.0.0.1:8000/)

## Selenium Test Automation
### Downloading & Configuring the Driver
1. Go to Chrome, click Settings > Help > About Google Chrome to check what version your Chrome browser is at.
![](media/aboutChromeMenu.png)
![](media/viewChromeVer.png)
3. Download the chromedriver that matches the version of your browser: https://chromedriver.chromium.org/downloads <br>
4. Make sure you have selenium installed: https://www.selenium.dev/documentation/getting_started/installing_selenium_libraries/ ( in command line: ```pip install selenium``` <br>
5. Add the driver to your system path
If you have a Mac, you can add the driver to your system by opening Terminal, then typing ```sudo nano /etc/paths```. Type in the path to the folder that contains the webdriver.<br>
### Running the Test
1. Open the project folder and navigate to 2021-fall-cs160-team-wanda/tutor4points. Run the command
```python manage.py test```<br>
2. You should see the driver being activated, the chrome window opening, and buttons being pressed automatically. The test results will be shown after the script is ran<br>
![](media/testResult.png)

