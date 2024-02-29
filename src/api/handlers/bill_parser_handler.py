import os
import requests


def parse_bill(*, image_path, bill_type):
    api_url = "https://bill-structurer-production.up.railway.app/parse-bill"

    # Define the headers
    headers = {"INVOICE_API_KEY": os.environ.get("INVOICE_API_KEY")}

    # Define the data and files to be sent in the POST request
    data = {"bill_type": bill_type}
    files = {"uploaded_file": (image_path, open(image_path, "rb"), "image/jpeg")}

    # Make the POST request
    response = requests.post(api_url, headers=headers, data=data, files=files)
    files["uploaded_file"][1].close()

    return response.json()
