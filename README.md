Flask Wrapper

A lightweight, feature-rich wrapper for Flask that simplifies common operations while maintaining Flask's flexibility.
Features

    Automatic Logging: Request/response logging with timing information
    Standardized Error Handling: Consistent error responses across your application
    Middleware Support: Easy registration of middleware functions
    Simplified JSON Responses: Helper methods for standardized API responses
    Blueprint Support: Maintain Flask's blueprint functionality
    Minimal Overhead: Thin wrapper that preserves Flask's performance

Installation

pip install flask-wrapper

Or clone this repository:

git clone https://github.com/yourusername/flask-wrapper.git
cd flask-wrapper
pip install -e .

Quick Start

from flask_wrapper import FlaskWrapper
from flask import request

# Create a Flask application using the wrapper
app = FlaskWrapper(__name__)

# Define routes using the wrapper
@app.route('/', methods=['GET'])
def hello_world():
    return app.json_response({"message": "Hello, World!"})

@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    # Simulate getting a user
    user = {"id": user_id, "name": "Example User"}
    return app.json_response(user)

@app.route('/users', methods=['POST'])
def create_user():
    # Get JSON data from request
    data = request.get_json()
    
    # Validate data
    if not data or 'name' not in data:
        return app.json_response({"error": "Name is required"}, 400)
    
    # Simulate creating a user
    user = {"id": "123", "name": data['name']}
    return app.json_response(user, 201)

# Run the application
if __name__ == '__main__':
    app.run(debug=True)

Adding Middleware

@app.add_middleware
def auth_middleware():
    # Example middleware that checks for an API key
    api_key = request.headers.get('X-API-Key')
    if not api_key and request.path != '/':
        return app.json_response({"error": "API key required"}, 401)

Using Blueprints

from flask import Blueprint, request

# Create a blueprint
api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/status', methods=['GET'])
def status():
    return {"status": "operational"}

# Register the blueprint with the wrapper
app.register_blueprint(api)

Configuration

config = {
    'SECRET_KEY': 'your-secret-key',
    'JSON_SORT_KEYS': False,
    'JSONIFY_PRETTYPRINT_REGULAR': True
}

app = FlaskWrapper(__name__, config=config)

Advanced Usage
Custom Error Handlers

@app.app.errorhandler(404)
def custom_not_found(error):
    return app.json_response({
        "error": "Resource not found",
        "status_code": 404,
        "details": "The requested URL was not found on the server"
    }, 404)

Accessing the Underlying Flask App

# You can access the underlying Flask app directly
@app.app.before_first_request
def before_first_request():
    print("This runs before the first request!")

Why Use Flask Wrapper?

    Consistency: Enforce consistent patterns across your Flask applications
    Productivity: Reduce boilerplate code for common operations
    Maintainability: Centralize cross-cutting concerns like logging and error handling
    Simplicity: Keep the simplicity of Flask while adding helpful utilities

Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

    Fork the repository
    Create your feature branch (git checkout -b feature/amazing-feature)
    Commit your changes (git commit -m 'Add some amazing feature')
    Push to the branch (git push origin feature/amazing-feature)
    Open a Pull Request

