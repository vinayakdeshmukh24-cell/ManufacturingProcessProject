# Run & Debug the Logic Minimizer in VS Code

This document shows quick steps to run the logic minimizer app from inside VS Code and optionally preview it in a Webview or external browser.

## Prerequisites
- Python 3.11+ and a virtual environment in `.venv`
- The Python extension for VS Code
- Streamlit and required packages installed (see `requirements.txt`) — we've included `sympy` for minimization

## Install dependencies
Open a PowerShell terminal in your project root and run:

```powershell
& ".\.venv\Scripts\Activate.ps1"
& ".\.venv\Scripts\python.exe" -m pip install -r requirements.txt
```

## Run from VS Code (tasks)
1. Press `Ctrl+Shift+P` → `Tasks: Run Task` → select `Run Streamlit Logic App`.
2. Open `http://localhost:8501` in your browser, or run the `Open Logic App in Browser` task.

This task uses the same venv Python executable and runs Streamlit.

## Run using debugger
1. Press `F5` (or `Run` → `Start Debugging`) and choose `Run Streamlit (logic app)`.
2. This will run `streamlit run streamlit_logic_app.py` in a debug session and you can set breakpoints in `streamlit_logic_app.py`.

## Preview inside VS Code (optional)
You can build a small VS Code Webview extension that loads `http://localhost:8501` in a webview panel. This is a little advanced — if you want it, I can scaffold the extension for you. For now the simple workflow is:
1. Start the Streamlit app in a terminal or with the task above.
2. Open the browser at `http://localhost:8501`.

## CI / Deploy from VS Code (optional)
- To deploy from VS Code, add a `render.yaml` or GitHub Action and push to your remote; then create a service on Render / Streamlit Cloud.
- I can automate that pipeline if you want.

If you'd like a one-click extension that opens the Streamlit app inside VS Code, say so and I'll scaffold the extension and add it to this repo.
