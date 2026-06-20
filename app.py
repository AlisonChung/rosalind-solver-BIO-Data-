import streamlit as st
import re
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
/* 전체 배경 */
.stApp { background: #ffffff; }

/* 타이틀 버튼 */
div[data-testid="stButton"] > button[kind="secondary"] {
    background: none;
    border: none;
    padding: 0;
    color: #1a1a1a;
    font-size: 2rem;
    font-weight: 700;
    letter-spacing: -0.5px;
    cursor: pointer;
    box-shadow: none;
}
div[data-testid="stButton"] > button[kind="secondary"]:hover {
    color: #2563eb;
    background: none;
    border: none;
    box-shadow: none;
}

/* metric 카드 */
div[data-testid="stMetric"] {
    background: #f8faff;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 16px 20px;
}
div[data-testid="stMetricLabel"] { font-size: 0.85rem; color: #64748b; }
div[data-testid="stMetricValue"] { font-size: 2rem; font-weight: 700; color: #1e3a5f; }

/* 총 길이 뱃지 */
.length-badge {
    display: inline-block;
    background: #2563eb;
    color: white;
    font-size: 0.85rem;
    font-weight: 600;
    padding: 4px 14px;
    border-radius: 999px;
    margin-bottom: 18px;
}

/* 섹션 헤더 */
.section-header {
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #94a3b8;
    margin: 28px 0 10px 0;
}

/* 업로드 영역 커스텀 */
section[data-testid="stFileUploaderDropzone"] {
    border: 2px dashed #cbd5e1 !important;
    border-radius: 12px !important;
    background: #f8faff !important;
}

/* 경고 메시지 */
.warn-box {
    background: #fffbeb;
    border-left: 3px solid #f59e0b;
    border-radius: 4px;
    padding: 10px 14px;
    font-size: 0.85rem;
    color: #92400e;
    margin-top: 12px;
}

/* 구분선 */
hr { border: none; border-top: 1px solid #e2e8f0; margin: 24px 0; }
</style>
""", unsafe_allow_html=True)


# ── 유틸 함수 ─────────────────────────────────────────────────────────────────
def extract_text_from_pdf(file_bytes: bytes) -> str:
    try:
        import pdfplumber
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            return "\n".join(
                page.extract_text() or "" for page in pdf.pages
            )
    except Exception as e:
        st.error(f"PDF 파싱 실패: {e}\n\n텍스트 파일(.txt)로 변환 후 다시 시도해 주세요.")
        return ""


def clean_sequence(raw: str) -> tuple[str, list[str]]:
    """FASTA 헤더·공백·줄바꿈 제거 후 순수 서열 반환. 잘못된 문자 목록도 같이 반환."""
    lines = raw.splitlines()
    seq_lines = [l for l in lines if not l.startswith(">")]
    joined = "".join(seq_lines).upper()
    joined = re.sub(r"\s+", "", joined)

    valid = re.sub(r"[^ACGT]", "", joined)
    invalid_chars = sorted(set(re.sub(r"[ACGT]", "", joined)))
    return valid, invalid_chars


def count_bases(seq: str) -> dict:
    return {b: seq.count(b) for b in "ACGT"}


def transcribe(seq: str) -> str:
    return seq.replace("T", "U")


# ── 세션 초기화 ───────────────────────────────────────────────────────────────
if "reset" not in st.session_state:
    st.session_state.reset = False


# ── 타이틀 (클릭하면 리셋) ────────────────────────────────────────────────────
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


# ── 파일 읽기 + 계산 (새 파일일 때만, 그 외엔 session_state 재사용) ──────────
file_id = f"{uploaded.name}_{uploaded.size}"

if st.session_state.get("file_id") != file_id:
    file_bytes = uploaded.read()

    if uploaded.name.endswith(".pdf"):
        raw_text = extract_text_from_pdf(file_bytes)
        if not raw_text:
            st.stop()
    else:
        raw_text = file_bytes.decode("utf-8", errors="replace")

    sequence, invalid_chars = clean_sequence(raw_text)
    counts   = count_bases(sequence)
    rna      = transcribe(sequence)
    total    = len(sequence)
    gc_pct   = (counts["G"] + counts["C"]) / total * 100 if total > 0 else 0
    copy_str = f"{counts['A']} {counts['C']} {counts['G']} {counts['T']}"

    st.session_state.file_id      = file_id
    st.session_state.sequence     = sequence
    st.session_state.invalid_chars = invalid_chars
    st.session_state.counts       = counts
    st.session_state.rna          = rna
    st.session_state.total        = total
    st.session_state.gc_pct       = gc_pct
    st.session_state.copy_str     = copy_str
else:
    sequence      = st.session_state.sequence
    invalid_chars = st.session_state.invalid_chars
    counts        = st.session_state.counts
    rna           = st.session_state.rna
    total         = st.session_state.total
    gc_pct        = st.session_state.gc_pct
    copy_str      = st.session_state.copy_str


# ── 서열 유효성 체크 ──────────────────────────────────────────────────────────
if not sequence:
    st.warning("유효한 서열을 찾을 수 없습니다. A/C/G/T로 이루어진 서열이 포함된 파일을 올려주세요.")
    st.stop()

if invalid_chars:
    st.markdown(
        f"<div class='warn-box'>⚠ A/C/G/T 외의 문자가 포함되어 있어 무시했습니다: "
        f"<b>{', '.join(invalid_chars)}</b></div>",
        unsafe_allow_html=True,
    )


# ── 결과 출력 ─────────────────────────────────────────────────────────────────
st.markdown("<div class='section-header'>염기 개수</div>", unsafe_allow_html=True)

st.markdown(
    f"<span class='length-badge'>총 서열 길이 {total:,} bp &nbsp;|&nbsp; GC {gc_pct:.1f}%</span>",
    unsafe_allow_html=True,
)

c1, c2, c3, c4 = st.columns(4)
c1.metric("A  (아데닌)",  f"{counts['A']:,}")
c2.metric("C  (사이토신)", f"{counts['C']:,}")
c3.metric("G  (구아닌)",  f"{counts['G']:,}")
c4.metric("T  (티민)",    f"{counts['T']:,}")

st.code(copy_str, language=None)

st.markdown("<div class='section-header'>RNA 전사 결과 (T → U)</div>", unsafe_allow_html=True)
st.code(rna, language=None)

st.markdown("<div class='section-header'>원본 DNA 서열</div>", unsafe_allow_html=True)
with st.expander("원본 서열 보기", expanded=False):
    st.code(sequence, language=None)
