# SHADOW Tendering Software

**SHADOW Tendering Software** is a basic tool designed to analyze tender documents (PDF, Word) using regular expressions and local AI model :Mistral 7B. The software extracts key information, answers specific questions, and generates a structured response — all within an intuitive graphical interface (Tkinter or PyQt).

---

## ✨ Features

- 📄 **Document Parsing**: Supports PDF, DOCX and TXT formats.
- 🔍 **Regex Extraction**: Uses configurable regular expressions to extract key tender data.
- 🤖 **Local AI Model Integration**: Answer questions using a local open-source model : Mistral 7B.
- 🧠 **Smart Q&A Engine**: Automatically answers questions based on document content, not just keywords.
- 🖥️ **User Interface**: Use PyQt for a simple interface.

---

## 🚀 Getting Started

This section will help you quickly install and run **TenderDoc Analyzer**, whether you're a developer or a non-technical user.

---

### 📦 Prerequisites

Before you begin, make sure you have:

- **Windows** (recommended)
- **Python 3.10+** installed and added to your system PATH  
  *(The app will prompt you to install Python 3.10.11 if not detected)*

---

### 📁 Quick Installation (Recommended)

A `start.bat` file is included to automate the entire setup. It will:

1. Check if Python 3.10 is installed.
2. If not installed, open the official Python installer download page.
3. Install all required Python libraries via `requirements.txt`.
4. Launch the application.

#### ✅ To install and launch the app:

Double-click on `start.bat` or run it from the terminal:

```bat
start.bat
```

> 📝 **Important:** If Python is not installed, follow the installer instructions and make sure to check **"Add Python to PATH"** before proceeding.

---

### ⚙️ Manual Installation (Advanced Users)

If you prefer manual installation:

#### 1. Install Python 3.10+

Download from:  
[https://www.python.org/downloads/release/python-31011/](https://www.python.org/downloads/release/python-31011/)

Make sure to check **"Add Python to PATH"** during installation.

#### 2. Install Python Dependencies

Run the following command in your terminal or command prompt:

```bash
pip install -r requirements.txt
```

This will install:

| Library               | Version       | Purpose                                                                 |
|----------------------|---------------|-------------------------------------------------------------------------|
| **PyQt5**            | ≥ 5.15.0      | Used to create the graphical interface (UI).                           |
| **pdfplumber**       | ≥ 0.5.28      | Extracts text from PDF files with layout awareness.                    |
| **python-docx**      | ≥ 0.8.11      | Parses and extracts content from Word (DOCX) documents.                |
| **transformers**     | ≥ 4.36.0      | Provides transformer-based models and pipelines (e.g., Mistral 7B).    |
| **torch**            | ≥ 2.0.0       | Backend for running AI models (PyTorch framework).                     |
| **pillow**           | ≥ 8.0.0       | Image processing (used for PDF previews and interface icons if needed).|
| **llama-cpp-python** | ≥ 0.2.72      | Interface to run LLaMA-based models (like Mistral 7B) locally via C++. |

### 3. Download the model
You must create a "models" folder and download `mistral-7b-instruct-v0.1.Q4_K_M` from [here](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf)
Put the model inside the folder.

#### 4. Launch the Application

Use the command below to start the app manually:

```bash
python main.py
```

---

### 🖥️ Application Workflow

Once launched, you will be guided through:

1. Selecting the tender document (PDF, Word, or TXT)
2. Questions that will be asked to the AI
3. Once ready, you just have to press the green button
   
---

### 🧪 Tested Environments

- ✅ Windows 11 (64-bit) with Intel I7-18000H and 32GB of RAM
- ✅ Python 3.10.11

---

## 📁 Folder Structure

```
SHADOW Tendring Software/
├── models/mistral-7b-instruct-v0.1.Q4_K_M.gguf                  # Mistral 7B
├── main.py                                                      # Main script
├── questions.json                                               # Default question storage
├── start.bat                                                    # Auto-setup script
└── requirements.txt                                             # Python dependencies
```

---

## 🧠 AI Model

This software currently uses Mistral 7b to combine precision and speed on all types of machines.
You can change the model but no support will be provided, you will have to make all the modifications by yourself.

How to change the model :

- Download and place the model files in the `models/` directory.
- Ensure the model path is correctly set in the configuration.

---

## 📃 License

**GPL-3.0 License** – This software is licensed under the GNU General Public License v3.0.  
You are free to use, modify, and distribute the software, provided that any derivative works are also distributed under the same license.

For more details, see the full license text here:  
[https://www.gnu.org/licenses/gpl-3.0.en.html](https://www.gnu.org/licenses/gpl-3.0.en.html)

---


## 🤝 Contribution

Feel free to fork, suggest improvements, or report issues on GitHub. Contributions are welcome!

---


# 🇫🇷 SHADOW Tendering Software

**SHADOW Tendering Software** est un outil simple conçu pour analyser des documents d’appel d’offres (PDF, Word) à l’aide d'expressions régulières et d’un modèle d’IA local : Mistral 7B. Le logiciel extrait les informations clés, répond à des questions précises et génère une réponse structurée — le tout via une interface graphique intuitive (Tkinter ou PyQt).

---

## ✨ Fonctionnalités

- 📄 **Analyse de documents** : Prise en charge des formats PDF, DOCX et TXT.
- 🔍 **Extraction par Regex** : Utilisation d'expressions régulières personnalisables pour extraire les données clés.
- 🤖 **Intégration d'un modèle IA local** : Réponse aux questions via un modèle open-source local : Mistral 7B.
- 🧠 **Moteur de questions/réponses intelligent** : Réponses automatiques basées sur le contenu réel du document.
- 🖥️ **Interface utilisateur** : Interface simple basée sur PyQt.

---

## 🚀 Premiers Pas

Cette section vous guide pour installer et lancer rapidement **TenderDoc Analyzer**, que vous soyez développeur ou non-technicien.

---

### 📦 Prérequis

Avant de commencer, assurez-vous d’avoir :

- **Windows** (recommandé)
- **Python 3.10+** installé et ajouté à votre PATH système  
  *(L’application vous proposera d’installer Python 3.10.11 si elle ne le détecte pas)*

---

### 📁 Installation Rapide (Recommandée)

Un fichier `start.bat` est inclus pour automatiser toute l’installation. Il va :

1. Vérifier si Python 3.10 est installé.
2. Si ce n’est pas le cas, ouvrir la page de téléchargement officielle.
3. Installer toutes les bibliothèques nécessaires via `requirements.txt`.
4. Lancer l’application.

#### ✅ Pour installer et lancer l'application :

Double-cliquez sur `start.bat` ou lancez-le dans le terminal :

```bat
start.bat
```

> 📝 **Important :** Si Python n’est pas installé, suivez les instructions de l’installeur et cochez **"Add Python to PATH"** avant de continuer.

---

### ⚙️ Installation Manuelle (Utilisateurs avancés)

Si vous préférez installer manuellement :

#### 1. Installer Python 3.10+

Téléchargez depuis :  
[https://www.python.org/downloads/release/python-31011/](https://www.python.org/downloads/release/python-31011/)

Assurez-vous de cocher **"Add Python to PATH"** lors de l’installation.

#### 2. Installer les dépendances Python

Dans un terminal ou invite de commandes :

```bash
pip install -r requirements.txt
```

Cela installera :

| Bibliothèque          | Version       | Rôle / Utilité                                                              |
|-----------------------|---------------|------------------------------------------------------------------------------|
| **PyQt5**             | ≥ 5.15.0      | Utilisée pour créer l'interface graphique (UI).                            |
| **pdfplumber**        | ≥ 0.5.28      | Permet d'extraire du texte des fichiers PDF tout en respectant leur mise en page. |
| **python-docx**       | ≥ 0.8.11      | Permet d'analyser et d'extraire le contenu des documents Word (DOCX).      |
| **transformers**      | ≥ 4.36.0      | Fournit des modèles de langage (ex. Mistral 7B) et des outils pour l’IA.    |
| **torch**             | ≥ 2.0.0       | Moteur d'exécution des modèles IA basé sur PyTorch.                         |
| **pillow**            | ≥ 8.0.0       | Utilisé pour le traitement d’images (ex. affichage d’icônes ou d’aperçus PDF). |
| **llama-cpp-python**  | ≥ 0.2.72      | Permet d'exécuter des modèles LLaMA localement (comme Mistral 7B).         |

### 3. Télécharger le modèle
Vous devez créer un dossier "models" et télécharger `mistral-7b-instruct-v0.1.Q4_K_M` depuis [ici](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf)
Une fois le téléchargement terminé, déplacez le modèle dans le dossier.

#### 4. Lancer l'application

Lancez le logiciel manuellement avec :

```bash
python main.py
```

---

### 🖥️ Fonctionnement

Une fois lancé, l'application vous guide à travers :

1. La sélection du document d’appel d’offres (PDF, Word ou TXT)
2. L'affichage des questions posées à l'IA
3. Une fois prêt, il vous suffit d’appuyer sur le bouton vert

---

### 🧪 Environnements testés

- ✅ Windows 11 (64 bits) avec Intel i7-18000H et 32 Go de RAM
- ✅ Python 3.10.11

---

## 📁 Structure des dossiers

```
SHADOW Tendring Software/
├── models/mistral-7b-instruct-v0.1.Q4_K_M.gguf                  # Mistral 7B
├── main.py                                                      # Script principal
├── questions.json                                               # Questions par défaut
├── start.bat                                                    # Script d’installation automatique
└── requirements.txt                                             # Dépendances Python
```

---

## 🧠 Modèle IA

Le logiciel utilise actuellement **Mistral 7B** pour combiner rapidité et précision, même sur des machines locales.  
Vous pouvez le remplacer, mais aucun support ne sera fourni : toutes les modifications devront être faites manuellement.

Comment changer le modèle :

- Téléchargez et placez les fichiers du modèle dans le dossier `models/`
- Vérifiez que le chemin vers le modèle est bien défini dans la configuration

---

## 📃 Licence

**Licence GPL-3.0** – Ce logiciel est sous licence GNU General Public License v3.0.  
Vous êtes libre d’utiliser, modifier et redistribuer le logiciel, à condition que tout dérivé soit distribué sous la même licence.

Texte complet de la licence disponible ici :  
[https://www.gnu.org/licenses/gpl-3.0.fr.html](https://www.gnu.org/licenses/gpl-3.0.fr.html)

---

## 🤝 Contribuer

N'hésitez pas à forker le projet, proposer des améliorations ou signaler des bugs sur GitHub. Toute contribution est la bienvenue !

