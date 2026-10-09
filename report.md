# Diagnostic Report

1. **Bug:** Sometimes the application stops responding / UI is inconsistent.
   **Responsible:** `main.py` -> `submit_guess`, `handle_keypad`, `handle_backspace`
   **Root Cause:** Redundant `refresh_all()` calls after Backspace could cause flickering/double event processing. Submitting an invalid guess silently clears `current_input` without showing the error on screen, causing confusion on why input vanished.
   **Proposed Fix:** Prevent multiple `refresh_all()` calls. If `res["valid"]` is False, do NOT clear `current_input`. Instead, display `res["message"]` on the UI.

2. **Bug:** The delete/backspace keypad button does not reliably remove the last entered digit.
   **Responsible:** `main.py` -> `handle_backspace`
   **Root Cause:** There is an inconsistent binding (`<BackSpace>`) which may not capture physical delete keys correctly across OS platforms, and the `refresh_all()` is fired repeatedly. 
   **Proposed Fix:** Consolidate UI updates to happen exactly once. Ensure the callback strictly slices the string once. Bind both `<BackSpace>` and `<Delete>` to cover cross-platform behavior.

3. **Bug:** Keypad input, displayed code slots, and submitted guesses can become inconsistent.
   **Responsible:** `main.py` -> `undo_guess` and `start_game`
   **Root Cause:** `undo_guess` restores game state but does NOT clear `current_input`, leaving stale digits on the display while the underlying game attempts reset.
   **Proposed Fix:** Add `self.current_input = ""` inside `undo_guess()`. Ensure `restart()` also correctly resets all UI components.

4. **Bug:** Undo and Restart may leave stale or inconsistent game state.
   **Responsible:** `game_logic.py` -> `undo` and `main.py` -> `undo_guess`
   **Root Cause:** The `Undo` flow fails to reset the unsubmitted digits correctly. The Restart action generates a new code but might leave previous UI visual statuses if not perfectly refreshed.
   **Proposed Fix:** Synchronize `current_input` erasure with `undo_guess` and `restart`. 

5. **Bug:** Duplicate submission from a single click.
   **Responsible:** `main.py` -> `submit_guess`
   **Root Cause:** Rapid Enter presses could theoretically bypass the `if` check before the first `refresh_all()` completes.
   **Proposed Fix:** Add an internal lock or clear `current_input` temporarily before processing.
