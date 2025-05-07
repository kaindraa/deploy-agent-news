"""Build LangChain chains from prompt templates for the Researcher Agent."""
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_deepseek import ChatDeepSeek

from prompts.planner_prompt import planner_prompt_template
from prompts.tavily_prompt import tavily_planner_prompt_template
from prompts.grader_prompt import grader_prompt_template
from prompts.writer_prompt import writer_prompt_template
import streamlit as st

llm = ChatDeepSeek(model_name="deepseek-chat", temperature=0.4,  api_key=st.secrets["DEEPSEEK_API_KEY"])
llm_reasonser = ChatDeepSeek(model_name="deepseek-reason", temperature=1,  api_key=st.secrets["DEEPSEEK_API_KEY"])
planner_chain = (
    PromptTemplate(
        input_variables=["topic"],
        template=planner_prompt_template,
    )
    | llm
    | StrOutputParser()
)

tavily_planner_chain = (
    PromptTemplate(
        input_variables=[
            "topic",
            "outline",
            "context",
            "iteration_count",
            "searched_query",
        ],
        template=tavily_planner_prompt_template,
    )
    | llm
    | StrOutputParser()
)

grader_chain = (
    PromptTemplate(
        input_variables=["topic", "outline", "context"],
        template=grader_prompt_template,
    )
    | llm
    | StrOutputParser()
)

writer_chain = (
    PromptTemplate(
        input_variables=["topic", "outline", "context"],
        template=writer_prompt_template,
    )
    | llm
    | StrOutputParser()
)
