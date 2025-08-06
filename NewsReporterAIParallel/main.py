import os
from dotenv import load_dotenv
from agents import reporter1, reporter2, analyst
from tasks import report_task1, report_task2, summary_task
from crewai import Crew

# Load environment variables
load_dotenv()

def main():
    # Check if required environment variables are set
    if not os.getenv("NEWSAPI_KEY"):
        print("Error: NEWSAPI_KEY not found in environment variables.")
        print("Please create a .env file and add your NewsAPI key:")
        print("NEWSAPI_KEY=your_api_key_here")
        return
    
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not found in environment variables.")
        print("Please add your OpenAI API key to the .env file:")
        print("OPENAI_API_KEY=your_openai_api_key_here")
        return
    
    print("Starting News Reporter AI Agent...")
    print("=" * 50)
    
    try:
        # Create the crew
        crew = Crew(
            agents=[reporter1, reporter2, analyst],
            tasks=[report_task1, report_task2, summary_task],
            verbose=True,  # Logs agent reasoning and tool usage
            process="sequential"  # Tasks execute in order
        )
        
        # Execute the crew
        result = crew.kickoff()
        
        print("\n" + "=" * 50)
        print("NEWS SUMMARY COMPLETED")
        print("=" * 50)
        print(result)
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Please check your API keys and internet connection.")

if __name__ == "__main__":
    main()