import tkinter as tk
from tkinter import messagebox
import random
from gtts import gTTS
import os

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

class SpellingGameGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("The Hearing Spell")
        self.master.geometry("600x600")

        # Definindo o tamanho da fonte proporcionalmente
        default_font = ("Arial", 12)

        # Adicionando título do jogo
        self.title_label = tk.Label(master, text="The Hearing Spell", font=("Arial", 20))
        self.title_label.pack(pady=10)

        # Centralizando os elementos na tela
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        self.current_word = ""
        self.current_difficulty = "facil"
        self.score = 0
        self.completed_difficulties = 0

        # Dicionário de pontuações por dificuldade
        self.score_map = {"facil": 1, "medio": 2, "dificil": 3}

        self.difficulty_label = tk.Label(master, text="", font=default_font)
        self.difficulty_label.pack()

        self.answer_entry = tk.Entry(master, font=default_font)
        self.answer_entry.pack(pady=10)

        self.hint_button = tk.Button(master, text="Dica", command=self.show_hint, font=default_font)
        self.hint_button.pack(pady=5)

        self.submit_button = tk.Button(master, text="Enviar", command=self.check_answer, font=default_font)
        self.submit_button.pack(pady=5)

        self.score_label = tk.Label(master, text="Pontuação: 0", font=default_font)
        self.score_label.pack(pady=10)

        # Rótulo para exibir a dica
        self.hint_label = tk.Label(master, text="", font=default_font)
        self.hint_label.pack(pady=5)

        self.set_difficulty_label()
        self.next_word()

    def set_difficulty_label(self):
        if self.current_difficulty == "facil":
            self.difficulty_label.config(text="Nível de dificuldade: Fácil")
        elif self.current_difficulty == "medio":
            self.difficulty_label.config(text="Nível de dificuldade: Médio")
        else:
            self.difficulty_label.config(text="Nível de dificuldade: Difícil")

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
                messagebox.showinfo("Fim do Jogo", "Todas as dificuldades foram completadas. Sua pontuação final é: {}".format(self.score))
                self.master.destroy()
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
        os.system("start palavra.mp3")

    def check_answer(self):
        user_answer = self.answer_entry.get()
        correct_answer = self.current_word.lower()

        if user_answer.lower() == correct_answer:
            # Pontuação de acordo com a dificuldade
            self.score += self.score_map[self.current_difficulty]
            self.score_label.config(text="Pontuação: {}".format(self.score))
            self.next_word()
        else:
            messagebox.showinfo("Resposta Incorreta", "A palavra correta era: {}".format(self.current_word))
            self.answer_entry.delete(0, tk.END)

    def show_hint(self):
        # Exibe a dica na tela
        self.hint_label.config(text="A palavra tem {} letras.".format(len(self.current_word)))

def main():
    root = tk.Tk()
    app = SpellingGameGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()





