import os
from flask import Flask, render_template, send_from_directory, request, jsonify

# Initialize Flask App
app = Flask(__name__)

# Secret key for session management (e.g., flash messages)
# It's recommended to set this as an environment variable for production
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'a-strong-default-secret-key-for-dev')

# --- Routes ---

@app.route('/')
def index():
    """Renders the main landing page."""
    return render_template('index.html')

@app.route('/download')
def download():
    """Handles the APK file download."""
    apk_filename = 'kamil_quran.apk'
    static_folder = os.path.join(app.root_path, 'static')
    apk_path = os.path.join(static_folder, apk_filename)

    if os.path.exists(apk_path):
        return send_from_directory(
            directory=static_folder,
            path=apk_filename,
            as_attachment=True
        )
    else:
        return jsonify({
            "status": "error",
            "message": f"{apk_filename} not found. Please ensure the file exists in the 'static' directory."
        }), 404

@app.route('/contact', methods=['POST'])
def contact():
    """Handles the contact form submission."""
    if request.is_json:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')

        # In a real application, you would email this or save it to a database.
        # For this task, we just print it to the console.
        print("--- New Contact Form Submission ---")
        print(f"Name: {name}")
        print(f"Email: {email}")
        print(f"Message: {message}")
        print("---------------------------------")

        return jsonify({
            "status": "success",
            "message": "Thank you for your message! We will get back to you soon."
        })
    else:
        return jsonify({
            "status": "error",
            "message": "Invalid request format. Please send JSON."
        }), 400

# --- Main Execution ---

if __name__ == '__main__':
    # Debug mode should be OFF in production
    app.run(debug=False, port=5000)
    app.run(debug=True, port=5000)

# --- PythonAnywhere WSGI Configuration Notes ---
#
# To deploy this application on PythonAnywhere:
#
# 1. Upload all project files (app.py, requirements.txt, templates/, static/)
#    to a directory in your PythonAnywhere account, e.g., /home/YOUR_USERNAME/kamil_quran_website
#
# 2. Go to the "Web" tab on your PythonAnywhere dashboard and create a new web app.
#    - Choose "Manual configuration" and select the Python version (e.g., Python 3.10).
#
# 3. Edit the WSGI configuration file. You can find the link to this file in the "Code"
#    section of the "Web" tab. Replace its contents with the following, making sure to
#    update 'YOUR_USERNAME' and the path to your project directory:
#
#    import sys
#    # The path to your project directory
#    path = '/home/YOUR_USERNAME/kamil_quran_website'
#    if path not in sys.path:
#       sys.path.insert(0, path)
#
#    # Import the Flask app instance
#    from app import app as application
#
# 4. In the "Virtualenv" section of the "Web" tab, create a virtual environment and
#    install the dependencies from your requirements.txt file:
#    - pip install -r /home/YOUR_USERNAME/kamil_quran_website/requirements.txt
#
# 5. Reload your web app from the "Web" tab. Your site should now be live.
#
# 6. Make sure your static file mappings are correct if you have issues with CSS/JS/images.
#    Go to the "Static files" section and map the URL /static/ to the directory
#    /home/YOUR_USERNAME/kamil_quran_website/static/.
#
