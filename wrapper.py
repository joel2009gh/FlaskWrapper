from flask import Flask, request, jsonify
import logging
import time
import traceback
from functools import wraps
from typing import Callable, Dict, Any, Optional, Union, List, Type

class FlaskWrapper:
    def __init__(self, name: str = __name__, config: Optional[Dict[str, Any]] = None):
        """Initialize the Flask wrapper with optional configuration."""
        self.app = Flask(name)
        
        # Configure the Flask app
        if config:
            self.app.config.update(config)
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(name)
        
        # Register error handlers
        self._register_error_handlers()
    
    def _register_error_handlers(self):
        """Register default error handlers."""
        @self.app.errorhandler(404)
        def not_found(error):
            return jsonify({"error": "Resource not found", "status_code": 404}), 404
        
        @self.app.errorhandler(500)
        def server_error(error):
            return jsonify({"error": "Internal server error", "status_code": 500}), 500
        
        @self.app.errorhandler(Exception)
        def handle_exception(e):
            self.logger.error(f"Unhandled exception: {str(e)}")
            self.logger.error(traceback.format_exc())
            return jsonify({"error": "Internal server error", "status_code": 500}), 500
    
    def route(self, rule: str, **options):
        """Decorator for registering a route with additional functionality."""
        def decorator(f):
            @wraps(f)
            def wrapped_function(*args, **kwargs):
                start_time = time.time()
                
                # Log the request
                self.logger.info(f"Request: {request.method} {request.path}")
                
                try:
                    # Call the original function
                    result = f(*args, **kwargs)
                    
                    # Log the response time
                    elapsed_time = time.time() - start_time
                    self.logger.info(f"Response time: {elapsed_time:.4f}s")
                    
                    return result
                except Exception as e:
                    self.logger.error(f"Error in route {rule}: {str(e)}")
                    self.logger.error(traceback.format_exc())
                    raise
            
            # Register the wrapped function with Flask
            endpoint = options.pop('endpoint', None)
            self.app.add_url_rule(rule, endpoint, wrapped_function, **options)
            return wrapped_function
        
        return decorator
    
    def run(self, host: str = '0.0.0.0', port: int = 5000, debug: bool = False, **options):
        """Run the Flask application."""
        self.logger.info(f"Starting Flask application on {host}:{port}")
        self.app.run(host=host, port=port, debug=debug, **options)
    
    def register_blueprint(self, blueprint, **options):
        """Register a Flask blueprint."""
        self.app.register_blueprint(blueprint, **options)
    
    def add_middleware(self, middleware_fn: Callable):
        """Add middleware to the Flask application."""
        self.app.before_request(middleware_fn)
    
    def json_response(self, data: Any, status_code: int = 200) -> Any:
        """Helper method to return a JSON response."""
        return jsonify(data), status_code
