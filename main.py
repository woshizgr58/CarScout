import scraper
import json

def main():
    print("Scraping Cars & Bids...")
    cars_n_bids_data = scraper.scrape_cars_n_bids()
    print("Cars & Bids data:", cars_n_bids_data)

    print("Scraping Bring a Trailer...")
    bat_data = scraper.scrape_bat()
    print("Bring a Trailer data:", bat_data)

    combined_data = {
        "CarsAndBids": cars_n_bids_data,
        "BringATrailer": bat_data
    }

    with open("auction_data.json", "w") as file:
        json.dump(combined_data, file, indent=4)
    
    print("Data saved to auction_data.json")

if __name__ == "__main__":
    main()
