# Necesarry Imports 
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException, ElementNotInteractableException 
import pandas as pd
import time 

# Webdriver parameters 
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# Initialize chrome webdriver
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver.get('https://www.brantcountyford.ca/vehicles/new/?st=price,asc&view=grid&sc=new')


num_pages = driver.find_element(By.XPATH,"/html/body/main/div/div/div[1]/div/div[2]/div[1]/div[2]/div/span").text
num_pages = int(num_pages.replace("of ",''))
count = 1

car_data = []
for i in range(1,num_pages):
    # Ensures we get all the data from scrolling down
    for i in range(1,100):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    elements = driver.find_elements_by_xpath("//div[contains(@class, 'vehicle-card__details')]")
    length = len(elements)

    for i in range(1,length+1):
        time.sleep(5)
  
        driver.find_element(By.XPATH,"/html/body/main/div/div/div[1]/div/div[2]/div[3]/div[{}]/div/div[2]".format(i)).find_element_by_link_text('View More Details').click()
      
     
        year = car_oem = car_name = car_model = car_registration = stock_number = vin_number = kilometres = condition = body_style = engine = transmission = drive_train = doors = fuel_type = city_fuel = hwy_fuel = key_features = sale_price = original_price = discount_price = ''
        print("This is car number: {}".format(count))
        time.sleep(5)
        car_name = driver.find_element(By.XPATH,"/html/body/main/div/div[1]/div/div/div[3]/div[1]/h1").text

        year = car_name[0:4]
        print("Year: {}".format(year))

        car_oem = 'Ford'
        print("Make: {}".format(car_oem))

        car_make = car_name[5:].replace('Ford ','')
        print("Model: {}".format(car_make))

        car_registration =  driver.find_element(By.XPATH,"/html/body/main/div/div[1]/div/div/div[3]/div[1]/div[1]/div").text
        
        reg_info = car_registration.replace('Stock #: ','').replace('VIN: ', '').replace(' ','*')

        stock_number = tuple(reg_info.split("*"))[0]
        print("Stock Number: {}".format(stock_number))

        vin_number = tuple(reg_info.split("*"))[1]
        print("VIN: {}".format(vin_number))

        kilometres = driver.find_element(By.XPATH,"/html/body/main/div/div[1]/div/div/div[3]/div[1]/div[2]/div/ul/li[1]/div/div/p").text
        print("Kilometres: {}".format(kilometres))
        
        condition = driver.find_element(By.XPATH,"/html/body/main/div/div[1]/div/div/div[3]/div[1]/div[2]/div/ul/li[2]/div/div/p").text 
        print("Condition: {}".format(condition)) 
        
        body_style = driver.find_element(By.XPATH,"/html/body/main/div/div[1]/div/div/div[3]/div[1]/div[2]/div/ul/li[3]/div/div/p").text
        print("Body Style: {}".format(body_style))
    
        engine = driver.find_element(By.XPATH,"/html/body/main/div/div[1]/div/div/div[3]/div[1]/div[2]/div/ul/li[4]/div/div/p").text
        print("Engine: {}".format(engine))
        
        transmission = driver.find_element(By.XPATH,"/html/body/main/div/div[1]/div/div/div[3]/div[1]/div[2]/div/ul/li[5]/div/div/p").text
        print("Transmission: {}".format(transmission))
        
        drive_train = driver.find_element(By.XPATH,"/html/body/main/div/div[1]/div/div/div[3]/div[1]/div[2]/div/ul/li[6]/div/div/p").text
        print("Drive Train: {}".format(drive_train))
        
        doors = driver.find_element(By.XPATH,"/html/body/main/div/div[1]/div/div/div[3]/div[1]/div[2]/div/ul/li[7]/div/div/p").text
        print("Doors: {}".format(doors))
        
        fuel_type = driver.find_element(By.XPATH,"/html/body/main/div/div[1]/div/div/div[3]/div[1]/div[2]/div/ul/li[8]/div/div/p").text
        print("Fuel Type: {}".format(fuel_type))

        ## Potential missing values 
        try:
            city_fuel = driver.find_element(By.XPATH,"/html/body/main/div/div[1]/div/div/div[3]/div[1]/div[2]/div/ul/li[9]/div/div/p").text
            #print("City Fuel Economy: {}".format(city_fuel))
        except NoSuchElementException:
            city_fuel = 'Missing Value'
            #print("City Fuel Economy: {}".format(city_fuel))
        
        try:
            hwy_fuel = driver.find_element(By.XPATH,"/html/body/main/div/div[1]/div/div/div[3]/div[1]/div[2]/div/ul/li[10]/div/div/p").text
        except NoSuchElementException:
            hwy_fuel = 'Missing Value'
        
        driver.find_element_by_class_name('apply-read-more__button').click()

        key_features = driver.find_element(By.XPATH,"/html/body/main/div/div[1]/div/div/div[3]/div[1]/div[3]/p").text
        key_features = key_features.replace("""Please Call 519-756-6191, Email sales@brantcountyford.ca for more information and availability on this vehicle.  Brant County Ford is a family owned dealership and has been a proud member of the Brantford community for over 40 years!
    ** PURCHASE PRICE ONLY (Includes) Fords Delivery Allowance & Non-stackable where applicable
    Read Less""", '')
        print("Key Features: {}".format(key_features))

        try: 
            original_price = driver.find_element(By.XPATH,"/html/body/main/div/div[1]/div/div/div[3]/div[2]/div/div[2]/div[1]/p").text
            original_price = original_price.replace('$','').replace(',','').replace("\n",'')

        except NoSuchElementException:
            original_price = 'Missing Value'
            
        try:
            discount_price = driver.find_element(By.XPATH,"/html/body/main/div/div[1]/div/div/div[3]/div[2]/div/div[2]/div[1]/div[1]/span/span").text
            discount_price = discount_price.replace('$','').replace(',','').replace("\n",'')

        except NoSuchElementException:
            discount_price = 'Missing Value'

        try:
            sale_price = driver.find_element(By.XPATH,"/html/body/main/div/div[1]/div/div/div[3]/div[2]/div/div[2]/div/div/div/div/div/span").text
            sale_price = sale_price.replace('$','').replace(',','').replace("\n",'')
        except NoSuchElementException:
            sale_price = ''
        if original_price != 'Missing Value' and discount_price != 'Missing Value':
            sale_price = int(original_price) - int(discount_price)

        print("City Fuel Economy: {}".format(city_fuel))
        print("Hwy Fuel Economy: {}".format(hwy_fuel))
        print("MSRP Price: {}".format(original_price))
        print("Sale Price: {}".format(sale_price))
        print("Discount Price: {}".format(discount_price))
        print()
        print()
        count+=1

        # Generate the list of data 
        current = [year,car_oem, car_make,vin_number, stock_number, kilometres, condition, body_style, engine, transmission, drive_train, doors, fuel_type, city_fuel, hwy_fuel, key_features, sale_price, original_price, discount_price]
        car_data.append(current)
        driver.back()
    if i != num_pages:
        driver.find_element(By.XPATH,"/html/body/main/div/div/div[1]/div/div[2]/div[1]/div[2]/button[2]/i").click()


car_data_df = pd.DataFrame(car_data, columns = ['year','car_oem', 'car_make', 'vin_number', 'stock_number', 'kilometres', 'condition', 'body_style', 'engine', 'transmission', 'drive_train', 
                'doors', 'fuel_type', 'city_fuel', 'hwy_fuel', 'key_features', 'sale_price', 'original_price', 'discount_price']
)
print(car_data_df)
car_data_df.to_csv('car_data.csv',index=False)