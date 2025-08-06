# 🤖 AI News Reporter (CrewAI + Streamlit)

A sophisticated AI-powered news aggregation system that uses CrewAI agents to fetch political and technology news in parallel, then provides intelligent analysis through a beautiful Streamlit web interface.

## 🌟 Features

- **Multi-Agent System**: Specialized AI agents for different news categories
- **Parallel Processing**: Politics and tech news fetched simultaneously
- **Intelligent Analysis**: AI-powered summarization and insight extraction
- **Interactive Web UI**: Beautiful Streamlit interface with real-time progress
- **Export Capabilities**: Download reports for offline viewing
- **Configuration Panel**: Easy-to-use settings and API key management

## 🏗️ Architecture

### Agents
- **🏛️ Politics News Reporter**: Specializes in Indian political developments
- **💻 Technology News Reporter**: Covers global tech innovations and startups  
- **📊 News Summary Analyst**: Creates comprehensive analysis and key insights

### Workflow
1. Both reporters work in parallel to fetch news from their domains
2. Summary analyst processes all collected news
3. Results are presented in a structured, easy-to-read format

## 📦 Installation

### Prerequisites
- Python 3.8+
- NewsAPI account ([Get free key](https://newsapi.org/))
- OpenAI account ([Get API key](https://platform.openai.com/))

### Setup Steps

1. **Clone the repository**:
   ```bash
   git clone <your-repo>
   cd ai-news-reporter
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env and add your API keys
   NEWSAPI_KEY=your_newsapi_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. **Create Streamlit config** (optional):
   ```bash
   mkdir -p .streamlit
   ```

## 🚀 Usage

### Method 1: Using the Launch Script (Recommended)
```bash
python run_app.py
```

### Method 2: Direct Streamlit Launch
```bash
streamlit run app.py
```

### Method 3: Command Line (Original)
```bash
python main.py
```

## 🖥️ Web Interface Guide

### Main Features

1. **Control Panel**:
   - Start news fetching with one click
   - Real-time progress monitoring
   - Status updates for each agent

2. **Configuration Sidebar**:
   - API key status checking
   - News category selection
   - Advanced settings (verbose mode, headline count)

3. **Agent Status Panel**:
   - Live agent status monitoring
   - Visual indicators for each agent's progress

4. **Results Display**:
   - Organized news summaries
   - Key insights and trends
   - Export functionality

### Screenshots & Demo

The interface includes:
- 🎨 Modern, responsive design
- 📊 Real-time progress bars
- 🔍 Detailed agent status
- 📱 Mobile-friendly layout

## 🔧 Configuration

### API Keys
- **NewsAPI**: Free tier allows 1000 requests/month
- **OpenAI**: Pay-per-use model for GPT API calls

### Customization Options
- Number of headlines per category (1-5)
- Verbose logging for debugging
- News categories (Politics/Tech toggle)

## 📁 Project Structure

```
ai-news-reporter/
├── app.py              # Streamlit web application
├── main.py             # Command-line interface
├── agents.py           # CrewAI agent definitions
├── tasks.py            # Task definitions for agents
├── tools.py            # News fetching tools
├── run_app.py          # Launch script with checks(optional)
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
├── .streamlit/
│   └── config.toml     # Streamlit configuration
└── README.md           # This file
```

## 🛠️ Development

### Adding New Agents
1. Define agent in `agents.py`
2. Create corresponding tasks in `tasks.py`
3. Add agent to crew in both `main.py` and `app.py`

### Customizing News Sources
- Modify the `news_fetcher` tool in `tools.py`
- Adjust API parameters for different regions/languages
- Add new news APIs as needed

### Styling the Web App
- Edit CSS in `app.py` for visual customization
- Modify `config.toml` for theme changes

## 🔍 Troubleshooting

### Common Issues

1. **Missing API Keys**:
   ```
   Error: NEWSAPI_KEY not found
   ```
   **Solution**: Create `.env` file with your API keys

2. **Import Errors**:
   ```
   ModuleNotFoundError: No module named 'crewai'
   ```
   **Solution**: Run `pip install -r requirements.txt`

3. **Network Issues**:
   ```
   Error fetching news: Connection timeout
   ```
   **Solution**: Check internet connection and API key validity

### Debug Mode
Enable verbose logging in the Streamlit sidebar to see detailed agent reasoning and API calls.

## 📊 Performance Notes

- **Response Time**: 30-60 seconds for complete news cycle
- **API Limits**: 
  - NewsAPI: 1000 requests/month (free tier)
  - OpenAI: Varies by model and usage
- **Concurrent Processing**: Politics and tech news fetched in parallel

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [CrewAI](https://github.com/joaomdmoura/crewAI) - Multi-agent orchestration framework
- [Streamlit](https://streamlit.io/) - Web app framework
- [NewsAPI](https://newsapi.org/) - News data provider
- [OpenAI](https://openai.com/) - Language model provider

## 📞 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Review the [CrewAI documentation](https://docs.crewai.com/)
3. Open an issue on GitHub

---

**Happy News Hunting! 📰🤖**