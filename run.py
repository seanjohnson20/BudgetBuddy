#from pocoo_test import *
from routes import app
from flask import Flask
from waitress import serve


    
if __name__ == "__main__":
    app.run(debug=True)
    #serve(app, host='0.0.0.0', port='5000')   
