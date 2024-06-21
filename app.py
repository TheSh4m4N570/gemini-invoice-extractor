import os
import streamlit as st
import google.generativeai as genai

from PIL import Image
from dotenv import load_dotenv
load_dotenv() # load all the env variables from .env file

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini Pro Vision
model = genai.GenerativeModel(model_name="gemini-pro-vision")

def get_gemini_response(input, image, prompt):
    response = model.generate_content([input, image[0], prompt])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        # the file into bytes
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Initialize streamlit app
st.set_page_config(page_title="Multilanguage Invoice Extractor")
st.header("Multilanguage Invoice Extractor")
input = st.text_input("Input prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image of the invoice...", type=["jpg", "png", "jpeg"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

submit = st.button("Tell me about the invoice")
input_prompt = """
    You are an expert in understanding invoices. We will upload an image as invoices and you will have to answer any
    questions based on the uploaded invoice image.
"""

# If submit button is clicked
if submit:
    image_data = input_image_setup(uploaded_file=uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)
    st.subheader("The response is ")
    st.write(response)