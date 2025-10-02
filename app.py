from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os

from utils.ocr_extraction import extract_equation_from_image
from utils.math_solver import solve_equation, predict_problem_type

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solve_text', methods=['POST'])
def solve_text():
    eq = request.form['equation']
    prob_type = predict_problem_type(eq)
    result = solve_equation(eq, prob_type)
    return render_template('index.html', result=result)

@app.route('/solve_image', methods=['POST'])
def solve_image():
    file = request.files['image']
    filename = secure_filename(file.filename)
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(path)

    equation = extract_equation_from_image(path)
    prob_type = predict_problem_type(equation)
    result = solve_equation(equation, prob_type)
    return render_template('index.html', result=f"📷 Detected: {equation} → {result}")

if __name__ == '__main__':
    app.run(debug=True)
  
