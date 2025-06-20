from llama_cpp import Llama
import sys
import os
import pdfplumber
from docx import Document
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QFileDialog,
    QVBoxLayout, QWidget, QLabel, QTextEdit, QProgressBar, QMessageBox, QComboBox, QTabWidget
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QMetaObject
import json
import threading


questions = [
    "Quel est l'objet principal de ce document ?",
    "Qui est l'entité émettrice de cet appel d'offre ?",
    "Quelles sont les dates importantes mentionnées (publication, remise des offres, début et fin du marché) ?",
    "Quels sont les critères ou conditions de participation ?",
    "Quels sont les montants ou budgets alloués ou estimés ?",
    "Y a-t-il des exigences spécifiques (techniques, administratives, environnementales) ?",
    "Quels documents doivent être fournis pour la candidature ?",
    "Quelles sont les modalités de dépôt des offres (format, adresse, délais) ?",
    "Quels sont les critères d’évaluation des offres ?",
    "Y a-t-il des pénalités ou clauses particulières en cas de non-respect ? Si oui, lesquelles ?",
    "Quels sont les délais d’exécution ou phases prévues pour le projet ?",
    "Quelles sont les garanties ou assurances exigées ?",
    "Y a-t-il des mentions relatives à la confidentialité ou à la propriété intellectuelle ?",
    "Quels sont les contacts ou informations pour obtenir des précisions ou documents complémentaires ?",
    "Quelles sont les modalités de paiement et conditions financières ?",
    "Y a-t-il des sous-traitants autorisés ou interdits ?",
    "Quels sont les risques ou contraintes signalés dans le document ?",
    "Y a-t-il des références normatives ou réglementaires à respecter ?",
    "Quelles sont les clauses de résiliation ou suspension du contrat ?",
    "Y a-t-il des annexes ou documents complémentaires mentionnés ?",
]


model_path = "models/mistral-7b-instruct-v0.1.Q4_K_M.gguf"
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Le fichier du modèle est introuvable : {model_path}")

try:
    llm = Llama(model_path=model_path, n_ctx=8192, n_threads=8)
except Exception as e:
    raise RuntimeError(f"Erreur lors du chargement du modèle: {e}")

def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        with pdfplumber.open(file_path) as pdf:
            return "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
    elif ext == ".docx":
        doc = Document(file_path)
        return "\n".join(paragraph.text for paragraph in doc.paragraphs)
    elif ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def run_with_timeout(func, args=(), kwargs=None, timeout=30):
    if kwargs is None:
        kwargs = {}
    result = [None]
    exception = [None]
    def target():
        try:
            result[0] = func(*args, **kwargs)
        except Exception as e:
            exception[0] = e
    thread = threading.Thread(target=target)
    thread.start()
    thread.join(timeout)
    if thread.is_alive():
        return "⚠️ Temps dépassé pour cette question."
    if exception[0]:
        raise exception[0]
    return result[0]

def ask_llm(question, context):
    max_context_length = 8000
    if len(context) > max_context_length:
        context = context[:max_context_length] + "\n... [contexte tronqué]"
    prompt = f"""
Tu es un expert en analyse de documents d'appels d'offres. En te basant **exclusivement** sur le contexte ci-dessous, tu dois répondre à la question de manière complète, précise et rigoureuse.

**INSTRUCTIONS IMPORTANTES :**
1. Réponds **clairement** et **directement** à la question posée.
2. Inclue **toutes les citations exactes** du document, placées entre guillemets, dès que possible.
3. Indique **le numéro de page** d'où provient chaque citation, si disponible dans le contexte.
4. Recherche **toutes les occurrences pertinentes**, y compris dans les titres ou sections spécifiques.
5. **Cite systématiquement les montants chiffrés**, les pourcentages, les délais et les conditions s’ils sont présents dans le contexte.
6. Ne t'arrête pas prématurément : continue jusqu'à ce que toutes les informations pertinentes soient citées.
7. Si l'information demandée **n'est pas présente**, écris explicitement : « L'information ne figure pas dans le contexte fourni. »
8. Ne fais **aucune supposition ou interprétation hors contexte**.
9. Si tu trouves une réponse potentiellement pertinente mais pas directement liée à la question, mentionne-la en précisant qu'elle pourrait être utile.
10. Recherche spécifiquement **les montants, conditions financières, et clauses importantes relatives aux avances**.

**EXEMPLE DE FORMAT ATTENDU :**

CONTEXTE :
[extrait simulé du document]

QUESTION :
Quel est l'objet du marché ?

RÉPONSE :
L'objet du marché est « la construction d'un bâtiment administratif », comme précisé à la page 3 du document. Une autre mention pertinente est trouvée dans la section intitulée "Objectifs", page 2 : « Ce marché vise à construire un bâtiment administratif moderne. »

---

CONTEXTE :
{context}

QUESTION :
{question}

RÉPONSE :
"""
    try:
        response = llm(prompt=prompt, temperature=0.7, max_tokens=3072, stop=["\n\n", "</s>"])
        answer = response["choices"][0]["text"].strip()
        if answer.endswith(":") or len(answer.split()) < 10:
            answer += "\n⚠️ La réponse semble incomplète. Veuillez vérifier le contexte ou poser une question plus précise."
        if not answer or "L'information ne figure pas" in answer:
            return "Je n'ai pas trouvé d'information pertinente pour répondre à cette question."
        return answer
    except Exception as e:
        return f"⚠️ Erreur : {str(e)}"

class AnalyseThread(QThread):
    progress_update = pyqtSignal(int)
    result_ready = pyqtSignal(list, str)
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
    def run(self):
        context = extract_text(self.file_path)
        answers = []
        for i, q in enumerate(questions):
            answer = ask_llm(q, context)
            answers.append(answer)
            self.progress_update.emit(int((i + 1) / len(questions) * 100))
        base_name = os.path.splitext(os.path.basename(self.file_path))[0]
        self.result_ready.emit(answers)

class AppelOffreApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Analyse Appel d'Offres - Mistral LLM")
        self.setFixedSize(700, 800)
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        main_tab = QWidget()
        self.tabs.addTab(main_tab, "Analyse")
        layout = QVBoxLayout()
        self.label = QLabel("Aucun fichier chargé")
        layout.addWidget(self.label)
        self.button_load = QPushButton("📂 Charger un fichier (PDF/DOCX/TXT)")
        self.button_load.clicked.connect(self.load_file)
        layout.addWidget(self.button_load)
        self.type_label = QLabel("Choisissez le type d'appel d'offre :")
        layout.addWidget(self.type_label)
        self.type_selector = QComboBox()
        self.type_selector.addItem("Sélectionner un type d'appel d'offre")
        self.type_selector.addItems([
            "CCAP", "CCTP", "RC", "AE", "BPU", "DPGF", "DCE", "OS", "CCAG", "PPSPS", "PGC", "DGD", "DOE", "PV", "DC1", "DC2", "ATTRI1", "NOTI2"
        ])
        self.type_selector.currentIndexChanged.connect(self.update_questions)
        layout.addWidget(self.type_selector)
        self.questions_label = QLabel("Questions à poser :")
        layout.addWidget(self.questions_label)
        self.questions_editor = QTextEdit()
        self.questions_editor.setPlaceholderText("Les questions générées apparaîtront ici. Vous pouvez les modifier, ajouter ou supprimer des questions.")
        layout.addWidget(self.questions_editor)
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setPlaceholderText("Les informations importantes détectées apparaîtront ici...")
        layout.addWidget(self.output)
        self.progress = QProgressBar()
        self.progress.setValue(0)
        layout.addWidget(self.progress)
        self.button_analyze = QPushButton("✅ Analyser le document")
        self.button_analyze.clicked.connect(self.analyze_file)
        layout.addWidget(self.button_analyze)
        self.additional_question_label = QLabel("Posez une question supplémentaire à l'IA  (Après l'analyse) :")
        layout.addWidget(self.additional_question_label)
        self.additional_question_input = QTextEdit()
        self.additional_question_input.setPlaceholderText("Entrez votre question ici...")
        layout.addWidget(self.additional_question_input)
        self.button_ask = QPushButton("🤖 Poser la question")
        self.button_ask.clicked.connect(self.ask_additional_question)
        layout.addWidget(self.button_ask)
        main_tab.setLayout(layout)
        info_tab = QWidget()
        self.tabs.addTab(info_tab, "Informations")
        info_message = (
            "Nom du logiciel : Analyse Appel d'Offres\n"
            "Version : 1.0.0\n"
            "Auteur : Axel LIEBENGUTH.\n"
            "Important : Ce logiciel utilise le modèle Mistral-7B-Instruct. Il peut faire des erreurs, pensez à vérifier les informations.\n"
            "Contact : En cas d'erreurs trop fréquentes ou de problèmes, envoyez un mail à a.liebenguth67@gmail.com\n"
        )
        info_layout = QVBoxLayout()
        info_label = QLabel(info_message)
        info_label.setWordWrap(True)
        info_layout.addWidget(info_label)
        info_tab.setLayout(info_layout)
        self.file_path = None
        self.context = None
        questions_file_path = "questions.json"
        with open(questions_file_path, "r", encoding="utf-8") as f:
            questions_data = json.load(f)
        self.default_questions = questions_data.get("default_questions", {})
        self.thread = None
    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Choisir un fichier", "", "Documents (*.pdf *.docx *.txt)")
        if file_path:
            self.file_path = file_path
            self.label.setText(f"Fichier sélectionné : {os.path.basename(file_path)}")
        else:
            self.label.setText("Aucun fichier chargé")
    def update_questions(self):
        selected_type = self.type_selector.currentText()
        if selected_type == "Sélectionner un type d'appel d'offre":
            self.questions_editor.clear()
        else:
            questions = self.default_questions.get(selected_type, [])
            self.questions_editor.setPlainText("\n".join(questions))
    def analyze_file(self):
        if not self.file_path:
            self.output.setText("Veuillez d'abord sélectionner un fichier.")
            return
        questions = self.questions_editor.toPlainText().strip().split("\n")
        if not questions:
            self.output.setText("Veuillez entrer au moins une question avant de continuer.")
            return
        self.output.setText("Analyse en cours...\n")
        self.progress.setValue(0)
        if self.thread and self.thread.isRunning():
            self.thread.stop()
            self.thread.wait()
        self.thread = AnalyseThreadCustom(self.file_path, questions)
        self.thread.progress_update.connect(self.progress.setValue)
        self.thread.result_ready.connect(self.on_analysis_done)
        self.thread.partial_result.connect(self.append_partial_result)
        self.thread.error_signal.connect(self.handle_error)
        self.thread.start()
    def closeEvent(self, event):
        if self.thread and self.thread.isRunning():
            self.thread.stop()
            self.thread.wait()
        event.accept()
    def on_analysis_done(self, important_info, context):
        self.context = context
        self.output.append("\n✅ Informations importantes détectées :\n")
        for info in important_info:
            self.output.append(f"➡️ {info}\n")
    def handle_error(self, error_message):
        QMessageBox.critical(self, "Erreur", error_message)
        self.output.append(f"❌ {error_message}\n")
    def append_partial_result(self, result):
        self.output.append(result)
    def ask_additional_question(self):
        question = self.additional_question_input.toPlainText().strip()
        if not question:
            self.output.append("❌ Veuillez entrer une question avant de continuer.")
            return
        if not self.context:
            self.output.append("❌ Aucun contexte disponible. Veuillez d'abord analyser un document.")
            return
        self.output.append(f"➡️ Question posée : {question}\n")
        answer = ask_llm(question, self.context)
        self.output.append(f"🤖 Réponse : {answer}\n")

class AnalyseThreadCustom(QThread):
    progress_update = pyqtSignal(int)
    result_ready = pyqtSignal(list, str)
    partial_result = pyqtSignal(str)
    error_signal = pyqtSignal(str)
    def __init__(self, file_path, questions):
        super().__init__()
        self.file_path = file_path
        self.questions = questions
        self._is_running = True
    def run(self):
        try:
            context = extract_text(self.file_path)
            important_info = []
            for i, q in enumerate(self.questions):
                if not self._is_running:
                    break
                try:
                    answer = ask_llm(q, context)
                    if answer and answer.lower() != "je n'ai pas trouvé d'information pertinente pour répondre à cette question.":
                        result = f"{q} : {answer}"
                        important_info.append(result)
                        self.partial_result.emit(f"➡️ {result}\n")
                    else:
                        self.partial_result.emit(f"❌ Pas de réponse pertinente trouvée pour : {q}\n")
                except Exception as e:
                    self.partial_result.emit(f"⚠️ Erreur lors de l'analyse de la question : {q}. Détails : {str(e)}\n")
                self.progress_update.emit(int((i + 1) / len(self.questions) * 100))
            self.result_ready.emit(important_info, context)
        except Exception as e:
            self.error_signal.emit(f"Une erreur s'est produite pendant l'analyse : {str(e)}")
    def stop(self):
        self._is_running = False
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AppelOffreApp()
    window.show()
    sys.exit(app.exec_())