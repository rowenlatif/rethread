import flask
from backend.db_connection import db


#Blueprint for seller-related routes - organizes a group of related routes
seller = flask.Blueprint('seller', __name__)


@seller.route('/seller-listings/<int:seller_id>', methods=['GET'])
def get_seller_listings(seller_id):
   query = """
       SELECT l.*
       FROM Listing l
       JOIN ListingTag lt ON l.listing_id = lt.listing_id
       JOIN Tag t ON lt.tag_id = t.tag_id
       JOIN User u ON u.location_id = (SELECT location_id FROM User WHERE user_id = %s)
       WHERE l.seller_id = %s
         AND t.tag_name IN ('trendy', 'professional', 'vintage');
   """
   # Log that this endpoint was called with the seller_id
   flask.current_app.logger.info(f'GET /seller-listings/{seller_id} route')
   cursor = db.get_db().cursor()
   cursor.execute(query, (seller_id, ))
   theData = cursor.fetchall()
   response = flask.make_response(flask.jsonify(theData))
   response.status_code = 200
   return response


@seller.route('/transactions/<int:seller_id>', methods=['GET'])
def get_seller_transactions(seller_id):
   query = '''
       SELECT t.transaction_id, t.price, t.status, t.timestamp, u.name AS buyer_name
       FROM Transaction t
       JOIN User u ON t.buyer_id = u.user_id
       WHERE t.seller_id = %s AND t.status = 'completed';
   '''
   flask.current_app.logger.info(f'GET /transactions/{seller_id} route')
   cursor = db.get_db().cursor()
   cursor.execute(query, (seller_id,))
   theData = cursor.fetchall()
   response = flask.make_response(flask.jsonify(theData))
   response.status_code = 200
   return response


@seller.route('/messages/<int:seller_id>', methods=['GET'])
def get_seller_messages(seller_id):
   query = '''
       SELECT m.message_id, u.name AS buyer_name, m.content, m.timestamp
       FROM Message m
       JOIN User u ON m.sender_id = u.user_id
       WHERE m.recipient_id = %s
       ORDER BY m.timestamp DESC;
   '''
   flask.current_app.logger.info(f'GET /messages/{seller_id} route')
   cursor = db.get_db().cursor()
   cursor.execute(query, (seller_id,))
   theData = cursor.fetchall()
   response = flask.make_response(flask.jsonify(theData))
   response.status_code = 200
   return response


@seller.route('/listing-photo', methods=['POST'])
def upload_photo():
   query = '''
           INSERT INTO ListingPhoto (photo_id, listing_id, tag_label, url)
           VALUES (%s, %s, %s, %s)
       '''
   data = flask.request.json
   photo_id = data.get('photo_id')
   listing_id = data.get('listing_id')
   tag_label = data.get('tag_label')
   url = data.get('url')


   cursor = db.get_db().cursor()
   cursor.execute(query, (photo_id, listing_id, tag_label, url,))
   db.get_db().commit()
   response = flask.make_response({'message': 'Photo uploaded successfully'}, 201)
   return response


@seller.route('/review', methods=['POST'])
def create_customer_review():
   query = '''
           INSERT INTO Review (review_id, reviewer_id, reviewee_id, comment, created_at, rating)
           VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP, %s)
       '''
   data = flask.request.json
   review_id = data.get('review_id')
   reviewer_id = data.get('reviewer_id')
   reviewee_id = data.get('reviewee_id')
   comment = data.get('comment')
   created_at = data.get('created_at')
   rating = data.get('rating')


   cursor = db.get_db().cursor()
   cursor.execute(query, (review_id, reviewer_id, reviewee_id, comment, created_at, rating,))
   db.get_db().commit()
   response = flask.make_response({'message': 'Review created successfully'}, 201)
   return response


@seller.route('/listings', methods=['POST'])
def create_listing():
   query = '''
           INSERT INTO Listing (listing_id, title, description, price, `condition`, brand, size, material, color, seller_id, group_id)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
       '''
   data = flask.request.json
   listing_id = data.get('listing_id')
   title = data.get('title')
   description = data.get('description')
   price = data.get('price')
   condition = data.get('condition')
   brand = data.get('brand')
   size = data.get('size')
   material = data.get('material')
   color = data.get('color')
   seller_id = data.get('seller_id')
   group_id = data.get('group_id')


   cursor = db.get_db().cursor()
   cursor.execute(query, (listing_id, title, description, price, condition, brand, size, material, color, seller_id, group_id,))
   db.get_db().commit()
   response = flask.make_response({'message': 'Listing posted!'}, 201)
   return response


@seller.route('/analytics/<int:seller_id>', methods=['GET'])
def get_listing_analytics(seller_id):
   query: str = '''
       SELECT l.title, la.views, la.saves, la.shares
       FROM Listing l
       JOIN ListingAnalytics la ON l.listing_id = la.listing_id
       WHERE l.seller_id = %s
       ORDER BY la.views DESC;
   '''
   flask.current_app.logger.info(f'GET /analytics/{seller_id} route')
   cursor = db.get_db().cursor()
   cursor.execute(query, (seller_id,))
   theData = cursor.fetchall()
   response = flask.make_response(flask.jsonify(theData))
   response.status_code = 200
   return response










