import os
import requests
from crewai_tools import tool
from dotenv import load_dotenv

load_dotenv()

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")

@tool("News Fetcher Tool")
def news_fetcher(query: str) -> str:
    """Fetch latest headlines using NewsAPI based on the query."""
    # Use the same logic as the direct function
    return fetch_news_direct(query)

# Create a separate function for direct testing
def fetch_news_direct(query: str) -> str:
    """Direct news fetcher function for testing (not wrapped as a tool)"""
    print(f"DEBUG: Starting news fetch for query: '{query}'")
    
    if not NEWSAPI_KEY:
        error_msg = "Error: NewsAPI key not found. Please set NEWSAPI_KEY in your .env file."
        print(f"DEBUG: {error_msg}")
        return error_msg
    
    print(f"DEBUG: Using API key: {NEWSAPI_KEY[:8]}...")
    
    # Enhanced parameters for better results
    url = "https://newsapi.org/v2/everything"  # Changed from top-headlines to everything for more results
    
    # Adjust query based on content
    if "politics" in query.lower() or "india" in query.lower():
        # Try different approaches for political news
        search_queries = [
            "India government OR Indian politics OR Modi OR BJP OR Congress OR election",
            "Indian parliament OR Delhi OR BJP OR Congress OR political",
            "India"
        ]
        for search_query in search_queries:
            print(f"DEBUG: Trying political query: {search_query}")
            params = {
                "q": search_query,
                "apiKey": NEWSAPI_KEY,
                "language": "en",
                "pageSize": 10,
                "sortBy": "publishedAt",
                "domains": "timesofindia.com,ndtv.com,hindustantimes.com,indianexpress.com"
            }
            
            try:
                response = requests.get(url, params=params, timeout=30)
                if response.status_code == 200:
                    data = response.json()
                    articles = data.get("articles", [])
                    # Filter for political content
                    political_articles = []
                    for article in articles:
                        title = article.get("title", "").lower()
                        description = article.get("description", "").lower() if article.get("description") else ""
                        if any(keyword in title + description for keyword in 
                               ["government", "politics", "political", "minister", "bjp", "congress", 
                                "election", "parliament", "modi", "policy", "cabinet"]):
                            political_articles.append(article)
                    
                    if len(political_articles) >= 3:
                        articles = political_articles
                        break
            except:
                continue
    else:
        # Tech news queries
        search_queries = [
            "artificial intelligence OR machine learning OR startup funding OR tech innovation",
            "technology breakthrough OR AI OR software OR tech company",
            "technology"
        ]
        for search_query in search_queries:
            print(f"DEBUG: Trying tech query: {search_query}")
            params = {
                "q": search_query,
                "apiKey": NEWSAPI_KEY,
                "language": "en",
                "pageSize": 10,
                "sortBy": "publishedAt",
                "domains": "techcrunch.com,theverge.com,wired.com,arstechnica.com,engadget.com"
            }
            
            try:
                response = requests.get(url, params=params, timeout=30)
                if response.status_code == 200:
                    data = response.json()
                    articles = data.get("articles", [])
                    # Filter for actual tech content (not financial)
                    tech_articles = []
                    for article in articles:
                        title = article.get("title", "").lower()
                        description = article.get("description", "").lower() if article.get("description") else ""
                        # Exclude financial/stock articles
                        if not any(keyword in title + description for keyword in 
                                  ["stock", "nasdaq", "nyse", "dividend", "earnings", "vs", "comparison"]):
                            if any(keyword in title + description for keyword in 
                                  ["technology", "tech", "ai", "software", "app", "innovation", "startup"]):
                                tech_articles.append(article)
                    
                    if len(tech_articles) >= 3:
                        articles = tech_articles
                        break
            except:
                continue
    
    print(f"DEBUG: Request URL: {url}")
    print(f"DEBUG: Request params: {params}")
    
    try:
        response = requests.get(url, params=params, timeout=30)
        print(f"DEBUG: Response status code: {response.status_code}")
        
        response.raise_for_status()  # Raises an HTTPError for bad responses
        
        data = response.json()
        print(f"DEBUG: Response data keys: {data.keys()}")
        
        if 'status' in data:
            print(f"DEBUG: API status: {data['status']}")
        
        if 'totalResults' in data:
            print(f"DEBUG: Total results available: {data['totalResults']}")
        
        print(f"DEBUG: Number of articles retrieved: {len(articles)}")
        
        if not articles:
            return f"No relevant news found for query: {query}."
        
        headlines = []
        for i, article in enumerate(articles[:3], 1):  # Limit to top 3
            title = article.get("title", "No title")
            source = article.get("source", {}).get("name", "Unknown source")
            published_at = article.get("publishedAt", "")[:10]  # Get date part
            
            # Clean up title (remove source name if it appears at the end)
            if source in title:
                title = title.replace(f" - {source}", "").strip()
            
            headline = f"{i}. {title} - {source} ({published_at})"
            headlines.append(headline)
            print(f"DEBUG: Added headline: {headline}")
        
        result = "\n".join(headlines)
        print(f"DEBUG: Final result length: {len(result)} characters")
        return result
        
    except requests.exceptions.Timeout:
        error_msg = "Error: Request timeout. Please check your internet connection."
        print(f"DEBUG: {error_msg}")
        return error_msg
    except requests.exceptions.HTTPError as e:
        error_msg = f"Error: HTTP {response.status_code} - {response.text}"
        print(f"DEBUG: {error_msg}")
        return error_msg
    except requests.exceptions.RequestException as e:
        error_msg = f"Error: Network error - {str(e)}"
        print(f"DEBUG: {error_msg}")
        return error_msg
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        print(f"DEBUG: {error_msg}")
        return error_msg

# Test function you can run separately
def test_news_fetcher():
    """Test function to debug the news fetcher"""
    print("Testing news fetcher...")
    print("="*50)
    
    # Test political news
    print("Testing political news:")
    politics_result = fetch_news_direct("India politics")
    print(f"Result: {politics_result}")
    print("\n" + "="*50)
    
    # Test tech news
    print("Testing tech news:")
    tech_result = fetch_news_direct("technology")
    print(f"Result: {tech_result}")
    print("="*50)

if __name__ == "__main__":
    test_news_fetcher()