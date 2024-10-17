from flask import Flask, render_template
from models import get_data

app = Flask(__name__)

@app.route('/')
def home():
    data = get_data()  # Esto simula datos del modelo
    return render_template('home.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)