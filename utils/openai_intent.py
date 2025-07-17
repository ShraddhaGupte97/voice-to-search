import openai, json, os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_structured_intent(user_query):
    """
    Extracts structured intent from a user query using OpenAI's GPT-3.5-turbo model.
    Args:
        user_query (str): The user's natural language query.
    Returns:
        dict: A dictionary containing the structured intent.
    """
    prompt = f"""
      You are a movie and TV show assistant.

      A user may describe what they want to watch in natural language.
      Your task is to extract their **intent** and output it in a structured JSON format with the following fields:

      Required fields:
      - genre (e.g., comedy, drama, horror, sci-fi, documentaries)
      - mood (e.g., lighthearted, dark, emotional, intense)
      - setting (e.g., high school, space, Seattle, hospital)
      - duration (e.g., short, long, under 1 hour, one season, multi-season)
      - duration_minutes (e.g., < 60, > 120)
      - type (either movie or tv show)
      - actors (list of names, if mentioned)
      - theme (e.g., family, rivalry, justice)

      Optional filters:
      - director
      - title
      - cast
      - country
      - rating (e.g., PG 13, NR)
      - release_year

      If something is implied, infer it. If it's not mentioned, leave it empty or as an empty list.
      Carefully distinguish between realistic and fictional content. If the user mentions psychology, real cases, true events, or motivations behind actions (e.g., "murderers", "why people kill", "true crime", "real events", "biopics", "psychological analysis"), prioritize genres like documentary, true crime, biography, or drama, and include relevant themes such as psychology, real story, or criminal behavior. Do not confuse these with fictional thrillers, horror, or purely entertainment-focused dramas.
      If the user's query implies a genre or category (e.g., feel-good implies comedy, dark implies thriller, murder implies crime, lawyers or courtroom does not imply drama), include that in the genre field.
      
      If duration is mentioned (e.g., 'under 1 hour', 'less than 90 minutes', 'around 2 hours'), return it in a structured duration_minutes field with an appropriate numeric or conditional expression. Use <, <=, >, or between where applicable. Only include `duration_minutes` if the user explicitly refers to numeric duration (e.g., "under 1 hour", "90 minutes", "around 2 hours"). Use `duration_minutes` for numeric conditions and `duration` for qualitative terms like "short", "long", "binge", etc.

      Examples:

      User: "I'm bored, do you have something funny and short?"
      Output:
      {{
        "genre": ["comedy"],
        "mood": ["lighthearted"],
        "setting": [],
        "duration": "short",
        "duration_minutes": "",
        "type": ["movie"],
        "actors": [],
        "theme": [],
        "director": [],
        "title": [],
        "cast": [],
        "country": [],
        "rating": "",
        "release_year": ""
      }}

      User: "Anything with doctors set in Seattle?"
      Output:
      {{
        "genre": ["drama"],
        "mood": [],
        "setting": ["Seattle", "hospital", "doctors"],
        "duration": "",
        "duration_minutes": "",
        "type": [],
        "actors": [],
        "theme": ["medical"],
        "director": [],
        "title": [],
        "cast": [],
        "country": [],
        "rating": "",
        "release_year": ""
      }}

      Now extract from this query: "{user_query}"
      Return only the JSON object.
      """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0125",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        print("Intent extraction failed:", e)
        return None