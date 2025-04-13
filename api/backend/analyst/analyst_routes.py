from flask import Blueprint, request, jsonify, make_response, current_app
from rethread.api.backend.db_connection import db


analyst = Blueprint('/analyst', __name__)


@analyst.route('/listings/recent', methods=['GET'])
def get_recent_listings():
    current_app.logger.info('GET /listings/recent route')

    query = ''''
        SELECT * FROM Listing
        WHERE timestamp >= CURRENT_DATE - INTERVAL 7 DAY;
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

@analyst.route('/trend-reports', methods=['POST'])
def log_trend_report():
    query = ''''
        INSERT INTO TrendReport (report_id, exported_format, title, summary, filters, created_at, created_by)
        VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP, %s);
    '''
    data = request.json
    report_id = data.get('report_id')
    exported_format = data.get('exported_format')
    title = data.get('title')
    summary = data.get('summary')
    filters = data.get('filters')
    created_at = data.get('created_at')
    created_by = data.get('created_by')

    cursor = db.get_db().cursor()
    cursor.execute(query, (report_id, exported_format, title, summary, filters, created_at, created_by))
    response = make_response(jsonify('trend report created'), 201)
    return response

@analyst.route('/price-history/<int:listing_id>', methods=['GET'])
def get_price_history(listing_id):
    query= ''''
    SELECT
        listing_id,
        MIN(price) AS min_price,
        MAX(price) AS max_price,
        (MAX(price) - MIN(price)) AS price_range
    FROM PriceHistory
    GROUP BY listing_id
    ORDER BY price_range DESC;'''

    current_app.logger.info(f'GET /price-history/{listing_id} route')
    cursor = db.get_db().cursor()
    cursor.execute(query, (listing_id))
    theData = cursor.fetchall()
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

@analyst.route('/search-trends', methods=['GET'])
def search_trends_time_demographic():

    query = ''''
            SELECT d.age, d.gender, d.location_id,
                   EXTRACT(MONTH FROM sq.timestamp) AS search_month,
                   COUNT(*) AS search_count
            FROM SearchQuery sq
            JOIN User u ON sq.user_id = u.user_id
            JOIN Demographic d ON u.demographic_id = d.demographic_id
            GROUP BY d.age, d.gender, d.location_id, search_month
            ORDER BY search_month, search_count DESC;
        '''

    current_app.logger.info(f'GET /search-trends route')
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

@analyst.route('/tags/trending', methods=['GET'])
def get_trending_tags():
    query = ''''
        SELECT t.tag_name, COUNT(*) AS usage_count
        FROM ListingTag lt
        JOIN Tag t ON lt.tag_id = t.tag_id
        JOIN Listing l ON lt.listing_id = l.listing_id
        WHERE l.timestamp >= CURRENT_DATE - INTERVAL 30 DAY
        GROUP BY t.tag_name
        ORDER BY usage_count DESC;
    '''
    current_app.logger.info('GET /tags/trending route')
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    return the_response

@analyst.route('/search-keywords', methods=['GET'])
def get_top_search_keywords():

    query = ''''
        SELECT keyword, SUM(usage_count) AS total_usage
        FROM SearchTrend
        WHERE trend_date >= CURRENT_DATE - INTERVAL 30 DAY
        GROUP BY keyword
        ORDER BY total_usage DESC
        LIMIT 10;
    '''

    current_app.logger.info('GET /search-keywords route')
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    the_response = make_response(theData)
    the_response.status_code = 200
    return the_response


