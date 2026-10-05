"""
=============================================================================
TECNOLÓGICO NACIONAL DE MÉXICO - INSTITUTO TECNOLÓGICO SUPERIOR DE URUAPAN
DIVISIÓN DE ESTUDIOS DE POSGRADO E INVESTIGACIÓN
MAESTRÍA EN INTELIGENCIA ARTIFICIAL

Materia: Inteligencia Artificial y su Ética
Actividad 17: PLN - Chatbot de Atención al Cliente (Gradio & CLI App)
Alumno: Juan Pablo Figueroa Moran (Matrícula: M26040059)
=============================================================================
"""

import sys
import json
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


def iniciar_interfaz_gradio(bot: ChatbotNLU):
    try:
        import gradio as gr
    except ImportError:
        print("[!] Gradio no está instalado. Ejecutando en modo consola interactiva...")
        iniciar_modo_consola(bot)
        return

    def responder(mensaje, historial):
        if not mensaje:
            return "", historial
        tag, conf, respuesta = bot.clasificar_intencion(mensaje)
        detalles = f"{respuesta}\n\n*(NLU Tag: `{tag}` | Confianza: `{conf*100:.1f}%`)*"
        historial = historial or []
        historial.append((mensaje, detalles))
        return "", historial

    with gr.Blocks(title="Chatbot de Atención al Cliente - TecNM / ITSU", theme=gr.themes.Soft()) as demo:
        gr.Markdown(
            """
            # 🤖 Asistente Virtual de Atención al Cliente
            ### Maestría en Inteligencia Artificial — Asignatura: Inteligencia Artificial y su Ética
            **Alumno:** Juan Pablo Figueroa Moran (M26040059)
            
            *Motor NLU Híbrido: RegEx + Similitud Cosenoidal TF-IDF con umbral de fallback del 60%.*
            """
        )
        
        chatbot = gr.Chatbot(label="Historial de Conversación", height=420)
        
        with gr.Row():
            txt_input = gr.Textbox(
                show_label=False,
                placeholder="Escribe tu consulta aquí (ej. '¿dónde está mi pedido?', 'facturación', 'métodos de pago')...",
                scale=8
            )
            btn_enviar = gr.Button("Enviar", variant="primary", scale=2)

        txt_input.submit(responder, [txt_input, chatbot], [txt_input, chatbot])
        btn_enviar.click(responder, [txt_input, chatbot], [txt_input, chatbot])

        gr.Markdown("---")
        gr.Markdown("### ⭐ Evaluación de Calidad del Servicio")
        with gr.Row():
            slider_rating = gr.Slider(minimum=1, maximum=5, step=1, value=5, label="Satisfacción del Usuario (1 a 5 Estrellas)")
            txt_comentario = gr.Textbox(placeholder="Comentarios adicionales opcionales...", label="Comentarios")
            btn_evaluar = gr.Button("Registrar Calificación", variant="secondary")

        lbl_resultado = gr.Label(label="Estado del Registro")
        btn_evaluar.click(registrar_satisfaccion, [slider_rating, txt_comentario], [lbl_resultado])

    print("[*] Iniciando servidor web de Gradio en http://127.0.0.1:7860 ...")
    demo.launch(server_name="127.0.0.1", server_port=7860, share=False)


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


def main():
    bot = ChatbotNLU()
    if "--cli" in sys.argv:
        iniciar_modo_consola(bot)
    else:
        iniciar_interfaz_gradio(bot)

if __name__ == "__main__":
    main()
