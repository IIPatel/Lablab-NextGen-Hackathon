import streamlit as st
from clarifai.client.model import Model
from clarifai.client.input import Inputs
import base64
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO

load_dotenv()
import os

#Function to encode image to base64 format
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

Function to analyze the O&M issue and provide a solution
def analyze_om_issue(base64_image, user_description):
    prompt = f"Analyze the following image from an Operations and Maintenance industry, considering the user's description of the issue: '{user_description}'. Provide a detailed, professional solution, including safety precautions and step-by-step instructions:"
    inference_params = dict(temperature=0.7, image_base64=base64_image)
    model_prediction = Model(
        "https://clarifai.com/openai/chat-completion/models/gpt-4-vision"
    ).predict_by_bytes(
        prompt.encode(), input_type="text", inference_params=inference_params
    )
    return model_prediction.outputs[0].data.text.raw
    
def understand_image(base64_image):
    prompt = "Analyze the content of this image and write a creative, engaging story that brings the scene to life. Describe the setting, and actions in a way that would captivate a young audience:"
    inference_params = dict(temperature=0.2, image_base64=base64_image)
    model_prediction = Model(
        "https://clarifai.com/openai/chat-completion/models/gpt-4-vision"
    ).predict_by_bytes(
        prompt.encode(), input_type="text", inference_params=inference_params
    )
    return model_prediction.outputs[0].data.text.raw

def generate_image(user_description):
    prompt = f"You are a professional scenery artist. Based on the below user's description and content, create a scenery without living beings: {user_description}"
    inference_params = dict(quality="standard", size="1024x1024")
    model_prediction = Model(
        f"https://clarifai.com/openai/dall-e/models/dall-e-3"
    ).predict_by_bytes(
        prompt.encode(), input_type="text", inference_params=inference_params
    )
    output_base64 = model_prediction.outputs[0].data.image.base64
    with open("generated_image.png", "wb") as f:
        f.write(output_base64)
    return "generated_image.png"

def text_to_speech(input_text):
    inference_params = dict(voice="alloy", speed=1.0)
    model_prediction = Model(
        "https://clarifai.com/openai/tts/models/openai-tts-1"
    ).predict_by_bytes(
        input_text.encode(), input_type="text", inference_params=inference_params
    )
    audio_base64 = model_prediction.outputs[0].data.audio.base64
    return audio_base64

def main():
    st.set_page_config(page_title="OMNI: AI O&M Assistant", layout="wide")
    st.title("OMNI: AI Operations and Maintenance Assistant")
   # st.set_page_config(page_title="Interactive Media Creator", layout="wide")
   # st.title("Interactive Media Creator")

    user_pat = st.text_input("Enter your Clarifai Personal Access Token:", type="password")

# Set the environment variable if the user has entered a PAT
    if user_pat:
        os.environ['CLARIFAI_PAT'] = user_pat
        clarifai_pat = os.getenv("CLARIFAI_PAT")


    with st.sidebar:
        st.header("Controls")
        uploaded_image = st.file_uploader("Upload an image related to your O&M issue", type=["png", "jpg", "jpeg"])
        om_issue_description = st.text_area("Describe your O&M Issue", height=100)
        analyze_btn = st.button("Analyze Issue")
        #st.header("Controls")
       # image_description = st.text_area("Description for Image Generation", height=100)
       # generate_image_btn = st.button("Generate Image")

    #col1, col2 = st.columns(2)
    

        if analyze_btn and uploaded_image and om_issue_description:
            with st.spinner("Analyzing O&M issue..."):
            base64_image = encode_image(uploaded_image)
            solution_text = analyze_om_issue(base64_image, om_issue_description)
            st.write(solution_text)
            audio_base64 = text_to_speech(solution_text)
            st.audio(audio_base64, format="audio/mp3")
            st.success("Analysis and audio solution generated!")
   # with col1:
       # st.header("Comic Art")
     #   if generate_image_btn and image_description:
           # with st.spinner("Generating image..."):
              #  image_path = generate_image(image_description)
               # if image_path:
                 #   st.image(
                     #   image_path,
                       # caption="Generated Comic Image",
                     #   use_column_width=True,
                  #  )
                 #   st.success("Image generated!")
              #  else:
                 #   st.error("Failed to generate image.")

  #  with col2:
      #  st.header("Story")
       # if generate_image_btn and image_description:
          #  with st.spinner("Creating a story..."):
         #       base64_image = encode_image(image_path)
              #  understood_text = understand_image(base64_image)
              #  audio_base64 = text_to_speech(understood_text)
             #   st.audio(audio_base64, format="audio/mp3")
              #  st.success("Audio generated from image understanding!")

if __name__ == "__main__":
    main()
