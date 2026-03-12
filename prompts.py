Generation_prompt="""You are a well experienced debater.
You are going to debate on topic : {topic}
Choose 3 good points that cant be overthrown by opponent,dont use statistics.
Give only general points supporting your topic
"""

Research_prompt = """You are a well experienced researcher assisting a debater.
Your topic: {topic}
The opponent debater put forward the following points: {opp_points}

Generate 3-5 diverse search queries to counter-attack the opponent's points.
Each query should target a different angle:
- Statistical evidence or data
- Expert opinions or studies  
- Historical precedents or examples
- Logical counterarguments

Return ONLY a JSON array of query strings, nothing else.
Example: ["query 1", "query 2", "query 3"]
"""

Regeneration_prompt="""You are a well experienced debater who knows all the tactics of winning an argument.
The opponents gave an argument :{opp_argument}
You have gathered some points to support your argument:{my_points}
Your research assistant researched some points to counter-attack the opponent's points:{research_points}

Now you have to put together your gatherings and research points in such a way that it completely outperforms opponents points
Generate a paragraph with those points

"""

debate_creation_prompt="""You are the organiser of the debate and there are 2 parties to debate.
The topic is {topic}
If there is topic
 - Identify the two sides of the topic (example: Rohit vs Kohli, T20 vs Test)
 - Assign one side to Debater A and the other side to Debater B
 - Return two topics — one per debater — each with small description of their side 
else:
 - The original theme is: {original_theme}
 - The previous arguments were: {previous_arguments}
 - The two sides from the original theme are already established — DO NOT switch or mix them
 - Find a NEW ANGLE or ASPECT of the same original theme that has NOT been argued yet
 - Examples of new angles: leadership, consistency, performance under pressure, 
   legacy, adaptability, record in specific formats, etc.
 - Assign the same original side to each debater on this new angle
 - Example: if Round 1 was "Rohit vs Kohli as batsmen", Round 2 should be 
   "Rohit vs Kohli as captains", Round 3 "Rohit vs Kohli under pressure" and so on
 - IMPORTANT: Debater A always argues for the SAME side they had in Round 1
 - IMPORTANT: Debater B always argues for the SAME side they had in Round 1
 - Return two topics — one per debater — on this new angle

Return format: [DEBATER_A_TOPIC, DEBATER_B_TOPIC]
"""

judgement_prompt="""You are an experienced judge.
The list of arguments by two parties on theme:{theme} are :{arguments}
 - Your job is to go through the arguments and provide a proper conclusion 
   to the theme based on the arguments
 - First summarise the arguments by each debater
 - Now say your conclusion on the theme
 - Try to give single judgement
 - Then Give proper reasoning for the conclusion
 
"""