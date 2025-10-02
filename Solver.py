from sympy import symbols, sympify, integrate, diff, solve

x = symbols('x')

def predict_problem_type(equation):
    if 'integrate' in equation or '∫' in equation:
        return 'integration'
    elif "'" in equation or 'diff' in equation:
        return 'derivative'
    elif '=' in equation:
        return 'equation'
    return 'auto'

def solve_equation(equation, problem_type='auto'):
    try:
        expr = sympify(equation)
        if problem_type == 'integration':
            return str(integrate(expr, x))
        elif problem_type == 'derivative':
            return str(diff(expr, x))
        elif problem_type == 'equation':
            return str(solve(expr, x))
        else:
            return str(expr.evalf())
    except Exception as e:
        return f"❌ Error: {e}"
      
