from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def Index():
    return render_template("index.html")

@app.route("/Summerize", methods=["GET", "POST"])
def Summerize():
    if request.method == "POST":
        try:
            API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
            headers = {"Authorization": "Bearer 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"}

            maxL = int(request.form["maxL"])
            minL = maxL // 4
            data = request.form["data"]

            print(f"maxL: {maxL}, minL: {minL}, data: {data}")

            def query(payload):
                response = requests.post(API_URL, headers=headers, json=payload)
                response.raise_for_status()  # Raise an error for bad status codes
                return response.json()

            output = query({
                "inputs": data,
                "parameters": {"min_length": minL, "max_length": maxL},
            })[0]

            print(f"API Output: {output}")

            return render_template("index.html", result=output["summary_text"], mini=minL)
        except requests.exceptions.RequestException as e:
            print(f"HTTP Request failed: {e}")
            return render_template("index.html", error="API request failed. Please check the API and try again.")
        except Exception as e:
            print(f"Error: {e}")
            return render_template("index.html", error=str(e))
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.debug = True
    app.run()
