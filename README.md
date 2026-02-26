# Wordle FSM Assignment

This project is a console-based Wordle simulator implemented in Python.
The round flow is controlled with a Finite State Machine (FSM) using `Enum` states (not booleans).

## Files
- `wordle_fsm.py` — main program

## How to run
```bash
python3 wordle_fsm.py
```

## What I tested (manual tests)
1. **Invalid word entry handling**
   - Entered words that were not exactly 5 letters (`abc`, `12345`, `abcdef`).
   - Verified game stayed in `WordEntryState` and requested input again.

2. **Confirm flow returns to entry**
   - Entered a valid 5-letter word, then answered `n` on confirmation.
   - Verified game returned to word entry and allowed replacing the guess.

3. **Round end on attempt limit**
   - Entered 6 incorrect guesses.
   - Verified transition to display summary and `You Lost.` result.

4. **Round end on win**
   - Tested with fixed secret word via direct class usage in Python REPL.
   - Verified correct guess sets `has_won=True` and summary displays `You Won.`.

## Notes
- `PlayRound()` contains FSM transitions:
  - `WordEntryState`
  - `ConfirmState`
  - `ScoreState`
  - `IsWinnerState`
  - `ReviewState`
  - `ConfirmStateAfterReview`
  - `DisplayState`
- The player has exactly 6 guesses.
