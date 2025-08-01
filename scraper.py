from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import re


def parse_time_left(time_str):
    """Parse time left string into minutes for sorting"""
    if not time_str or time_str == "null":
        return 999999  # Very high number for sorting purposes

    time_str = time_str.lower().strip()

    # Handle different time formats
    if 'day' in time_str:
        days = int(re.search(r'(\d+)', time_str).group(1))
        return days * 24 * 60  # Convert to minutes
    elif 'hour' in time_str:
        hours = int(re.search(r'(\d+)', time_str).group(1))
        return hours * 60  # Convert to minutes
    elif 'minute' in time_str:
        minutes = int(re.search(r'(\d+)', time_str).group(1))
        return minutes
    elif 'second' in time_str:
        return 1  # Less than 1 minute
    else:
        return 999999  # Default for unknown formats

def add_car(car_id, model, year, current_bid, description, location, time_left, image_url, auction_url, cars_dict):
    time_left_minutes = parse_time_left(time_left)
    cars_dict[car_id] = {
        "Model": model,
        "Year": year,
        "Current Bid": current_bid,
        "Description": description,
        "Location": location,
        "Time Left": time_left,
        "Time_Left_Minutes": time_left_minutes,
        "Image_URL": image_url,
        "Auction_URL": auction_url
    }



def scrape_cars_n_bids():
    """Scrapes the models of all cars for auction on CarsandBids
    Known problems: 
    - doesn't get bids fast enough
    - time isn't displayed in the list properly
    """
    
    cars_dict = {}
    carsnbids = 'https://carsandbids.com/'

    # Use ChromeDriver from Homebrew installation on macOS
    cService = Service(executable_path="/opt/homebrew/bin/chromedriver")
    driver = webdriver.Chrome(service = cService)

    driver.get(carsnbids) # open a chromedriver window

    time.sleep(1)
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # scroll to the bottom of page
    # time.sleep(10)
    
    # below all need .text when iterating to get text
    # all should have same length
    car_titles = driver.find_elements(By.XPATH,'//div[@class="auction-title"]//a') # get list of car names, split into year and model when iterating
    current_bids = driver.find_elements(By.XPATH, '//span[@class="bid-value"]') # get list of current bids
    descriptions = driver.find_elements(By.XPATH, '//p[@class="auction-subtitle"]') # get list of descriptions
    locations = driver.find_elements(By.XPATH, '//p[@class="auction-loc"]') # get list of locations
    times_left = driver.find_elements(By.XPATH, '//span[contains(@class, "ticking")]') # gets time left of the auction
    images = driver.find_elements(By.XPATH, '//img[contains(@src, "carsandbids.com")]') # get list of car images

    # print(f"Found {len(car_titles)} car titles")
    # print(f"Found {len(current_bids)} current bids")
    # print(f"Found {len(descriptions)} descriptions")
    # print(f"Found {len(locations)} locations")
    # print(f"Found {len(times_left)} times left")

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
        
        # Get image URL
        try:
            image_url = images[i].get_attribute('src')
        except IndexError:
            image_url = ""
        
        # Get auction URL
        try:
            auction_url = car_titles[i].get_attribute('href')
        except IndexError:
            auction_url = ""
        
        add_car(car_id, model, year, current_bid, description, location, str(time_left), image_url, auction_url, cars_dict)
        # except IndexError:
        #     print("index error")
    


    # for car in cars:
    #     car_names.append(car.text)
    
    # print("end cars and bids")

    driver.quit()
    return cars_dict

# scrape_cars_n_bids()
# print(all_cars)

def scrape_bat():
    """Scrapes the models of all cars for auction on Bring a Trailer
    Consider adding feature that has user input zip code and finds the closest auction in replacement for the "location" key
    Known problems: 
    - time isn't displayed in the list properly
    
    """
    ## currently not working, need to separate keys
    
    cars_dict = {}
    bat = "https://bringatrailer.com/auctions/"

    # Use ChromeDriver from Homebrew installation on macOS
    cService = Service(executable_path="/opt/homebrew/bin/chromedriver")
    driver = webdriver.Chrome(service= cService)

    driver.get(bat)

    time.sleep(.5)

    last_height = driver.execute_script("return document.body.scrollHeight")

    start_time = time.time() # gets the current time 

    num_auctions_box = driver.find_element(By.XPATH, '//div[@class="auctions-header"]//h2').text

    # Remove commas from the number before converting to int
    num_auctions = int(num_auctions_box.split()[0].replace(',', ''))
    
    count = 0

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # scroll to the bottom of page

        

        new_height = driver.execute_script("return document.body.scrollHeight")
        # time.sleep(.5)

        if count == num_auctions / 100:
            # print(count, num_auctions)
            # print("end scroll bat")
            break # exit if theres not more content

        last_height = new_height 
        
        if time.time() - start_time > 3:
            # print("Time limit reached. Stopping scroll.")
            break  # Exit after 15 seconds
            
        count += 1

    # cars = driver.find_elements(By.XPATH, '//a[@class="listing-card bg-white-transparent"]//div[@class="content"]//h3')
    car_titles = driver.find_elements(By.XPATH,'//div[@class="content-main"]//h3[@data-bind="html: title"]') # get list of car names, split into year and model when iterating
    auction_links = driver.find_elements(By.XPATH,'//a[@class="listing-card bg-white-transparent"]') # get list of auction links
    current_bids = driver.find_elements(By.XPATH, '//span[@class="bid-formatted bold"]') # get list of current bids
    descriptions = driver.find_elements(By.XPATH, '//div[@class="item-excerpt"]') # get list of descriptions
    # locations = driver.find_elements(By.XPATH, '//li[@class="auction-item "]//p[@class="auction-loc"]') # get list of locations
    time_left_countdowns = driver.find_elements(By.XPATH, '//span[@class="countdown-text final-countdown"]') # get time left of auction < 24hrs
    times_left_days = driver.find_elements(By.XPATH, '//span[@class="countdown-text"]') # get days left of the auction
    images = driver.find_elements(By.XPATH, '//div[@class="listing-card"]//img') # get list of car images

    # time_left_countdowns.extend(times_left_days)
    combine_times_left = time_left_countdowns + times_left_days
    

    time.sleep(1)

    for i in range (len(car_titles)):
        # try:
        car_text = car_titles[i].text
        car_id = i + 1
        # year = car_text.split()[0]
        # model = " ".join(car_text.split()[1:])

        # Find teh first 4-digit number as the year
        year_match = re.search(r"\b\d{4}\b", car_text)
        if year_match:
            year = year_match.group()
        else:
            year = None

        # Find the model by removing the year from the text
        model = car_text.replace(year, "").strip() if year else car_text
        
        try: 
            time_left = combine_times_left[i].text
            current_bid = current_bids[i].text
        except (IndexError, TypeError) as e:
            # print(e)
            current_bid = "null"
            time_left = "null"
        description = descriptions[i].text
        location = "null"
        
        # Get image URL
        try:
            image_url = images[i].get_attribute('src')
        except IndexError:
            image_url = ""
        
        # Get auction URL
        try:
            auction_url = auction_links[i].get_attribute('href')
        except IndexError:
            auction_url = ""
        
        add_car(car_id, model, year, current_bid, description, location, str(time_left), image_url, auction_url, cars_dict)
    

    # print("end bat")

    # print(len(car_titles))
    # print(len(current_bids))
    # print(len(descriptions))
    # print(len(locations))
    # print(len(combine_times_left))

    driver.quit()
    return cars_dict

# scrape_bat()
# print(all_cars)


