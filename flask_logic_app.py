from flask import Flask, render_template, request, redirect, url_for
import itertools
import re
from sympy import sympify, simplify_logic

app = Flask(__name__)


def extract_variables(expression: str):
    tokens = re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", expression)
    keywords = {"and", "or", "not", "True", "False"}
    variables = sorted(set([t for t in tokens if t not in keywords]))
    return variables


def generate_truth_combinations(variables):
    return list(itertools.product([True, False], repeat=len(variables)))


def evaluate_expression(expression: str, variables, combinations):
    truth_results = []
    expr = (
        expression.replace("^", " and ")
        .replace("∨", " or ")
        .replace("∧", " and ")
        .replace("¬", " not ")
    )
    for combo in combinations:
        local_dict = dict(zip(variables, combo))
        try:
            result = bool(eval(expr, {}, local_dict))
        except Exception:
            result = None
        truth_results.append(result)
    return truth_results


def build_truth_table(variables, combinations, results):
    rows = []
    for combo, res in zip(combinations, results):
        row = {var: int(val) for var, val in zip(variables, combo)}
        row['RESULT'] = None if res is None else int(res)
        rows.append(row)
    return rows


def minimize_expression(expr):
    expr_sympy = sympify(expr.replace("and", "&").replace("or", "|").replace("not", "~"))
    try:
        return simplify_logic(expr_sympy, force=True)
    except Exception as e:
        return f"(could not minimize: {e})"


@app.route('/', methods=['GET'])
def home():
    return render_template('logic.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    expr = request.form.get('expression', '').strip()
    if not expr:
        return redirect(url_for('home'))

    variables = extract_variables(expr)
    combinations = generate_truth_combinations(variables)
    results = evaluate_expression(expr, variables, combinations)
    table = build_truth_table(variables, combinations, results)

    if all(r is True for r in results):
        expr_type = 'Tautology'
    elif all(r is False for r in results):
        expr_type = 'Contradiction'
    else:
        expr_type = 'Contingent'

    minimized = minimize_expression(expr)

    return render_template('result.html', expression=expr, variables=variables, table=table, expr_type=expr_type, minimized=minimized)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
