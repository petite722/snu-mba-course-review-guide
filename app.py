
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
.block-container { max-width: 880px; padding-top: 1.6rem; padding-bottom: 2.2rem; }
h1 { font-size: 1.9rem !important; }
h2 { font-size: 1.32rem !important; margin-top: 1.3rem !important; }
h3 { font-size: 1.12rem !important; margin-top: 1.1rem !important; }
h4 { font-size: 1.02rem !important; margin-top: 1rem !important; }
p, li, div, label { font-size: 0.96rem !important; line-height: 1.55 !important; }
.stCaptionContainer p { font-size: 0.88rem !important; }
hr { margin: 1rem 0; }
.small-note { color: #666; font-size: 0.88rem; }
</style>
""", unsafe_allow_html=True)

st.title("SNU MBA Course Review Guide")
lang = st.radio("표시 언어 / Display language", ["한국어", "English"], horizontal=True)

if lang == "한국어":
    st.caption("이 가이드는 2025년 입학생들의 수업 후기를 바탕으로 정리한 비공식 자료입니다. 원문 후기와 기출문제 내용은 포함하지 않았습니다.")
    download_label = "전체 수업 목록 다운로드"
    search_label = "수업 이름이나 교수님으로 찾기"
    search_placeholder = "예: 전략, Strategy, 최종학, 한정석, Operations"
    select_label = "수업 선택"
    no_result = "검색 결과가 없습니다. 과목명이나 교수님 이름을 다르게 입력해보세요."
    no_summary = "이 수업은 아직 표시할 수 있는 후기 요약이 없습니다."
    highlights = "후기에서 정리한 내용"
    reviews_word = "후기"
    based_word = "기준"
    final_note = "한국어/영어 후기를 합산한 같은 데이터가 언어만 바뀌어 표시됩니다."
else:
    st.caption("This guide is an unofficial summary based on course reviews from the 2025 MBA cohort. Original review texts and past exam materials are not included.")
    download_label = "Download full course list"
    search_label = "Find a course or professor"
    search_placeholder = "e.g., Strategy, Operations, Choi, Han, 최종학"
    select_label = "Select a course"
    no_result = "No results found. Try another course or professor name."
    no_summary = "No review summary is available for this course yet."
    highlights = "Review highlights"
    reviews_word = "reviews"
    based_word = "based on"
    final_note = "The Korean and English views are based on the same combined review data. Only the display language changes."

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

placeholder = "수업을 선택하세요" if lang == "한국어" else "Select a course"
options = [placeholder] + [c["display"] for c in filtered]

selected_display = st.selectbox(select_label, options)

if selected_display == placeholder:
    st.info(
        "궁금한 수업을 검색하거나 목록에서 선택해 주세요."
        if lang == "한국어"
        else "Search for a course or select one from the list."
    )
    st.stop()

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
