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


if __name__=='__main__':
    state={
        'input': '',
        'debate_topics': [],
        'count': 0,
        'arguments': [],
        'judgement': ''
    }
    #second_state={'inputt': 'who is better batsman among rohit and virat', 'debate_topics': ['Rohit Sharma: Analyzing his batting technique, consistency, and record in international cricket', 'Virat Kohli: Evaluating his batting style, adaptability, and performance across formats'], 'count': 0, 'arguments': ['Debater_A:<think>\nOkay, the user wants a paragraph that combines my initial points with the research findings and counters the opponent\'s points effectively. Let me start by recalling the three main points I outlined earlier: adaptive technique, consistency in evolving roles, and influence in high-pressure situations. Now, looking at the research snippets, there are mentions of Rohit\'s ODI average and strike rate, his elegant yet precise batting style, the ICC player ratings, and unique achievements like his 264 in an ODI.\n\nThe opponent\'s points focus on stats like averages and strike rates, which I need to handle without using statistics. The user wants to outperform these by emphasizing aspects that can\'t be easily countered. For instance, Rohit\'s technique and adaptability can be highlighted as strengths that stats alone don\'t capture. Also, his unique achievements, like the highest ODI score, showcase his impact beyond averages.\n\nI should structure the paragraph to first address the batting technique, using the research snippet about his combination of elegance and precision. Then move to consistency, weaving in the idea of sustained performance across roles. Finally, highlight his record in high-stakes moments. I need to ensure that the points are interconnected and reinforce each other, making it difficult for opponents to refute by focusing on qualitative aspects rather than quantitative ones. Also, the mention of his 264 runs and ability to adapt in red ball cricket from the research can be used to show his versatility beyond stats.\n\nWait, the user mentioned not to use statistics, but the research includes stats. How to handle that? The example given in the initial plan didn\'t use stats, so perhaps paraphrase the research stats into non-statistical language. For example, instead of saying "average above 48," focus on consistency over time and impact in crucial games. The key is to use the research to support the qualitative points, not the stats. Also, mention his highest score as a testament to his capacity for domination. Make sure the paragraph flows logically, connecting technique to consistency to high-pressure performance, while incorporating the research elements that highlight his unique attributes beyond mere numbers.\n</think>\n\nRohit Sharma’s batting technique is a masterclass in adaptability and precision, blending elegance with calculated efficiency. His relaxed yet controlled stance, combined with micro-adjustments in shot selection and footwork, allows him to thrive across all formats and conditions—whether dismantling spin with placement in Tests or unleashing devastating power in T20I finales. This technical finesse has enabled him to outmaneuver a spectrum of bowlers, neutralizing their tactics while maintaining unflappable composure. Over two decades, his consistency has transcended mere statistics: his ability to evolve from a finisher to a Test captain, and later a white-ball innovator, underscores a career defined by resilience and strategic intelligence. Even amid evolving roles, his knack for delivering in pivotal moments—whether steering India from collapse or accelerating run chases—solidifies his reputation as a match-winning stalwart. Beyond numbers, Rohit’s legacy includes trailblazing feats like scoring the highest individual ODI score (264*) and translating white-ball flair into red-ball success, proving that his impact is as much about leadership and mental fortitude as it is about batting prowess. These qualities create an indomitable narrative, rendering superficial criticisms or isolated statistical comparisons irrelevant in the face of a player who consistently redefines excellence through holistic mastery of the game.', 'Debater_B:<think>\nOkay, let\'s tackle this. The user wants a paragraph that combines the main points about Virat Kohli with the opponent\'s arguments about batting averages and strike rates. The opponent is using stats, but the user isn\'t allowed to use stats directly. Hmm, how to counter that without stats?\n\nFirst, focus on Kohli\'s adaptability and technique. The opponent mentioned his averages and strike rates, but the user\'s points should highlight qualitative strengths. Like his ability to adjust to different formats, which the opponent can\'t easily dispute with numbers alone. Also, Kohli\'s mental resilience and leadership role in the team are key aspects. The opponent might have used logical fallacies like over-reliance on statistics, which can be countered by emphasizing non-quantifiable qualities. \n\nThe research snippets mention Kohli\'s records but we need to paraphrase without using the stats. For example, instead of saying "58.71 average," talk about his consistency and mastery over time. Mention his leadership in guiding the team and how his strategic adaptability in various formats makes him unique. Also, note that he\'s overcome challenges beyond just numbers, like transitioning from a specialist to a finisher in T20s. \n\nNeed to weave in the opponent\'s points as counterarguments. Maybe start by acknowledging the stats they use, then pivot to how Kohli\'s intangible skills make those numbers secondary. Use the logical fallacies point to suggest that relying solely on stats is a fallacy. \n\nStructure the paragraph to first address the opponent\'s statistical focus, then contrast with Kohli\'s adaptability, leadership, and mental resilience. Make sure it flows logically, connecting each strength to counter the opponent\'s points effectively without using specific numbers. Use terms like "technical flexibility," "strategic evolution," and "mental fortitude" to convey the message. Avoid any mention of the actual stats from the snippets but imply his superiority through these qualitative aspects.\n</think>\n\nWhile opponents may fixate on statistical markers like averages and strike rates, Virat Kohli’s dominance in cricket transcends quantitative metrics. His technical flexibility—marked by an elegant yet relentless approach—enables mastery across all formats, where adaptability in shot selection, footwork, and temperament neutralizes opposition strategies. For instance, his transition from a Test-era anchor to a T20 finisher exemplifies a rare strategic evolution, blending calculated aggression with situational awareness. Unlike rigid comparisons to numbers, Kohli’s leadership and mental fortitude, honed through decades of high-pressure encounters, redefine his impact. Even during extended dry spells, his discipline to recalibrate and deliver in critical moments—be it steering Indian innings or dismantling attacks—cements his legacy as a player shaped by resilience, not just data. By highlighting such intangibles—his ability to elevate teammates, innovate in tactical roles, and endure adversity—the debate shifts from transient statistics to enduring qualities that no opponent can quantify or counter.']}
    # organiser=organiser_node(second_state)
    # debate=debate_node(organiser)
    # print(organiser['debate_topics'])
    # print()
    # print(debate)
    # for argument in debate['arguments']:
    #     print(argument)
    #     print("--------------------------------------------------------------")
    # judgement=judge_node(second_state)
    # print(judgement['judgement'])
    judgement=multiAgent_debater.invoke(state)
    print(judgement['judgement'])