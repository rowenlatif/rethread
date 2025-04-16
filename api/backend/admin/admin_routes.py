from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db




admin = Blueprint('admin', __name__)


@admin.route('/messages', methods=['GET'])
def get_recent_messages():
   query = '''
       SELECT
           m.message_id,
           m.listing_id,
           m.content,
           m.timestamp,
           sender.user_id AS sender_id,
           sender.role AS sender_role,
           recipient.user_id AS recipient_id,
           recipient.role AS recipient_role
       FROM Message m
       JOIN User sender ON m.sender_id = sender.user_id
       JOIN User recipient ON m.recipient_id = recipient.user_id
       ORDER BY m.timestamp DESC
       LIMIT 50;
   '''
   current_app.logger.info(f'GET /messages route')
   cursor = db.get_db().cursor()
   cursor.execute(query)
   theData = cursor.fetchall()
   response = make_response(jsonify(theData))
   response.status_code = 200
   return response


@admin.route('/sellers/activity', methods=['GET'])
def get_seller_activity():
   query = '''
       SELECT
           u.user_id,
           u.role,
           l.listing_id,
           l.title,
           l.timestamp,
           t.transaction_id,
           t.status,
           t.timestamp
       FROM User u
       JOIN Listing l ON u.user_id = l.seller_id
       LEFT JOIN Transaction t ON l.listing_id = t.listing_id
       WHERE u.role = 'seller'
       ORDER BY t.timestamp DESC;
   '''
   current_app.logger.info(f'GET /sellers/activity route')
   cursor = db.get_db().cursor()
   cursor.execute(query)
   theData = cursor.fetchall()
   response = make_response(jsonify(theData))
   response.status_code = 200
   return response


@admin.route('/flags', methods=['GET'])
def get_flagged_content():
   query = '''
       SELECT
           f.flag_id,
           f.content_type,
           f.content_id,
           f.reason,
           f.severity,
           f.created_at,
           u.user_id AS flagged_by
       FROM FlaggedContent f
       JOIN User u ON f.flagged_by = u.user_id
       ORDER BY f.severity DESC, f.created_at DESC;
   '''
   current_app.logger.info(f'GET /flags route')
   cursor = db.get_db().cursor()
   cursor.execute(query)
   theData = cursor.fetchall()
   response = make_response(jsonify(theData))
   response.status_code = 200
   return response


@admin.route('/verifications', methods=['GET'])
def get_user_verifications():
   query = '''
       SELECT
           v.verification_id,
           v.user_id,
           v.method,
           v.status,
           v.verified_at
       FROM Verification v
       ORDER BY v.status, v.verified_at DESC;
   '''
   current_app.logger.info(f'GET /verifications route')
   cursor = db.get_db().cursor()
   cursor.execute(query)
   theData = cursor.fetchall()
   response = make_response(jsonify(theData))
   response.status_code = 200
   return response


@admin.route('/reviews/flagged', methods=['GET'])
def get_low_rated_reviews():
   query = '''
       SELECT
           r.review_id,
           r.reviewer_id,
           r.reviewee_id,
           r.rating,
           r.comment,
           r.created_at
       FROM Review r
       WHERE r.rating <= 2
       ORDER BY r.created_at DESC;
   '''
   current_app.logger.info(f'GET /reviews/flagged route')
   cursor = db.get_db().cursor()
   cursor.execute(query)
   theData = cursor.fetchall()
   response = make_response(jsonify(theData))
   response.status_code = 200
   return response


@admin.route('/groups', methods=['POST'])
def create_group():
   data = request.json
   query = '''
       INSERT INTO `Group` (group_id, created_by, name, type)
       VALUES (%s, %s, %s, %s)
   '''
   cursor = db.get_db().cursor()
   cursor.execute(query, (
       data['group_id'],
       data['created_by'],
       data['name'],
       data['type']
   ))
   db.get_db().commit()
   response = make_response({'message': 'Group created successfully'})
   response.status_code = 201
   return response

@admin.route('/groups/all', methods=['GET'])
def get_all_groups():
   query = '''
       SELECT
           g.group_id,
            g.created_by,
            g.name,
            g.type
        FROM `Group` g
        ORDER BY g.group_id ASC;
   '''
   current_app.logger.info(f'GET /groups/all route')
   cursor = db.get_db().cursor()
   cursor.execute(query)
   theData = cursor.fetchall()
   response = make_response(jsonify(theData))
   response.status_code = 200
   return response
