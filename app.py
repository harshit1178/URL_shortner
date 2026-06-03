from flask import Flask, render_template, request, redirect, url_for   
import database
import utils

app=Flask(__name__)

# Trigger database initialization when the app starts up
database.init_db()

@app.route("/", methods=["GET", "POST"])
def home():
    short_url=None
    error_message=None

    if request.method=="POST":
        #extraction of long url from user by the form
        original_url=request.form.get("long_url")

        if original_url:
            # adding https:// if the user forgets to add it
            if not original_url.startswith("http://") and not original_url.startswith("https://"):
                original_url = "https://" + original_url
            
            code = utils.generate_short_code()
            database.save_url(code, original_url)

            #crration of clickable short URL
            short_url = request.host_url + code
        else:
            error_message = "Please enter a valid URL!"
        
    return render_template("index.html", short_url=short_url, error_message=error_message)


@app.route("/<short_code>")
def redirect_to_original(short_code):
    # Asking database.py to find the long URL for this short code
    original_url = database.get_original_url(short_code)
    
    if original_url:
        # Increment the click count for analytics
        database.increment_click(short_code)
        return redirect(original_url)
    
    # If the short code doesn't exist in our DB, show a 404 error
    return "URL Not Found", 404

if __name__ == "__main__":
    app.run(debug=True)
    
