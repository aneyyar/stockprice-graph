from flask import Flask, render_template, request
import yfinance as yf
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get the stock symbol and date range from the form
        symbol = request.form["symbol"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]

        # Retrieve the historical stock data
        stock = yf.Ticker(symbol)
        data = stock.history(start=start_date, end=end_date)

        # Create a line graph of the closing prices
        plt.plot(data["Close"])
        plt.xlabel("Date")
        plt.ylabel("Closing Price")
        plt.title(symbol + " Stock Price")

        # Save the graph to a buffer
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        graph_url = base64.b64encode(buffer.getvalue()).decode()

        # Render the template with the graph
        return render_template("templates/index.html", graph_url=graph_url)

    # If the request is a GET request, render the template without a graph
    return render_template("templates/index.html")

if __name__ == "__main__":
    app.run(debug=True)