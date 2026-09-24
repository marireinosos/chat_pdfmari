File "/mount/src/chat_pdfmari/app.py", line 2
  💄✨ Glow Coach — Tu Asistente de Maquillaje Personal con IA
  ^
SyntaxError: invalid character '💄' (U+1F484)    }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] label { color: #f0d9e6 !important; font-size: 0.87rem !important; }

    h1 {
        font-family: 'Playfair Display', serif !important;
        background: linear-gradient(90deg, #ffd6a5, #ff8fb1 50%, #d9a7ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700 !important;
    }
    h2, h3, h4 { color: #fbe8f0 !important; font-weight: 600 !important; }
    p, li, .stMarkdown { color: #ecd6e2 !important; }

    textarea, input[type="text"], input[type="password"],
    div[data-baseweb="input"] input,
    div[data-baseweb="base-input"] {
        background-color: #3a1830 !important;
        border: 1px solid rgba(255,214,165,0.3) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        caret-color: #ffffff !important;
    }
    textarea:focus, input:focus {
        border-color: #ff8fb1 !important;
        box-shadow: 0 0 0 3px rgba(255,143,177,0.25) !important;
    }
    ::placeholder { color: #c9a3b8 !important; opacity: 1 !important; }

    .stButton > button {
        background: linear-gradient(90deg, #ffd6a5, #ff8fb1, #d9a7ff) !important;
        background-size: 200% auto !important;
        color: #2b0f26 !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        padding: 0.55rem 1.2rem !important;
        box-shadow: 0 4px 20px rgba(255,143,177,0.35) !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        background-position: right center !important;
        box-shadow: 0 6px 26px rgba(217,167,255,0.5) !important;
        transform: translateY(-2px) !important;
    }

    .header-banner {
        border-radius: 22px;
        overflow: hidden;
        margin-bottom: 22px;
        box-shadow: 0 10px 46px rgba(255,143,177,0.3);
        border: 1px solid rgba(255,214,165,0.25);
    }

    .glass-card {
        background: rgba(255,255,255,0.055);
        backdrop-filter: blur(14px);
        border: 1px solid rgba(255,214,165,0.18);
        border-radius: 18px;
        padding: 22px 26px;
        margin-bottom: 18px;
        box-shadow: 0 6px 28px rgba(0,0,0,0.25);
    }

    .chip-tag {
        display:inline-block; background: rgba(255,255,255,0.07); border:1px solid rgba(255,214,165,0.25);
        border-radius:20px; padding:5px 14px; font-size:0.82rem; color:#fbe8f0; margin:3px;
    }

    [data-testid="stChatMessage"] {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,214,165,0.14);
        border-radius: 16px;
        padding: 4px 8px;
    }

    div[data-testid="stExpander"] { border: 1px solid rgba(255,214,165,0.18) !important; border-radius: 14px !important; background: rgba(255,255,255,0.05) !important; }
    hr { border-color: rgba(255,214,165,0.18) !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ESTADO DE SESIÓN
# ─────────────────────────────────────────────
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []  # [{"role": "user"/"assistant", "content": str}]
if "knowledge_base" not in st.session_state:
    st.session_state.knowledge_base = None
if "prompt_pendiente" not in st.session_state:
    st.session_state.prompt_pendiente = None

# ─────────────────────────────────────────────
# BANNER
# ─────────────────────────────────────────────
BANNER_ARCHIVO = "BANNER-COLECCION.jpg.webp"
try:
    st.markdown('<div class="header-banner">', unsafe_allow_html=True)
    if os.path.exists(BANNER_ARCHIVO):
        st.image(BANNER_ARCHIVO, use_container_width=True)
    else:
        st.warning(f"No se encontró la imagen '{BANNER_ARCHIVO}' en la carpeta del proyecto. "
                   f"Verifica que esté en la raíz del repo, junto a app.py.")
    st.markdown('</div>', unsafe_allow_html=True)
except Exception as e:
    st.warning(f"No se pudo mostrar el banner ({BANNER_ARCHIVO}): {e}")

st.markdown("<h1 style='margin-bottom:0;'>💄 Glow Coach</h1>", unsafe_allow_html=True)
st.markdown("<p style='margin-top:4px; font-size:1.05rem;'>Tu asistente personal de maquillaje — con IA, con onda y con consejos hechos a tu medida ✨</p>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SIDEBAR — clave API + perfil de belleza + catálogo
# ─────────────────────────────────────────────
with st.sidebar:
    st.subheader("🔑 Conexión")
    ke = st.text_input("Ingresa tu clave de OpenAI", type="password")
    if ke:
        os.environ["OPENAI_API_KEY"] = ke
    else:
        st.warning("Ingresa tu clave de API para activar a Glow Coach")

    st.divider()
    st.subheader("💫 Tu perfil de belleza")
    tono_piel = st.selectbox("Tono de piel", ["Claro", "Medio claro", "Medio", "Medio oscuro", "Oscuro"])
    subtono = st.selectbox("Subtono", ["Cálido", "Frío", "Neutro", "No estoy segura"])
    tipo_piel = st.selectbox("Tipo de piel", ["Grasa", "Seca", "Mixta", "Normal", "Sensible"])
    estilo = st.selectbox("Estilo que te gusta", ["Natural / no-makeup", "Glam / dramático", "Editorial / creativo",
                                                   "Clásico elegante", "Colorido / experimental"])
    ocasion = st.selectbox("¿Para qué ocasión?", ["Uso diario", "Trabajo/estudio", "Fiesta o evento", "Fotos/sesión", "Boda"])

    st.divider()
    st.subheader("📚 Catálogo de productos (opcional)")
    pdf = st.file_uploader("Sube un PDF con tu catálogo o lista de productos", type="pdf")
    if pdf is not None and ke and st.session_state.knowledge_base is None:
        with st.spinner("💅 Leyendo tu catálogo..."):
            pdf_reader = PdfReader(pdf)
            texto = "".join(page.extract_text() or "" for page in pdf_reader.pages)
            splitter = CharacterTextSplitter(separator="\n", chunk_size=500, chunk_overlap=20, length_function=len)
            chunks = splitter.split_text(texto)
            embeddings = OpenAIEmbeddings()
            st.session_state.knowledge_base = FAISS.from_texts(chunks, embeddings)
        st.success(f"Catálogo cargado — {len(chunks)} fragmentos listos para recomendar desde ahí ✨")

    st.divider()
    st.caption("Glow Coach usa tu perfil para personalizar cada recomendación 💖")

# ─────────────────────────────────────────────
# PROMPT DE SISTEMA — persona + perfil
# ─────────────────────────────────────────────
def construir_system_prompt():
    return f"""Eres Glow Coach, una asesora de maquillaje experta, cálida, divertida y muy up-to-date con tendencias.
Hablas en español, con un tono cercano, motivador y con toques de humor, usando emojis con buen gusto (no exageres).
Das consejos prácticos, específicos y accionables — nunca respuestas genéricas de manual.

Perfil de belleza de la persona:
- Tono de piel: {tono_piel}
- Subtono: {subtono}
- Tipo de piel: {tipo_piel}
- Estilo preferido: {estilo}
- Ocasión objetivo: {ocasion}

Reglas:
- Adapta SIEMPRE tus recomendaciones (colores, técnicas, productos) a este perfil.
- Si sugieres colores o tonos, sé específica (ej. "un rosa durazno cálido", no solo "un rosa").
- Si no tienes info del catálogo, da recomendaciones generales por tipo de producto, no marcas inventadas.
- Estructura las respuestas con pasos o viñetas cuando sea una rutina.
- Sé breve pero completa — nada de relleno innecesario.
"""


def responder(pregunta):
    llm = ChatOpenAI(model="gpt-4o", temperature=0.7)

    contexto_catalogo = ""
    if st.session_state.knowledge_base is not None:
        docs = st.session_state.knowledge_base.similarity_search(pregunta, k=4)
        contexto_catalogo = "\n\n".join(d.page_content for d in docs)

    historial = "\n".join(
        f"{'Usuaria' if m['role'] == 'user' else 'Glow Coach'}: {m['content']}"
        for m in st.session_state.mensajes[-6:]
    )

    prompt_final = construir_system_prompt()
    if contexto_catalogo:
        prompt_final += f"\n\nInformación disponible del catálogo de productos de la usuaria:\n{contexto_catalogo}\n" \
                         f"Usa esto para recomendar productos concretos del catálogo cuando aplique."
    prompt_final += f"\n\nConversación reciente:\n{historial}\n\nUsuaria: {pregunta}\nGlow Coach:"

    respuesta = llm.invoke(prompt_final)
    return respuesta.content


# ─────────────────────────────────────────────
# SUGERENCIAS RÁPIDAS
# ─────────────────────────────────────────────
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown("#### ⚡ Prueba con una sugerencia rápida")
sugerencias = {
    "🌤️ Rutina de diario": "Dame una rutina de maquillaje rápida para el día a día según mi perfil.",
    "🌙 Look de noche": "Sugiéreme un look de maquillaje de noche/fiesta según mi perfil.",
    "🎨 Paleta para mi tono": "¿Qué colores de sombras y labiales me favorecen según mi tono y subtono de piel?",
    "💡 Que dure más": "Dame tips para que mi maquillaje dure todo el día sin arruinarse.",
}
cols_sug = st.columns(len(sugerencias))
for col, (nombre, texto_sug) in zip(cols_sug, sugerencias.items()):
    if col.button(nombre, use_container_width=True):
        st.session_state.prompt_pendiente = texto_sug
st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CHAT
# ─────────────────────────────────────────────
st.markdown("### 💬 Chatea con Glow Coach")

for m in st.session_state.mensajes:
    with st.chat_message(m["role"], avatar="💄" if m["role"] == "assistant" else "🙋‍♀️"):
        st.markdown(m["content"])

entrada_usuario = st.chat_input("Pregúntame lo que quieras sobre maquillaje...")
pregunta_final = st.session_state.prompt_pendiente or entrada_usuario
st.session_state.prompt_pendiente = None

if pregunta_final:
    if not ke:
        st.warning("Ingresa tu clave de OpenAI en la barra lateral para poder responderte 🔑")
    else:
        st.session_state.mensajes.append({"role": "user", "content": pregunta_final})
        with st.chat_message("user", avatar="🙋‍♀️"):
            st.markdown(pregunta_final)

        with st.chat_message("assistant", avatar="💄"):
            with st.spinner("💅 Preparando tu recomendación..."):
                try:
                    respuesta = responder(pregunta_final)
                except Exception as e:
                    respuesta = f"Ups, algo salió mal al conectar con OpenAI: {e}"
            st.markdown(respuesta)

        st.session_state.mensajes.append({"role": "assistant", "content": respuesta})

if st.session_state.mensajes:
    st.divider()
    if st.button("🗑️ Reiniciar conversación"):
        st.session_state.mensajes = []
        st.rerun()
