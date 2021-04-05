from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import MarsApp


# Flask Setup
app = Flask(__name__)

# Create connection variable
#conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
#client = pymongo.MongoClient(conn)

# Use flask_pymongo to set up mongo connection
#app.config["MONGO_URI"] = "mongodb://localhost:27017/MarsApp"
#mongo = PyMongo(app)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")
# Connect to a database. Will create one if not already available.
#db = client.mars_db
#collection = db.mars_data

@app.route("/")
def index():
    mars_dict = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars_dict)

#@app.route("/")
#def index():
#    mars = mongo.db.mars.find_one()
#    return render_template("index.html", mars=mars)

@app.route("/scrape")
def scraper():
    mars = MarsApp.scrape_info()
    mongo.db.collection.update({}, mars, upsert=True)
    return redirect("/")
   
#@app.route("/scrape")
#def scraper():
#    mars = mongo.db.mars
#    mars_data = MarsApp.scrape()
#    mars.update({}, mars_data, upsert=True)
#    return redirect("/", code=302)    

if __name__ == "__main__":
    app.run(debug=True)
