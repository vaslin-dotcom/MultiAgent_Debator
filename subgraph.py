from langgraph.graph import StateGraph, END
from schemas import debaterState,groq_llm,tool,search_tool,ResearchOutput
from prompts import Generation_prompt,Regeneration_prompt,Research_prompt

def generator_node(state: debaterState):
    llm=groq_llm(structured=False)
    response=llm.invoke(Generation_prompt.format(
        topic=state['topic']
    ))
    research_llm=groq_llm(structured=True,output=ResearchOutput)
    research_result=research_llm.invoke(Research_prompt.format(
        topic=state['topic'],
        opp_points=state['opp_arguments']
    ))
    # print("--------------research queries---------------")
    # print(research_result.queries)
    return{
        **state,'my_generation':response.content,
        'tool_query':research_result.queries
    }

def research_node(state: debaterState):
    queries=state['tool_query']
    output=[]
    for query in queries:
        output.append(search_tool.invoke(query))
    return{
    **state,'tool_output':output
    }

def regeneration_node(state: debaterState):
    research_output=state['tool_output']
    regeneration_llm=groq_llm(structured=False)
    regeneration_result=regeneration_llm.invoke(Regeneration_prompt.format(
        opp_argument=state['opp_arguments'],
        my_points=state['my_generation'],
        topic=state['topic'],
        research_points=research_output
    ))
    return{
        **state,'my_arguments':[regeneration_result.content],
        'tool_query':[],
        'tool_output':[],
        'my_generation':''
    }

subGraph=StateGraph(debaterState)
subGraph.add_node('generator',generator_node)
subGraph.add_node('researcher',research_node)
subGraph.add_node('regenerator',regeneration_node)
subGraph.add_edge('generator','researcher')
subGraph.add_edge('researcher','regenerator')
subGraph.set_entry_point('generator')
subGraph.add_edge('regenerator',END)

debater=subGraph.compile()

if __name__=='__main__':
    state={
        'topic': 'Hitman Rohit sharma',
        'my_generation': '',
        'tool_query': [],
        'tool_output': [],
        'my_arguments': [],
        'opp_arguments': []
    }
    # generation=generator_node(state)
    # research=research_node(generation)
    # regeneration=regeneration_node(research)
    # print('-------------Generation result---------------')
    # print(generation)
    # print('-------------Research result------------------')
    # print(research)
    # print('-------------Regeneration result---------------')
    # print(regeneration)
    # print('-------------Overal arguments---------------')
    # print(regeneration['my_arguments'])

    app=subGraph.compile()
    result=app.invoke(state)
    print(result['my_arguments'])