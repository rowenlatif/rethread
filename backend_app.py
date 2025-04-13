###
# Main application interface
###

#importing create app function
from backend.rest_entry import create_app

#c
app = create_app()

if __name__ == '__main__':
    # run in debug mode
    # this app will be bound to port 4000
    app.run(debug=True, host = '0.0.0.0', port = 4000)