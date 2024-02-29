import streamlit as st
from PIL import Image
import os

from api.handlers.file_handler import (
    concatenate_images_vertically,
    convert_pdf_to_images,
)
from api.handlers.bill_parser_handler import parse_bill

st.title("Upload an Iberdrola Invoice")

uploaded_file = st.file_uploader(
    "Upload an Iberdrola Invoice",
    type=["pdf", "jpg", "png", "jpeg", "PNG", "JPG", "JPEG", "PDF"],
)

if uploaded_file is not None:
    # Check the file format
    if uploaded_file.name.lower().endswith(".pdf"):
        # Convert PDF to images
        images = convert_pdf_to_images(uploaded_file)

        # Concatenate images vertically
        image = concatenate_images_vertically(images)
        st.session_state["image"] = image
    else:
        # For non-PDF files, just display the uploaded image
        image = Image.open(uploaded_file)
        st.session_state["image"] = image

if "image" in st.session_state:
    st.image(image, caption="Uploaded Image", use_column_width=True)

    temporary_file_path = "temp_image_upload.jpg"
    image.save(temporary_file_path)

    if st.button("Parse Bill"):

        with st.spinner("Parsing the bill..."):
            parsed_bill = parse_bill(image_path=temporary_file_path, bill_type="iberdrola")
            if parsed_bill is None:
                st.error("Failed to parse the bill, please try again.")
            else:
                st.success("Bill parsed successfully!")
                os.remove(temporary_file_path)
                st.session_state["parsed_bill"] = parsed_bill

if "parsed_bill" in st.session_state:
    st.write(st.session_state["parsed_bill"])
