import scraper
import json

def main():
    print("🚗 Starting CarScout scraper...")
    print("📊 Scraping Cars & Bids...")
    cars_n_bids_data = scraper.scrape_cars_n_bids()
    print(f"✅ Found {len(cars_n_bids_data)} Cars & Bids auctions")

    print("📊 Scraping Bring a Trailer...")
    bat_data = scraper.scrape_bat()
    print(f"✅ Found {len(bat_data)} Bring a Trailer auctions")

    combined_data = {
        "CarsAndBids": cars_n_bids_data,
        "BringATrailer": bat_data
    }

    with open("auction_data.json", "w") as file:
        json.dump(combined_data, file, indent=4)
    
    total_auctions = len(cars_n_bids_data) + len(bat_data)
    print(f"💾 Data saved to auction_data.json ({total_auctions} total auctions)")

if __name__ == "__main__":
    main()
