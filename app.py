import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.title("🏃‍♂️ Carrera de Hábitos")

# Conexión segura
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # Intentamos leer la Hoja 2
    df = conn.read(worksheet="Hoja 2", ttl=0)
    
    # Limpiamos los nombres de las columnas por si tienen espacios locos
    df.columns = df.columns.str.strip()

    # 🏁 Mostrar la pista de carrera
    st.subheader("Pista de Competición")
    for index, row in df.iterrows():
        pista = " — " * int(row['Total Puntos']) + row['Emoji']
        st.write(f"**{row['Participante']}** ({row['Total Puntos']} pts)")
        st.info(pista)

    st.divider()

    # ✍️ Formulario para sumar puntos
    with st.form("registro"):
        st.write("### ¿Completaste un hábito?")
        # Usamos el nombre de la columna ya limpio
        lista_nombres = df['Participante'].tolist()
        usuario = st.selectbox("Selecciona tu nombre", lista_nombres)
        
        if st.form_submit_button("➕ Sumar 1 punto"):
            df.loc[df['Participante'] == usuario, 'Total Puntos'] += 1
            conn.update(worksheet="Hoja2", data=df)
            st.success("¡Punto guardado!")
            st.rerun()

except Exception as e:
    st.error(f"Error de lectura: {e}")
    st.write("Columnas detectadas en la hoja:", df.columns.tolist() if 'df' in locals() else "No se pudo leer la hoja")
