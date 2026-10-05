"""
=============================================================================
TECNOLÓGICO NACIONAL DE MÉXICO - INSTITUTO TECNOLÓGICO SUPERIOR DE URUAPAN
DIVISIÓN DE ESTUDIOS DE POSGRADO E INVESTIGACIÓN
MAESTRÍA EN INTELIGENCIA ARTIFICIAL

Materia: Inteligencia Artificial y su Ética
Actividad 17: PLN - Chatbot de Atención al Cliente (Gradio, CLI & Demo)
Alumno: Juan Pablo Figueroa Moran (Matrícula: M26040059)
=============================================================================
"""

import sys
import json
import time
from datetime import datetime
from nlu_engine import ChatbotNLU

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

FEEDBACK_LOG = "satisfaccion_feedback.json"


def registrar_satisfaccion(estrellas: int, comentario: str = "") -> str:
    registro = {
        "timestamp": datetime.now().isoformat(),
        "calificacion": estrellas,
        "comentario": comentario
    }
    datos = []
    try:
        with open(FEEDBACK_LOG, "r", encoding="utf-8") as f:
            datos = json.load(f)
    except Exception:
        datos = []
    
    datos.append(registro)
    with open(FEEDBACK_LOG, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)
    
    return f"¡Gracias por tu valoración de {estrellas} estrellas! Tu retroalimentación nos ayuda a mejorar."


def ejecutar_demostracion_automatica(bot: ChatbotNLU):
    """Ejecuta una simulación completa de atención al cliente sin bloquear la consola."""
    print("=" * 75)
    print("  TECNM / ITSU - CHATBOT NLU CON FILTROS ÉTICOS Y REGISTRO DE SATISFACCIÓN")
    print("  DEMOSTRACIÓN DE ATENCIÓN AL CLIENTE Y CASOS LÍMITE (FALLBACK)")
    print("=" * 75)

    consultas_prueba = [
        "¿Dónde viene mi paquete con guía #84920?",
        "Quiero devolver un producto que llegó defectuoso",
        "¿Cuáles son los métodos de pago aceptados?",
        "El acelerador cuántico orbital está descalibrado"  # Caso ambiguo para probar fallback
    ]

    for q in consultas_prueba:
        print(f"\nUsuario > {q}")
        tag, conf, respuesta = bot.clasificar_intencion(q)
        print(f"Chatbot > {respuesta}")
        print(f"          [Intención: '{tag}' | Certidumbre NLU: {conf*100:.1f}%]")

    # Registro de satisfacción
    msg_fb = registrar_satisfaccion(5, "Atención rápida y clara.")
    print(f"\n[+] Encuesta de Satisfacción Automatizada: {msg_fb}")

    # Consideración ética
    print("\n" + "=" * 75)
    print("  CONSIDERACIONES ÉTICAS EN AGENTES CONVERSACIONALES")
    print("=" * 75)
    print("  1. Transparencia Algorítmica: El usuario siempre debe saber que interactúa con una IA.")
    print("  2. Derecho de Transferencia: Si la certidumbre es < 60%, se ofrece un agente humano.")
    print("  3. Privacidad: Los mensajes de chat no almacenan datos bancarios ni PII sensible.")
    print("=" * 75)


def iniciar_modo_consola(bot: ChatbotNLU):
    print("=" * 75)
    print("  MODO CONSOLA - ASISTENTE VIRTUAL DE ATENCIÓN AL CLIENTE")
    print("  (Escribe 'salir' para terminar o 'evaluar' para calificar)")
    print("=" * 75)
    
    while True:
        try:
            entrada = input("\nUsuario > ").strip()
            if entrada.lower() in ["salir", "exit", "quit"]:
                print("[*] Sesión finalizada. ¡Hasta pronto!")
                break
            elif entrada.lower() == "evaluar":
                stars = input("Calificación de satisfacción (1 a 5): ").strip()
                coment = input("Comentario opcional: ").strip()
                try:
                    s_int = int(stars)
                    print(registrar_satisfaccion(s_int, coment))
                except ValueError:
                    print("[!] Calificación no válida.")
                continue

            tag, conf, respuesta = bot.clasificar_intencion(entrada)
            print(f"Bot > {respuesta}")
            print(f"      [Intención: '{tag}' | Certidumbre NLU: {conf*100:.1f}%]")
        except (KeyboardInterrupt, EOFError):
            break


def iniciar_interfaz_gradio(bot: ChatbotNLU):
    try:
        import gradio as gr
    except ImportError:
        print("[*] Módulo 'gradio' no disponible. Ejecutando demostración interactiva en consola...")
        ejecutar_demostracion_automatica(bot)
        return

    def responder(mensaje, historial):
        if not mensaje:
            return "", historial
        tag, conf, respuesta = bot.clasificar_intencion(mensaje)
        detalles = f"{respuesta}\n\n*(NLU Tag: `{tag}` | Confianza: `{conf*100:.1f}%`)*"
        historial = historial or []
        historial.append((mensaje, detalles))
        return "", historial

    with gr.Blocks(title="Chatbot de Atención al Cliente - TecNM/ITSU") as demo:
        gr.Markdown("# 🤖 Asistente Virtual Inteligente con NLU\n### Maestría en IA - TecNM / ITSU")
        chatbot = gr.Chatbot(label="Conversación")
        msg = gr.Textbox(label="Tu consulta:", placeholder="Ej: ¿Dónde viene mi pedido?")
        msg.submit(responder, [msg, chatbot], [msg, chatbot])

    demo.launch(server_name="127.0.0.1", server_port=7860, share=False)


def main():
    bot = ChatbotNLU()
    if "--cli" in sys.argv:
        iniciar_modo_consola(bot)
    elif "--gradio" in sys.argv:
        iniciar_interfaz_gradio(bot)
    else:
        # Modo por defecto: demostración completa con métricas
        ejecutar_demostracion_automatica(bot)


if __name__ == "__main__":
    main()
