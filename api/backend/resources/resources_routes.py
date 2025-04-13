from flask import Blueprint, request, jsonify, make_response, current_app
from rethread.api.backend.db_connection import db

resources = Blueprint('/resources', __name__)


@resources.route('/listing', methods=['GET'])
def get_all_listings():
    query = ''''
        SELECT listing_id, title, price
        FROM Listing;
    '''
    current_app.logger.info('GET /listings route')
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response



@resources.route('/listing/<int:listing_id>', methods=['GET'])
def get_listing_by_id(listing_id):
    query = ''''
        SELECT *
        FROM Listing
        WHERE listing_id = %s;
    '''
    current_app.logger.info(f'GET /listing/{listing_id} route')
    cursor = db.get_db().cursor()
    cursor.execute(query, (listing_id,))
    theData = cursor.fetchall()
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response



@resources.route('/PriceHistory/<int:listing_id>', methods=['PUT'])
def update_listing_price(listing_id):
    data = request.json
    new_price = data.get('new_price')

    query = ''''
        UPDATE PriceHistory
        SET price = %s
        WHERE listing_id = %s;
    '''
    current_app.logger.info(f'PUT /listing/{listing_id} route')
    cursor = db.get_db().cursor()
    cursor.execute(query, (new_price, listing_id))
    db.get_db().commit()
    response = make_response(jsonify({'message': 'Price updated'}))
    response.status_code = 200
    return response



@resources.route('/products/<int:listing_id>', methods=['DELETE'])
def mark_product_as_sold(listing_id):

    query = ''''
        INSERT INTO Transaction (listing_id, method, buyer_id, seller_id, status, payment, price, timestamp)
        VALUES (%s, NULL, NULL, NULL, 'sold', NULL, 0.00, CURRENT_TIMESTAMP);
    '''
    current_app.logger.info(f'DELETE /products/{listing_id} route - marked as sold')

    cursor = db.get_db().cursor()
    cursor.execute(query, (listing_id,))
    db.get_db().commit()

    response = make_response({'message': f'Product {listing_id} marked as sold via transaction'}, 200)
    return response




