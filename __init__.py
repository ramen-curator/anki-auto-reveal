from aqt.reviewer import Reviewer
from aqt.qt import QTimer

# 延迟时间（毫秒）
DELAY_MS = 7000

# 保存原方法，防止无限递归
_original_show_question = Reviewer._showQuestion

def patched_show_question(self):
    result = _original_show_question(self)
    QTimer.singleShot(DELAY_MS, lambda: reveal_answer_if_safe(self))
    return result

def reveal_answer_if_safe(reviewer):
    if reviewer and reviewer.state == "question":
        reviewer._showAnswer()

Reviewer._showQuestion = patched_show_question
