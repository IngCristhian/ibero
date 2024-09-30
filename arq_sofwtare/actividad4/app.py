from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

def calcular_area(figura, valores):
    if figura == 'circulo':
        radio = float(valores[0])
        return math.pi * radio ** 2
    elif figura == 'cuadrado':
        lado = float(valores[0])
        return lado ** 2
    elif figura == 'triangulo':
        base = float(valores[0])
        altura = float(valores[1])
        return (base * altura) / 2
    else:
        return "Figura no válida"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calcular', methods=['POST'])
def calcular():
    data = request.get_json()
    figura = data['figura']
    valores = data['valores']
    area = calcular_area(figura, valores)
    return jsonify({'resultado': area})

if __name__ == '__main__':
    app.run(debug=True)