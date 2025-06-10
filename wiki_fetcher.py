# utils/wiki_fetcher.py
import wikipedia

def fetch_wikipedia_summary(topic: str, sentences: int = 5) -> str:
    """
    Fetch a short summary from Wikipedia based on a topic.
    """
    try:
        summary = wikipedia.summary(topic, sentences=sentences)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Topic is ambiguous. Options: {e.options[:5]}"
    except wikipedia.exceptions.PageError:
        return "Page not found."
    except Exception as e:
        return f"An error occurred: {e}"
