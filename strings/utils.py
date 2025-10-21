def parse_natural_language_query(query: str) -> dict:
    query = query.lower().strip()
    parsed_filters = {}

    if "single word" in query or "one word" in query:
        if 'word_count' in parsed_filters and parsed_filters['word_count'] != '1':
             raise ValueError("Conflicting word count filters: 'single word' conflicts with another count.")
        parsed_filters['word_count'] = '1'
        
    word_to_num = {"two": 2, "three": 3, "four": 4, "five": 5} 
    for word, num in word_to_num.items():
        if f"{word} word" in query or f"{word} words" in query:
            if 'word_count' in parsed_filters and parsed_filters['word_count'] != str(num):
                raise ValueError(f"Conflicting word count filters: '{word}' conflicts with another count.")
            
            parsed_filters['word_count'] = str(num)
            
    if not parsed_filters:
        raise ValueError("Unable to parse a valid filter from the query.")

    return parsed_filters