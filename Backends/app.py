
from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
# Enable CORS so React (localhost:3000) can securely request data from Flask (localhost:5000)
CORS(app) 

@app.route('/api/sentiment-data', methods=['GET'])
def get_sentiment_data():
    try:
        # 1. Read the CSV file you generated earlier
        df = pd.read_csv('analyzed_social_data.csv')
        
        # 2. Count how many Positive, Neutral, and Negative posts there are
        counts = df['sentiment'].value_counts().to_dict()
        
        # 3. Format the data exactly how our React Recharts library expects it
        formatted_data = [
            {"name": "Positive", "count": counts.get("Positive", 0)},
            {"name": "Neutral", "count": counts.get("Neutral", 0)},
            {"name": "Negative", "count": counts.get("Negative", 0)}
        ]
        
        # 4. Send the JSON response to the frontend
        return jsonify(formatted_data)
        
    except FileNotFoundError:
        return jsonify({"error": "Data file not found. Run the analysis script first."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting Flask server on http://localhost:5000")
    app.run(debug=True, port=5000)