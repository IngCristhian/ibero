document.getElementById('figura').addEventListener('change', mostrarInputs);
document.getElementById('formulario').addEventListener('submit', calcularArea);

function mostrarInputs() {
    const figura = document.getElementById('figura').value;
    const inputsDiv = document.getElementById('inputs');
    inputsDiv.innerHTML = ''; // Limpiar inputs anteriores

    if (figura === 'circulo') {
        inputsDiv.innerHTML = `
            <label for="radio">Radio del Círculo:</label>
            <input type="number" id="radio" required>
        `;
    } else if (figura === 'cuadrado') {
        inputsDiv.innerHTML = `
            <label for="lado">Lado del Cuadrado:</label>
            <input type="number" id="lado" required>
        `;
    } else if (figura === 'triangulo') {
        inputsDiv.innerHTML = `
            <label for="base">Base del Triángulo:</label>
            <input type="number" id="base" required>
            <label for="altura">Altura del Triángulo:</label>
            <input type="number" id="altura" required>
        `;
    }
}

function calcularArea(e) {
    e.preventDefault();
    
    const figura = document.getElementById('figura').value;
    let valores = [];
    
    if (figura === 'circulo') {
        valores.push(document.getElementById('radio').value);
    } else if (figura === 'cuadrado') {
        valores.push(document.getElementById('lado').value);
    } else if (figura === 'triangulo') {
        valores.push(document.getElementById('base').value);
        valores.push(document.getElementById('altura').value);
    }

    fetch('/calcular', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ figura: figura, valores: valores })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('resultado').textContent = `El área es: ${data.resultado}`;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}