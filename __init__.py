import os
import json
from aqt import mw
from aqt.qt import QTimer, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton
from aqt.reviewer import Reviewer
from aqt.utils import showInfo
from aqt import gui_hooks

# Config path
def get_config_path():
    return os.path.join(mw.pm.profileFolder(), "auto_reveal", "config.json")

default_config = {
    "allowed_models": ["Your Note Type Here"],
    "allowed_decks": ["Your Deck Here"],
    "delay_seconds": 7
}

def load_config():
    path = get_config_path()
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return default_config.copy()

def save_config(config):
    path = get_config_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

# -- snip --
_config_cache = None

def get_config():
    global _config_cache
    if _config_cache is None:
        _config_cache = load_config()
    return _config_cache

# Auto-flip logic
LONGFORM_TAG = "longform"
_original_show_question = Reviewer._showQuestion

timer_ref = None  # store last timer so we can cancel it

def patched_show_question(self):
    global timer_ref  # track the current timer

    result = _original_show_question(self)

    model_name = self.card.note().model()["name"]
    deck_name = mw.col.decks.name(self.card.did)
    allowed_models = get_config().get("allowed_models", [])
    allowed_decks = get_config().get("allowed_decks", [])
    delay = get_config().get("delay_seconds", 7) * 1000  # convert to ms

    #  cancel previous timer
    if timer_ref is not None:
        timer_ref.stop()
        timer_ref.deleteLater()
        timer_ref = None

    if model_name not in allowed_models:
        return result
    if allowed_decks and deck_name not in allowed_decks:
        return result

    if LONGFORM_TAG in self.card.note().tags:
        delay = int(delay * 2)

    #  create a new one
    timer = QTimer()
    timer.setSingleShot(True)

    def flip_if_same_card():
        if self and self.state == "question":
            self._showAnswer()

    timer.timeout.connect(flip_if_same_card)
    timer.start(delay)
    timer_ref = timer  # track this timer

    return result

def reveal_answer_if_safe(reviewer):
    if reviewer and reviewer.state == "question":
        reviewer._showAnswer()

Reviewer._showQuestion = patched_show_question

# Settings window
class SettingsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Auto Reveal Settings")
        self.setMinimumWidth(400)

        layout = QVBoxLayout()

        self.label_models = QLabel("Allowed note types (comma-separated):")
        layout.addWidget(self.label_models)

        self.input_models = QLineEdit()
        self.input_models.setText(", ".join(get_config().get("allowed_models", [])))
        layout.addWidget(self.input_models)

        self.label_deck = QLabel("Allowed deck names (comma-separated):")
        layout.addWidget(self.label_deck)

        self.input_deck = QLineEdit()
        self.input_deck.setText(", ".join(get_config().get("allowed_decks", [])))
        layout.addWidget(self.input_deck)

        self.label_delay = QLabel("Auto reveal delay (seconds):")
        layout.addWidget(self.label_delay)

        self.input_delay = QLineEdit()
        self.input_delay.setText(str(get_config().get("delay_seconds", 7)))
        layout.addWidget(self.input_delay)

        self.save_button = QPushButton("Save Settings")
        self.save_button.clicked.connect(self.save)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def save(self):
        models = [m.strip() for m in self.input_models.text().split(",") if m.strip()]
        decks = [d.strip() for d in self.input_deck.text().split(",") if d.strip()]
        try:
            delay = max(1, int(float(self.input_delay.text().strip())))
        except:
            delay = 7

        config = get_config()
        config["allowed_models"] = models
        config["allowed_decks"] = decks
        config["delay_seconds"] = delay

        save_config(config)
        showInfo("Settings saved. Restart Anki to apply changes.")
        self.close()

def open_settings():
    dialog = SettingsDialog()
    dialog.exec()

action = mw.form.menuTools.addAction("Auto Reveal (Timer) Settings")
action.triggered.connect(open_settings)
