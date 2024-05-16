# Para o programa compilar corretamente, instalar as bibliotecas pelo terminal com os comandos:
# pip install gtts
# pip install kivy

import random
import os
from kivy.core.audio import SoundLoader
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from gtts import gTTS

# Dicionários de palavras e suas ortografias corretas
palavras_facil = {
    "casa": "casa",
    "flor": "flor",
    "sol": "sol",
    "mesa": "mesa",
    "gato": "gato"
}

palavras_medio = {
    "relógio": "relógio",
    "jardim": "jardim",
    "livro": "livro",
    "avião": "avião",
    "sorriso": "sorriso"
}

palavras_dificil = {
    "espetacular": "espetacular",
    "simultaneamente": "simultaneamente",
    "exasperado": "exasperado",
    "incessante": "incessante",
    "consequência": "consequência"
}

class SpellingGameGUI(App):
    def __init__(self):
        super(SpellingGameGUI, self).__init__()
        self.current_word = ""
        self.current_difficulty = "facil"
        self.score = 0
        self.completed_difficulties = 0
        # Dicionário de pontuações por dificuldade
        self.score_map = {"facil": 1, "medio": 2, "dificil": 3}
        self.difficulty_label = Label(text="")
        self.set_difficulty_label()
        self.next_word()

    def set_difficulty_label(self):
        if self.current_difficulty == "facil":
            self.difficulty_text = "Nível de dificuldade: Fácil"
        elif self.current_difficulty == "medio":
            self.difficulty_text = "Nível de dificuldade: Médio"
        else:
            self.difficulty_text = "Nível de dificuldade: Difícil"

        self.difficulty_label.text = self.difficulty_text

    def play_audio(self):
        sound = SoundLoader.load("palavra.mp3")
        if sound:
            sound.play()

    def next_word(self):
        if self.current_difficulty == "facil":
            words = palavras_facil
        elif self.current_difficulty == "medio":
            words = palavras_medio
        else:
            words = palavras_dificil

        if not words:
            self.completed_difficulties += 1
            if self.completed_difficulties >= 3:  # Todas as dificuldades foram concluídas
                self.show_end_game_popup()
                return
            else:
                if self.current_difficulty == "facil":
                    self.current_difficulty = "medio"
                elif self.current_difficulty == "medio":
                    self.current_difficulty = "dificil"
                self.set_difficulty_label()
                self.next_word()
                return

        self.current_word, _ = random.choice(list(words.items()))
        del words[self.current_word]

        tts = gTTS(text=self.current_word, lang='pt')
        tts.save("palavra.mp3")

    def check_answer(self, user_answer):
        correct_answer = self.current_word.lower()

        if user_answer.lower() == correct_answer:
            # Pontuação de acordo com a dificuldade
            self.score += self.score_map[self.current_difficulty]
            self.score_label.text = f'Pontuação: {self.score}'
            self.next_word()
        else:
            self.show_wrong_answer_popup()

    def build(self):
        layout = GridLayout(cols=1)

        layout.add_widget(self.difficulty_label)

        self.answer_entry = TextInput(hint_text='Digite a palavra aqui')
        layout.add_widget(self.answer_entry)

        self.hint_button = Button(text='Dica')
        self.hint_button.bind(on_press=self.show_hint)
        layout.add_widget(self.hint_button)

        self.submit_button = Button(text='Enviar')
        self.submit_button.bind(on_press=lambda instance: self.check_answer(self.answer_entry.text))
        layout.add_widget(self.submit_button)

        self.score_label = Label(text=f'Pontuação: {self.score}')
        layout.add_widget(self.score_label)

        self.hint_label = Label()
        layout.add_widget(self.hint_label)

        self.audio_button = Button(text='Reproduzir Áudio')
        self.audio_button.bind(on_press=lambda instance: self.play_audio())
        layout.add_widget(self.audio_button)

        return layout

    def show_hint(self, instance):
        # Exibe a dica na tela
        self.hint_label.text = f'A palavra tem {len(self.current_word)} letras.'

    def show_wrong_answer_popup(self):
        popup = Popup(title='Resposta Incorreta',
                      content=Label(text=f'A palavra correta era: {self.current_word}'),
                      size_hint=(None, None), size=(400, 200))
        popup.open()

    def show_end_game_popup(self):
        popup = Popup(title='Fim do Jogo',
                      content=Label(text=f'Todas as dificuldades foram completadas.\nSua pontuação final é: {self.score}'),
                      size_hint=(None, None), size=(400, 200))
        popup.open()

if __name__ == '__main__':
    SpellingGameGUI().run()










