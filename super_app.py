import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import random
import time
import pandas as pd

# Personalizando el diseño con CSS
st.markdown("""
    <style>
        .main {
            background-color: #f0f8ff;
            color: #333;
        }
        .sidebar .sidebar-content {
            background-color: #ffcccb;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 12px;
        }
        h1 {
            font-family: 'Comic Sans MS', sans-serif;
            color: #2f4f4f;
        }
        h2 {
            font-family: 'Arial', sans-serif;
            color: #008b8b;
        }
    </style>
""", unsafe_allow_html=True)

# Encabezado atractivo
st.markdown("""
    <h1 style="text-align: center;">¡Bienvenido a la Super IA de Funciones Matemáticas! 🎉</h1>
""", unsafe_allow_html=True)

# Definición de funciones matemáticas
x = sp.symbols('x')

def derivar_funcion(expr):
    return sp.diff(expr, x)

def integrar_funcion(expr):
    return sp.integrate(expr, x)

def graficar_funcion(expr):
    f = sp.lambdify(x, expr, "numpy")
    x_vals = np.linspace(-10, 10, 400)
    y_vals = f(x_vals)
    fig, ax = plt.subplots()
    ax.plot(x_vals, y_vals)
    ax.grid(True)
    ax.set_title(f"Gráfico de {expr}")
    return fig

def generar_funcion_polinomica(grado=2, coef_min=-5, coef_max=5):
    funcion = 0
    for g in range(grado, -1, -1):
        coef = random.randint(coef_min, coef_max)
        if coef != 0:
            funcion += coef * x**g
    return funcion

def generar_funcion_trigonometrica():
    funciones_trigo = [sp.sin, sp.cos, sp.tan]
    f_trig = random.choice(funciones_trigo)(x)
    coef = random.randint(-5, 5)
    if coef == 0:
        coef = 1
    return coef * f_trig

def generar_funcion_mixta():
    polinomio = generar_funcion_polinomica(grado=random.randint(1, 3))
    trigonometrica = generar_funcion_trigonometrica()
    return polinomio + trigonometrica

def resolver_ecuacion(ecuacion):
    soluciones = sp.solve(ecuacion, x)
    return soluciones

def guardar_puntaje(nombre, puntaje):
    df = pd.DataFrame({'Nombre': [nombre], 'Puntaje': [puntaje]})
    try:
        df_existente = pd.read_csv('puntajes.csv')
        df = pd.concat([df_existente, df], ignore_index=True)
    except FileNotFoundError:
        pass
    df.to_csv('puntajes.csv', index=False)

def mostrar_ranking():
    try:
        df = pd.read_csv('puntajes.csv')
        df_sorted = df.sort_values(by='Puntaje', ascending=False)
        st.write("## Ranking de Estudiantes:")
        st.write(df_sorted)
    except FileNotFoundError:
        st.write("Aún no hay puntajes guardados.")

# Modo Examen
def modo_examen():
    st.header("📝 Modo Examen")
    nombre = st.text_input("Tu nombre para guardar el puntaje:")
    
    if st.button("Comenzar Examen"):
        preguntas = []
        respuestas_correctas = 0
        tiempo_inicio = time.time()

        for i in range(5):
            st.subheader(f"Pregunta {i+1}")
            tipo = random.choice(["derivar", "integrar"])
            if tipo == "derivar":
                funcion = generar_funcion_polinomica(grado=random.randint(1, 3))
                st.latex(f"\\text{{Deriva: }} {sp.latex(funcion)}")
                respuesta_usuario = st.text_input(f"Respuesta derivada {i+1}:", key=f"der{i}")
                correcta = derivar_funcion(funcion)
            else:
                funcion = generar_funcion_polinomica(grado=random.randint(1, 3))
                st.latex(f"\\text{{Integra: }} {sp.latex(funcion)}")
                respuesta_usuario = st.text_input(f"Respuesta integral {i+1}:", key=f"int{i}")
                correcta = integrar_funcion(funcion)

            if respuesta_usuario:
                try:
                    respuesta_expr = sp.sympify(respuesta_usuario)
                    diferencia = sp.simplify(correcta - respuesta_expr)
                    if diferencia == 0:
                        respuestas_correctas += 1
                        st.success("✅ ¡Correcto!")
                    else:
                        st.error(f"❌ Incorrecto. Respuesta correcta: {correcta}")
                except Exception as e:
                    st.error(f"Error al interpretar tu respuesta: {e}")

        tiempo_total = time.time() - tiempo_inicio
        st.info(f"Examen terminado en {round(tiempo_total, 2)} segundos.")
        st.success(f"Puntaje final: {respuestas_correctas}/5")

        if nombre:
            guardar_puntaje(nombre, respuestas_correctas)
            st.success("🎉 Puntaje guardado exitosamente.")

# Menú Principal
st.sidebar.title("Menú Principal")
opcion = st.sidebar.selectbox("¿Qué quieres hacer?", 
    ["Derivar", "Integrar", "Graficar", "Evaluar Respuesta", "Generar Función", 
     "Resolver Ecuación", "Modo Examen", "Subir Imagen", "Ranking de Estudiantes"])

# Funciones principales
if opcion == "Derivar" or opcion == "Integrar" or opcion == "Graficar" or opcion == "Evaluar Respuesta" or opcion == "Resolver Ecuación":
    funcion_usuario = st.text_input("Ingresa una función de x o ecuación (ej: x**2 + 3*x + 2 o x**2-4)", "x**2 + 3*x + 2")
    if funcion_usuario:
        expr = sp.sympify(funcion_usuario)

if opcion == "Derivar":
    if st.button("Derivar"):
        resultado = derivar_funcion(expr)
        st.success(f"La derivada es: {resultado}")

elif opcion == "Integrar":
    if st.button("Integrar"):
        resultado = integrar_funcion(expr)
        st.success(f"La integral es: {resultado} + C")

elif opcion == "Graficar":
    if st.button("Graficar"):
        fig = graficar_funcion(expr)
        st.pyplot(fig)

elif opcion == "Evaluar Respuesta":
    operacion = st.radio("¿Qué operación quieres evaluar?", ("Derivada", "Integral"))
    respuesta_usuario = st.text_input("Ingresa tu respuesta")
    if st.button("Evaluar"):
        correcta = derivar_funcion(expr) if operacion == "Derivada" else integrar_funcion(expr)
        try:
            respuesta_expr = sp.sympify(respuesta_usuario)
            diferencia = sp.simplify(correcta - respuesta_expr)
            if diferencia == 0:
                st.success("✅ ¡Respuesta correcta!")
            else:
                st.error(f"❌ Respuesta incorrecta. La respuesta correcta era: {correcta}")
        except Exception as e:
            st.error(f"Error: {e}")

elif opcion == "Generar Función":
    tipo = st.radio("Tipo de función a generar:", ("Polinómica", "Trigonométrica", "Mixta"))
    if st.button("Generar"):
        if tipo == "Polinómica":
            nueva_funcion = generar_funcion_polinomica(grado=random.randint(2, 4))
        elif tipo == "Trigonométrica":
            nueva_funcion = generar_funcion_trigonometrica()
        else:
            nueva_funcion = generar_funcion_mixta()
        st.success(f"Función generada: {nueva_funcion}")
        
        accion = st.radio("¿Qué quieres hacer con esta función?", ("Derivar", "Integrar"))
        if accion == "Derivar":
            resultado = derivar_funcion(nueva_funcion)
            st.info(f"La derivada es: {resultado}")
        else:
            resultado = integrar_funcion(nueva_funcion)
            st.info(f"La integral es: {resultado} + C")

elif opcion == "Resolver Ecuación":
    if st.button("Resolver"):
        soluciones = resolver_ecuacion(expr)
        st.success(f"Soluciones: {soluciones}")

elif opcion == "Modo Examen":
    modo_examen()

elif opcion == "Subir Imagen":
    st.subheader("📷 Subir Imagen")
    archivo = st.file_uploader("Sube una imagen de una función o ecuación")
    if archivo:
        st.image(archivo, caption="Imagen subida")
        st.info("🚀 En el futuro podríamos aplicar OCR para leer la función automáticamente.")

elif opcion == "Ranking de Estudiantes":
    mostrar_ranking()
