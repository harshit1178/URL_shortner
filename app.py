from flask import Flask, render_template, request, redirect, url_for   
import database
import utils
import qrcode
import io
import base64

app=Flask(__name__)

# Trigger database initialization when the app starts up
database.init_db()

@app.route("/", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])

@app.route("/", methods=["GET", "POST"])

@app.route("/", methods=["GET", "POST"])
def home():
    short_url = None
    error = None
    qr_base64 = None  # Holds our dynamic image data string
    
    if request.method == "POST":
        original_url = request.form.get("long_url").strip()
        custom_alias = request.form.get("custom_alias").strip()
        if original_url and "." in original_url:
            if not original_url.startswith("http://") and not original_url.startswith("https://"):
                original_url = "https://" + original_url

            if custom_alias:
                # Clean up the alias (remove spaces or slashes if any)
                custom_alias = custom_alias.replace(" ", "-")
                
                # Check database memory to see if it's already taken
                if database.is_alias_taken(custom_alias):
                    error = f"The alias '{custom_alias}' is already taken! Please try another one."
                else:
                    # It's unique! Use the custom alias as our code identifier
                    database.save_url(custom_alias, original_url, is_custom=1)
                    short_url = request.host_url + custom_alias
            else:
                # No custom alias provided? Proceed with standard duplicate check + random code generator
                existing_code = database.check_duplicate_url(original_url)
                if existing_code:
                    short_url = request.host_url + existing_code
                else:
                    code = utils.generate_short_code()
                    database.save_url(code, original_url, is_custom=0)
                    short_url = request.host_url + code

            # 📱 DYNAMIC ENGINE: If a short URL was successfully created, generate its QR code
            if short_url:
                # 1. Create the QR Code object
                qr = qrcode.QRCode(version=1, box_size=10, border=2)
                qr.add_data(short_url)
                qr.make(fit=True)
                
                # 2. Compile it as an image in RAM memory using Pil
                img = qr.make_image(fill_color="black", back_color="transparent")
                
                # 3. Stream the image bytes into a virtual memory buffer
                buffer = io.BytesIO()
                img.save(buffer, format="PNG")
                
                # 4. Convert those raw bytes into a Base64 text string for HTML rendering
                qr_base64 = base64.b64encode(buffer.getvalue()).decode()
                
        else:
            error = "Please enter a valid URL structure (e.g., website.com)!"
            
    return render_template("index.html", short_url=short_url, error=error, qr_base64=qr_base64)

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

@app.route("/analytics")
def analytics():
    #  list of all URLs from the database memory
    all_links = database.get_all_urls()
    
    # 2. Pass that list 
    return render_template("analytics.html", links=all_links)

@app.route("/delete/<short_code>")
def delete_link(short_code):
    database.delete_url(short_code)
    return redirect("/analytics")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    
