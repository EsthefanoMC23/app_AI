import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objs as go
import random

st.set_page_config(layout="wide")
st.title("📊 App Educativa de Funciones Matemáticas")

x = sp.symbols('x')
y = sp.symbols('y')

# --------------------------------------------
# Funciones auxiliares (omitidas aquí por brevedad: parse_function, explicar_derivada, etc.)
# Puedes pegar el resto del código desde la última versión sin cambios aquí abajo
# --------------------------------------------

def main():
    menu = st.sidebar.selectbox("Selecciona una herramienta:", [
        "Gráfico de funciones",
        "Evaluar función",
        "Derivar función",
        "Integrar función",
        "Dominio y recorrido",
        "Función inversa",
        "Resolver inecuaciones",
        "Límites"
    ])

    if menu == "Gráfico de funciones":
        st.header("📈 Gráfico interactivo de funciones")
        expr_input = st.text_input("Ingresa la función f(x):", value="x**2")
        if expr_input:
            expr = parse_function(expr_input)
            graficar_funcion(expr)

    elif menu == "Evaluar función":
        st.header("🧪 Evaluar función en un punto")
        expr_input = st.text_input("Función f(x):", value="x**2 + 3*x")
        valor_x = st.number_input("Valor de x:", value=2.0)
        if expr_input:
            expr = parse_function(expr_input)
            resultado, pasos = evaluar_funcion(expr, valor_x)
            st.markdown(pasos)

    elif menu == "Derivar función":
        st.header("🔁 Derivar una función")
        expr_input = st.text_input("Función f(x):", value="x**3 + 2*x")
        if expr_input:
            expr = parse_function(expr_input)
            derivada, pasos = explicar_derivada(expr)
            st.markdown(pasos)

    elif menu == "Integrar función":
        st.header("📐 Integrar una función")
        expr_input = st.text_input("Función f(x):", value="x**2")
        if expr_input:
            expr = parse_function(expr_input)
            integral, pasos = explicar_integral(expr)
            st.markdown(pasos)

    elif menu == "Dominio y recorrido":
        st.header("🧭 Dominio y recorrido de una función")
        expr_input = st.text_input("Función f(x):", value="sqrt(x - 2)")
        if expr_input:
            expr = parse_function(expr_input)
            dominio, recorrido = dominio_y_recorrido(expr)
            st.markdown(f"**Dominio:** {dominio}")
            st.markdown(f"**Recorrido:** {recorrido}")
            graficar_funcion(expr)

    elif menu == "Función inversa":
        st.header("🔄 Encontrar función inversa")
        expr_input = st.text_input("Función f(x):", value="(x - 1)/(x + 2)")
        if expr_input:
            expr = parse_function(expr_input)
            inversa, pasos = calcular_inversa(expr)
            if inversa:
                st.markdown(pasos)
                graficar_funcion(expr, inversa_expr=inversa)
            else:
                st.error(pasos)

    elif menu == "Resolver inecuaciones":
        st.header("⚖️ Resolver inecuaciones")
        ineq_input = st.text_input("Inecuación (ej: x**2 - 4 > 0):", value="x**2 - 4 > 0")
        if ineq_input:
            resultado, pasos = resolver_inecuacion(ineq_input)
            if resultado:
                st.markdown(pasos)
            else:
                st.error(pasos)

    elif menu == "Límites":
        st.header("➗ Cálculo de Límite")
        st.markdown("Esta sección te ayuda a **entender el concepto de límite** y cómo se aplica.")
        st.latex(r"\lim_{x \to a} f(x) = L")
        st.markdown("Esto representa el valor al que se acerca una función cuando x se acerca a cierto punto.")

        st.subheader("📘 Demostración del límite como derivada")
        st.markdown("La derivada de una función en un punto se define como el límite de la pendiente de la recta secante cuando h tiende a 0:")
        st.latex(r"f'(a) = \lim_{h \to 0} \frac{f(a+h) - f(a)}{h}")
        st.markdown("Esta fórmula representa la **pendiente de la recta tangente** en el punto $x = a$.")

        st.subheader("🧮 Calculadora de Límites")
        funcion_limite = st.text_input("Ingresa la función f(x):", value="(x**2 - 1)/(x - 1)")
        punto_limite = st.text_input("¿A qué valor tiende x?:", value="1")

        if funcion_limite and punto_limite:
            expr = parse_function(funcion_limite)
            try:
                punto_val = float(punto_limite)
                limite, explicacion = calcular_limite(expr, punto_val)
                if limite is not None:
                    st.success(f"Resultado del límite: {limite}")
                    st.markdown(explicacion)
                else:
                    st.error(explicacion)
            except ValueError:
                st.error("El punto debe ser un número válido.")

if __name__ == "__main__":
    main()
