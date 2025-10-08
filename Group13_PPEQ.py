#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import pandas as pd

# ==============================
# Session State Initialization
# ==============================
if 'students' not in st.session_state:
    st.session_state.students = {}
if 'global_count' not in st.session_state:
    st.session_state.global_count = 0

# ==============================
# Constants
# ==============================
VOWELS = set("AEIOU")

ACCENT_MAP = {
    'À':'A','Á':'A','Â':'A','Ã':'A','Ä':'A','Å':'A','Ā':'A','Ă':'A','Ą':'A',
    'à':'A','á':'A','â':'A','ã':'A','ä':'A','å':'A','ā':'A','ă':'A','ą':'A',
    'Ç':'C','Ć':'C','Ĉ':'C','Ċ':'C','Č':'C','ç':'C','ć':'C','ĉ':'C','ċ':'C','č':'C',
    'È':'E','É':'E','Ê':'E','Ë':'E','Ē':'E','Ĕ':'E','Ė':'E','Ę':'E','Ě':'E',
    'è':'E','é':'E','ê':'E','ë':'E','ē':'E','ĕ':'E','ė':'E','ę':'E','ě':'E',
    'Ì':'I','Í':'I','Î':'I','Ï':'I','Ĩ':'I','Ī':'I','Ĭ':'I','Į':'I','İ':'I',
    'ì':'I','í':'I','î':'I','ï':'I','ĩ':'I','ī':'I','ĭ':'I','į':'I','ı':'I',
    'Ñ':'N','Ń':'N','Ņ':'N','Ň':'N','ñ':'N','ń':'N','ņ':'N','ň':'N',
    'Ò':'O','Ó':'O','Ô':'O','Õ':'O','Ö':'O','Ø':'O','Ō':'O','Ŏ':'O','Ő':'O',
    'ò':'O','ó':'O','ô':'O','õ':'O','ö':'O','ø':'O','ō':'O','ŏ':'O','ő':'O',
    'Œ':'OE','œ':'OE',
    'Ù':'U','Ú':'U','Û':'U','Ü':'U','Ũ':'U','Ū':'U','Ŭ':'U','Ů':'U','Ű':'U','Ų':'U',
    'ù':'U','ú':'U','û':'U','ü':'U','ũ':'U','ū':'U','ŭ':'U','ů':'U','ű':'U','ų':'U',
    'Ý':'Y','ý':'Y','ÿ':'Y','Ÿ':'Y',
    'ß':'SS',
    'Ä':'A','Ö':'O','Ü':'U','ä':'A','ö':'O','ü':'U',
    'Å':'A','å':'A','Ø':'O','ø':'O','Æ':'AE','æ':'AE',
    'Ł':'L','ł':'L','Š':'S','š':'S','Ž':'Z','ž':'Z','Ć':'C','ć':'C','Đ':'D','đ':'D','Ř':'R','ř':'R','Ň':'N','ň':'N'
}

# ==============================
# Utility Functions
# ==============================
def remove_accents(s: str) -> str:
    return "".join(ACCENT_MAP.get(ch, ch) for ch in s)

def is_valid_name_input(s: str) -> bool:
    return all(c.isalpha() or c in " -" for c in s)

def normalize_name_for_key(s: str) -> str:
    s = remove_accents(s)
    s = s.upper().replace(" ", "").replace("-", "")
    return s

def extract_consonants(name_norm: str) -> str:
    consonants = [c for c in name_norm if c not in VOWELS]
    return "".join(consonants[:3]).ljust(3, "X")

def extract_letters(name_norm: str) -> str:
    return name_norm[:3].ljust(3, "X")

def generate_registration_number(last_name: str, first_name: str) -> str:
    if not (is_valid_name_input(last_name) and is_valid_name_input(first_name)):
        return "❌ Error: Names must contain only letters, spaces, or hyphens."

    last_norm = normalize_name_for_key(last_name)
    first_norm = normalize_name_for_key(first_name)
    key = (last_norm, first_norm)

    if key in st.session_state.students:
        return f"⚠️ Already registered: {st.session_state.students[key]['reg']}"

    field1 = extract_consonants(last_norm)
    field2 = extract_letters(first_norm)

    st.session_state.global_count += 1
    count = str(st.session_state.global_count).rjust(3, "0")
    reg_number = field1 + field2 + count

    st.session_state.students[key] = {
        "reg": reg_number,
        "last": last_name,
        "first": first_name
    }
    return reg_number

# ==============================
# Streamlit UI
# ==============================
st.set_page_config(page_title="Student Registration Number Generator", page_icon="🎓", layout="centered")

st.title(" Student Registration Number Generator ( Group 14)")

st.write(
    """
    Enter a **last name** and **first name** to generate a unique student registration number.
    The number is based on consonants, letters, and a sequential counter.
    """
)
st.markdown(
    """
    **Group Members:**  
    Rabecca Kanini KATING'U  <br>
    Samuel AGYEKUM  <br>
    Zo Lalaina Andrianina ANDRIANANTENAINA  <br>
    Loyde AIJUKA
    """,
    unsafe_allow_html=True
)

# Input form
with st.form("registration_form"):
    last_name = st.text_input("Last Name")
    first_name = st.text_input("First Name")
    submit_button = st.form_submit_button("Generate Registration Number")

if submit_button:
    if last_name.strip() == "" or first_name.strip() == "":
        st.error("⚠️ Please fill in both last name and first name.")
    else:
        reg_num = generate_registration_number(last_name.strip(), first_name.strip())
        if reg_num.startswith("❌"):
            st.error(reg_num)
        elif reg_num.startswith("⚠️"):
            st.warning(reg_num)
        else:
            st.success(f"✅ Registration Number: **{reg_num}**")

# Display all registered students
if st.session_state.students:
    st.subheader("📋 Registered Students")
    df = pd.DataFrame(st.session_state.students.values())
    st.dataframe(df, use_container_width=True)
else:
    st.info("No students registered yet.")

# Footer
st.markdown("---")
st.caption("Developed with ❤️ using Streamlit")
