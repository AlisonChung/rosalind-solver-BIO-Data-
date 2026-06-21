import streamlit as st
import io

# ── 페이지 설정 ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DNA Sequence Analyzer",
    page_icon="🧬",
    layout="centered",
)

# ── 스타일 ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.stApp { background: #ffffff; }

div[data-testid="stButton"] > button[kind="secondary"] {
    background: none; border: none; padding: 0;
    color: #1a1a1a; font-size: 2rem; font-weight: 700;
    letter-spacing: -0.5px; cursor: pointer; box-shadow: none;
}
div[data-testid="stButton"] > button[kind="secondary"]:hover {
    color: #2563eb; background: none; border: none; box-shadow: none;
}

div[data-testid="stMetric"] {
    background: #f8faff; border: 1px solid #e2e8f0;
    border-radius: 10px; padding: 16px 20px;
}
div[data-testid="stMetricLabel"] { font-size: 0.85rem; color: #64748b; }
div[data-testid="stMetricValue"] { font-size: 2rem; font-weight: 700; color: #1e3a5f; }

.length-badge {
    display: inline-block; background: #2563eb; color: white;
    font-size: 0.85rem; font-weight: 600; padding: 4px 14px;
    border-radius: 999px; margin-bottom: 6px;
}

.section-header {
    font-size: 0.78rem; font-weight: 700; letter-spacing: 0.08em;
    text-transform: uppercase; color: #94a3b8; margin: 28px 0 10px 0;
}

section[data-testid="stFileUploaderDropzone"] {
    border: 2px dashed #cbd5e1 !important;
    border-radius: 12px !important;
    background: #f8faff !important;
}

hr { border: none; border-top: 1px solid #e2e8f0; margin: 24px 0; }
</style>
""", unsafe_allow_html=True)


# ── 유틸 함수 ─────────────────────────────────────────────────────────────────
def extract_text_from_pdf(file_bytes: bytes) -> str:
    try:
        import pdfplumber
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)
    except Exception as e:
        st.error(f"PDF 파싱 실패: {e}")
        return ""


def parse_fasta(raw: str) -> dict:
    sequences = {}
    for block in raw.split(">")[1:]:
        lines = block.strip().splitlines()
        name = lines[0]
        seq  = "".join(lines[1:]).upper()
        sequences[name] = seq
    return sequences


def gc_content(seq: str) -> float:
    return (seq.count("G") + seq.count("C")) / len(seq) * 100


def transcribe(seq: str) -> str:
    return seq.replace("T", "U")


def count_bases(seq: str) -> dict:
    return {b: seq.count(b) for b in "ACGT"}


# ── 타이틀 ───────────────────────────────────────────────────────────────────
col_title, col_space = st.columns([3, 1])
with col_title:
    if st.button("🧬 DNA Sequence Analyzer", type="secondary", key="title_btn"):
        st.session_state.clear()
        st.rerun()

st.markdown(
    "<p style='color:#94a3b8; font-size:0.88rem; margin-top:-8px;'>"
    "타이틀 클릭 시 처음으로 돌아갑니다</p>",
    unsafe_allow_html=True,
)
st.markdown("<hr>", unsafe_allow_html=True)


# ── 파일 업로드 ───────────────────────────────────────────────────────────────
uploaded = st.file_uploader(
    "서열 파일을 업로드하세요",
    type=["txt", "pdf"],
    label_visibility="collapsed",
    help=".txt 또는 .pdf (FASTA 형식 포함)",
)

if not uploaded:
    st.markdown(
        "<p style='text-align:center; color:#94a3b8; margin-top:16px;'>"
        ".txt 또는 .pdf 파일을 올려주세요 — FASTA 형식도 지원합니다 🧬"
        "</p>",
        unsafe_allow_html=True,
    )
    st.stop()


# ── 파일 읽기 + 계산 ──────────────────────────────────────────────────────────
file_id = f"{uploaded.name}_{uploaded.size}"

if st.session_state.get("file_id") != file_id:
    file_bytes = uploaded.read()

    if uploaded.name.endswith(".pdf"):
        raw_text = extract_text_from_pdf(file_bytes)
        if not raw_text:
            st.stop()
    else:
        raw_text = file_bytes.decode("utf-8", errors="replace")

    sequences = parse_fasta(raw_text)

    st.session_state.file_id   = file_id
    st.session_state.sequences = sequences
else:
    sequences = st.session_state.sequences


if not sequences:
    st.warning("유효한 FASTA 서열을 찾을 수 없습니다.")
    st.stop()


# ── 로잘린드 GC 정답 ──────────────────────────────────────────────────────────
best_name = max(sequences, key=lambda name: gc_content(sequences[name]))
best_gc   = gc_content(sequences[best_name])

st.markdown("<div class='section-header'>🏆 Highest GC-content</div>", unsafe_allow_html=True)
st.code(f"{best_name}\n{best_gc:.6f}", language=None)
st.markdown("<hr>", unsafe_allow_html=True)


# ── 결과 출력 (서열마다) ──────────────────────────────────────────────────────
for name, seq in sequences.items():
    counts = count_bases(seq)
    gc     = gc_content(seq)
    rna    = transcribe(seq)
    total  = len(seq)

    with st.expander(f"🧬 {name}  —  {total:,} bp  |  GC {gc:.6f}%", expanded=False):
        st.markdown("<div class='section-header'>염기 개수</div>", unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("A  (아데닌)",   f"{counts['A']:,}")
        c2.metric("C  (사이토신)", f"{counts['C']:,}")
        c3.metric("G  (구아닌)",   f"{counts['G']:,}")
        c4.metric("T  (티민)",     f"{counts['T']:,}")

        st.markdown("<div class='section-header'>RNA 전사 결과 (T → U)</div>", unsafe_allow_html=True)
        st.code(rna, language=None)

        st.markdown("<div class='section-header'>원본 DNA 서열</div>", unsafe_allow_html=True)
        st.code(seq, language=None)
