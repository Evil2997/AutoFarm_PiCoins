import pyautogui as pg
from pytesseract import pytesseract


def check_consent_on_screen() -> bool:
    screenshot = pg.screenshot()
    recognized_text = pytesseract.image_to_string(screenshot, lang='eng')
    required_phrases = [
        "I consent to allow Pi Network to collect and process certain personal information",
        "I consent to Pi Network transferring my personal data from the EU/EEA to the U.S. or Canada",
        "consent to Pi Network transferring my pet ata from the",
        "DC EU/EEA to the U.S. or Canada, where its s and its service",
        "providers are based, Learn More",
    ]
    for phrase in required_phrases:
        if phrase in recognized_text:
            return True

    return False
