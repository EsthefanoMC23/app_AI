import streamlit as st
import sympy as sp
import plotly.graph_objs as go
import pyttsx3
import speech_recognition as sr
import openai

# Configura tu clave de OpenAI
openai.api_key = "TU_API_KEY_AQUI"

# Inicializa el motor de voz
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def hablar(texto):
    engine.say(texto)
    engine.runAndWait()

def escuchar_microfono():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Escuchando...")
        audio = recognizer.listen(source)
        try:
            texto = recognizer.recognize_google(audio, language='es-ES')
            return texto
        except sr.UnknownValueError:
            return "No entendí. Por favor, intenta de nuevo."
        except sr.RequestError:
            return "Error al conectar con el servicio de reconocimiento de voz."

# Función IA general
def responder_ia(prompt_usuario):
    respuesta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Eres un asistente experto en matemáticas y educación."},
            {"role": "user", "content": prompt_usuario}
        ]
    )
    mensaje = respuesta.choices[0].message["content"]
    return mensaje.strip()

# Análisis matemático
def analizar_funcion(expresion_str):
    x = sp.symbols('x')
    try:
        funcion = sp.sympify(expresion_str)
    except:
        return "No se pudo interpretar la función.", None, None

    dominio = sp.calculus.util.continuous_domain(funcion, x, sp.S.Reals)
    recorrido = sp.ImageSet(sp.Lambda(x, funcion), dominio)
    
    return funcion, dominio, recorrido

# Gráfico
def graficar_funcion(funcion, variable):
    x_vals = [i/10 for i in range(-100, 100)]
    y_vals = []
    for val in x_vals:
        try:
            y = funcion.subs(variable, val).evalf()
            y_vals.append(y)
        except:
            y_vals.append(None)

    trace = go.Scatter(x=x_vals, y=y_vals, mode='lines', name='Función')
    layout = go.Layout(title='Gráfico de la función', xaxis_title='x', yaxis_title='f(x)')
    fig = go.Figure(data=[trace], layout=layout)
    return fig

# Interfaz principal
st.set_page_config(page_title="IA Matemática Interactiva", layout="wide")
st.title("🧠📊 Asistente Inteligente de Matemáticas")
st.markdown("Puedes **escribir** o **hablar** tu duda, y la IA te responderá. También puedes analizar funciones matemáticas.")

# Entrada por voz al cargar
if "voz_inicial" not in st.session_state:
    with st.spinner("Iniciando reconocimiento de voz..."):
        entrada = escuchar_microfono()
        st.session_state["voz_inicial"] = entrada
        st.write("🗣️ Dijiste:", entrada)
else:
    entrada = st.session_state["voz_inicial"]

# Entrada manual
entrada_manual = st.text_input("Escribe una duda o función matemática (ej: sin(x), x**2 + 3*x - 4):", value=entrada)

if st.button("🔎 Analizar / Responder"):
    if any(p in entrada_manual.lower() for p in ["dominio", "recorrido", "gráfica", "función", "derivada", "integral"]):
        funcion, dominio, recorrido = analizar_funcion(entrada_manual)
        if isinstance(funcion, str):
            st.error(funcion)
        else:
            st.success(f"✅ Función: {funcion}")
            st.info(f"📌 Dominio: {dominio}")
            st.info(f"📌 Recorrido: {recorrido}")
            fig = graficar_funcion(funcion, sp.symbols('x'))
            st.plotly_chart(fig)
            hablar(f"El dominio de la función es {dominio}")
    else:
        respuesta = responder_ia(entrada_manual)
        st.success(respuesta)
        hablar(respuesta)

st.markdown("---")
st.markdown("🎤 ¿Quieres hablar de nuevo?")
if st.button("🎙️ Hablar ahora"):
    entrada_voz = escuchar_microfono()
    st.write("🗣️ Dijiste:", entrada_voz)
    respuesta = responder_ia(entrada_voz)
    st.success(respuesta)
    hablar(respuesta)
