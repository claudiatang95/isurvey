import streamlit as st
from agent_functions import generate_response


st.title("Survey on the Use of Generative AI ")

st.write("1. Which generative AI tool do you use most frequently?")
st.checkbox("ChatGPT")
st.checkbox("Copilot")
st.checkbox("Other",key="tool_other")

question_purpose = "2. What are the purposes of using generative AI in your daily life?"
st.write(question_purpose)
choice_a = st.checkbox("Information searching")
choice_b = st.checkbox("Assistance with tasks(e.g. planning trips, writing, or translating)")
choice_c = st.checkbox("Other",key="purpose_other")


if choice_a:
   st.write("What kinds of information do you primarily search with AI?")
   choice_a_a = st.checkbox("Health information")
   choice_a_b = st.checkbox("Entertainment")
   choice_a_c = st.checkbox("Unfamiliar topics")
 
if choice_b:
   st.write("What kinds of tasks do you primarily use AI to assist with")
   choice_b_a = st.checkbox("Writing")
   choice_b_b = st.checkbox("Summarizing")
   choice_b_c = st.checkbox("Making plans")
   choice_b_d = st.checkbox("Translation")


if choice_c:
    answer_purpose = st.text_input("Please specify")
    if answer_purpose:
      response_task_manager = generate_response("task_manager",question_original=question_purpose,answer = answer_purpose,question_generated=None,choices=None)
      st.write("Task manager:")
      st.write(response_task_manager['result'])
      st.write(response_task_manager['reason'])
      if response_task_manager['result']=="yes":
         response_question_designer = generate_response("question_designer",question_original=question_purpose,answer = answer_purpose,question_generated=None,choices=None)
         st.write("Question designer:")
         question_generated = response_question_designer['question']
         choices = response_question_designer['choices']
         st.write(question_generated)
         st.write(choices)
         if question_generated:
           response_reviewer = generate_response("reviewer",question_original=question_purpose,answer = answer_purpose,question_generated=question_generated,choices=choices)
           if response_reviewer['result']=="success":
            st.write("Reviewer:")
            st.write(response_reviewer['question'])
            st.write(response_reviewer['choices'])
           else:
            st.write(response_reviewer['result'])
            st.write(response_reviewer['reason'])



