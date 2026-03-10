from flask import Flask, jsonify
from app.utils.data_loader import load_all_sheets
import json

app = Flask(__name__)

def df_to_json_ready(df):
    """Helper to convert DataFrame to a dictionary ready for JSON serialization"""
    # Replace NaN/NaT with None for valid JSON
    clean_df = df.fillna("")
    return clean_df.to_dict(orient='records')

@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    """
    Return high-level summary metrics across the sheets.
    """
    data = load_all_sheets()
    
    metrics = {
        "status": "success",
        "available_sheets": list(data.keys()),
        "record_counts": {sheet: len(df) for sheet, df in data.items()}
    }
    
    # Calculate some dynamic metrics if specific sheets exist
    if "Closures Summary" in data:
        closures_df = data["Closures Summary"]
        # Assuming there are columns that look like closures or we just count rows
        pass
        
    return jsonify(metrics)

@app.route('/api/closures', methods=['GET'])
def get_closures():
    """
    Return closures data.
    """
    data = load_all_sheets()
    if "Closures Summary" in data:
        return jsonify({
            "status": "success",
            "data": df_to_json_ready(data["Closures Summary"])
        })
    else:
        return jsonify({"status": "error", "message": "Closures Summary sheet not found."}), 404

@app.route('/api/performance', methods=['GET'])
def get_performance():
    """
    Return behavioral or combined performance data.
    """
    data = load_all_sheets()
    if "Behavioral Metrics" in data:
        return jsonify({
            "status": "success",
            "data": df_to_json_ready(data["Behavioral Metrics"])
        })
    else:
        # Fallback to general metrics if exact sheet doesn't exist
        return jsonify({"status": "error", "message": "Behavioral Metrics sheet not found."}), 404

@app.route('/api/all', methods=['GET'])
def get_all_data():
    """
    Return all sheets data.
    """
    data = load_all_sheets()
    json_data = {sheet: df_to_json_ready(df) for sheet, df in data.items()}
    return jsonify({
        "status": "success",
        "data": json_data
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
