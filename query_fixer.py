import re

def fix_sql_spacing(query):
    # Add a space after commas if missing
    #query = query.replace("ObservationGROUP", "Observation GROUP")
    query = re.sub(r',(\S)', r', \1', query)
    query = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', query)
    query = re.sub(r'(\d)([a-zA-Z])', ' ', query)
    
    # Remove space inside SQL functions like COUNT (*)
    query = re.sub(r'(\b[A-Z]+\b) \(', r'\1(', query)
    
    # Add spaces around SQL keywords
    keywords = ['SELECT', 'FROM', 'WHERE', 'GROUP BY', 'ORDER BY', 'HAVING', 'JOIN', 'ON', 'AS', 'AND', 'OR', 'NOT', 'SUM', 'COUNT']
    for keyword in keywords:
        query = re.sub(r'(?i)(\b' + keyword + r'\b)(\S)', r'\1 \2', query)  # Space after keyword
        query = re.sub(r'(\S)(\b' + keyword + r'\b)', r'\1 \2', query)  # Space before keyword
    
    # Fix missing space between functions and FROM, GROUP BY, etc.
    query = re.sub(r'(\))(\bFROM\b|\bGROUP BY\b|\bORDER BY\b)', r'\1 \2', query, flags=re.IGNORECASE)
    
    # Remove extra spaces
    query = re.sub(r'\s+', ' ', query).strip()
    
    return query

#print(fix_sql_spacing("SELECT survived AS survived, COUNT (*) AS countFROM ObservationGROUP BY survived"))