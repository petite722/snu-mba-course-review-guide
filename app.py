
import json
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="SNU MBA Course Review Guide", page_icon="🎓", layout="centered")

DATA_PATH = Path(__file__).parent / "course_reviews.json"
CSV_PATH = Path(__file__).parent / "course_list.csv"

with open(DATA_PATH, "r", encoding="utf-8") as f:
    COURSES = json.load(f)

st.markdown("""
<style>
.block-container { max-width: 980px; padding-top: 2.2rem; padding-bottom: 3rem; }
h1 { font-size: 2.15rem !important; }
h2 { font-size: 1.45rem !important; margin-top: 1.6rem !important; }
h3 { font-size: 1.20rem !important; margin-top: 1.3rem !important; }
h4 { font-size: 1.08rem !important; margin-top: 1.15rem !important; }
p, li, div, label { font-size: 1.05rem !important; line-height: 1.68 !important; }
.stCaptionContainer p { font-size: 0.94rem !important; }
hr { margin: 1.3rem 0; }
.small-note { color: #666; font-size: 0.94rem; }
</style>
""", unsafe_allow_html=True)

st.title("SNU MBA Course Review Guide")
lang = st.radio("표시 언어 / Display language", ["한국어", "English"], horizontal=True)

if lang == "한국어":
    st.caption("2025년 입학생들의 한국어/영어 수업 후기를 합산해 정리한 비공식 수강 후기 가이드입니다. 원문 후기와 기출문제 내용은 포함하지 않습니다. 한국어와 영어 화면은 같은 후기 수와 같은 내용을 기준으로 표시됩니다.")
    download_label = "전체 수업 목록 다운로드"
    search_label = "수업 이름이나 교수님으로 찾기"
    search_placeholder = "예: 전략, Strategy, 최종학, 한정석, Operations"
    select_label = "수업 선택"
    no_result = "검색 결과가 없습니다. 과목명이나 교수님 이름을 다르게 입력해보세요."
    no_summary = "이 수업은 아직 표시할 수 있는 후기 요약이 없습니다."
    highlights = "후기에서 정리한 내용"
    reviews_word = "후기"
    based_word = "개 기준"
    final_note = "한국어/영어 후기를 합산한 같은 데이터가 언어만 바뀌어 표시됩니다. 문구를 수정하려면 source_summary_workbook.xlsx의 한국어 원문 데이터를 수정한 뒤 앱 데이터를 다시 생성하면 됩니다."
else:
    st.caption("This unofficial course guide is based on the combined Korean and English reviews from the 2025 MBA cohort. Original review text and past exam content are not included. The Korean and English views use the same review count and the same content, shown in different languages.")
    download_label = "Download full course list"
    search_label = "Find a course or professor"
    search_placeholder = "e.g., Strategy, Operations, Choi, Han, 최종학"
    select_label = "Select a course"
    no_result = "No results found. Try another course or professor name."
    no_summary = "No review summary is available for this course yet."
    highlights = "Review highlights"
    reviews_word = "reviews"
    based_word = "based on"
    final_note = "The Korean and English views are based on the same combined review data. Only the display language changes. To edit wording, update the source summary workbook and regenerate the app data."

if CSV_PATH.exists():
    st.download_button(
        label=download_label,
        data=CSV_PATH.read_bytes(),
        file_name="snu_mba_course_list.csv",
        mime="text/csv",
        use_container_width=True,
    )

query = st.text_input(search_label, placeholder=search_placeholder)
filtered = COURSES
if query.strip():
    q = query.strip().lower()
    filtered = [c for c in COURSES if q in c.get("search_text", "").lower()]

if not filtered:
    st.warning(no_result)
    st.stop()

options = [c["display"] for c in filtered]
selected_display = st.selectbox(select_label, options)
course = next(c for c in filtered if c["display"] == selected_display)
meta = course["meta"]
data = course["ko"] if lang == "한국어" else course["en"]

st.divider()
st.subheader(f"{meta['course']} | {meta['professor']}")
count = int(meta.get('review_count', data.get('review_count', 0)) or 0)
if lang == "한국어":
    st.caption(f"{meta.get('term_module','')} · {meta.get('course_language','')} · {reviews_word} {count}개 {based_word}")
else:
    st.caption(f"{meta.get('term_module','')} · {meta.get('course_language','')} · {count} {reviews_word}")

sections = data.get("sections", [])
if not sections:
    st.info(no_summary)
else:
    st.markdown(f"### {highlights}")
    for section in sections:
        title = section.get("title", "").strip()
        bullets = [b.strip() for b in section.get("bullets", []) if b and b.strip()]
        if not title or not bullets:
            continue
        st.markdown(f"#### {title}")
        for bullet in bullets:
            st.markdown(f"- {bullet}")

st.divider()
st.caption(final_note)
