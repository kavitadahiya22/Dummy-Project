# Penetration Testing Framework# Penetration Testing Framework



A comprehensive, modular penetration testing framework built with FastAPI, CrewAI agents, and Docker integration.A comprehensive, modular penetration testing framework built with FastAPI, CrewAI agents, and Docker integration. This framework provides automated security testing capabilities with intelligent reasoning through Ollama DeepSeek and comprehensive result storage in OpenSearch.



## 📁 Project Structure## 🚨 **ETHICAL USE NOTICE**



```**This tool is designed for authorized penetration testing only. Currently restricted to testing juice-shop.herokuapp.com. Unauthorized use against any other targets is prohibited and may be illegal.**

penetration-testing-framework/

├── 📄 main.py                    # Main FastAPI application## 🏗️ Architecture

├── 📄 main_demo.py               # Demo version for testing

├── 📄 requirements.txt           # Python dependencies```

├── 📄 .gitignore                 # Git ignore patterns┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐

││   FastAPI Web  │    │   CrewAI Agents  │    │ Docker Security │

├── 📁 pentest_app/               # Core application modules│   Interface     │───▶│   Orchestration  │───▶│     Tools       │

│   ├── 📁 agents/               # CrewAI agents└─────────────────┘    └──────────────────┘    └─────────────────┘

│   ├── 📁 modules/              # Testing modules (recon, vuln scan, etc.)         │                        │                        │

│   └── 📁 utils/                # Utilities (OpenSearch, Docker)         ▼                        ▼                        ▼

│┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐

├── 📁 scripts/                   # Automation scripts│   OpenSearch    │    │ Ollama DeepSeek  │    │   Result        │

│   ├── 📁 powershell/           # PowerShell automation│   Results DB    │    │   AI Reasoning   │    │   Analytics     │

│   │   ├── complete-test.ps1    # Full automated testing└─────────────────┘    └──────────────────┘    └─────────────────┘

│   │   ├── run-project.ps1      # Quick project startup```

│   │   ├── setup-git.ps1        # Git repository setup

│   │   └── validate-test.ps1    # Validation scripts## 🔧 Features

│   ├── 📁 testing/              # API testing scripts

│   │   ├── test-api.py          # Python API tests### Core Capabilities

│   │   ├── test-api.ps1         # PowerShell API tests- **Modular Architecture**: Separate modules for different testing phases

│   │   └── test-command.ps1     # Simple API testing- **AI-Powered Analysis**: CrewAI agents with Ollama DeepSeek reasoning

│   ├── start-server.bat         # Windows batch startup- **Comprehensive Logging**: All results stored in OpenSearch

│   └── start.sh                 # Linux/Mac startup- **Docker Isolation**: Security tools run in isolated containers

│- **REST API**: FastAPI-based web interface

├── 📁 docker/                    # Docker configuration- **Real-time Monitoring**: Track test progress and results

│   ├── Dockerfile               # Container definition

│   ├── docker-compose.yml       # Multi-service orchestration### Security Modules

│   └── .dockerignore           # Docker ignore patterns1. **Reconnaissance**: Port scanning, service detection, DNS enumeration

│2. **Vulnerability Scanning**: Nikto, OWASP ZAP, custom vulnerability checks

├── 📁 config/                    # Configuration files3. **Exploitation**: SQLMap, safe exploitation testing

│   └── .env.example             # Environment variables template4. **Password Testing**: Hydra, John the Ripper integration

│5. **Network Analysis**: Traffic analysis and monitoring

├── 📁 docs/                      # Documentation

│   └── README.md                # Detailed documentation### Security Controls

│- ✅ **Target Restriction**: Limited to authorized targets only

└── 📁 .github/                   # GitHub configuration- ✅ **User Consent**: Explicit consent required before testing

    └── copilot-instructions.md  # AI assistant instructions- ✅ **Audit Logging**: Complete audit trail in OpenSearch

```- ✅ **Rate Limiting**: Respectful testing to avoid DoS

- ✅ **Ethical Boundaries**: Non-destructive testing only

## 🚀 Quick Start

## 📋 Prerequisites

### Option 1: Demo Mode (Fastest)

```powershell- **Docker & Docker Compose**: Latest versions

# Start the demo server- **Python 3.11+**: For local development

python -m uvicorn main_demo:app --reload --host 127.0.0.1 --port 8000- **4GB+ RAM**: For running all containers

- **Network Access**: To OpenSearch instance and target

# Test the API

.\scripts\testing\test-command.ps1## 🚀 Quick Start

```

### 1. Clone and Setup

### Option 2: Automated Setup

```powershell```bash

# Run complete setup and testinggit clone <your-repo>

.\scripts\powershell\run-project.ps1cd penetration-testing-framework

``````



### Option 3: Docker Deployment### 2. Docker Deployment (Recommended)

```powershell

# Full containerized deployment```bash

cd docker# Build and start all services

docker-compose up --builddocker-compose up --build

```

# Check service health

## 🔧 Configurationcurl http://localhost:8000/health

```

Copy the environment template:

```powershell### 3. Local Development Setup

Copy-Item "config\.env.example" ".env"

# Edit .env with your settings```bash

```# Create virtual environment

python -m venv venv

## 📊 API Endpointssource venv/bin/activate  # On Windows: venv\Scripts\activate



- **Health Check**: `GET /health`# Install dependencies

- **Start Pentest**: `POST /invoke_pentest`pip install -r requirements.txt

- **Check Status**: `GET /pentest_status/{run_id}`

- **API Docs**: `GET /docs`# Start Ollama separately

docker run -d -p 11434:11434 ollama/ollama:latest

## 🧪 Testing

# Pull DeepSeek model

Run all tests:docker exec <ollama-container> ollama pull deepseek-coder

```powershell

.\scripts\testing\test-api.ps1# Run the application

```uvicorn main:app --reload

```

Quick validation:

```powershell## 📖 Usage Examples

.\scripts\powershell\validate-test.ps1

```### Basic Penetration Test



## 🔒 Security Notice```bash

# Start a penetration test

**This framework is designed for authorized penetration testing only.**curl -X POST "http://localhost:8000/invoke_pentest" \

- Currently restricted to `juice-shop.herokuapp.com`  -H "Content-Type: application/json" \

- User consent required before testing  -d '{

- All activities logged for audit purposes    "target": "https://juice-shop.herokuapp.com",

- Non-destructive testing approach only    "consent_acknowledged": true

  }'

## 📖 Documentation

# Response

Full documentation is available in the `docs/` folder:{

- [Detailed README](docs/README.md)  "run_id": "123e4567-e89b-12d3-a456-426614174000",

- API documentation at `/docs` when server is running  "status": "initiated",

  "message": "Penetration test has been started. Use the run_id to check status.",

## 🛠️ Development  "target": "https://juice-shop.herokuapp.com",

  "timestamp": "2025-09-16T10:30:00Z",

Setup development environment:  "estimated_duration": "15-30 minutes"

```powershell}

# Install dependencies```

pip install -r requirements.txt

### Check Test Status

# Start development server

python -m uvicorn main:app --reload```bash

```# Check test progress

curl "http://localhost:8000/pentest_status/123e4567-e89b-12d3-a456-426614174000"

## 🤝 Contributing

# Response

1. Fork the repository{

2. Create a feature branch  "run_id": "123e4567-e89b-12d3-a456-426614174000",

3. Make your changes  "status": "running",

4. Run tests: `.\scripts\testing\test-api.ps1`  "progress": {

5. Submit a pull request    "current_phase": "vulnerability_scanning",

    "completed_modules": ["recon"],

## 📝 License    "total_modules": 5,

    "percentage": 20

This project is for educational and authorized security testing purposes only.  },

  "start_time": "2025-09-16T10:30:00Z"

---}

```

**⚠️ ETHICAL USE ONLY**: Use responsibly and only against authorized targets.
### Retrieve Results

```bash
# Get detailed results
curl "http://localhost:8000/pentest_results/123e4567-e89b-12d3-a456-426614174000"

# Response includes all findings, tool outputs, and analysis
```

### Specific Module Testing

```bash
# Run only specific modules
curl -X POST "http://localhost:8000/invoke_pentest" \
  -H "Content-Type: application/json" \
  -d '{
    "target": "https://juice-shop.herokuapp.com",
    "consent_acknowledged": true,
    "modules": ["recon", "vuln_scan"]
  }'
```

## 📊 OpenSearch Integration

### Accessing Results Dashboard

1. **OpenSearch Dashboards**: https://cybrty-dev-ca.wonderfuldune-e921120d.eastus.azurecontainerapps.io
2. **Index Pattern**: `pentest-results`
3. **Key Fields**:
   - `run_id`: Unique test identifier
   - `timestamp`: When finding was discovered
   - `target`: Target URL tested
   - `tool`: Tool that generated the finding
   - `severity`: Finding severity (high/medium/low/info)
   - `finding`: Description of the finding

### Sample Queries

```json
# High severity findings
{
  "query": {
    "term": { "severity": "high" }
  }
}

# Findings for specific target
{
  "query": {
    "term": { "target": "https://juice-shop.herokuapp.com" }
  }
}

# Recent test runs
{
  "query": {
    "range": {
      "timestamp": {
        "gte": "now-24h"
      }
    }
  }
}
```

## 🔧 Configuration

### Environment Variables

```bash
# OpenSearch Configuration
OPENSEARCH_HOST=cybrty-dev-ca.wonderfuldune-e921120d.eastus.azurecontainerapps.io
OPENSEARCH_PORT=443
OPENSEARCH_USE_SSL=true
OPENSEARCH_INDEX=pentest-results

# Ollama Configuration
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=deepseek-coder

# Application Configuration
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO
```

### Docker Compose Override

Create `docker-compose.override.yml` for custom configurations:

```yaml
version: '3.8'
services:
  pentest-framework:
    environment:
      - LOG_LEVEL=DEBUG
    volumes:
      - ./custom-config:/app/config
```

## 🧪 API Documentation

### Interactive Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/invoke_pentest` | POST | Start penetration test |
| `/pentest_status/{run_id}` | GET | Check test status |
| `/pentest_results/{run_id}` | GET | Get detailed results |
| `/authorized_targets` | GET | List authorized targets |

## 🛠️ Development

### Project Structure

```
penetration-testing-framework/
├── main.py                     # FastAPI application
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Container definition
├── docker-compose.yml          # Multi-container setup
├── pentest_app/
│   ├── __init__.py
│   ├── agents/
│   │   ├── __init__.py
│   │   └── pentest_agent.py    # CrewAI agent orchestration
│   ├── modules/
│   │   ├── __init__.py
│   │   ├── recon.py            # Reconnaissance module
│   │   ├── vuln_scan.py        # Vulnerability scanning
│   │   ├── exploit.py          # Exploitation testing
│   │   ├── crack.py            # Password cracking
│   │   └── sniff.py            # Network sniffing
│   └── utils/
│       ├── __init__.py
│       ├── opensearch_client.py # OpenSearch integration
│       └── docker_runner.py     # Docker tool execution
└── .github/
    └── copilot-instructions.md  # Development guidelines
```

### Adding New Modules

1. Create new module in `pentest_app/modules/`
2. Implement the standard interface:
   ```python
   class NewModule:
       def __init__(self, run_id, target, opensearch_client):
           # Initialize module
           
       async def execute(self) -> Dict[str, Any]:
           # Execute testing logic
           return results
   ```
3. Register in `pentest_agent.py`
4. Add tests and documentation

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest tests/

# Run with coverage
pytest --cov=pentest_app tests/
```

## 🔒 Security Considerations

### Ethical Guidelines
- **Only test authorized targets**
- **Obtain explicit permission before testing**
- **Use non-destructive testing methods**
- **Respect rate limits and system resources**
- **Report findings responsibly**

### Technical Security
- **Container isolation** for tool execution
- **Non-root user** in containers
- **Resource limits** to prevent resource exhaustion
- **Input validation** for all user inputs
- **Comprehensive logging** for audit purposes

## 🐛 Troubleshooting

### Common Issues

1. **Ollama Not Starting**
   ```bash
   # Check container logs
   docker logs ollama-service
   
   # Manually start Ollama
   docker exec -it ollama-service ollama serve
   ```

2. **OpenSearch Connection Failed**
   ```bash
   # Test connectivity
   curl -k https://cybrty-dev-ca.wonderfuldune-e921120d.eastus.azurecontainerapps.io/es/_cluster/health
   
   # Check application logs
   docker logs pentest-framework
   ```

3. **Docker Build Issues**
   ```bash
   # Clean build
   docker-compose down
   docker system prune -f
   docker-compose up --build
   ```

4. **Permission Denied Errors**
   ```bash
   # Fix file permissions
   sudo chown -R $USER:$USER .
   chmod +x scripts/*.sh
   ```

### Debug Mode

```bash
# Run in debug mode
docker-compose -f docker-compose.yml -f docker-compose.debug.yml up
```

### Logs

```bash
# View application logs
docker logs -f pentest-framework

# View all service logs
docker-compose logs -f

# Export logs
docker logs pentest-framework > pentest.log 2>&1
```

## 📈 Performance Optimization

### Scaling
- **Horizontal scaling**: Multiple worker containers
- **Resource limits**: Configure CPU/memory limits
- **Load balancing**: Use nginx or similar
- **Database optimization**: OpenSearch cluster setup

### Monitoring
- **Health checks**: Built-in health endpoints
- **Metrics**: Prometheus-compatible metrics
- **Alerting**: Integration with monitoring systems

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

### Code Style
- Follow PEP 8 for Python code
- Use type hints
- Add docstrings for all functions
- Run black formatter before committing

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## ⚠️ Disclaimer

This tool is for educational and authorized testing purposes only. Users are responsible for ensuring they have proper authorization before conducting any security testing. The authors are not responsible for any misuse of this tool.

## 📞 Support

- **Issues**: Submit GitHub issues for bugs
- **Documentation**: Check wiki for detailed guides
- **Community**: Join discussions in GitHub Discussions

---

**Remember: Always obtain proper authorization before conducting penetration testing!**