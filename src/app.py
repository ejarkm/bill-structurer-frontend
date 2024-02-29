import streamlit as st
from PIL import Image

from api.handlers.bill_parser_handler import parse_bill
from api.handlers.file_handler import (concatenate_images_vertically,
                                       convert_pdf_to_images)

st.set_page_config(
    page_title="Spaik Invoice Parser",
    page_icon="🧊",
)

st.title("Upload an Iberdrola Invoice")

uploaded_file = st.file_uploader(
    "Upload an Iberdrola Invoice",
    type=["pdf", "jpg", "png", "jpeg"],
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

        attempts = 0  # Initialize the attempts counter
        max_attempts = 3  # Define the maximum number of attempts
        while attempts < max_attempts:
            try:
                with st.spinner("Parsing the bill..."):
                    parsed_bill = parse_bill(
                        image_path=temporary_file_path, bill_type="iberdrola"
                    )

                # If parse_bill succeeds, save the result and break the loop
                st.session_state["parsed_bill"] = parsed_bill
                break  # Exiting the loop after successful execution

            except Exception as e:
                attempts += 1  # Increment attempt counter if an exception occurred
                if attempts == max_attempts:
                    st.error(
                        f"Failed to parse bill after {max_attempts} attempts. Please check the bill format or try again later."
                    )
                else:
                    st.warning(f"Attempt {attempts} failed. Retrying...")


if "parsed_bill" in st.session_state:
    st.write(st.session_state["parsed_bill"])
