# NOTE: This code requires Streamlit to be installed and run in a local environment or on Streamlit Cloud.
# To run this, save as app.py and execute with: streamlit run app.py

import streamlit as st
import os
from datetime import datetime
import base64

# Set storage folder (you can map this to OneDrive on your PC if you run locally)
SAVE_DIR = r"D:\OneDrive - Advance IT Solution Enterprise\Daily_Log_App_1129"
os.makedirs(SAVE_DIR, exist_ok=True)
UPLOAD_DIR = os.path.join(SAVE_DIR, "attachments")
os.makedirs(UPLOAD_DIR, exist_ok=True)

st.title("🗒️ Daily Work Log")

# Input fields
note_title = st.text_input("Title")
note_tags = st.text_input("Tags (comma separated)")
note_text = st.text_area("Write your notes here (Markdown supported)")

uploaded_images = st.file_uploader("Upload images", accept_multiple_files=True, type=["png", "jpg", "jpeg"])
uploaded_files = st.file_uploader("Upload other files (Excel, Word, PDF, etc.)", accept_multiple_files=True, type=["pdf", "docx", "xlsx", "txt", "pptx"])

# Save button
if st.button("💾 Save Note"):
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    safe_title = note_title.strip().replace(' ', '_').replace('/', '_') or "untitled"
    filename = f"{SAVE_DIR}/{timestamp}_{safe_title}.html"

    with open(filename, "w", encoding="utf-8") as f:
        f.write("<html><body style='font-family: Arial, sans-serif;'>\n")
        f.write(f"<h1>{note_title}</h1>\n")
        f.write(f"<p><strong>Tags:</strong> {note_tags}</p>\n")
        f.write(f"<p><strong>Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p><hr>\n")
        f.write(f"<div>{note_text.replace(chr(10), '<br>')}</div><br><br>\n")

        # Save and show images
        if uploaded_images:
            f.write("<h2>Images</h2>\n")
            for i, image in enumerate(uploaded_images):
                ext = image.name.split('.')[-1]
                img_name = f"{timestamp}_{i}.{ext}"
                img_path = os.path.join(UPLOAD_DIR, img_name)
                with open(img_path, "wb") as img_file:
                    img_file.write(image.read())
                f.write(f"<img src='attachments/{img_name}' style='max-width:100%;'><br><br>\n")

        # Save and link uploaded files
        if uploaded_files:
            f.write("<h2>Attached Files</h2><ul>\n")
            for i, doc in enumerate(uploaded_files):
                file_name = f"{timestamp}_{doc.name}"
                file_path = os.path.join(UPLOAD_DIR, file_name)
                with open(file_path, "wb") as doc_file:
                    doc_file.write(doc.read())
                f.write(f"<li><a href='attachments/{file_name}' target='_blank'>{doc.name}</a></li>\n")
            f.write("</ul>\n")

        f.write("</body></html>")

    st.success(f"Note saved as {filename}")

# Search notes
st.markdown("---")
st.header("🔍 Search Notes")
query = st.text_input("Search by keyword")

if query:
    matches = []
    for fname in os.listdir(SAVE_DIR):
        filepath = os.path.join(SAVE_DIR, fname)
        if os.path.isfile(filepath) and fname.endswith(".html"):
            with open(filepath, encoding="utf-8") as f:
                content = f.read()
                if query.lower() in content.lower():
                    matches.append((fname, content[:300]))

    if matches:
        for fname, preview in matches:
            st.markdown(f"### {fname}")
            st.markdown(f"```\n{preview}...\n```")
            st.markdown("---")
    else:
        st.info("No matches found.")
