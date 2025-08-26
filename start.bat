@echo off
REM Ativa o ambiente virtual (ajuste o caminho se necessário)
call venv\Scripts\activate

REM Inicia o servidor FastAPI com reload automático
uvicorn main:app --reload --host 0.0.0.0

pause