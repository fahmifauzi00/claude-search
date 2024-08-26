import os
import json
import logging
from dotenv import load_dotenv
import boto3
from langchain_aws import ChatBedrock
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain.tools import BaseTool
from typing import Optional, List
from chat_history import chat_history
from tools import search_tool
from datetime import datetime

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bedrock_client = boto3.client(
    service_name="bedrock-runtime",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_DEFAULT_REGION")
)


def get_bedrock_response_with_tools(prompt: str, tools: Optional[List[BaseTool]] = None, memory: Optional[ConversationBufferMemory] = None):
    llm = ChatBedrock(
        model_id="anthropic.claude-3-haiku-20240307-v1:0",
        model_kwargs=dict(temperature=0.3, max_tokens=500),
        region_name=os.getenv("AWS_DEFAULT_REGION"),
        client=bedrock_client,
        credentials_profile_name="default"
    )
    
    if memory is None:
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    
    # Decision-making step
    current_date = datetime.now().strftime("%Y-%m-%d")
    decision_prompt = f"Given the following user input, decide if you need to use external tools to answer accurately with the most up-to-date information. Respond with 'Yes' if there's any chance that current data might improve the answer, or 'No' if you're absolutely certain your knowledge is sufficient and current. Current date: {current_date}. User input: {prompt}"
    decision = llm.invoke(decision_prompt).content.strip().lower()
    
    if decision == 'yes':
        langchain_tools = tools if tools else []

        new_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful assistant. Use the provided tools when necessary to answer questions accurately. Your answers should be concise and to the point. You should respond with 'I don't know' if you are unsure about the answer. ",
                ),
                ("placeholder", "{chat_history}"),
                ("human", "{input}"),
                ("placeholder", "{agent_scratchpad}"),
            ]
        )
        
        agent = create_tool_calling_agent(
            tools=langchain_tools,
            llm=llm,
            prompt=new_prompt,
        )
        
        agent_executor = AgentExecutor(
            agent=agent,
            tools=langchain_tools,
            verbose=True,
            handle_parsing_errors=True,
            memory=memory
        )

        response = agent_executor.invoke({"input": prompt})
        return {"answer": response['output'], "used_tools": True}
    else:
        response = llm.invoke(prompt)
        return {"answer": response.content, "used_tools": False}

def chat_with_search(user_input: str, memory: ConversationBufferMemory):
    user_input = f"User input: {user_input}"
    
    tools = [search_tool]
    
    logger.info(f"Sending request to agent")
    response = get_bedrock_response_with_tools(user_input, tools, memory)
    logger.info(f"Agent response: {response}")
    
    if response["used_tools"]:
        logger.info("Tools were used in generating the response")
    else:
        logger.info("Simple LLM response was generated without using tools")
    
    return response["answer"]