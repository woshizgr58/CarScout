from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time


all_cars = {}
# vehicle = {
#     "Model": "",
#     "Year": "",
#     "Current Bid": "",
#     "Description": "",
#     "Location": ""

# }

def add_car(car_id, model, year, current_bid, description, location):
    all_cars[car_id] = {
        "Model": model,
        "Year": year,
        "Current Bid": current_bid,
        "Description": description,
        "Location": location
    }



def scrape_cars_n_bids():
    """Scrapes the models of all cars for auction on CarsandBids"""

    carsnbids = 'https://carsandbids.com/'

    cService = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service = cService)

    driver.get(carsnbids) # open a chromedriver window

    time.sleep(1)
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # scroll to the bottom of page
    # time.sleep(10)
    
    # below all need .text when iterating to get text
    # all should have same length
    car_titles = driver.find_elements(By.XPATH,'//div[@class="auction-title"]//a') # get list of car names, split into year and model when iterating
    current_bids = driver.find_elements(By.XPATH, '//li[@class="auction-item "]//span[@class="bid-value"]') # get list of current bids
    descriptions = driver.find_elements(By.XPATH, '//li[@class="auction-item "]//p[@class="auction-subtitle"]') # get list of descriptions
    locations = driver.find_elements(By.XPATH, '//li[@class="auction-item "]//p[@class="auction-loc"]') # get list of locations

    print(len(car_titles))
    print(len(current_bids))
    print(len(descriptions))
    print(len(locations))

    time.sleep(5)

    for i in range (len(car_titles)):
        # try:
        car_text = car_titles[i].text
        car_id = i + 1
        year = car_text.split()[0]
        model = " ".join(car_text.split()[1:])
        # current_bid = current_bids[i].text
        current_bid = "null"
        description = descriptions[i].text
        location = locations[i].text
        add_car(car_id, model, year, current_bid, description, location)
        # except IndexError:
        #     print("index error")
    


    # for car in cars:
    #     car_names.append(car.text)
    
    print("end cars and bids")

    driver.quit()

scrape_cars_n_bids()
print(all_cars)

def scrape_bat():
    """Scrapes the models of all cars for auction on Bring a Trailer"""
    ## currently not working, need to separate keys
    bat = "https://bringatrailer.com/auctions/"

    cService = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service= cService)

    driver.get(bat)

    time.sleep(.5)

    last_height = driver.execute_script("return document.body.scrollHeight")

    start_time = time.time() # gets the current time 

    num_auctions_box = driver.find_element(By.XPATH, '//div[@class="auctions-header"]//h2').text

    num_auctions = int(num_auctions_box.split()[0])
    
    count = 0

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # scroll to the bottom of page

        

        new_height = driver.execute_script("return document.body.scrollHeight")
        # time.sleep(.5)

        if count == num_auctions / 100:
            print(count, num_auctions)
            print("end scroll bat")
            break # exit if theres not more content

        last_height = new_height 
        
        if time.time() - start_time > 3:
            print("Time limit reached. Stopping scroll.")
            break  # Exit after 15 seconds
            
        count += 1

    cars = driver.find_elements(By.XPATH, '//a[@class="listing-card bg-white-transparent"]//div[@class="content"]//h3')

    time.sleep(1)
    for car in cars:
        car_names.append(car.text)

    print("end bat")

    driver.quit()


# scrape_cars_n_bids()
# print(car_names, len(car_names))
# scrape_bat()
# print(car_names, len(car_names))

