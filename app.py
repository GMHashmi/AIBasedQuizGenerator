import streamlit as st
from docx import Document
from pptx import Presentation
from transformers import pipeline
import random
import os




# Function to extract text from a Word document
def extract_text_from_docx(file):
    doc = Document(file)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

# Function to extract text from a PowerPoint presentation
def extract_text_from_pptx(file):
    presentation = Presentation(file)
    full_text = []
    for slide in presentation.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                full_text.append(shape.text)
    return '\n'.join(full_text)

# Function to generate questions using a Hugging Face model
def generate_questions(text, num_questions=5):
    # Load the question-generation pipeline
    qg_model = pipeline('text2text-generation', model='valhalla/t5-small-qa-qg-hl')
    # Generate questions
    generated = qg_model(text)
    return [q['generated_text'] for q in generated[:num_questions]]

# Function to create multiple choice quiz with options
def create_quiz(questions, num_options=4):
    quiz = []
    for question in questions:
        options = [f"Option {i+1}" for i in range(num_options)]  # Placeholder options
        correct_option = random.choice(options)
        quiz.append({
            "question": question,
            "options": options,
            "answer": correct_option
        })
    return quiz

# Function to create an answer key
def create_answer_key(quiz):
    return {i+1: q['answer'] for i, q in enumerate(quiz)}

# Main app function
def main():
    st.title("Quiz Generator")

    # File uploader for the document
    uploaded_file = st.file_uploader("Upload your document", type=["docx", "pptx"])
    
    # If the user uploads a file
    if uploaded_file is not None:
        # Determine the file type and extract text accordingly
        if uploaded_file.name.endswith(".docx"):
            text = extract_text_from_docx(uploaded_file)
        elif uploaded_file.name.endswith(".pptx"):
            text = extract_text_from_pptx(uploaded_file)

        # Display the extracted text
        st.write("Extracted Text:")
        st.write(text)

        # Number input for the number of quiz questions
        num_questions = st.number_input("How many questions would you like in the quiz?", min_value=1, max_value=20, step=1)

        # Generate the quiz when the user clicks the button
        if st.button("Generate Quiz"):
            questions = generate_questions(text, num_questions)
            quiz = create_quiz(questions)

            st.write("Quiz:")
            for i, q in enumerate(quiz):
                st.write(f"Q{i+1}: {q['question']}")
                for opt in q['options']:
                    st.write(f"- {opt}")

            # Generate and display the answer key
            answer_key = create_answer_key(quiz)
            st.write("Answer Key:")
            st.write(answer_key)

if __name__ == "__main__":
    main()
