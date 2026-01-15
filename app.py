import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.title("🏃 Carrera de Hábitos")

# 1. Asegúrate de que esta URL sea la de tu hoja "La foca"
url_sheet = "https://docs.google.com/spreadsheets/d/1Bk5dt6ud_wy3W1px1zlYfht5-KE52lzkok9SaaB0m6g/edit?gid=215890415#gid=215890415"

# Conexión segura con los Secrets
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # 2. Leemos la pestaña con el nuevo nombre: Hoja_2
    df = conn.read(spreadsheet=url_sheet, worksheet="Hoja_2", ttl=0)
    
    # Limpiamos nombres de columnas
    df.columns = df.columns.str.strip()

    # 🏁 Mostrar la pista de carrera
    st.subheader("Pista de Competición")
    for index, row in df.iterrows():
        puntos = int(row['Total Puntos'])
        pista = " — " * puntos + row['Emoji']
        st.write(f"**{row['Participante']}** ({puntos} pts)")
        st.info(pista)

    st.divider()

    # ✍️ Formulario para sumar puntos
    with st.form("registro"):
        st.write("### ¿Completaste un hábito?")
        lista_nombres = df['Participante'].tolist()
        usuario = st.selectbox("¿Quién eres?", lista_nombres)
        
        if st.form_submit_button("➕ Sumar 1 punto"):
            # Actualizamos el dato localmente
            df.loc[df['Participante'] == usuario, 'Total Puntos'] += 1
            # Escribimos de vuelta en el Excel usando Hoja_2
            conn.update(spreadsheet=url_sheet, worksheet="Hoja_2", data=df)
            st.success("¡Punto guardado!")
            st.rerun()

except Exception as e:
    st.error(f"Error: {e}")
    st.write("Verifica que la pestaña en el Excel se llame exactamente 'Hoja_2'.")
