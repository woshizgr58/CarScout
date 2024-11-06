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

def add_car(car_id, model, year, current_bid, description, location, time_left):
    all_cars[car_id] = {
        "Model": model,
        "Year": year,
        "Current Bid": current_bid,
        "Description": description,
        "Location": location,
        "Time Left": time
    }



def scrape_cars_n_bids():
    """Scrapes the models of all cars for auction on CarsandBids
    Current issues: doesn't get bids fast enough
    """

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
    times_left = driver.find_elements(By.XPATH, '//span[@class="ticking  "]') # gets time left of the auction

    print(len(car_titles))
    print(len(current_bids))
    print(len(descriptions))
    print(len(locations))
    print(len(times_left))

    time.sleep(5)

    for i in range (len(car_titles)):
        # try:
        car_text = car_titles[i].text
        car_id = i + 1
        year = car_text.split()[0]
        model = " ".join(car_text.split()[1:])
        try: 
            # still doesn't properly scrape the time
            time_left = times_left[i].text
            current_bid = current_bids[i].text
        except IndexError:
            current_bid = "null"
            time_left = "null"
        description = descriptions[i].text
        location = locations[i].text
        
        add_car(car_id, model, year, current_bid, description, location, time_left)
        # except IndexError:
        #     print("index error")
    


    # for car in cars:
    #     car_names.append(car.text)
    
    print("end cars and bids")

    driver.quit()

# scrape_cars_n_bids()
# print(all_cars)

def scrape_bat():
    """Scrapes the models of all cars for auction on Bring a Trailer
    Consider adding feature that has user input zip code and finds the closest auction in replacement for the "location" key
    """
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

    # cars = driver.find_elements(By.XPATH, '//a[@class="listing-card bg-white-transparent"]//div[@class="content"]//h3')
    car_titles = driver.find_elements(By.XPATH,'//div[@class="content-main"]//h3[@data-bind="html: title"]') # get list of car names, split into year and model when iterating
    current_bids = driver.find_elements(By.XPATH, '//span[@class="bid-formatted bold"]') # get list of current bids
    descriptions = driver.find_elements(By.XPATH, '//div[@class="item-excerpt"]') # get list of descriptions
    # locations = driver.find_elements(By.XPATH, '//li[@class="auction-item "]//p[@class="auction-loc"]') # get list of locations
    time_left_countdowns = driver.find_elements(By.XPATH, '//span[@class="countdown-text final-countdown"]') # get time left of auction < 24hrs
    times_left_days = driver.find_elements(By.XPATH, '//span[@class="countdown-text"]') # get days left of the auction

    # time_left_countdowns.extend(times_left_days)
    combine_times_left = time_left_countdowns + times_left_days
    

    time.sleep(1)

    for i in range (len(car_titles)):
        # try:
        car_text = car_titles[i].text
        car_id = i + 1
        year = car_text.split()[0]
        model = " ".join(car_text.split()[1:])
        
        try: 
            time_left = combine_times_left[i].text
            current_bid = current_bids[i].text
        except (IndexError, TypeError) as e:
            # print(e)
            current_bid = "null"
            time_left = "null"
        description = descriptions[i].text
        location = "null"
        
        add_car(car_id, model, year, current_bid, description, location, time_left)
    

    print("end bat")

    print(len(car_titles))
    print(len(current_bids))
    print(len(descriptions))
    # print(len(locations))
    print(len(combine_times_left))

    driver.quit()

scrape_bat()
print(all_cars)


