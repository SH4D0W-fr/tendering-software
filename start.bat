@echo off
REM Vérification de la version de Python (3.10 recommandé)
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python n'est pas installé. Installation de Python 3.10...
    powershell -Command "Start-Process 'https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe' -Wait"
    echo Veuillez installer Python 3.10 avec l'option 'Add Python to PATH', puis relancez ce script.
    pause
    exit /b 1
)

REM Installation des dépendances Python
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Création du dossier models si nécessaire
IF NOT EXIST "models" (
    mkdir models
)

REM Téléchargement automatique du modèle si absent
IF NOT EXIST "models\mistral-7b-instruct-v0.1.Q4_K_M.gguf" (
    echo Téléchargement du modèle Mistral-7B-Instruct...
    powershell -Command "Invoke-WebRequest -Uri 'https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf' -OutFile 'models/mistral-7b-instruct-v0.1.Q4_K_M.gguf'"
)

REM Vérification si Visual Studio est installé
reg query "HKLM\SOFTWARE\Microsoft\VisualStudio\SxS\VS7" >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Visual Studio n'est pas installé. Installation de Visual Studio...
    powershell -Command "Start-Process 'https://aka.ms/vs/17/release/vs_community.exe' -ArgumentList '--add Microsoft.VisualStudio.Workload.Python --add Microsoft.VisualStudio.Workload.NativeDesktop --add Microsoft.VisualStudio.Workload.VCTools --wait' -Wait"
    echo Visual Studio a été installé avec succès.
) ELSE (
    echo Visual Studio est déjà installé.
)

REM Lancement du programme principal
python main.py

pause
