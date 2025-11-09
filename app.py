from flask import Flask, render_template
import sqlite3
import plotly.graph_objects as go
from plotly.utils import PlotlyJSONEncoder
import json

app = Flask(__name__)

DB_PATH = "API_DATA.db"

@app.route("/")
def index():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT url, response_time, status_code, timestamp FROM api_data ORDER BY id DESC LIMIT 50")
    data = c.fetchall()
    conn.close()

    # --- Prepare data for graph ---
    timestamps = [row[3] for row in data][::-1]
    response_times = [row[1] for row in data][::-1]

    # --- Build Plotly line chart ---
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=timestamps, y=response_times,
        mode="lines+markers",
        name="Response Time (s)"
    ))
    fig.update_layout(
        title="API Response Time Trend",
        xaxis_title="Timestamp",
        yaxis_title="Response Time (seconds)",
        template="plotly_white"
    )
    graph_json = json.dumps(fig, cls=PlotlyJSONEncoder)

    # --- Summary stats ---
    avg_response = round(sum(response_times) / len(response_times), 3) if response_times else 0
    total_calls = len(response_times)

    return render_template("index.html",
                           data=data,
                           graphJSON=graph_json,
                           avg_response=avg_response,
                           total_calls=total_calls)

if __name__ == "__main__":
    app.run(debug=True)

