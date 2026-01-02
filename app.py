from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import openai

from utils.ocr_extraction import extract_equation_from_image
from utils.math_solver import solve_equation, predict_problem_type

openai.api_key = "not_share_know,biruk"

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['upload_f'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def gpt5_explain(equation, result):
    prompt = f"Explain the solution of this math problem in Thai, briefly and clearly:\nEquation: {equation}\nAnswer: {result}"
    response = openai.ChatCompletion.create(
        model="gpt-5-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=100
    )
    return response.choices[0].message['content'].strip()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solve_text', methods=['POST'])
def solve_text():
    eq = request.form['equation']
    prob_type = predict_problem_type(eq)
    result = solve_equation(eq, prob_type)
    explanation = gpt5_explain(eq, result)
    return render_template('index.html', result=result, explanation=explanation)

@app.route('/solve_image', methods=['POST'])
def solve_image():
    file = request.files['image']
    filename = secure_filename(file.filename)
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(path)
    equation = extract_equation_from_image(path)
    prob_type = predict_problem_type(equation)
    result = solve_equation(equation, prob_type)
    explanation = gpt5_explain(equation, result)
    return render_template('index.html', result=f"📷 {equation} → {result}", explanation=explanation)

if __name__ == '__main__':
    app.run(debug=True)
