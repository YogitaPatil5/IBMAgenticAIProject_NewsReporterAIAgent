from crewai import Task
from agents import reporter1, reporter2, analyst

report_task1 = Task(
    description="""Use the news_fetcher tool to get political news from India. 
    Call the tool with query 'India politics' to fetch relevant headlines.""",
    expected_output="""A formatted list of exactly 3 political news headlines from India, 
    each including the headline title and source. If no news is found, report the exact 
    error message returned by the tool.""",
    agent=reporter1
)

report_task2 = Task(
    description="""Search for and retrieve the top 3 most recent and significant technology 
    news headlines from around the world. Focus on innovations, startup news, tech industry 
    developments, and breakthrough technologies. Use the search query 'technology' to fetch 
    relevant global tech news.""",
    expected_output="""A formatted list of exactly 3 technology news headlines from around 
    the world, each including the headline title and source. Present them as:
    1. [Headline] - [Source]
    2. [Headline] - [Source]
    3. [Headline] - [Source]""",
    agent=reporter2
)

summary_task = Task(
    description="""Analyze and summarize all the news headlines collected by both reporters. 
    Create a comprehensive summary that organizes the information clearly and highlights the 
    key points from both political and technology news sectors.""",
    expected_output="""A well-organized summary containing:
    
    ## Political News Summary (India)
    - Brief bullet points summarizing the 3 political headlines
    
    ## Technology News Summary (Global)  
    - Brief bullet points summarizing the 3 technology headlines
    
    ## Key Insights
    - 2-3 key insights or trends identified from the collected news""",
    agent=analyst,
    context=[report_task1, report_task2]  # This ensures the analyst gets outputs from both reporters
)