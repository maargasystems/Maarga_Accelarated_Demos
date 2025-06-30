# 🤖 Maarga AI Accelerated Agents Collection

Welcome to the **Maarga AI Accelerated Agents Collection** - a comprehensive suite of AI-powered applications designed to automate and enhance various workflows across different domains. This repository contains 12 specialized AI agents, each containerized with Docker for easy deployment and scaling.

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- API keys for the required services (see individual agent requirements)

### Running All Agents
```bash
# Start all agents at once
docker-compose up

# Start specific agents
docker-compose up Data_Analyst_Agent AI_Travel_Planner

# Run in background
docker-compose up -d
```

### Accessing the Agents
Once running, access each agent through their respective ports:
- **Data Analyst Agent**: http://localhost:8501
- **AI Travel Planner**: http://localhost:8502
- **BreakUp Recovery Agent**: http://localhost:8503
- **AI Medical Imaging Agent**: http://localhost:8504
- **AI Music Generator**: http://localhost:8505
- **AI Data Visualization Agent**: http://localhost:8506
- **AI Startup Trend Analysis**: http://localhost:8507
- **XAI Finance Agent**: http://localhost:8508
- **OpenAI Research Agent**: http://localhost:8509
- **AI Blog to Podcast Agent**: http://localhost:8510
- **Multimodal AI Agent**: http://localhost:8511
- **Multimodal AI Agent (Image)**: http://localhost:8512

## 🎯 Agent Descriptions

### 📊 Data Analyst Agent
**Port**: 8501  
**Purpose**: Advanced data analysis and visualization tool powered by AI  
**Features**:
- Upload CSV/Excel files for analysis
- Natural language querying of data using DuckDB
- Automated data preprocessing and cleaning
- Interactive data exploration with Pandas
- AI-powered insights and recommendations

**Tech Stack**: Streamlit, DuckDB, Pandas, OpenRouter API

---

### ✈️ AI Travel Planner
**Port**: 8502  
**Purpose**: Intelligent travel itinerary planning and research  
**Features**:
- Personalized travel recommendations
- Real-time flight and accommodation research
- Budget optimization suggestions
- Local attractions and activity planning
- Weather-aware scheduling

**Tech Stack**: Streamlit, SerpAPI, OpenRouter (GPT-4o)

---

### 💔 BreakUp Recovery Agent
**Port**: 8503  
**Purpose**: Emotional support and guidance for relationship recovery  
**Features**:
- Personalized recovery strategies
- Emotional wellness tracking
- Activity recommendations
- Progress monitoring
- Mental health resources

**Tech Stack**: Streamlit, OpenRouter API

---

### 🏥 AI Medical Imaging Agent
**Port**: 8504  
**Purpose**: AI-powered medical image analysis and interpretation  
**Features**:
- Medical image upload and analysis
- AI-assisted diagnosis suggestions
- Radiological pattern recognition
- Educational insights about conditions
- Research integration for context

**Tech Stack**: Streamlit, Google Gemini 2.5 Flash, PIL, DuckDuckGo Tools

**⚠️ Disclaimer**: For educational purposes only. Always consult qualified healthcare professionals.

---

### 🎵 AI Music Generator Agent
**Port**: 8505  
**Purpose**: AI-powered music composition and generation  
**Features**:
- Text-to-music generation
- Multiple genre support
- Customizable duration and style
- High-quality audio output (MP3)
- Creative prompt interpretation

**Tech Stack**: Streamlit, ModelsLab API, OpenRouter (GPT-4o)

---

### 📈 AI Data Visualization Agent
**Port**: 8506  
**Purpose**: Automated data visualization and chart generation  
**Features**:
- Intelligent chart type selection
- Interactive visualizations
- Data pattern recognition
- Export capabilities
- Dashboard creation

**Tech Stack**: Streamlit, OpenRouter API, Visualization Libraries

---

### 💼 AI Startup Trend Analysis Agent
**Port**: 8507  
**Purpose**: Market research and startup trend analysis  
**Features**:
- Industry trend identification
- Market opportunity analysis
- Competitive landscape research
- Investment pattern analysis
- Startup ecosystem insights

**Tech Stack**: Streamlit, OpenRouter API, Web Research Tools

---

### 💰 XAI Finance Agent
**Port**: 8508  
**Purpose**: Financial analysis and investment research using Grok AI  
**Features**:
- Real-time stock analysis
- Financial data interpretation
- Market trend analysis
- Investment recommendations
- Portfolio optimization insights

**Tech Stack**: Streamlit, X.AI Grok-3-Beta, YFinance, DuckDuckGo Tools

---

### 🔬 OpenAI Research Agent
**Port**: 8509  
**Purpose**: Advanced research and knowledge synthesis  
**Features**:
- Academic paper analysis
- Research topic exploration
- Citation management
- Knowledge graph creation
- Synthesis and summarization

**Tech Stack**: Streamlit, OpenRouter API, Research Tools

---

### 🎙️ AI Blog to Podcast Agent
**Port**: 8510  
**Purpose**: Convert written content to engaging podcast audio  
**Features**:
- Blog URL scraping with Firecrawl
- Content summarization and restructuring
- Natural voice synthesis
- Multiple voice options
- Audio file generation (MP3/WAV)

**Tech Stack**: Streamlit, Firecrawl, ElevenLabs, OpenRouter API

---

### 🧠 Multimodal AI Agent
**Port**: 8511  
**Purpose**: Video analysis and multimodal content understanding  
**Features**:
- Video upload and analysis
- Visual content interpretation
- Cross-modal reasoning
- Web research integration
- Real-time processing

**Tech Stack**: Streamlit, Google Gemini 2.0, DuckDuckGo Tools

---

### 🖼️ Multimodal AI Agent (Image)
**Port**: 8512  
**Purpose**: Image analysis and visual AI capabilities  
**Features**:
- Image upload and analysis
- Visual question answering
- Object detection and recognition
- Scene understanding
- Web-enhanced analysis

**Tech Stack**: Streamlit, Google Gemini 2.0, Image Processing Libraries

## 🛠️ Development Setup

### Individual Agent Development
```bash
# Navigate to specific agent directory
cd ai_blog_to_podcast_agent

# Create virtual environment
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the agent
streamlit run app.py
```

### Docker Development
```bash
# Build specific agent
docker build -f dockerfile -t agent_name ./agent_directory

# Run with custom configuration
docker run -p 8501:8501 -v $(pwd)/agent_directory:/app agent_name
```

## 🔧 Configuration

### API Keys Required
Different agents require different API keys. Configure them through the Streamlit interface:

- **OpenRouter API**: Required for most agents (GPT-4o, Grok, etc.)
- **ElevenLabs API**: For voice synthesis (Blog to Podcast Agent)
- **Firecrawl API**: For web scraping (Blog to Podcast Agent)
- **SerpAPI**: For search functionality (Travel Planner)
- **ModelsLab API**: For music generation
- **Google AI API**: For Gemini models (Medical Imaging, Multimodal agents)

### Environment Variables
```bash
# Example .env file
OPENROUTER_API_KEY=your_openrouter_key
ELEVEN_LABS_API_KEY=your_elevenlabs_key
FIRECRAWL_API_KEY=your_firecrawl_key
SERP_API_KEY=your_serpapi_key
MODELS_LAB_API_KEY=your_modelslab_key
GOOGLE_API_KEY=your_google_ai_key
```

## 📁 Project Structure

```
docker_demo/
├── docker-compose.yml          # Multi-agent orchestration
├── dockerfile                  # Shared Docker configuration
├── README.md                   # This file
├── ai_blog_to_podcast_agent/   # Blog → Podcast conversion
├── AI_Data_Visualisation_Agent/# Data visualization
├── ai_medical_imaging_agent/   # Medical image analysis
├── ai_music_generator_agent/   # Music generation
├── ai_startup_trend_analysis_agent/ # Startup analysis
├── AI_Travel_Planner/          # Travel planning
├── BreakUp_Recovery_Agent/     # Emotional support
├── Data_Analyst_Agent/         # Data analysis
├── multimodal_ai_agent/        # Video analysis
├── multimodal_ai_agent_Image/  # Image analysis
├── opeani_research_agent/      # Research assistance
└── xai_finance_agent/          # Financial analysis
```

Each agent directory contains:
- `app.py` - Main Streamlit application
- `requirements.txt` - Python dependencies
- `README.md` - Agent-specific documentation (where available)

## 🚀 Deployment

### Production Deployment
```bash
# Production build
docker-compose -f docker-compose.yml up --build -d

# Scale specific services
docker-compose up --scale Data_Analyst_Agent=3

# Monitor logs
docker-compose logs -f agent_name
```

### Cloud Deployment
The agents can be deployed on various cloud platforms:
- **AWS ECS/Fargate**
- **Google Cloud Run**
- **Azure Container Instances**
- **Kubernetes clusters**

## 🔍 Monitoring and Health Checks

```bash
# Check agent status
docker-compose ps

# View logs
docker-compose logs agent_name

# Health check endpoints
curl http://localhost:8501/_stcore/health
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-agent`
3. Commit changes: `git commit -am 'Add new agent'`
4. Push to branch: `git push origin feature/new-agent`
5. Submit a Pull Request

### Adding a New Agent
1. Create agent directory: `mkdir new_agent/`
2. Add `app.py`, `requirements.txt`, and `README.md`
3. Update `docker-compose.yml` with new service
4. Test locally before submitting PR

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Open an issue in the repository
- Check individual agent README files
- Review API documentation for external services

## 🙏 Acknowledgments

- **Agno**: AI agent framework
- **Streamlit**: Web application framework
- **OpenRouter**: Multi-model API access
- **ElevenLabs**: Voice synthesis
- **Firecrawl**: Web scraping
- **ModelsLab**: AI model APIs
- **Google AI**: Gemini models

---

**Built with ❤️ by the Maarga AI Team**

> 🌟 Star this repository if you find it helpful!
