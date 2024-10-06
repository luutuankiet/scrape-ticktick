from flask import Flask, request, jsonify, send_from_directory
import psycopg2
import psycopg2.extras
from helper.source_env import hostname, database, user, password, port, target_schema
import os
from flask_cors import CORS

# Flask app setup
app = Flask(__name__, static_folder='static')

# for nginx
from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1)


# Configure CORS
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins (adjust as needed)

def get_db_connection():
    """Create a new database connection for each request."""
    return psycopg2.connect(
        host=hostname,
        database=database,
        user=user,
        password=password,
        port=port
    )

# Route for serving the index.html file
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

# Route for search
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    connection = None
    try:
        # Create a new connection for this request
        connection = get_db_connection()
        with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            # Safely format schema name into the SQL query
            sql = f"SELECT * FROM {target_schema}.search_gtd(%s);"
            cursor.execute(sql, (query,))
            result = cursor.fetchall()

            # Convert result to JSON
            rows = [dict(row) for row in result]
            return jsonify(rows)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        if connection:
            connection.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=60005)