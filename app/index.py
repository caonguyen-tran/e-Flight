from app import app
from flask import redirect, render_template


@app.route('/', methods=['get'])
def index():
    return render_template('index.html')


if __name__ == "__main__":
    from app import admin
    app.run()
