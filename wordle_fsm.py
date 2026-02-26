"""Console Wordle simulator driven by a finite state machine (FSM)."""

from __future__ import annotations

from enum import Enum, auto
import random


class GameState(Enum):
    """FSM states for a Wordle round."""

    WORD_ENTRY = auto()
    CONFIRM = auto()
    SCORE = auto()
    IS_WINNER = auto()
    REVIEW = auto()
    CONFIRM_AFTER_REVIEW = auto()
    DISPLAY = auto()


class Wordle:
    """Wordle game round managed by explicit FSM states."""

    def __init__(self, secret_word: str | None = None) -> None:
        words = ["apple", "brave", "chair", "droid", "eagle", "flame", "grape"]
        self.secret_word = (secret_word or random.choice(words)).lower()
        self.attempt_count = 0
        self.has_won = False
        self.attempts: list[str] = []
        self._current_guess = ""

    def PlayRound(self) -> None:
        """Run one round using a finite state machine."""

        state = GameState.WORD_ENTRY

        while True:
            if state == GameState.WORD_ENTRY:
                guess = input("Enter a 5-letter word: ").strip().lower()
                if len(guess) == 5 and guess.isalpha():
                    self._current_guess = guess
                    state = GameState.CONFIRM
                else:
                    print("Invalid input. Please enter exactly five letters.")

            elif state == GameState.CONFIRM:
                answer = input(f"Use '{self._current_guess}'? (y/n): ").strip().lower()
                if answer in ("y", "yes"):
                    state = GameState.SCORE
                elif answer in ("n", "no"):
                    state = GameState.WORD_ENTRY
                else:
                    print("Please answer with y or n.")

            elif state == GameState.SCORE:
                self.Score()
                state = GameState.IS_WINNER

            elif state == GameState.IS_WINNER:
                if self.IsWinner():
                    state = GameState.DISPLAY
                elif self.attempt_count >= 6:
                    state = GameState.DISPLAY
                else:
                    state = GameState.REVIEW

            elif state == GameState.REVIEW:
                self._display_review()
                state = GameState.CONFIRM_AFTER_REVIEW

            elif state == GameState.CONFIRM_AFTER_REVIEW:
                input("Press Enter to continue to the next guess...")
                state = GameState.WORD_ENTRY

            elif state == GameState.DISPLAY:
                self.Display()
                return

    def Score(self) -> None:
        """Store guess and update attempt count."""

        self.attempts.append(self._current_guess)
        self.attempt_count += 1

    def IsWinner(self) -> bool:
        """Update and return win status."""

        self.has_won = self._current_guess == self.secret_word
        return self.has_won

    def Display(self) -> None:
        """Show attempts and round result, then pause for Enter."""

        print("\n===== Round Summary =====")
        if self.attempts:
            for idx, guess in enumerate(self.attempts, start=1):
                print(f"Attempt {idx}: {guess}")
        else:
            print("No attempts were recorded.")

        print(f"Total attempts used: {self.attempt_count}/6")
        if self.has_won:
            print("You Won.")
        else:
            print("You Lost.")

        input("Press Enter to return to the main menu...")

    def _display_review(self) -> None:
        """Show clue information after an incorrect guess."""

        present_letters = sorted({ch for ch in self._current_guess if ch in self.secret_word})
        correctly_placed = [
            ch
            for idx, ch in enumerate(self._current_guess)
            if ch == self.secret_word[idx]
        ]

        present_str = ", ".join(present_letters) if present_letters else "None"
        correct_pos_str = ", ".join(correctly_placed) if correctly_placed else "None"

        print("\nReview:")
        print(f"Letters present in secret word: {present_str}")
        print(f"Letters correct and in right position: {correct_pos_str}\n")


def main() -> None:
    """Main menu loop."""

    while True:
        print("\n=== Wordle Menu ===")
        print("1) Play a round of Wordle")
        print("2) Leave")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            game = Wordle()
            game.PlayRound()
        elif choice == "2":
            print("Thanks for Playing and come back another time!")
            break
        else:
            print("Invalid menu option. Please choose 1 or 2.")


if __name__ == "__main__":
    main()
