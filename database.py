import sqlite3
import json
from datetime import datetime

def create_database():
    """Create the SQLite database and tables"""
    conn = sqlite3.connect('auctions.db')
    cursor = conn.cursor()
    
    # Create auctions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS auctions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            auction_id TEXT,
            source TEXT NOT NULL,
            model TEXT,
            year INTEGER,
            current_bid TEXT,
            description TEXT,
            location TEXT,
            time_left TEXT,
            time_left_minutes INTEGER,
            image_url TEXT,
            auction_url TEXT,
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create index for faster queries
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_source_model 
        ON auctions(source, model)
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Database created successfully")

def import_json_to_sqlite():
    """Import data from auction_data.json to SQLite database"""
    # Load JSON data
    with open('auction_data.json', 'r') as file:
        data = json.load(file)
    
    conn = sqlite3.connect('auctions.db')
    cursor = conn.cursor()
    
    # Clear existing data
    cursor.execute('DELETE FROM auctions')
    
    # Insert Cars & Bids data
    for auction_id, auction_data in data.get('CarsAndBids', {}).items():
        cursor.execute('''
            INSERT INTO auctions 
            (auction_id, source, model, year, current_bid, description, location, time_left, time_left_minutes, image_url, auction_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            auction_id,
            'CarsAndBids',
            auction_data.get('Model', ''),
            auction_data.get('Year'),
            auction_data.get('Current Bid', ''),
            auction_data.get('Description', ''),
            auction_data.get('Location', ''),
            auction_data.get('Time Left', ''),
            auction_data.get('Time_Left_Minutes'),
            auction_data.get('Image_URL', ''),
            auction_data.get('Auction_URL', '')
        ))
    
    # Insert Bring a Trailer data
    for auction_id, auction_data in data.get('BringATrailer', {}).items():
        cursor.execute('''
            INSERT INTO auctions 
            (auction_id, source, model, year, current_bid, description, location, time_left, time_left_minutes, image_url, auction_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            auction_id,
            'BringATrailer',
            auction_data.get('Model', ''),
            auction_data.get('Year'),
            auction_data.get('Current Bid', ''),
            auction_data.get('Description', ''),
            auction_data.get('Location', ''),
            auction_data.get('Time Left', ''),
            auction_data.get('Time_Left_Minutes'),
            auction_data.get('Image_URL', ''),
            auction_data.get('Auction_URL', '')
        ))
    
    conn.commit()
    conn.close()
    print("✅ Data imported to SQLite database")

def query_examples():
    """Show example queries you can run"""
    conn = sqlite3.connect('auctions.db')
    cursor = conn.cursor()
    
    print("\n📊 Database Query Examples:")
    print("=" * 50)
    
    # Total auctions by source
    cursor.execute('''
        SELECT source, COUNT(*) as count 
        FROM auctions 
        GROUP BY source
    ''')
    results = cursor.fetchall()
    print("📈 Auctions by source:")
    for source, count in results:
        print(f"   {source}: {count} auctions")
    
    # Recent BMW auctions
    cursor.execute('''
        SELECT model, year, current_bid, source 
        FROM auctions 
        WHERE model LIKE '%BMW%' 
        ORDER BY scraped_at DESC 
        LIMIT 5
    ''')
    results = cursor.fetchall()
    print("\n🚗 Recent BMW auctions:")
    for model, year, bid, source in results:
        print(f"   {year} {model} - {bid} ({source})")
    
    # Expensive auctions (>$50k)
    cursor.execute('''
        SELECT model, year, current_bid, source 
        FROM auctions 
        WHERE current_bid LIKE '%$%' 
        AND CAST(REPLACE(REPLACE(REPLACE(current_bid, '$', ''), ',', ''), ' ', '') AS INTEGER) > 50000
        ORDER BY CAST(REPLACE(REPLACE(REPLACE(current_bid, '$', ''), ',', ''), ' ', '') AS INTEGER) DESC
        LIMIT 5
    ''')
    results = cursor.fetchall()
    print("\n💰 Expensive auctions (>$50k):")
    for model, year, bid, source in results:
        print(f"   {year} {model} - {bid} ({source})")
    
    conn.close()

if __name__ == "__main__":
    create_database()
    import_json_to_sqlite()
    query_examples() 