from flask import Flask, render_template, jsonify, request
import sqlite3
import json
from datetime import datetime

app = Flask(__name__)

def get_db_connection():
    """Create a database connection"""
    conn = sqlite3.connect('auctions.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    """Home page with auction statistics"""
    conn = get_db_connection()
    
    # Get basic stats
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) as total FROM auctions')
    total_auctions = cursor.fetchone()['total']
    
    cursor.execute('SELECT source, COUNT(*) as count FROM auctions GROUP BY source')
    source_stats = cursor.fetchall()
    
    cursor.execute('''
        SELECT model, year, current_bid, source, description 
        FROM auctions 
        ORDER BY scraped_at DESC 
        LIMIT 10
    ''')
    recent_auctions = cursor.fetchall()
    
    conn.close()
    
    return render_template('index.html', 
                         total_auctions=total_auctions,
                         source_stats=source_stats,
                         recent_auctions=recent_auctions)

@app.route('/api/auctions')
def api_auctions():
    """API endpoint to get auctions with filters"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get query parameters
    source = request.args.get('source')
    model = request.args.get('model')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    
    # Build query
    query = 'SELECT * FROM auctions WHERE 1=1'
    params = []
    
    if source:
        query += ' AND source = ?'
        params.append(source)
    
    if model:
        query += ' AND model LIKE ?'
        params.append(f'%{model}%')
    
    if min_price:
        query += ' AND current_bid LIKE "%$%" AND CAST(REPLACE(REPLACE(REPLACE(current_bid, "$", ""), ",", ""), " ", "") AS INTEGER) >= ?'
        params.append(int(min_price))
    
    if max_price:
        query += ' AND current_bid LIKE "%$%" AND CAST(REPLACE(REPLACE(REPLACE(current_bid, "$", ""), ",", ""), " ", "") AS INTEGER) <= ?'
        params.append(int(max_price))
    
    query += ' ORDER BY scraped_at DESC LIMIT 100'
    
    cursor.execute(query, params)
    auctions = cursor.fetchall()
    
    conn.close()
    
    # Convert to list of dictionaries
    result = []
    for auction in auctions:
        result.append({
            'id': auction['id'],
            'auction_id': auction['auction_id'],
            'source': auction['source'],
            'model': auction['model'],
            'year': auction['year'],
            'current_bid': auction['current_bid'],
            'description': auction['description'],
            'location': auction['location'],
            'time_left': auction['time_left'],
            'time_left_minutes': auction['time_left_minutes'],
            'image_url': auction['image_url'],
            'auction_url': auction['auction_url'],
            'scraped_at': auction['scraped_at']
        })
    
    return jsonify(result)

@app.route('/proxy-image/<path:image_url>')
def proxy_image(image_url):
    """Proxy images to avoid CORS issues"""
    try:
        import requests
        from urllib.parse import unquote
        
        # Decode the URL
        decoded_url = unquote(image_url)
        
        # Fetch the image
        response = requests.get(decoded_url, timeout=10)
        response.raise_for_status()
        
        # Return the image with proper headers
        from flask import Response
        return Response(
            response.content,
            status=200,
            headers={
                'Content-Type': response.headers.get('Content-Type', 'image/jpeg'),
                'Cache-Control': 'public, max-age=3600'
            }
        )
    except Exception as e:
        print(f"Error proxying image {image_url}: {e}")
        return '', 404

@app.route('/api/stats')
def api_stats():
    """API endpoint for statistics"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get various stats
    cursor.execute('SELECT COUNT(*) as total FROM auctions')
    total = cursor.fetchone()['total']
    
    cursor.execute('SELECT source, COUNT(*) as count FROM auctions GROUP BY source')
    by_source = cursor.fetchall()
    
    cursor.execute('''
        SELECT model, COUNT(*) as count 
        FROM auctions 
        WHERE model IS NOT NULL AND model != ''
        GROUP BY model 
        ORDER BY count DESC 
        LIMIT 10
    ''')
    top_models = cursor.fetchall()
    
    conn.close()
    
    return jsonify({
        'total_auctions': total,
        'by_source': [dict(row) for row in by_source],
        'top_models': [dict(row) for row in top_models]
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000) 