# Canvas LMS AI student progress tracker
This project aims to demostrate the use of an AI Agent created using LangChain to assist in:- 
- Providing comprehesive student progress reports
- Identify and provide early intervesions to struggling students
- Construct personalized follow up email to any students based on the perfomance data

## How it works
The student tracker is an AI agent that acts as a instructor assistant by providing course analysis.
It analyzes Canvas LMS Data provided in [this file](agent_prompt.txt) or fetches the data from the API if the file does not exist. The process of fetching from API takes time before it start eccepting prompts.
Once it analyzes the data, it will start accepting prompts like:-
* Analyze a specific Student10 performance
* Identify students who are struggling
* Provide suggestions for improvement
* Construct a personalized email to a struggling student

## Prerequisites
- Python 3.12
- Access to Canvas LMS token

## Configurations
Add .env file with the following configurations
```
GROQ_API_KEY=<paste your GROQ API KEY here>
CANVAS_API_BASEURL=<Specify your Canvas LMS instance>
CANVAS_LMS_API_TOKEN=<Generate API token and paste it here>
LLM_MODEL=llama-3.3-70b-versatile
```

## Setup
1. Clone the repository
2. Setup a virtual environment and activate ```python -m venv .venv && source .venv/bin/activate```
3. Install dependancies ```pip install -r requirements.txt```
4. Start the agent ```python -m agent```

## Future development
- Create a web frontend dashboard
- Add more LangChain tools:-
    - sending emails
    - scheduling calendar sessions 
    - search and recommend additional resources






