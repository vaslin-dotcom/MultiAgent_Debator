from typing import TypedDict, List,Annotated
from operator import add
from langgraph.graph import add_messages
import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_community.tools import DuckDuckGoSearchResults
from pydantic import BaseModel,Field

search_tool = DuckDuckGoSearchResults(num_results=1)
tool=[search_tool]
load_dotenv()

think_model="qwen/qwen3-32b"
systematic_model="openai/gpt-oss-20b"

class ResearchOutput(BaseModel):
    model_config = {"arbitrary_types_allowed": True}
    queries:List[str]=Field(description="List of Queries")
class OrganizerOutput(BaseModel):
    model_config = {"arbitrary_types_allowed": True}
    topics:List[str]=Field(description="List of Topics")

def groq_llm(tool=None, structured=True,output=None):
    key = os.getenv("GROQ_API_KEY")
    url = "https://api.groq.com/openai/v1"

    if structured:
        llm = ChatOpenAI(model=systematic_model, temperature=0.1, api_key=key, base_url=url)
        if tool:
            llm = llm.bind_tools(tools=tool)  # ✅ bind first
        return llm.with_structured_output(output)  # ✅ then structure
    else:
        llm = ChatOpenAI(model=think_model, api_key=key, base_url=url)
        if tool:
            return llm.bind_tools(tools=tool)
        return llm
class debaterState(TypedDict):
    topic: str
    my_generation: str
    tool_query: List[str]
    tool_output: List[str]
    my_arguments: List[str]
    opp_arguments: List[str]


class organizerState(TypedDict):
    input: str
    debate_topics:List[str]
    count: Annotated[int,add]
    arguments: Annotated[List[str],add_messages]
    judgement:str
