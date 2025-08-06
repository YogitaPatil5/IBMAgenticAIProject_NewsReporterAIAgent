#!/usr/bin/env python3
"""
Debug script to test your NewsAPI setup and CrewAI configuration
"""
import os
import requests
from dotenv import load_dotenv

def test_environment():
    """Test environment variables"""
    print("🔍 Testing Environment Setup")
    print("=" * 50)
    
    load_dotenv()
    
    newsapi_key = os.getenv("NEWSAPI_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    
    if newsapi_key:
        print(f"✅ NewsAPI Key found: {newsapi_key[:8]}...{newsapi_key[-4:]}")
    else:
        print("❌ NewsAPI Key not found")
        return False
    
    if openai_key:
        print(f"✅ OpenAI Key found: {openai_key[:8]}...{openai_key[-4:]}")
    else:
        print("❌ OpenAI Key not found")
        return False
    
    return True

def test_newsapi_directly():
    """Test NewsAPI directly"""
    print("\n🔍 Testing NewsAPI Direct Connection")
    print("=" * 50)
    
    load_dotenv()
    api_key = os.getenv("NEWSAPI_KEY")
    
    if not api_key:
        print("❌ No API key to test with")
        return False
    
    # Test 1: Simple everything search
    print("Test 1: Simple search for 'India'")
    try:
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": "India",
            "apiKey": api_key,
            "language": "en",
            "pageSize": 3
        }
        
        response = requests.get(url, params=params, timeout=30)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 401:
            print("❌ Invalid API Key")
            return False
        elif response.status_code == 429:
            print("❌ Rate limit exceeded")
            return False
        
        data = response.json()
        total_results = data.get('totalResults', 0)
        articles = data.get('articles', [])
        
        print(f"Total Results: {total_results}")
        print(f"Articles Retrieved: {len(articles)}")
        
        if articles:
            print("✅ Sample headlines:")
            for i, article in enumerate(articles[:2], 1):
                title = article.get('title', 'No title')
                source = article.get('source', {}).get('name', 'Unknown')
                print(f"  {i}. {title} - {source}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Test 2: Top headlines from India
    print("\nTest 2: Top headlines from India")
    try:
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            "country": "in",
            "apiKey": api_key,
            "pageSize": 3
        }
        
        response = requests.get(url, params=params, timeout=30)
        data = response.json()
        articles = data.get('articles', [])
        
        print(f"Top headlines from India: {len(articles)} articles")
        if articles:
            print("✅ Sample headlines:")
            for i, article in enumerate(articles[:2], 1):
                title = article.get('title', 'No title')
                source = article.get('source', {}).get('name', 'Unknown')
                print(f"  {i}. {title} - {source}")
    
    except Exception as e:
        print(f"❌ Error testing top headlines: {e}")
    
    return True

def test_crewai_imports():
    """Test CrewAI imports"""
    print("\n🔍 Testing CrewAI Imports")
    print("=" * 50)
    
    try:
        from crewai import Agent, Task, Crew
        print("✅ CrewAI core imports successful")
    except ImportError as e:
        print(f"❌ CrewAI import error: {e}")
        return False
    
    try:
        from crewai_tools import tool
        print("✅ CrewAI tools import successful")
    except ImportError as e:
        print(f"❌ CrewAI tools import error: {e}")
        return False
    
    return True

def test_openai_connection():
    """Test OpenAI connection"""
    print("\n🔍 Testing OpenAI Connection")
    print("=" * 50)
    
    load_dotenv()
    openai_key = os.getenv("OPENAI_API_KEY")
    
    if not openai_key:
        print("❌ No OpenAI API key to test")
        return False
    
    try:
        import openai
        
        # Set the API key
        openai.api_key = openai_key
        
        # Test with a simple completion (using older API for compatibility)
        try:
            response = requests.get(
                "https://api.openai.com/v1/models",
                headers={"Authorization": f"Bearer {openai_key}"},
                timeout=10
            )
            
            if response.status_code == 200:
                print("✅ OpenAI API connection successful")
                models = response.json()
                print(f"Available models: {len(models.get('data', []))}")
                return True
            else:
                print(f"❌ OpenAI API error: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ OpenAI API test failed: {e}")
            return False
            
    except ImportError:
        print("❌ OpenAI package not installed")
        return False

def main():
    """Run all tests"""
    print("🚀 CrewAI News Reporter - Debug Mode")
    print("=" * 50)
    
    all_passed = True
    
    # Test 1: Environment
    if not test_environment():
        all_passed = False
    
    # Test 2: NewsAPI
    if not test_newsapi_directly():
        all_passed = False
    
    # Test 3: CrewAI imports
    if not test_crewai_imports():
        all_passed = False
    
    # Test 4: OpenAI connection
    if not test_openai_connection():
        all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All tests passed! Your setup should work.")
        print("\n📝 Next steps:")
        print("1. Run: python tools.py (to test news fetching)")
        print("2. Run: streamlit run app.py (to start the web app)")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        print("\n🔧 Common solutions:")
        print("- Check your .env file has the correct API keys")
        print("- Verify your NewsAPI key is valid at https://newsapi.org/")
        print("- Make sure you have internet connection")
        print("- Try: pip install --upgrade crewai crewai-tools openai")

if __name__ == "__main__":
    main()