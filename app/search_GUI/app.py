from flask import Flask, request, jsonify, send_from_directory
import psycopg2
import psycopg2.extras
from helper.source_env import hostname, database, user, password, port, target_schema
import os
from flask_cors import CORS

# Flask app setup
app = Flask(__name__, static_folder='static')

# Database connection configuration
connection = psycopg2.connect(
    host=hostname,
    database=database,
    user=user,
    password=password,
    port=port
)


# Configure CORS
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins (adjust as needed)


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

    try:
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=60005)