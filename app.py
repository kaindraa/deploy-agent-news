from datetime import date
import streamlit as st, ast
from typing import TypedDict, List, Optional
from langgraph.graph import START, END, StateGraph
from tavily import TavilyClient
from chains import planner_chain, tavily_planner_chain, grader_chain, writer_chain
from graph import build_graph
from utils import clean_json_string, clean_markdown

st.set_page_config(page_title="LLM Agent for News Search & Report Generation", layout="wide")
st.title("📰 LLM Agent for News Search & Report Generation")
st.markdown("""
*Personal Project of [kaindraa](https://github.com/kaindraa)  <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" width="20" style="vertical-align:middle" />*
""", unsafe_allow_html=True)

st.markdown("""
Cukup masukkan **topik berita** yang ingin dicari, **LLM Agent** akan merancang strategi pencarian, menelusuri web, dan menulis laporan berita terstruktur secara **otomatis** untuk Anda.   Anda dapat mengatur tingkat **kompleksitas pencarian** dan **rentang waktu berita** melalui panel kiri aplikasi.   Seluruh proses pencarian dan penyusunan laporan ditampilkan secara **transparan**, agar Anda dapat mengikuti setiap tahap kerja agen.
""")

with st.expander("**Arsitektur Agent**", expanded=True):
    st.markdown("""                
Arsitektur agen ini dibangun menggunakan framework **LangChain** dan **LangGraph**, yang memungkinkan pengelolaan alur kerja berbasis node secara modular dan iteratif.   Untuk pencarian berita secara real-time, aplikasi ini terintegrasi dengan **Tavily**, yakni layanan API pencarian web yang menyediakan hasil aktual dari berbagai sumber.   LLM yang digunakan berbasis **DeepSeek**, yang berperan sebagai inti pemrosesan dalam setiap tahap: mulai dari memahami topik, menyusun query, mengevaluasi hasil pencarian, hingga menulis laporan akhir.

Arsitektur agen terdiri dari berbagai komponen:
1. **Planner**: Menyusun struktur informasi penting dari topik yang diberikan.
2. **Web Search Planner**: Merancang query pencarian berdasarkan outline yang dihasilkan.
3. **Grader**: Mengevaluasi apakah informasi yang dikumpulkan sudah mencukupi.
4. **Writer**: Menulis laporan akhir secara terstruktur dan lengkap.

Berikut adalah visualisasi arsitektur agen yang digunakan:
""")

    st.image("images/agent_architecture.png", caption="Agent Architecture Overview", use_container_width=True)


topic = st.text_area("**Topik Pencarian**", height=100, placeholder="Contoh: bagaimana ekonomi Indonesia pada Q1 2025?")

with st.sidebar:
    st.header("⚙️ Pengaturan Pencarian Berita")

    with st.expander("📘 Penjelasan Parameter"):
        st.markdown("""
        - **Max Iteration**: Batas jumlah iterasi pencarian dan evaluasi sebelum penulisan laporan dimulai.
        - **Queries per Iteration**: Banyak pertanyaan pencarian (query) yang diajukan ke web di tiap iterasi.
        - **Articles per Query**: Banyaknya artikel berita yang diambil untuk setiap query.
        - **Time Range**: Membatasi pencarian berita berdasarkan waktu terbit, dihitung mundur dari hari ini
        """)

    max_search_steps = st.number_input("**Max Iteration**", 1, 4, value=3)
    queries_per_step = st.number_input("**Queries per Iteration**", 1, 5, value=4)
    articles_per_query = st.number_input("**Articles per Query**", 1, 10, value=8)
    time_filters = {
        "Tanpa rentang waktu": None,
        "1 hari terakhir": "day",
        "1 minggu terakhir": "week",
        "1 bulan terakhir": "month",
        "1 tahun terakhir": "year"
    }

    selected_label = st.selectbox("**Time Range**", list(time_filters.keys()))

time_filter = time_filters[selected_label]

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    run = st.button("🚀 Jalankan", use_container_width=True)

stage_placeholder = st.empty()
stage_placeholder.info("📍 Tahap saat ini: Menunggu mulai…")
outline_placeholder = st.empty()
iteration_blocks = []

ENABLE_LOG = False
logs: List[str] = []
log_placeholder = st.empty()

def log(msg: str):
    if ENABLE_LOG:
        logs.append(msg)
        log_placeholder.text("\n".join(logs[-25:]))

def planner(state):
    stage_placeholder.info("📍 Tahap saat ini: 📝 Merencanakan struktur laporan.")
    log("📝 Menjalankan Planner …")

    outline = planner_chain.invoke({
        "topic": state["topic"],
        "time_range_input": time_filter,
        "current_date": date.today().strftime("%d %B %Y")
    })

    outline = clean_markdown(outline)
    with outline_placeholder.expander("📑 Outline Laporan"):
        st.markdown(outline)

    return dict(
        topic=state["topic"],
        outline=outline,
        context="",
        iteration_count=1,
        is_continue="true",
        searched_query=[],
        result=None
    )

def web_planner(state):
    iter_num = state["iteration_count"]
    stage_placeholder.info(f"📍 Tahap saat ini: 🔍 Iterasi {iter_num} – Merancang Query Pencarian web")
    block = st.container(); iteration_blocks.append(block)
    raw = tavily_planner_chain.invoke({
        "topic": state["topic"], "outline": state["outline"], "context": state["context"],
        "iteration_count": iter_num, "searched_query": state["searched_query"],
        "max_queries": queries_per_step

    })
    queries = ast.literal_eval(clean_json_string(raw))[:queries_per_step]
    with block.expander(f"📋 Query pencarian web – Iterasi {iter_num}", expanded=False):
        for q in queries: st.markdown(f"- {q}")
    log(f"📋 Iterasi-{iter_num} query: {queries}")
    return dict(queries=queries, searched_query=state["searched_query"]+queries,
                iteration_count=iter_num+1)

def web_retriever(state):
    iter_num = state["iteration_count"]-1
    stage_placeholder.info(f"📍 Tahap saat ini: 🌐 Iterasi {iter_num} – Mengambil berita")
    ctx_parts = []
    results_block = iteration_blocks[iter_num-1].expander(
        f"📚 Konteks Iterasi {iter_num} dari Pencarian web", expanded=False)
    for q in state["queries"]:
        log(f"🌐 Mencari: {q}")
        res = tavily.search(query=q, topic="news", search_depth="advanced",
                            max_results=articles_per_query, time_range=time_filter)
        results_block.markdown(f"**🔎 Query:** {q}")
        for r in res["results"]:
            url, content = r.get("url",""), r.get("content","")
            results_block.markdown(f"- [{url}]({url}) → {content[:250]}…")
            ctx_parts.append(f"{url} - {content}")
    return {"context": state["context"]+"\n"+"\n".join(ctx_parts)}

def grader(state):
    stage_placeholder.info("📍 Tahap saat ini: 📊 Evaluasi Kelengkapan")
    if state["iteration_count"] > max_search_steps:
        log("⏹️ Iterasi maksimal tercapai.")
        return {"is_continue": "false"}
    is_continue = grader_chain.invoke({
        "topic": state["topic"],
        "outline": state["outline"],
        "context": state["context"]
    })
    log(f"📊 Grader: continue={is_continue}")
    return {"is_continue": is_continue}

def writer(state):
    stage_placeholder.info("📍 Tahap saat ini: ✍️ Menulis Laporan Akhir")
    log("✍️ Menulis laporan akhir …")
    report = writer_chain.invoke({
        "topic": state["topic"],
        "outline": state["outline"],
        "context": state["context"]
    })
    st.markdown("---")
    st.subheader("📌 Laporan Akhir")
    report = clean_markdown(report)
    st.markdown(report, unsafe_allow_html=True)
    return {"result": report}

def branch(state):
    return "web_planner" if state["is_continue"] == "true" else "writer"

agent = build_graph(planner, web_planner, web_retriever, grader, writer, branch)

if run:
    if not topic.strip():
        st.error("Topik tidak boleh kosong!")
        st.stop()
    tavily = TavilyClient( api_key=st.secrets["DEESEEK_API_KEY"])
    for _ in agent.stream({"topic": topic}):
        pass
