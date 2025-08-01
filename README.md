# 🚗 CarScout - Auction Database & Web Application

A comprehensive web scraping and database system for car auctions from Cars & Bids and Bring a Trailer.

## 📋 Features

- **Web Scraping**: Automatically scrapes auction data from Cars & Bids and Bring a Trailer
- **SQLite Database**: Stores auction data in a local SQLite database
- **Web Interface**: Beautiful, responsive web application to browse and search auctions
- **API Endpoints**: RESTful API for programmatic access to auction data
- **Real-time Filtering**: Search by model, price range, and auction source

## 🏗️ Architecture

```
CarScout/
├── main.py              # Main scraper script
├── scraper.py           # Web scraping functions
├── database.py          # SQLite database operations
├── web_app.py           # Flask web application
├── templates/
│   └── index.html       # Web interface template
├── auction_data.json    # Raw scraped data (JSON)
├── auctions.db          # SQLite database file
└── README.md           # This file
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install selenium flask
```

### 2. Install ChromeDriver (macOS)
```bash
brew install chromedriver
```

### 3. Run the Scraper
```bash
python main.py
```
This will:
- Scrape Cars & Bids (195+ auctions)
- Scrape Bring a Trailer (1,194+ auctions)
- Save data to `auction_data.json`

### 4. Import to Database
```bash
python database.py
```
This will:
- Create SQLite database (`auctions.db`)
- Import all auction data
- Show example queries

### 5. Start Web Application
```bash
python web_app.py
```
Then visit: http://localhost:5000

## 📊 Database Schema

```sql
CREATE TABLE auctions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    auction_id TEXT,
    source TEXT NOT NULL,           -- 'CarsAndBids' or 'BringATrailer'
    model TEXT,
    year INTEGER,
    current_bid TEXT,
    description TEXT,
    location TEXT,
    time_left TEXT,
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔍 Example Queries

### Find all BMW auctions
```sql
SELECT * FROM auctions WHERE model LIKE '%BMW%';
```

### Find expensive auctions (>$50k)
```sql
SELECT * FROM auctions 
WHERE current_bid LIKE '%$%' 
AND CAST(REPLACE(REPLACE(REPLACE(current_bid, '$', ''), ',', ''), ' ', '') AS INTEGER) > 50000;
```

### Get auction statistics by source
```sql
SELECT source, COUNT(*) as count FROM auctions GROUP BY source;
```

## 🌐 Web Application Features

### Dashboard
- Total auction count
- Auctions by source
- Recent auctions

### Search & Filter
- **Source**: Cars & Bids or Bring a Trailer
- **Model**: Search by car model (e.g., "BMW", "Porsche")
- **Price Range**: Filter by minimum and maximum price
- **Real-time Results**: Instant filtering with AJAX

### API Endpoints
- `GET /api/auctions` - Get auctions with filters
- `GET /api/stats` - Get database statistics

## 🛠️ Development

### Adding New Auction Sources
1. Add scraping function to `scraper.py`
2. Update `main.py` to call new function
3. Update database import in `database.py`

### Customizing the Web Interface
- Edit `templates/index.html` for UI changes
- Modify `web_app.py` for new API endpoints
- Add CSS/JS for enhanced functionality

## 📈 Data Flow

```
Web Scraping (Selenium) 
    ↓
JSON Storage (auction_data.json)
    ↓
SQLite Database (auctions.db)
    ↓
Web Application (Flask)
    ↓
User Interface (HTML/CSS/JS)
```

## 🔧 Configuration

### ChromeDriver Path
Update the ChromeDriver path in `scraper.py` if needed:
```python
cService = Service(executable_path="/opt/homebrew/bin/chromedriver")
```

### Database Location
The SQLite database is created as `auctions.db` in the project root.

### Web Server
The Flask app runs on `http://localhost:5000` by default.

## 🚀 Production Deployment

### Option 1: Simple Hosting
- Use `gunicorn` for production WSGI server
- Deploy to Heroku, Railway, or similar platforms
- Add environment variables for configuration

### Option 2: Full Stack
- Replace SQLite with PostgreSQL/MySQL
- Add user authentication
- Implement real-time updates
- Add email notifications

### Option 3: Serverless
- Convert to AWS Lambda functions
- Use DynamoDB or RDS for database
- Deploy with API Gateway

## 📝 API Documentation

### GET /api/auctions
Returns filtered auction data.

**Query Parameters:**
- `source`: Filter by auction source
- `model`: Search by car model
- `min_price`: Minimum price filter
- `max_price`: Maximum price filter

**Example:**
```
GET /api/auctions?source=CarsAndBids&model=BMW&min_price=50000
```

### GET /api/stats
Returns database statistics.

**Response:**
```json
{
  "total_auctions": 1390,
  "by_source": [
    {"source": "CarsAndBids", "count": 196},
    {"source": "BringATrailer", "count": 1194}
  ],
  "top_models": [...]
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Troubleshooting

### ChromeDriver Issues
- Ensure ChromeDriver is installed: `brew install chromedriver`
- Check Chrome browser version compatibility
- Update ChromeDriver if needed

### Database Issues
- Delete `auctions.db` and re-run `python database.py`
- Check JSON file integrity: `python -m json.tool auction_data.json`

### Web App Issues
- Ensure Flask is installed: `pip install flask`
- Check port 5000 is available
- Review browser console for JavaScript errors

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the code comments
3. Open an issue on GitHub

---

**Happy Car Hunting! 🚗💨** 