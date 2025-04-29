import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objs as go

st.set_page_config(layout="wide")
st.title("📊 App Educativa de Funciones Matemáticas")

x = sp.symbols('x')

# Función para convertir el texto ingresado en una expresión de SymPy
def parse_function(expr_input):
    try:
        expr = sp.sympify(expr_input)
        return expr
    except Exception as e:
        return None  # Retorna None si ocurre un error

# Función para graficar una función
def graficar_funcion(expr, inversa_expr=None):
    f = sp.lambdify(x, expr, modules=["numpy"])
    xs = np.linspace(-10, 10, 1000)
    fig = go.Figure()

    try:
        ys = f(xs)
        fig.add_trace(go.Scatter(x=xs, y=ys, mode='lines', name='f(x)', line=dict(color='blue')))
    except:
        st.error("❌ No se pudo graficar f(x).")

    if inversa_expr:
        inv = sp.lambdify(x, inversa_expr, modules=["numpy"])
        try:
            ys_inv = inv(xs)
            fig.add_trace(go.Scatter(x=ys_inv, y=xs, mode='lines', name='f⁻¹(x)', line=dict(color='red', dash='dash')))
        except:
            st.error("❌ No se pudo graficar la inversa.")

    fig.update_layout(title='Gráfico interactivo',
                      xaxis_title='x', yaxis_title='y',
                      hovermode='closest')
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_yaxes(rangeslider_visible=True)
    st.plotly_chart(fig, use_container_width=True)

# Función para evaluar una función en un punto
def evaluar_funcion(expr, valor_x):
    try:
        resultado = expr.subs(x, valor_x)
        pasos = f"**Paso 1:** Sustituir x = {valor_x} en f(x): {expr} = {resultado}"
        return resultado, pasos
    except:
        return None, "Error al evaluar la función."

# Función para derivar una función
def explicar_derivada(expr):
    try:
        derivada = sp.diff(expr, x)
        pasos = f"**Paso 1:** Derivamos la función f(x) = {expr} respecto a x. Resultado: f'(x) = {derivada}"
        return derivada, pasos
    except:
        return None, "Error al derivar la función."

# Función para integrar una función
def explicar_integral(expr):
    try:
        integral = sp.integrate(expr, x)
        pasos = f"**Paso 1:** Integramos la función f(x) = {expr} respecto a x. Resultado: ∫f(x)dx = {integral}"
        return integral, pasos
    except:
        return None, "Error al integrar la función."

# Función para encontrar dominio y recorrido de una función
def dominio_y_recorrido(expr):
    try:
        dominio = sp.solveset(sp.And(expr >= 0, x >= 0), x)
        recorrido = sp.Range(-10, 10)  # Solo un ejemplo simple, puedes mejorarlo.
        return dominio, recorrido
    except:
        return None, "Error al calcular el dominio y recorrido."

# Función para encontrar la función inversa
def calcular_inversa(expr):
    try:
        inversa = sp.solve(expr - y, x)
        if inversa:
            inversa_expr = inversa[0]
            pasos = f"**Paso 1:** Encontramos la función inversa de f(x) = {expr}. Resultado: f⁻¹(x) = {inversa_expr}"
            return inversa_expr, pasos
        else:
            return None, "No se pudo encontrar la inversa."
    except:
        return None, "Error al calcular la inversa."

# Función para resolver inecuaciones
def resolver_inecuacion(ineq_input):
    try:
        ineq_expr = sp.sympify(ineq_input)
        soluciones = sp.solve_univariate_inequality(ineq_expr, x)
        pasos = f"**Paso 1:** Resolviendo la inecuación {ineq_input}. Soluciones: {soluciones}"
        return soluciones, pasos
    except:
        return None, "Error al resolver la inecuación."

# Función para calcular límites
def calcular_limite(expr, punto_val):
    try:
        limite = sp.limit(expr, x, punto_val)
        explicacion = f"**Paso 1:** Aplicamos el límite de f(x) = {expr} cuando x tiende a {punto_val}. Resultado: {limite}"
        return limite, explicacion
    except:
        return None, "Error al calcular el límite."

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
