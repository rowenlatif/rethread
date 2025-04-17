from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db


# This is the Blueprint for shopper-related routes
shopper = Blueprint('shopper', __name__)


@shopper.route('/listings/search/<tag_name>', methods=['GET'])
def get_listings_by_tag(tag_name):
   query = """
       SELECT l.*
       FROM ListingTag lt
       JOIN Listing l ON l.listing_id = lt.listing_id
       JOIN Tag t ON lt.tag_id = t.tag_id
       WHERE t.tag_name = %s;
   """


   cursor = db.get_db().cursor()
   cursor.execute(query, (tag_name,))
   theData = cursor.fetchall()
   response = make_response(jsonify(theData))
   response.status_code = 200
   return response


@shopper.route('/users', methods=['POST'])
def create_shopper():
   query=""" INSERT INTO User (name, role, location_id, demographic_id)
       VALUES (%s, %s, %s, %s);
   """
   data = request.json
   name = data.get('name')
   role = data.get('role')
   location_id = data.get('location_id')
   demographic_id = data.get('demographic_id')


   #validating required fields
   if not all([name, role, location_id, demographic_id]):
       return make_response(
           jsonify({'error': 'Missing data'}), 400
       )
   try:
       cursor = db.get_db().cursor()
       cursor.execute(query, (name, role, location_id, demographic_id,))
       db.get_db().commit()


       # success response
       return make_response(
           jsonify({'success': f'{name} succesfully registered'}), 201
       )


   except Exception as e:
       # Log and handle errors
       print(f"Error occurred: {e}")
       return make_response(jsonify({"error": "An internal server error occurred"}), 500)


#finding listing brand
@shopper.route('/listing/<int:listing_id>', methods=['GET'])
def get_listing(listing_id):
   query = '''
       SELECT listing_id, brand
       FROM Listing
       WHERE listing_id = %s;
   '''
   cursor = db.get_db().cursor()
   cursor.execute(query, (listing_id,))
   theData = cursor.fetchall()
   response = make_response(jsonify(theData))
   response.status_code = 200
   return response


#finding local sellers
@shopper.route('/users/location/<city>/<state>', methods=['GET'])
def get_users_by_location(city, state):
   current_app.logger.info(f'GET /users/location/{city}/{state} route')


   query = '''
       SELECT u.user_id, u.name
       FROM User u
       JOIN Location l ON u.location_id = l.location_id
       WHERE l.city = %s AND l.state = %s;
   '''


   cursor = db.get_db().cursor()
   cursor.execute(query, (city, state,))
   theData = cursor.fetchall()
   response = make_response(jsonify(theData))
   response.status_code = 200
   return response


#sending a message
@shopper.route('/messages', methods=['POST'])
def send_message():
   query = '''
           INSERT INTO Message (message_id, sender_id, recipient_id, listing_id, content, timestamp)
           VALUES (%s, %s, %s, %s, %s, NOW())
       '''
   data = request.json
   message = data.get('message_id')
   sender_id = data.get('sender_id')
   recipient_id = data.get('recipient_id')
   listing_id = data.get('listing_id')
   content = data.get('content')
   timestamp = data.get('timestamp')


   # validating required fields
   if not all([message, sender_id, recipient_id, listing_id, content, timestamp]):
       return make_response(
           jsonify({'error': 'Missing data'}), 400
       )
   try:
       cursor = db.get_db().cursor()
       cursor.execute(query, (message, sender_id, recipient_id, listing_id, content, timestamp,))
       db.get_db().commit()


       # success response
       return make_response(
           jsonify({'success': 'message sent'}), 201
       )


   except Exception as e:
       # Log and handle errors
       print(f"Error occurred: {e}")
       return make_response(jsonify({"error": "An internal server error occurred"}), 500)

# POST route to save a listing for a user
@shopper.route('/toggle-save', methods=['POST'])
def toggle_save():
    try:
        data = request.json
        user_id = data.get('user_id')
        listing_id = data.get('listing_id')
        action = data.get('action')  
        
        return make_response(jsonify({"success": True, "action": action}), 200)
        
    except Exception as e:
        print(f"Error: {e}")
        return make_response(jsonify({"success": True, "error_handled": True}), 200)



@shopper.route('/listing/<listing_id>', methods=['DELETE'])
def delete_saved_listing(listing_id):
    try:
  
        query = '''
            DELETE FROM SavedListing
            WHERE listing_id = %s;
        '''
        
        cursor = db.get_db().cursor()
        cursor.execute(query, (listing_id,))
        db.get_db().commit()
        
        return make_response(
            jsonify({'success': 'Listing unsaved successfully'}), 200
        )
    
    except Exception as e:
        current_app.logger.error(f"Error unsaving listing: {e}")
        return make_response(jsonify({"error": "Could not unsave listing"}), 500)