import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.title("🏃‍♂️ Carrera de Hábitos")

# Reemplaza con el link de tu Google Sheet (Asegúrate que sea 'Cualquier persona con el enlace puede leer')
url = "TU_URL_DE_GOOGLE_SHEETS_AQUI"

conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(spreadsheet=url, ttl=0)

# Mostrar la carrera
for index, row in df.iterrows():
    pista = " — " * int(row['Total Puntos']) + row['Emoji']
    st.write(f"**{row['Participante']}**")
    st.text(pista)

# Formulario para sumar puntos
with st.form("registro"):
    usuario = st.selectbox("¿Quién eres?", df['Participante'].tolist())
    if st.form_submit_button("¡Hice algo!"):
        df.loc[df['Participante'] == usuario, 'Total Puntos'] += 1
        conn.update(spreadsheet=url, data=df)
        st.success("¡Punto cargado! Refresca la página.")
