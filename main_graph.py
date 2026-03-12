from schemas import organizerState,groq_llm,OrganizerOutput
from prompts import debate_creation_prompt,judgement_prompt
from langgraph.graph import END,StateGraph
from subgraph import debater

def organiser_node(state:organizerState):
    debate_theme=''
    organiser_llm=groq_llm(structured=True,output=OrganizerOutput)
    if not state['arguments']:
        debate_theme=input("Enter your topic: ")
    topics=organiser_llm.invoke(debate_creation_prompt.format(
        topic=debate_theme ,
        original_theme=state['debate_topics'],
        previous_arguments=state['arguments']
    ))
    return{
        **state,'debate_topics':topics.topics,
        'input':state['input'] or debate_theme
    }

def debate_node(state:organizerState):
    arguments=[]
    debater_a_state={
        'topic': state['debate_topics'][0],
        'my_generation': '',
        'tool_query': [],
        'tool_output': [],
        'my_arguments': [],
        'opp_arguments': state['arguments'][-1] if state ['arguments'] else []
    }

    debater_a=debater
    debater_b=debater
    intermediate_state=debater_a.invoke(debater_a_state)
    arguments.append(f"Debater_A:{intermediate_state['my_arguments']}")
    debater_b_state = {
        'topic': state['debate_topics'][1],
        'my_generation': '',
        'tool_query': [],
        'tool_output': [],
        'my_arguments': [],
        'opp_arguments': intermediate_state['my_arguments']
    }
    final_state=debater_b.invoke(debater_b_state)
    arguments.append(f"Debater_B:{final_state['my_arguments']}")

    return{
        **state,'arguments':arguments,
        'count':1
    }
def judge_node(state:organizerState):
    judgement_llm=groq_llm(structured=False)
    judgement=judgement_llm.invoke(judgement_prompt.format(
        theme=state['input'],
        arguments=state['arguments']
    ))
    return{
        **state,'judgement':judgement.content
    }
def condition(state:organizerState):
    if state['count']<=5:
        return 'organiser'
    else:
        return 'judgement'

mainGraph=StateGraph(organizerState)
mainGraph.add_node('organiser',organiser_node)
mainGraph.add_node('debate',debate_node)
mainGraph.add_node('judgement',judge_node)
mainGraph.set_entry_point('organiser')
mainGraph.add_edge('organiser','debate')
mainGraph.add_edge('judgement',END)
mainGraph.add_conditional_edges('debate',condition,{
    'organiser':'organiser',
    'judgement':'judgement',
})

multiAgent_debater=mainGraph.compile()

if __name__ == '__main__':
    # Generate graph visualization
    image_bytes = multiAgent_debater.get_graph(xray=True).draw_mermaid_png()

    with open("debate_graph.png", "wb") as f:
        f.write(image_bytes)

    print("Graph saved as debate_graph.png")