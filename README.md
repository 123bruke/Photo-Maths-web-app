# creating simple  photo maths web app

import io
import os
import uuid

from flask import Flask, request, render_template_string
from PIL import Image, ImageOps
import pytesseract
import sympy as sp
import numpy as np
import matplotlib
matplotlib.use("Agg")  # Needed so matplotlib works without a display (server-safe)
import matplotlib.pyplot as plt


# --- SETUP FLASK APP ---
app = Flask(__name__)

# Make sure we have a "static" folder to save graphs
os.makedirs("static", exist_ok=True)


#  HTML PAGE (frontend) 
# This is the web interface (a very simple page).
TEMPLATE = """
<!doctype html>
<html>
<head>
    <title>PhotoMath Flask</title>
</head>
<body>
    <h2>📸 Welcome to PhotoMath Flask</h2>
    <p>Upload a math equation photo and choose an operation:</p>

    <form method="post" enctype="multipart/form-data">
        <input type="file" name="photo" required>
        <select name="action">
            <option value="auto">Auto (Everything)</option>
            <option value="derivative">Derivative</option>
            <option value="integral">Integral</option>
            <option value="domain">Domain & Range</option>
        </select>
        <button type="submit">🔍 Analyze</button>
    </form>

    {% if ocr %}
        <h4>📄 OCR Extracted Text</h4>
        <pre>{{ ocr }}</pre>
    {% endif %}

    {% if result %}
        <h4>✅ Result</h4>
        <pre>{{ result }}</pre>
    {% endif %}

    {% if plot %}
        <h4>📊 Graph</h4>
        <img src="{{ plot }}" width="400">
    {% endif %}
</body>
</html>
"""


#  main  FUNCTIONS 

def clean_text(txt):
    """
    Clean up OCR text so Sympy can understand it.
    Example: replace weird characters like − with - and ^ with **.
    """
    return (
        txt.replace("−", "-")
           .replace("^", "**")
           .replace("÷", "/")
           .strip()
    )


def plot_expression(expr, var):
    """
    Create a graph for the given math expression.
    Save it as a PNG inside 'static/' and return the file path.
    """
    xs = np.linspace(-10, 10, 400)  # X-axis values
    f = sp.lambdify(var, expr, "numpy")  # Convert sympy -> numpy function
    ys = f(xs)

    plt.figure()
    plt.axhline(0, color="black")  # X-axis
    plt.axvline(0, color="black")  # Y-axis
    plt.plot(xs, ys, label=str(expr))
    plt.legend()
    plt.grid(True)

    filename = f"static/{uuid.uuid4().hex}.png"
    plt.savefig(filename)
    plt.close()

    return "/" + filename


# FLASK ROUTE

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    ocr_text = None
    plot = None

    if request.method == "POST":
        # 1️⃣ Get uploaded image
        file = request.files["photo"]
        img = Image.open(io.BytesIO(file.read()))

        # 2️⃣ OCR: Convert image to text
        ocr_text = pytesseract.image_to_string(ImageOps.grayscale(img))

        # 3️⃣ Take only the first line (most likely the equation)
        expr_text = clean_text(ocr_text.split("\n")[0])

        # 4️⃣ Turn text into a sympy expression
        expr = sp.sympify(expr_text)

        # 5️⃣ If no variable, assume "x"
        var = list(expr.free_symbols)[0] if expr.free_symbols else sp.Symbol("x")

        # 6️⃣ Check user’s choice
        action = request.form["action"]

        if action == "derivative":
            derivative = sp.diff(expr, var)
            result = f"f' = {derivative}"
            plot = plot_expression(derivative, var)

        elif action == "integral":
            integral = sp.integrate(expr, var)
            result = f"∫f dx = {integral} + C"
            plot = plot_expression(expr, var)

        elif action == "domain":
            domain = sp.calculus.util.continuous_domain(expr, var, sp.S.Reals)
            frange = sp.calculus.util.function_range(expr, var, sp.S.Reals)
            result = f"Domain: {domain}\nRange: {frange}"
            plot = plot_expression(expr, var)

        else:  # Auto mode: show everything
            derivative = sp.diff(expr, var)
            integral = sp.integrate(expr, var)
            result = (
                f"Expression: {expr}\n"
                f"Derivative: {derivative}\n"
                f"Integral: {integral} + C"
            )
            plot = plot_expression(expr, var)

    # Render the page
    return render_template_string(
        TEMPLATE,
        result=result,
        ocr=ocr_text,
        plot=plot
    )


# --- RUN APP ---
if __name__ == "__main__":
    print("🚀 Running PhotoMath Flask on http://127.0.0.1:5000")
    app.run(debug=True)
