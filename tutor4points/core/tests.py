from django.test.testcases import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from django.contrib.auth import get_user_model
from .models import School
import time
class CashOutFormTest (LiveServerTestCase):

    def setUp(self):
        #add school
        sjsu = School.objects.create(name="San Jose State University")

        #create test user 1 - tutee
        get_user_model().objects.create_user (first_name = "tutee", last_name="student", email = "user1@gmail.com", username = "tuteestudent", password = "Testing", is_tutor = True, school = sjsu, is_active = True)
        #create test user 2 - tutor
        get_user_model().objects.create_user (first_name = "tutor", last_name="student", email = "user2@gmail.com", username = "tutorstudent", password = "Testing", is_tutor = True, school = sjsu, is_active = True)
        
        self.driver = webdriver.Chrome()
        
    def tearDown(self):
        return self.driver.quit() 

    #test inputting negative number into field
    def test_negative_number (self):
        self.logintutee()
        self.driver.find_element_by_id('points-link').send_keys(Keys.RETURN) #go to points page
        # time.sleep(100)
        self.transfer_points("-10", "Tutor Student", delay=2) #try to transfer -10 points to tutor student
        assert 'Please enter a positive value' in self.driver.page_source #make sure error message shows up

    #test inputting number of points larger than current points balance
    def test_number_larger_than_balance (self):
        self.logintutee()
        self.driver.find_element_by_id('points-link').send_keys(Keys.RETURN) #go to points page
        self.transfer_points("100", "Tutor Student", delay=3)
        assert 'Please enter a value less than or equal to your current points balance' in self.driver.page_source #make sure error message shows up

    #test transferring number of points lesser than current points balance
    def test_transfer_points (self):
        self.logintutor()
        self.driver.find_element_by_id('points-link').send_keys(Keys.RETURN) #go to points page
        self.purchase_points("100", delay=3) #set tutor points balance to 100
        self.logout()

        self.logintutee()
        self.driver.find_element_by_id('points-link').send_keys(Keys.RETURN) #go to points page
        self.purchase_points("150", delay=3) #set tutee balance to 150 

        #transfer 150 points from tutor to tutee
        select = Select(self.driver.find_element_by_id('id_tutors'))
        self.transfer_points ("150", "Tutor Student", delay=3)
        tutee_total_pts = self.driver.find_element_by_id('total-points').text.replace ("\n", " ") #get tutee total points balance
        assert tutee_total_pts == "0 points"
        self.logout()

        self.logintutor()
        self.driver.find_element_by_id('points-link').send_keys(Keys.RETURN)
        time.sleep (3)
        tutor_total_pts = self.driver.find_element_by_id('total-points').text.replace ("\n", " ") #get tutor total points balance
        assert tutor_total_pts == "250 points"

    #helper functions
    #can only be run on homepage
    def logintutee(self, delay=0):
        self.driver.get (self.live_server_url + "/login")
        username_field = self.driver.find_element_by_id('id_username')
        password_field = self.driver.find_element_by_id('id_password')
        login_btn = self.driver.find_element_by_id ('login-btn')

        username_field.clear()
        username_field.send_keys('tuteestudent')
        password_field.clear()
        password_field.send_keys('Testing')
        login_btn.send_keys (Keys.RETURN)
        time.sleep (delay)

    #can only be run on homepage
    def logintutor(self, delay=0):
        self.driver.get (self.live_server_url + "/login")
        username_field = self.driver.find_element_by_id('id_username')
        password_field = self.driver.find_element_by_id('id_password')
        login_btn = self.driver.find_element_by_id ('login-btn')

        username_field.clear()
        username_field.send_keys('tutorstudent')
        password_field.clear()
        password_field.send_keys('Testing')
        login_btn.send_keys (Keys.RETURN)
        time.sleep (delay)

    #user must be logged in
    def logout (self):
        self.driver.find_element_by_id('logout-btn').send_keys (Keys.RETURN)

    #can only be run on "points" page
    def purchase_points (self, amount, delay=0):
        purchased_pts_field = self.driver.find_element_by_id('id_purchased_points')
        purchased_pts_field.clear()
        purchased_pts_field.send_keys (amount)
        self.driver.find_element_by_id('purchase-btn').send_keys(Keys.RETURN)
        time.sleep (delay)

    #can only be run on "points" page
    def transfer_points (self, amount, tutor_name, delay=0):
        select = Select(self.driver.find_element_by_id('id_tutors'))
        select.select_by_visible_text (tutor_name)
        transfer_pts_field = self.driver.find_element_by_id('id_amount_to_transfer')
        transfer_pts_field.clear()
        transfer_pts_field.send_keys(amount)
        self.driver.find_element_by_id('transfer-btn').send_keys(Keys.RETURN)
        time.sleep (delay)