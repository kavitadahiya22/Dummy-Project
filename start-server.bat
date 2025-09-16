@echo off
echo Starting Penetration Testing Framework Demo...
python -m uvicorn main_demo:app --host 127.0.0.1 --port 8003
pause