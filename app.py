import streamlit as st
from streamlit_gsheets import GSheetsConnection

# --- CAPA DE SEGURIDAD ---
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if st.session_state["password_correct"]:
        return True

    st.title("🔒 Acceso Privado")
    password_input = st.text_input("Ingresa la contraseña para ver la carrera", type="password")
    
    if st.button("Entrar"):
        # Asegúrate de haber puesto 'password' en los Secrets de Streamlit
        if password_input == st.secrets["password"]:
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("❌ Contraseña incorrecta")
    return False

# TODO EL CONTENIDO DE LA APP DEBE IR DENTRO DE ESTE 'IF'
if check_password():
    st.title("🏃 Carrera de Hábitos")
    
    # 1. REEMPLAZA EL "2" POR TU URL REAL DE GOOGLE SHEETS
    url_sheet = "https://docs.google.com/spreadsheets/d/1Bk5dt6ud_wy3W1px1zlYfht5-KE52lzkok9SaaB0m6g/edit?gid=215890415#gid=215890415"
    
    conn = st.connection("gsheets", type=GSheetsConnection)

    try:
        # 2. Leemos la pestaña Hoja_2
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
                # Escribimos de vuelta en el Excel
                conn.update(spreadsheet=url_sheet, worksheet="Hoja_2", data=df)
                st.success("¡Punto guardado!")
                st.rerun()

    except Exception as e:
        st.error(f"Error: {e}")
        st.write("Verifica la URL y que la pestaña se llame 'Hoja_2'.")
