#importing required libraries
import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
import streamlit as st
from langchain_community.callbacks.manager import get_openai_callback
from src.mcqgenerator.logger import logging
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain

#read Responce json file tp format the MCQs
with open('Response.json', 'r') as file:
    try:
        JSON_Response = json.load(file)
    except json.JSONDecodeError as e:
        st.error(f"Error parsing JSON: {e}")

#creating a Title for the APP
st.title("MCQs Creator Application with LangChain 🔗 and Open AI 🤖") 

# Display an image (e.g., LangChain logo) at the top
st.image("langchainsymbol.png", width=150)

with st.form("user input"):
    upload_file = st.file_uploader("Upload PDF or Text file")
    mcq_count = st.number_input("no of MCQs",min_value=3,max_value=50)
    subject = st.text_input("Insert Subject",max_chars=20)
    tone = st.text_input("Complexity Level of Questions",max_chars=20, placeholder="simple")
    button=st.form_submit_button("Generate MCQs")

    if button and upload_file is not None and mcq_count and subject and tone:
        with st.spinner("loading..."):
            try:
                text = read_file(upload_file)
                #count tokens and cost of the API
                with get_openai_callback() as cb:
                    response = generate_evaluate_chain(
                        {
                            "text": text,
                            "number": mcq_count,
                            "subject": subject,
                            "tone": tone,
                            "JSON_Response": json.dumps(JSON_Response)
                        }
                    )
                #st.write(response)

            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error")

            else:
                st.write(f"Total Tokens: {cb.total_tokens}")
                st.write(f"Prompt Tokens: {cb.prompt_tokens}")
                st.write(f"Completion Tokens: {cb.completion_tokens}")
                st.write(f"Total Cost: {cb.total_cost}")


                if isinstance(response,dict):
                    #Extract the quize data from the responce
                    quiz = response.get("quiz",None)
                    if quiz is not None:
                        table_data = get_table_data(quiz)
                        if table_data is not None:
                            df = pd.DataFrame(table_data)
                            df.index=df.index+1
                            st.table(df)
                            #Display the review in a text box as well
                            st.text_area(label="Review", value=response.get("review", "No review available"))

                        else:
                            st.error("Error in processing the table data")
                    else:
                        st.write("Quiz data not found in the response.")

                else:
                    st.write("Invalid Responce format")

                