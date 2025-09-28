# 🏥 Simulador THERAC-25 - Educación en Calidad de Software

**Propósito Educativo:** Demostrar cómo los errores de software pueden tener consecuencias mortales y la importancia de las herramientas modernas de calidad.

## ⚡ Inicio Rápido

### 🌐 Interfaz Web (Recomendado)
```bash
# Ejecutar simulador con interfaz web en español
docker-compose up therac_web

# Acceder en: http://localhost:8080
```

### 🔧 Desarrollo Local
```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar interfaz web
python src/web_interface/app.py
```

## 🎯 Funcionalidades

### ✅ **Interfaz Web Completa**
- **Panel de control** en español con campos intuitivos
- **Simulación en tiempo real** de la máquina Therac-25
- **Logs detallados** de eventos y errores
- **Reproducción de bugs históricos** que causaron muertes

### 🐛 **Bugs Históricos Simulados**
1. **Race Condition**: Cambios rápidos X-ray ↔ Electron sin sincronización
2. **Counter Overflow**: Contador de 8 bits que bypasea seguridad tras 256 usos
3. **Edit Race Condition**: Edición durante operación corrompe configuración

### 🔬 **Pipeline de Calidad Integrado**
- **Docker**: Contenedor optimizado
- **Análisis Estático**: Pylint, SonarCloud
- **Seguridad**: OWASP, Bandit, Safety
- **Pruebas**: Pytest con cobertura
- **Carga**: k6 para detectar condiciones de carrera

## 🚨 Reproducir Accidentes Históricos

### **1. Race Condition Mortal**
1. Configura: 200 cGy, posición (10, 15)
2. Cambia rápidamente: Rayos X → Electrones → Rayos X
3. Dispara mientras la mesa se mueve
4. **Resultado histórico**: Sobredosis de 25,000 rads = muerte

### **2. Counter Overflow Bug**
1. Click "Configurar Tratamiento" 256 veces consecutivas
2. Observa contador reseteo a 0
3. Controles de seguridad deshabilitados
4. **Resultado histórico**: Bypass total de validaciones

### **3. Edit Race Condition**
1. Configura tratamiento
2. Cambia modo inmediatamente
3. Usa "Edición Rápida" para modificar dosis
4. **Resultado histórico**: Configuración parcial corrupta

## 📊 Herramientas de Calidad

```bash
# Ejecutar pipeline completo
gh workflow run quality-pipeline.yml

# Análisis local
pylint src/simulator/
pytest src/tests/ --cov=src/simulator
bandit -r src/
```

## 🎓 Valor Educativo

**Demostración práctica de que:**
- Cada muerte del Therac-25 era **100% prevenible**
- Las herramientas modernas **habrían detectado todos los bugs**
- La calidad del software **salva vidas** en sistemas críticos

## ⚙️ Arquitectura

```
src/
├── web_interface/     # Interfaz web Flask (Español)
├── simulator/         # Lógica core con bugs reproducidos
└── tests/            # Suite completa de pruebas

docker/               # Configuración Docker optimizada
quality/             # Scripts k6 y herramientas de calidad
.github/workflows/   # Pipeline CI/CD automatizado
```

## 🤝 Contribuciones

Este proyecto es para **educación en calidad de software**. Las contribuciones deben mantener los bugs históricos para valor educativo.

## ⚠️ Advertencia

**SOLO PARA EDUCACIÓN.** Los bugs reproducidos mataron pacientes reales. Este simulador demuestra la importancia crítica de la calidad en software médico.

---
*💀 En memoria de las víctimas del Therac-25: Que sus tragedias sirvan para prevenir futuras muertes por errores de software.*