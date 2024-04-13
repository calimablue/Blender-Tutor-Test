# Cell 1: Setup
import streamlit as st
from openai import OpenAI
import os

# Get your OpenAI API key from environment variables 
api_key = os.getenv("OPENAI_API_KEY")  # Used in production
client = OpenAI(api_key=api_key)

# Cell 2: Title & Description
st.title('Blender Project Generator')
st.markdown('I was made to help generate Blender project ideas.')

# Cell 3: Function to generate text using OpenAI
def analyze_text(text="A stopwatch", desiredTime=5, skillLevel = "Beginner", projectType = "model"):
    if not api_key:
        st.error("OpenAI API key is not set. Please set it in your environment variables.")
        return
    
    client = OpenAI(api_key=api_key)
    model = "gpt-3.5-turbo"  # Using the GPT-3.5 model

    # Instructions for the AI (adjust if needed)
    messages = [
        {"role": "system", "content": "You are an assistant who helps generate inspiring and instructive Blender modeling project ideas. When designing projects, please ensure the difficulty aligns with their reported skill level, the generated project can reasonably be completed in their desired amount of time, and that the subject matter and project type (e.g. model or animation) aligns with what was requested."},
        {"role": "user", "content": f"Please generate a new Blender project plan for me. I would like the output to include the following sections: 1. **PROJECT OVERVIEW** - Provide a detailed list including the project name, subject matter, estimated difficulty, estimated completion time, and some engaging background flavor text to get me excited about the project. 2. **REQUIRED SKILLS** - List the specific Blender skills required for this project, such as sculpting, texturing, animating, scripting, instancing, modifiers, and retopology. 3. **RECOMMENDED STEPS** - Please provide a detailed guide for creating a simple {projectType} in Blender. Each step should include specific objectives, essential Blender tools or techniques to be used, and expert advice to help me optimize my workflow and achieve professional results. Additionally, include tailored advice for each step to help me navigate through the complexities of the suggested project. /n I am currently a {skillLevel} in Blender looking for an approximately {desiredTime} hour project that features {text} as the subject matter."}
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.15  # Lower temperature for less random responses
    )
    return response.choices[0].message.content

def generate_image(text="A stopwatch"):
    if not api_key:
        st.error("OpenAI API key is not set. Please set it in your environment variables.")
        return

    response = client.images.generate(
        model="dall-e-3",
        prompt=text,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    # Assuming the API returns an image URL; adjust based on actual response structure
    return response.data[0].url

# Cell 4: Streamlit UI 
user_input = st.text_area("Indicate a subject matter of interest:", "A capybarra on a tugboat")
desired_project_time = st.sidebar.slider("Desired Time in Hours", 0, 100, 5)
skill_level = st.sidebar.selectbox("Your Skill Level", ["Beginner", "Intermediate", "Advanced"])
project_type = st.sidebar.selectbox("Your Desired Project Type", ["Animation", "Model"])

if st.button('Generate My Project Idea'):
    with st.spinner('Generating Project Outline Content...'):
        post_text = analyze_text(user_input, desired_project_time, skill_level, project_type)
        st.write(post_text)

    with st.spinner('Generating Inspirational Image...'):
        thumbnail_url = generate_image(user_input)  # Consider adjusting the prompt for image generation if needed
        st.image(thumbnail_url, caption='Generated Thumbnail')
