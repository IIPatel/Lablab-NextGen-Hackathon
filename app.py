import streamlit as st
from clarifai.client.model import Model
import base64
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO

load_dotenv()
import os
