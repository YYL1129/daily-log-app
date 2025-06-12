# NOTE: This code requires Streamlit to be installed and run in a local environment or on Streamlit Cloud.
# To run this, save as app.py and execute with: streamlit run app.py

# IMPORTANT: Streamlit must be installed and available in the execution environment.
import streamlit as st

import os
from datetime import datetime
import base64

# Set storage folder (you can map this to OneDrive on your PC if you run locally)
SAVE_DIR = "notes"
os.makedirs(SAVE_DIR, exist_ok=True)

st.title("🗒️ Daily Work Log")

# Input fields
note_title = st.text_input("Title")
note_tags = st.text_input("Tags (comma separated)")
note_text = st.text_area("Write your notes here (Markdown supported)")

uploaded_images = st.file_uploader("Upload images", accept_multiple_files=True, type=["png", "jpg", "jpeg"])

# Save button
if st.button("💾 Save Note"):
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    safe_title = note_title.strip().replace(' ', '_').replace('/', '_') or "untitled"
    filename = f"{SAVE_DIR}/{timestamp}_{safe_title}.md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# {note_title}\n")
        f.write(f"**Tags**: {note_tags}\n")
        f.write(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(note_text + "\n\n")

        # Save images as base64
        if uploaded_images:
            f.write("## Attached Images\n")
            for image in uploaded_images:
                img_bytes = image.read()
                encoded = base64.b64encode(img_bytes).decode()
                ext = image.name.split('.')[-1]
                f.write(f"![](data:image/{ext};base64,{encoded})\n")

    st.success(f"Note saved as {filename}")

# Search notes
st.markdown("---")
st.header("🔍 Search Notes")
query = st.text_input("Search by keyword")

if query:
    matches = []
    for fname in os.listdir(SAVE_DIR):
        filepath = os.path.join(SAVE_DIR, fname)
        if os.path.isfile(filepath):
            with open(filepath, encoding="utf-8") as f:
                content = f.read()
                if query.lower() in content.lower():
                    matches.append((fname, content[:300]))

    if matches:
        for fname, preview in matches:
            st.markdown(f"### {fname}")
            st.markdown(f"```
{preview}...
```")
            st.markdown("---")
    else:
        st.info("No matches found.")
