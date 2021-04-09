from .libs import ai
_ai=ai.Ai()

def Synthesis(say,save_file="SpeechSynthesis.mp3"):
    return _ai.SpeechSynthesis(say,save_file)
