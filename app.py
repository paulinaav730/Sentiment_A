from textblob import TextBlob
import streamlit as st
from PIL import Image
from googletrans import Translator
import asyncio

# ---------------------------------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# ---------------------------------------------------------

st.set_page_config(
    page_title="Escuchadero EAFIT",
    page_icon="💙",
    layout="wide"
)

# ---------------------------------------------------------
# ESTILOS
# ---------------------------------------------------------

st.markdown("""
<style>

    /* Fondo general */
    .stApp {
        background-color: #f5f8fc;
    }

    /* Contenedor principal */
    .main {
        padding-top: 1rem;
    }

    /* Título */
    .titulo {
        text-align: center;
        color: #0057B8;
        font-size: 42px;
        font-weight: 700;
        margin-top: 15px;
        margin-bottom: 5px;
    }

    .subtitulo {
        text-align: center;
        color: #555555;
        font-size: 20px;
        margin-bottom: 30px;
    }

    /* Caja de bienvenida */
    .bienvenida {
        background-color: white;
        padding: 25px;
        border-radius: 18px;
        border: 1px solid #e1e8f0;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.06);
        margin-bottom: 25px;
    }

    .bienvenida h3 {
        color: #0057B8;
        margin-bottom: 10px;
    }

    .bienvenida p {
        color: #555555;
        font-size: 17px;
        line-height: 1.6;
    }

    /* Resultado */
    .resultado {
        background-color: white;
        padding: 30px;
        border-radius: 18px;
        border: 1px solid #e1e8f0;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.06);
        margin-top: 25px;
    }

    .resultado h2 {
        color: #0057B8;
    }

    /* Métricas */
    .metrica {
        background-color: #f5f8fc;
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        margin-top: 10px;
    }

    .metrica-titulo {
        color: #666666;
        font-size: 14px;
    }

    .metrica-valor {
        color: #0057B8;
        font-size: 28px;
        font-weight: bold;
    }

    /* Pie */
    .footer {
        text-align: center;
        color: #777777;
        margin-top: 40px;
        padding: 20px;
        font-size: 14px;
    }

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# IMAGEN PRINCIPAL
# ---------------------------------------------------------

image = Image.open("EAFIT.png")

st.image(
    image,
    use_container_width=True
)


# ---------------------------------------------------------
# ENCABEZADO
# ---------------------------------------------------------

st.markdown(
    '<div class="titulo">💙 Aquí puedes ser escuchado</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitulo">Este es un espacio para expresar lo que estás sintiendo.</div>',
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# MENSAJE DE BIENVENIDA
# ---------------------------------------------------------

st.markdown("""
<div class="bienvenida">

<h3>👋 Hola, estamos aquí para escucharte</h3>

<p>
A veces poner en palabras lo que sentimos puede ser difícil.
Escribe aquí lo que quieras compartir. No tienes que escribir
perfecto ni pensar demasiado en qué decir.
</p>

<p>
<strong>Este espacio analiza el tono emocional de lo que escribes
para ayudarte a identificar cómo se está sintiendo tu mensaje.</strong>
</p>

</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:

    st.header("💙 Sobre este espacio")

    st.write("""
    Este aplicativo utiliza análisis de sentimiento para identificar
    la polaridad y subjetividad de un texto.
    """)

    st.divider()

    st.subheader("📊 ¿Qué analizamos?")

    st.write("""
    **Polaridad**

    Indica si el texto tiene una tendencia positiva, negativa
    o neutral.

    Va desde **-1 hasta 1**.

    **Subjetividad**

    Indica qué tan emocional u opinativo es el texto.

    Va desde **0 hasta 1**.
    """)

    st.divider()

    st.caption(
        "💙 Expresar lo que sientes también es una forma de cuidarte."
    )


# ---------------------------------------------------------
# ÁREA PARA ESCRIBIR
# ---------------------------------------------------------

st.markdown("### 💬 Cuéntame, ¿cómo te sientes?")

text = st.text_area(
    "Escribe aquí lo que quieras compartir:",
    placeholder="Por ejemplo: Hoy me sentí muy cansado porque tuve muchas cosas que hacer...",
    height=180
)


# ---------------------------------------------------------
# BOTÓN
# ---------------------------------------------------------

boton = st.button(
    "💙 Quiero ser escuchado",
    use_container_width=True
)


# ---------------------------------------------------------
# ANÁLISIS
# ---------------------------------------------------------

if boton:

    if text.strip() == "":
        st.warning(
            "💙 Escribe algo primero. Este espacio está aquí para escucharte."
        )

    else:

        with st.spinner("Estoy leyendo lo que compartiste... 💙"):

            try:

                # ---------------------------------------------
                # TRADUCCIÓN
                # ---------------------------------------------

                async def traducir(texto):

                    async with Translator() as translator:

                        resultado = await translator.translate(
                            texto,
                            src="es",
                            dest="en"
                        )

                        return resultado.text

                trans_text = asyncio.run(traducir(text))


                # ---------------------------------------------
                # ANÁLISIS DE SENTIMIENTO
                # ---------------------------------------------

                blob = TextBlob(trans_text)

                polarity = round(
                    blob.sentiment.polarity,
                    2
                )

                subjectivity = round(
                    blob.sentiment.subjectivity,
                    2
                )


                # ---------------------------------------------
                # DETERMINAR SENTIMIENTO
                # ---------------------------------------------

                if polarity > 0:

                    sentimiento = "Positivo 😊"

                    mensaje = """
                    Parece que hay una tendencia positiva en lo que
                    compartiste. Qué bueno que hayas encontrado un
                    espacio para expresar eso que estás sintiendo. 💙
                    """

                elif polarity < 0:

                    sentimiento = "Negativo 😔"

                    mensaje = """
                    Parece que lo que compartiste tiene una tendencia
                    emocional negativa. Gracias por ponerlo en palabras.
                    A veces expresar lo que sentimos es un primer paso
                    importante. 💙
                    """

                else:

                    sentimiento = "Neutral 😐"

                    mensaje = """
                    Lo que compartiste tiene una tendencia neutral.
                    De cualquier manera, gracias por tomarte el tiempo
                    de expresar lo que estás pensando. 💙
                    """


                # ---------------------------------------------
                # RESULTADO
                # ---------------------------------------------

                st.markdown("""
                <div class="resultado">
                """, unsafe_allow_html=True)

                st.markdown(
                    "## 💙 Gracias por compartirlo"
                )

                st.write(mensaje)

                st.divider()

                # ---------------------------------------------
                # MÉTRICAS
                # ---------------------------------------------

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.markdown(
                        f"""
                        <div class="metrica">

                        <div class="metrica-titulo">
                        SENTIMIENTO
                        </div>

                        <div class="metrica-valor">
                        {sentimiento}
                        </div>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )


                with col2:

                    st.markdown(
                        f"""
                        <div class="metrica">

                        <div class="metrica-titulo">
                        POLARIDAD
                        </div>

                        <div class="metrica-valor">
                        {polarity}
                        </div>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )


                with col3:

                    st.markdown(
                        f"""
                        <div class="metrica">

                        <div class="metrica-titulo">
                        SUBJETIVIDAD
                        </div>

                        <div class="metrica-valor">
                        {subjectivity}
                        </div>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )


                st.divider()

                st.caption(
                    "Este resultado corresponde únicamente al análisis "
                    "del texto escrito y no constituye una evaluación profesional."
                )

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )


            except Exception as e:

                st.error(
                    "No pudimos analizar el texto en este momento. "
                    "Intenta nuevamente."
                )

                st.write(e)


# ---------------------------------------------------------
# PIE DE PÁGINA
# ---------------------------------------------------------

st.markdown("""
<div class="footer">

💙 <strong>Escuchadero EAFIT</strong><br>

Un espacio para expresar lo que sientes.

</div>
""", unsafe_allow_html=True)
