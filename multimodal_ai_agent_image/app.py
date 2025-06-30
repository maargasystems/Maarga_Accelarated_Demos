import streamlit as st
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.media import Image
import tempfile
import os

def main():
    # Streamlit app title
    st.title("Multimodal Reasoning AI Agent 🧠")
    
    # Get OpenRouter API key from user
    openrouter_api_key = st.text_input("Enter your OpenRouter API Key", type="password")
    st.info("💡 Get your OpenRouter API key from https://openrouter.ai/")
    
    if not openrouter_api_key:
        st.warning("Please enter your OpenRouter API key to continue.")
        return
    
    # Set up the reasoning agent with OpenRouter
    agent = Agent(
        model=OpenAIChat(
            id="google/gemini-2.5-flash-preview-05-20:thinking",
            base_url="https://openrouter.ai/api/v1",
            api_key=openrouter_api_key,
        ), 
        markdown=True
    )

    # Instruction
    st.write(
        "Upload an image and provide a reasoning-based task for the AI Agent. "
        "The AI Agent will analyze the image and respond based on your input."
    )

    # File uploader for image
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        try:
            # Save uploaded file to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                temp_path = tmp_file.name

            # Display the uploaded image
            st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

            # Input for dynamic task
            task_input = st.text_area(
                "Enter your task/question for the AI Agent:"
            )

            # Button to process the image and task
            if st.button("Analyze Image") and task_input:
                with st.spinner("AI is thinking... 🤖"):
                    try:
                        # Create Image object from the temporary file
                        image = Image(filepath=temp_path)
                        
                        # Call the agent with the dynamic task and image object
                        response = agent.run(
                            message=task_input, 
                            images=[image]
                        )
                        
                        # Display the response from the model
                        st.markdown("### AI Response:")
                        st.markdown(response.content)
                    except Exception as e:
                        st.error(f"An error occurred during analysis: {str(e)}")
                    finally:
                        # Clean up temp file
                        if os.path.exists(temp_path):
                            os.unlink(temp_path)

        except Exception as e:
            st.error(f"An error occurred while processing the image: {str(e)}")

if __name__ == "__main__":
    main()