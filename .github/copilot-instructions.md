# Penetration Testing Framework - Copilot Instructions

This is a comprehensive Python-based penetration testing framework with the following components:

## Project Structure
- `main.py` - FastAPI service with `/invoke_pentest` endpoint
- `pentest_app/agents/` - CrewAI agent definitions
- `pentest_app/modules/` - Modular penetration testing tools
- `pentest_app/utils/` - OpenSearch client and Docker utilities
- `Dockerfile` - Container setup with all security tools

## Key Features
- Modular penetration testing phases (Recon, Vuln Scan, Exploitation, etc.)
- CrewAI agent orchestration with Ollama DeepSeek reasoning
- OpenSearch integration for result storage and analytics
- Docker containerization with pre-installed security tools
- Ethical constraints limited to juice-shop.herokuapp.com

## Security Guidelines
- All operations limited to authorized target (juice-shop.herokuapp.com)
- User consent required before execution
- Comprehensive logging for audit trails
- Results stored in OpenSearch for analysis

## Development Focus
- Async FastAPI endpoints for scalability
- Exception handling and proper logging
- Modular design for extensibility
- Docker-first deployment approach