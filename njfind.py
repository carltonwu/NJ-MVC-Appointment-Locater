import re
import time
import pathlib

from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import winsound

base_url_link = 'https://telegov.njportal.com/njmvc/AppointmentWizard/'

print()

# Technical names of appointments and web IDs
names_of_appointments = ['Permits/License', 'CDL Permit', 'Real ID', 'Non-Driver ID', 'Knowledge Test', 'License or Non Driver ID Renewal', 'CDL Renewl', 'Out of State Transfer', 'Initial Title or Registration', 'Senior Hours', 'Registration Renewal', 'Duplicate or Replace Title']
types_of_appointments = ['15', '14', '12', '16', '17', '11', '6', '7', '8', '9', '10', '13']

# Print list of appointment names
for index, name in enumerate(names_of_appointments) :
    print(str(index) + ' - ' + name)

# User input for appointment type
while True:
    try:
        appointment_index = int(input('\nSelect appointment type (Range 0-11):\n'))
        
        if (appointment_index >= 0 and appointment_index <= 11):
            break
    except:
        print('Please enter a valid integer')

url_id_extension = types_of_appointments[appointment_index]
id_name = names_of_appointments[appointment_index]

print('\n\n' + id_name)


# Beep
def beep():
    winsound.Beep(300, 300)
    winsound.Beep(250, 400)
    winsound.Beep(300, 300)
    winsound.Beep(250, 400)
    winsound.Beep(300, 300)
    winsound.Beep(250, 400)


def job(url_id_extension, id_name):
    # Print date
    now = datetime.now()
    dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
    print("\nDate Time: ", dt_string)
    
    # Options for Chrome driver, prevents window from oppening
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    # Current dir path
    cur_path = pathlib.Path(__file__).parent.resolve()
    cur_path = cur_path / 'chromedriver'
    
    # Selenium Chrome driver
    driver = webdriver.Chrome(executable_path = cur_path, options = options)
    
    # Open appoint page
    driver.get(base_url_link+url_id_extension)
    
    # Wait for dynamic HTML to be generated
    time.sleep(0.25)
    
    # Copies webpage source
    html = driver.page_source
    
    # Scrape HTML
    soup = BeautifulSoup(html ,'lxml')
    
    found = 0
    
    # Find all divs with class text-capitalize
    for location in soup.find_all('div', {'class': 'text-capitalize'}):
        # Get name of the current location
        name = location.find('span').get_text()
        name = re.sub(id_name, '', name)
        
        # Find appointment information
        appointments_info = location.find('span', id = re.compile('^dateText')).get_text()

        # If none available
        if appointments_info == "No Appointments Available" :
            dumb = 0
            #print('\nNo appointments available at ' + name)
        else:# If available
            # Split sentence into list of words
            info_list = appointments_info.split()

            appointments_available = info_list[0]
            appointment_date = info_list[5]
            appointment_time = info_list[6]
            print('\n' + appointments_available + ' ' + id_name + ' appointment(s) available at ' + name)
            print('    Earliest appointment on ' + appointment_date + ' at ' + appointment_time + ' -----------------------------------------------------------------------')
            beep()
            found += 1

    if found == 0:
        print('No available appointments at this time')
    # Quit Selenium Chrome driver
    driver.quit()

while True :
    try:
        job(url_id_extension, id_name)
    except:
        print("Something went wrong")
        # Sleeps 60 seconds
        time.sleep(60)
    else:
        # Sleeps 60 seconds
        time.sleep(60)
    
