import os
#from langchain_community.llms import HuggingFaceHub
from langchain_huggingface import HuggingFaceEndpoint
from query import sqlite_query
from query_fixer import fix_sql_spacing
from graph import detect_graph_type, graph_generator

#add huggingface acess token 


chat_model = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.3", 
    max_new_tokens = 100,
    top_k=1,
    temperature=2,
    stop_sequences=[";", "[nthg]", ".\n", ". Here's "]
    
    
)
chat_model_sql = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.3", 
    max_new_tokens = 75,
    top_k=1,
    temperature=1,
    stop_sequences=[";", "[nthg]", "**"]
    
    
)

def query_generator(q_text):

    prompt = f"""
You are Titanic-Chat, an expert in understanding user queries and generating valid SQLite queries only when necessary. 
Provide clear, direct responses. Try to quantify your query if needed.

The table 'Observation' of the Titanic Ship Dataset contains the following columns:
- age (REAL): Age of the passenger
- pclass (INT): Passenger's class 
- sibsp (INT): Number of siblings and spouses a passenger had on board
- parch (INT): Number of parents and children aboard
- sex_id (TEXT): Gender (1 = male, 0 = female)
- fare (REAL): Ticket fare
- adult_male (INT): Adult Male (1 = yes, 0 = no)
- alone (INT): Alone (1 = yes, 0 = not alone)
- embarked_id (INT): Port of embarkation (1 = Cherbourg, 2 = Queenstown, 3 = Southampton)
- survived (INTEGER): Survival status (1 = survived, 0 = did not survive)

**Instructions:**
- If the user's question requires data is within the scope of 'Observation' Table, generate a valid SQLite query with proper spacing.
- If the question does not require any data from the 'Observation' or it is a Generic Question for example: "how are you ?" or "what is your name ?", respond with `[nthg]`.
- Do not include explanations or any extra text, just the SQL query or `[nthg]`.

**Question:** {q_text}
"""
    response = chat_model_sql.invoke(prompt)
    response = response.replace("`", "")
    response = response.replace("``", "")
    response = response.replace("\n", "")
    response = response.replace("```", "")
    response = response.replace("sqlSELECT", "SELECT")
    response = response.replace("**Answer:** `", "")
    response = response.replace("**Answer:**", "")
    response = fix_sql_spacing(response)
    print(response, end="\n")

    return response


def agent(text):
    plotted_graph = None
    graph_text = ""
    graph_type = detect_graph_type(text)
    print(graph_type)
    
    ask_sql_query = query_generator(text)                    # SQLite query Generator
    result, sql_query = sqlite_query(ask_sql_query)

    if graph_type != "No graph":
        plotted_graph = graph_generator(graph_type, result)
        if plotted_graph != None:
            print("graph path: ", plotted_graph)
            graph_text= "A relevant graph is generated generated and included with your output based on the provided data, acknowledge its inclusion without explicitly stating its creation process. "
    if result != "[nthg]" or result != [] or result != " " or result != "" or sql_query == "error":
        response = chat_model.invoke(f"You are Titanic-Chat, an AI chatbot. Answer the following question: {text}. {graph_text}Additionally, use insights from the executed SQL query: {sql_query} and the retrieved data: {result}. However, do not mention the SQL query or the retrieval process in your response. Ensure your response is in natural language only and clearly presents the relevant information.")
        print("Data based response passed.")
        return response, plotted_graph
    else:
        
        text_response = """You are Titanic-Chat, an AI chatbot. Use the following data to answer questions concisely and clearly without mentioning the source of the data:

                    Total passengers: 891
                    Total survivors: 342 (38.4%)
                    Total non-survivors: 549 (61.6%)
                    Male passengers: 577, with 109 survivors (18.9%) and 468 non-survivors (81.1%)
                    Female passengers: 314, with 233 survivors (74.2%) and 81 non-survivors (25.8%)
                    First-class passengers: 216, with 136 survivors (62.9%)
                    Second-class passengers: 184, with 87 survivors (47.3%)
                    Third-class passengers: 491, with 119 survivors (24.2%)
                    Embarkation ports: Southampton (644), Cherbourg (168), Queenstown (77)
                    Answer the following question based on this information: {text}"""

        return text_response, plotted_graph