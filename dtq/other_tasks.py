from dtq.app import app


@app.task
def hello():
    return "Hello, from other queue."
