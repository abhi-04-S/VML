from flask import Flask, render_template, request

app = Flask(__name__)

# Route for handling both GET (viewing the form) and POST (submitting the form)
@app.route("/", methods=["GET", "POST"])
def index():
    # If the user submitted the form
    if request.method == "POST":
        # Extract form inputs using their 'name' attributes
        name = request.form.get("name")
        bio = request.form.get("bio")
        image_url = request.form.get("image_url")
        
        # Simple server-side validation: provide defaults for empty fields
        if not name:
            name = "Anonymous User"
        if not bio:
            bio = "This profile is newly created and does not have a biography yet."
        if not image_url:
            # High-end default avatar from Unsplash
            image_url = "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&q=80&w=250&h=250"
            
        # Render the template with the provided profile data
        return render_template("index.html", name=name, bio=bio, image_url=image_url)
    
    # If it is a GET request, render the template without credentials/profile data
    return render_template("index.html", name=None, bio=None, image_url=None)

if __name__ == "__main__":
    # Start the local development server on port 5000 with auto-reload/debugger active
    app.run(debug=True)
