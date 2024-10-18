#Importing Required Libraries
from langchain_community.llms import OpenAI
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from langchain_community.callbacks.manager import get_openai_callback
import os
import json
import pandas as pd
import traceback
from dotenv import load_dotenv
import PyPDF2

# Load environment variables from the .env file
load_dotenv() 
my_key = os.getenv("APIKey")  # Fetch the API key

#Model
llm = ChatOpenAI(openai_api_key = my_key, model_name = "gpt-3.5-turbo", temperature= 0.7 )

with open('Response.json', 'r') as file:
    try:
        JSON_Response = json.load(file)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")

######################Quize Generation Prompt#####################

TEMPLATE1 ="""
Text:{text}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz  of {number} multiple choice questions for {subject} students in {tone} tone. 
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like  RESPONSE_JSON below  and use it as a guide. \
Ensure to make {number} MCQs
### RESPONSE_JSON
{JSON_Response}
"""
quize_generation_prompt = PromptTemplate(
    input_variables=["text","number","subject","tone","JSON_Response"],
    template= TEMPLATE1)

#quize_chain
quize_chain = LLMChain(llm=llm, prompt=quize_generation_prompt, output_key="quiz", verbose=True)

#####################Quize Evaluation Prompt#####################

TEMPLATE2 ="""
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis. 
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz questions which need to be changed and change the tone such that it perfectly fits the student abilities
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""
quiz_evaluation_prompt = PromptTemplate(
    input_variables=["subject", "quiz"], 
    template=TEMPLATE2)

review_chain = LLMChain(llm=llm, prompt=quiz_evaluation_prompt, output_key="review", verbose=True)

#####################Sequention Chain: combine Quize chain&review chain#############
# Define SequentialChain
generate_evaluate_chain = SequentialChain(
    chains=[quize_chain, review_chain], 
    input_variables=["text", "number", "subject", "tone", "JSON_Response"],
    output_variables=["quiz", "review"],  # Ensure this matches the output keys
    verbose=True)





