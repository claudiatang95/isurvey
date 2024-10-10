from openai import AzureOpenAI
import json

endpoint_url = 'xxx'
api_key = "xxx"
deployment_name='xxx' 

client = AzureOpenAI(
    api_key=api_key,  
    api_version="2024-06-01",
    azure_endpoint = endpoint_url
    )

def task_manager():
    prompt = f''' 
             You are a survey designer. Complete the following task step by step. 
             Step 1: Assess whether the user answer for question is relevant. If no, output result and reason in json format {{"result":"no","reason":"does not make sense"}}.If yes, go to step 2.
             Step 2: Assess whether the user answer is broad enough to warrant a follow-up question. If the answer is already detailed enough, You should output {{"result":"no","reason","detailed enough"}}. 
             If the answer is general, You should output{{"result":"yes","reason","follow-up question needed"}}
             For example: ##What are the purposes of using generative AI in your daily life?## User answer is ##Chat with personal stuff## or "stock market trends analysis##, such answer is detailed enough and no follow-up question is needed. 
             If user answers ##decision making## or ##give investment advice## or ##play games##, such answer is general and follow-up question is needed. 
             '''
    return prompt

def task_manager_user(question,answer):
    prompt = f'''The question is ##{question}##, the user answer is ##{answer}##.'''
    return prompt


def question_designer():
    prompt = '''
             You are a survey designer. Generate follow-up questions to gather more detailed information based on user answer.
             For example: question What are the purposes of using computer in your daily life? Choices: A. Search information, B: Entertainment C. Other.
             The follow-up for question for choice A and B are “What kinds of information do you use your computer to search for?” and “What types of entertainment do you enjoy on your computer?”. 
             Your job is to generate follow-up question based on respondent's specification when respondent chooses "other" option. 
             For example: 
             When a respondent chooses "Other” and specifies "work", you should ask a follow-up question like, “What types of work tasks do you use the computer for?”
             For the follow-up question, provide three common choices and one “Other” option. Ensure that each choice is mutually exclusive and broad, avoiding specific examples.  
             You can formulate question from different angles, such as types of tasks, information, impact, in what context or aspects, and so on. 
             If you think the specification is detailed enough, leave the question and choices empty.
             output in json format 
             {"question":generated question, 
             "choices":["A.choice","B.Choice","C.Choice","D.Other"]}
             '''
    return prompt

def question_designer_user(question,anwswer):
    prompt = f'''
             Generate follow-up question for question ##{question}## when user answers ##{anwswer}##
             '''
    return prompt



def reviewer():
    prompt = f''' 
You are a survey reviewer. Review the question and answer choices step by step.
Step 1: Does the question repeat or overlap with other questions listed below enclosed by ***? 
***Which generative AI tool do you use most frequently A. ChatGPT B. Copilot C Other***
•If it repeats or overlaps, stop and output the result and reason in JSON format: {{"result":"stop_step1","reason":"overlapss}}
•If it does not repeat or overlap, proceed to Step 2.

Step 2: Review the survey question and answer choices. Based on survey design principles, improve the wording for clarity, neutrality, and simplicity. Ensure that the question is not leading, double-barreled, or biased.
•Output the improved question and choices in JSON format:{{"result":"success","question":"improved survey question","choices":"improved survey choices"}}
             '''
    return prompt

def reviewer_user(question,choices):
    prompt = f'''
             Review this question and choices:
             ##{question}##,
             ##{choices}##
             '''
    return prompt


def generate_prompt(agent,question_original,answer,question_generated,choices):
    if agent=="task_manager":
        system_prompt = task_manager()
        user_prompt = task_manager_user(question_original,answer)
    if agent=="question_designer":
        system_prompt = question_designer()
        user_prompt = question_designer_user(question_original,answer)
    if agent=="reviewer":
        system_prompt = reviewer()
        user_prompt = reviewer_user(question_generated,choices)
    return system_prompt,user_prompt

def generate_response(agent,question_original,answer,question_generated,choices):
    system,user=generate_prompt(agent,question_original,answer,question_generated,choices)
    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ],
        temperature=0,
        response_format={"type": "json_object"}
    )
    result = json.loads(response.model_dump_json())
    json_str = result['choices'][0]['message']['content']
    json_obj = json.loads(json_str)
    return json_obj

