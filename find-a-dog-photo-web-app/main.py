# --- import Flask library boilerplate ---
# --- import Flask render_template module to enable Flask to configure Jinja to insert content into HTML template ---
# --- import Flask request module wh holds data client sends to the app (POST data and URL parameters) ---
from flask import Flask, render_template, request

# --- import Flask requests library wh allows app to request data from other sites. has built-in methods to GET, POST, and DELETE data from a server ---
import requests

#imports a dictionary of data from dog_breeds.py and "prettifies", or styles, the dog names when they appear in the HTML page
from dog_breeds import prettify_dog_breed

app = Flask("app")

#function adds a dash in the URL between breed names with multiple words like miniature poodle
def check_breed(breed):
  return "/".join(breed.split("-"))

# --- routes ---
@app.route("/", methods = ["GET", "POST"])
def dog_image_gallery():
  errors = []
  if request.method == "POST":
# --- "breed" is the drop down menu in the HTML ---
    breed = request.form.get("breed")
    number = request.form.get("number")
# --- if a breed not selected ---
    if not breed:
# --- appending empty errors list ---
      errors.append("Oops! Please choose a breed.")
    if not number:
      errors.append("Oops! Please choose a number.")
        
    if breed and number:
# --- building URL for GET request ---
      response = requests.get("https://dog.ceo/api/breed/" + check_breed(breed) + "/images/random/" + number)

# --- API returns data as a request object ---
# --- request object includes JSON file ---
# --- data stores JSON file converted to dictionary. response.json method converts ---
      data = response.json()

# --- dog_images variable holds data dictionary with "message" as key
      dog_images = data["message"]

# --- calling the prettify function, setting images to hold the dog_images dictionary data, setting breed to hold the dog breed from the POST request ---
      return render_template("dogs.html", images = dog_images, breed = prettify_dog_breed(breed), errors = [])
# --- handle the HTML template rendering when no dropdown selection has been made yet ---
  return render_template("dogs.html", images = [], breed = "", errors = errors)

@app.route("/random", methods = ["POST"])
def get_random():
  response = requests.get("https://dog.ceo/api/breeds/image/random")
  data = response.json()
  dog_images = [data["message"]]
  return render_template("dogs.html", images = dog_images)


app.debug = True
app.run(host='0.0.0.0', port=8080)