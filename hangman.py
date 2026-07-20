import random
import sys
import argparse
from typing import List, Set


VOWELS = {"A", "E", "I", "O", "U"}

# Bu fonksiyon verilen dosya yolundan kelimeleri yukluyor.
# icindeki kelimeleri satir satir okuyup, sadece harflerden olusan
# ve en az 5 harfli olanlari listeye ekler.
def load_words(path: str) -> List[str]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        print(f"File error: Cannot read '{path}': {e}")
        sys.exit(2)

    words = []
    for line in lines:
        word = line.strip()
        # Sadece alfabetik ve minimum uzunluk kontrolu:
        if word.isalpha():
            word = word.upper()
            if len(word) >= 5:
                words.append(word)

    # Dosyada hic uygun kelime yoksa hata mesaji verir.
    if not words:
        print("File error: words.txt must contain valid alphabetic words (min length 5).")
        sys.exit(2)

    return words

# Bu fonksiyon ekranda gorunen adam cizimini can sayisi dustukce degiştirir.
def display_hangman(lives: int, initial_lives: int) -> None:
    stages = [
        r"""
 +---+
 |   |
     |
     |
     |
     |
=========
""",
        r"""
 +---+
 |   |
 O   |
     |
     |
     |
=========
""",
        r"""
 +---+
 |   |
 O   |
 |   |
     |
     |
=========
""",
        r"""
 +---+
 |   |
 O   |
/|   |
     |
     |
=========
""",
        r"""
 +---+
 |   |
 O   |
/|\  |
     |
     |
=========
""",
        r"""
 +---+
 |   |
 O   |
/|\  |
/    |
     |
=========
""",
        r"""
 +---+
 |   |
 O   |
/|\  |
/ \  |
     |
=========
"""
    ]

    # Burada kac can kaybettigini bulup ona gore hangi şeklin gosterilecegini secer.
    lost_lives = initial_lives - lives
    if lost_lives < 0:
        lost_lives = 0

    # sekil sayisindan fazla asamaya cikilmasin diye sinir koyulmustur.
    max_stage = min(initial_lives, len(stages) - 1)
    if lost_lives > max_stage:
        lost_lives = max_stage

    print(stages[lost_lives])

# Bu fonksiyon dogru bilinen harfleri gosterip, bilinmeyenleri "_" olarak yazar.
def render_word(secret: str, guessed: Set[str]) -> str:
    return " ".join([c.lower() if c in guessed else "_" for c in secret])

# Burada oyunun o anki durumunu ekrana yazdirir
# kelime, can sayısı, tahmin edilen harfler ve adam çizimi
def display_state(secret: str, guessed: Set[str], lives: int, initial_lives: int):
    print(f"Word: {render_word(secret, guessed)}")
    print(f"Lives: {lives}")
    print(f"Guessed: {', '.join(sorted(guessed)) if guessed else '-'}")
    display_hangman(lives, initial_lives)

# Tum harfler acildi mi diye kontrol eden basit bir fonksiyon
def all_revealed(secret: str, guessed: Set[str]) -> bool:
    return set(secret).issubset(guessed)

# Kullanici '?' girerse ipucu verir,
# Kelimedeki ilk acilmamis harfi gosterir ve bir can eksiltir.
def handle_hint(secret: str, guessed: Set[str], lives: int):
    for ch in secret:
        if ch not in guessed:
            guessed.add(ch)
            lives -= 1
            print(f"[HINT] Revealed: {ch.lower()} (-1 life)")
            return guessed, lives

    print("[HINT] No hidden letters left.")
    return guessed, lives

# Oyun dongusu baslatilir.
# Kullanicidan harf aliniyor, kontroller yapiliyor,
# can sayisi azaliyor veya kazanip kaybetme durumu burada belirleniyor.
def play_game(secret: str, lives: int = 6, mode: str = "classic", hint_on: bool = True, initial_lives: int = None):
    guessed = set()
    if initial_lives is None:
        initial_lives = lives

    while True:
        # her turda ekrani gunceller.
        display_state(secret, guessed, lives, initial_lives)

        # tum harfler acildiysa oyuncu kazanmiş oluyor
        if all_revealed(secret, guessed):
            print(f"Congratulations! Word: {secret}")
            sys.exit(0)

        try:
            user_input = input("> Enter a letter: ").strip()
        except EOFError:
            print("\nGame ended. Word:", secret)
            sys.exit(0)

        if not user_input:
            print("Invalid input: enter a letter.")
            continue

        # Kullanici '?' girerse ipucu istedigini belirtmis olur.
        if user_input == "?":
            if not hint_on:
                print("Hint is disabled.")
                continue
            guessed, lives = handle_hint(secret, guessed, lives)
            if lives <= 0:
                display_state(secret, guessed, lives, initial_lives)
                print("Game over. Word:", secret)
                sys.exit(0)
            continue

        # Kullanici sadece bir harf girmelidir.
        if len(user_input) != 1 or not user_input.isalpha():
            print("Invalid input: enter a single A-Z letter.")
            continue

        letter = user_input.upper()

        # Ayni harf tekrar tahmin edilirse uyarı verir.
        if letter in guessed:
            print("Warning: letter already guessed.")
            continue

        guessed.add(letter)

        # Harf yanlissa can azalir
        if letter not in secret:
            if mode == "classic":
                lives -= 1
            else:
                # hard mod hem normal can azaltiyor hem de sesli harfse ekstra azaltiyor
                lives -= 1
                if letter in VOWELS:
                    lives -= 1

            # can kalmadiysa oyun bitiyor
            if lives <= 0:
                display_state(secret, guessed, lives, initial_lives)
                print("Game over. Word:", secret)
                sys.exit(0)

        # dogru tahminle tum harfler acildiysa tekrar kontrol edilir
        if all_revealed(secret, guessed):
            display_state(secret, guessed, lives, initial_lives)
            print(f"Congratulations! Word: {secret}")
            sys.exit(0)

# Bu kisim komut satirindan alinan parametreleri isler.
def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--words", required=True)
    parser.add_argument("--lives", type=int, default=6)
    parser.add_argument("--mode", choices=["classic", "hard"], default="classic")
    parser.add_argument("--seed", type=str, default=None)
    parser.add_argument("--hint", choices=["on", "off"], default="off")

    args = parser.parse_args()

    # Can sayisi 3 ile 10 arasinda olmak zorunda olacak sekilde ayarlanmistir.
    if not (3 <= args.lives <= 10):
        print("Error: --lives must be between 3 and 10.")
        sys.exit(2)

    # kelime dosyasını yukler.
    words = load_words(args.words)

    # seed verilmisse ayni kelimeyi uretmeli, verilmemisse rastgele uretir
    rng = random.Random(args.seed)
    secret = rng.choice(words)
    # hint on verilirse ipucu verilir , verilmezse yani hint off verilirse ipucu gosterilmez .
    hint_on = (args.hint == "on")

    # oyunu baslatir.
    play_game(secret, args.lives, args.mode, hint_on, args.lives)

if __name__ == "__main__":
    main()
