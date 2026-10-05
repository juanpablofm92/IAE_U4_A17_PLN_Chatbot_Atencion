# Actividad 17: Chatbot de Atención al Cliente (NLU & Gradio)

**Tecnológico Nacional de México**  
**Instituto Tecnológico Superior de Uruapan**  
**División de Estudios de Posgrado e Investigación**  
**Maestría en Inteligencia Artificial**  

* **Asignatura:** Inteligencia Artificial y su Ética  
* **Alumno:** Juan Pablo Figueroa Moran  
* **Matrícula:** M26040059  

---

## 📌 1. Descripción del Proyecto

Este proyecto consiste en un **Agente Conversacional (Chatbot)** de atención y soporte a clientes dotado de un motor NLU (*Natural Language Understanding*) híbrido en Python. El sistema procesa preguntas frecuentes de comercio electrónico y servicios digitales clasificándolas en 8 intenciones canónicas:
1. `saludo`
2. `envios` (rastreo, tiempos, cobertura)
3. `devoluciones` (garantías, reembolsos)
4. `soporte_tecnico` (fallos, firmware, reinicios)
5. `metodos_pago` (tarjetas, MSI, transferencias)
6. `facturacion` (CFDI 4.0, RFC, tickets)
7. `horarios_sucursales` (horarios y tiendas)
8. `contacto_humano` (transferencia a asesor real)

---

## ⚙️ 2. Motor NLU y Regla de Fallback

El procesamiento se compone de tres etapas:
1. **Filtro Determinista (RegEx):** Detección inmediata de expresiones literales y comandos directos.
2. **Clasificación Cosenoidal TF-IDF:** Matriz dispersa de n-gramas (unigramas y bigramas) calculando similitud angular $\cos(\theta) = \frac{\mathbf{u} \cdot \mathbf{v}}{\|\mathbf{u}\|\|\mathbf{v}\|}$.
3. **Umbral de Fallback ($< 60\%$):** Si el vector de usuario no alcanza al menos $0.60$ de afinidad con los patrones del catálogo, el sistema emite una respuesta de aclaración ética solicitando reformulación o derivando al usuario hacia un agente humano.

---

## 🚀 3. Instalación y Ejecución

```bash
pip install -r requirements.txt
```

### Ejecutar interfaz web (Gradio)
```bash
python app.py
```
Abrirá automáticamente la interfaz en `http://127.0.0.1:7860`.

### Ejecutar en consola CLI
```bash
python app.py --cli
```

---

## ⚖️ 4. Consideraciones Éticas en Agentes Conversacionales

1. **Principio de Transparencia:** El sistema declara explícitamente ser un asistente virtual automatizado, evitando engañar al usuario haciéndose pasar por humano (Directrices Éticas para una IA Fiable de la UE).
2. **Vía de Escape a Asesor Humano:** Garantiza siempre una opción clara para transferir al usuario a un agente humano en casos de insatisfacción o problemas complejos.
3. **Registro Ético de Feedback:** Las evaluaciones ⭐ 1-5 se auditan sin almacenar datos personales no autorizados.
