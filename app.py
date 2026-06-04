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

    if request.method == "POST":
        original_url = request.form.get("long_url").strip()
        
        # 1. Core URL Validation: Ensuring it has a domain structure (contains a '.')
        if original_url and "." in original_url:
            
            # 2. Auto-patching missing http/https protocol prefix
            if not original_url.startswith("http://") and not original_url.startswith("https://"):
                original_url = "https://" + original_url

            # 3. Duplicate Check: See if we have already shortened this link before
            existing_code = database.check_duplicate_url(original_url)
            
            if existing_code:
                short_url = request.host_url + existing_code
            else:
                code = utils.generate_short_code()
                database.save_url(code, original_url)
                short_url = request.host_url + code
        else:
            error_message = "Please enter a valid URL structure (e.g., website.com)!"
        
    return render_template("index.html", short_url=short_url, error=error_message)


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
    
