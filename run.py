from routes import app
from flask import Flask
from waitress import serve
import os

if __name__ == "__main__":
    app.run(debug=True)   # uncomment for flask server
    #serve(app, host='0.0.0.0', port='5000')   # uncomment for waitress server
    
    #port = int(os.environ.get('PORT', 5000))     # uncomment for Heroku server
    #app.run(host='0.0.0.0', port=port, debug=True) # uncomment for Heroku server