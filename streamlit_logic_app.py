import streamlit as st
import pandas as pd
import itertools
import re
from sympy import symbols, simplify_logic, sympify


# ------------------ Helper functions (adapted from your script) ------------------
def extract_variables(expression: str):
    tokens = re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", expression)
    keywords = {"and", "or", "not", "True", "False"}
    variables = sorted(set([t for t in tokens if t not in keywords]))
    return variables


def generate_truth_combinations(variables):
    return list(itertools.product([True, False], repeat=len(variables)))


def evaluate_expression(expression: str, variables, combinations):
    truth_results = []

    # normalize logical operators to python boolean operators
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
        except Exception as e:
            # bubble up the exception to the caller
            raise ValueError(f"Error evaluating expression: {e}")
        truth_results.append(result)

    return truth_results


def build_truth_table_df(variables, combinations, results):
    rows = []
    for combo, res in zip(combinations, results):
        row = {var: int(val) for var, val in zip(variables, combo)}
        row["RESULT"] = int(res)
        rows.append(row)

    df = pd.DataFrame(rows)
    return df


def check_expression_type(results):
    if all(results):
        return "Tautology (Always TRUE)"
    elif not any(results):
        return "Contradiction (Always FALSE)"
    else:
        return "Contingent (Sometimes TRUE, Sometimes FALSE)"


def minimize_expression(expr, variables):
    # Convert Python boolean operators to sympy style
    expr_sympy = sympify(expr.replace("and", "&").replace("or", "|").replace("not", "~"))
    try:
        minimized = simplify_logic(expr_sympy, force=True)
    except Exception as e:
        # return the original or a helpful message
        minimized = f"(could not minimize: {e})"
    return minimized


# ------------------ Streamlit UI ------------------
st.set_page_config(page_title="Logic Minimizer & Truth Table", layout="centered")

st.title("Logic Minimizer & Truth Table")
st.markdown("Enter a logical expression using variables (letters, digits, underscores) and operators: and, or, not. You can also use ∧ ∨ ¬ or ^ for convenience.")

expr_input = st.text_area("Logical expression", value="p and (not q) or r", height=120)

if st.button("Analyze"):
    expr = expr_input.strip()
    if not expr:
        st.error("Please enter a logical expression.")
    else:
        try:
            variables = extract_variables(expr)
            st.subheader("Detected variables")
            if variables:
                st.write(variables)
            else:
                st.info("No variables detected. Try using names like p, q, r or x1, a_b.")

            combinations = generate_truth_combinations(variables)

            results = evaluate_expression(expr, variables, combinations)

            df = build_truth_table_df(variables, combinations, results)

            st.subheader("Truth Table")
            st.dataframe(df)

            st.download_button("Download truth table (CSV)", df.to_csv(index=False), file_name="truth_table.csv", mime="text/csv")

            status = check_expression_type(results)
            st.success(f"Expression type: {status}")

            st.subheader("Minimized expression (SymPy)")
            minimized = minimize_expression(expr, variables)
            st.code(str(minimized))

        except Exception as exc:
            st.error(str(exc))

st.markdown("---")
st.markdown("Tips: Use parentheses for grouping. Example expressions:\n- p and q\n- p or (not q)\n- (a and b) or c")
