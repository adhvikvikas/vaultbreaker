import unittest
from dsa import Stack, GuessHistory
from game_logic import Game

class TestDSA(unittest.TestCase):
    def test_stack_operations(self):
        s = Stack()
        s.push(1)
        s.push(2)
        self.assertEqual(s.size(), 2)
        self.assertEqual(s.pop(), 2)
        self.assertEqual(s.size(), 1)
        self.assertEqual(s.peek(), 1)
        self.assertFalse(s.is_empty())
        s.clear()
        self.assertTrue(s.is_empty())

    def test_history_operations(self):
        h = GuessHistory()
        h.add({"guess": "1234"})
        h.add({"guess": "5678"})
        self.assertEqual(h.size(), 2)
        self.assertEqual(h.get_last()["guess"], "5678")
        self.assertEqual(h.get_previous()["guess"], "1234")
        h.remove_last()
        self.assertEqual(h.size(), 1)

class TestGameLogic(unittest.TestCase):
    def test_game_flow_and_feedback(self):
        g = Game(code_length=4, secret_code="1234")
        self.assertEqual(g.attempts_left, 6)
        
        # 1. FIRST GUESS (0 positions matched)
        res1 = g.make_guess("5678")
        self.assertEqual(res1["entry"]["trend"], "INCORRECT")
        self.assertEqual(res1["entry"]["score"], 0)
        self.assertEqual(g.guess_stack.size(), 1)
        
        # 2. WARMER (1 position matched, score increased)
        res2 = g.make_guess("1975") # '1' is correct
        self.assertEqual(res2["entry"]["trend"], "WARMER")
        self.assertEqual(res2["entry"]["score"], 1)
        
        # 3. SAME (1 position matched, score unchanged)
        res3 = g.make_guess("1098") # '1' is correct
        self.assertEqual(res3["entry"]["trend"], "SAME")
        self.assertEqual(res3["entry"]["score"], 1)
        
        # 4. COLDER (0 positions matched, score decreased)
        res4 = g.make_guess("9876")
        self.assertEqual(res4["entry"]["trend"], "COLDER")
        self.assertEqual(res4["entry"]["score"], 0)
        
        # Undo tests
        self.assertEqual(g.guess_stack.size(), 4)
        popped = g.undo()
        self.assertEqual(popped, "9876")
        self.assertEqual(g.guess_stack.size(), 3)
        self.assertEqual(g.history.size(), 3)
        
        # 5. CORRECT (vault unlocked)
        res_win = g.make_guess("1234")
        self.assertEqual(res_win["entry"]["trend"], "CORRECT")
        self.assertEqual(res_win["entry"]["score"], 4)
        self.assertTrue(g.is_won)

    def test_restart(self):
        g = Game(code_length=4, secret_code="1234")
        g.make_guess("5678")
        g.restart(secret_code="9999")
        self.assertEqual(g.guess_stack.size(), 0)
        self.assertEqual(g.history.size(), 0)
        self.assertEqual(g.secret_code, "9999")

class TestAppIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from main import VaultBreakerApp
        cls.app = VaultBreakerApp()
        cls.app.update() # init widgets
        
    def setUp(self):
        self.app.start_game(4, 6)
        self.app.game.secret_code = "1234"

    def test_scenario_1_backspace(self):
        # 1. Enter 1234, press Backspace, and verify that the display becomes 123.
        for key in ['1', '2', '3', '4']:
            self.app.handle_keypad(key)
        self.app.handle_backspace()
        self.assertEqual(self.app.current_input, "123")

    def test_scenario_2_clear(self):
        # 2. Enter a digit, press Clear, and verify that all four slots become empty.
        self.app.handle_keypad('7')
        self.app.clear_input()
        self.assertEqual(self.app.current_input, "")

    def test_scenario_3_incomplete_submit(self):
        # 3. Enter fewer than four digits and submit. Verify error, input preserved, no attempt consumed.
        self.app.handle_keypad('1')
        self.app.handle_keypad('2')
        self.app.submit_guess()
        self.assertEqual(self.app.current_input, "12") # Preserved
        self.assertEqual(self.app.game.attempts_left, 6) # No attempt consumed

    def test_scenario_4_and_5_submit_valid(self):
        # 5. Enter four digits, delete the last digit, enter a replacement, and submit.
        for key in ['5', '6', '7', '8']:
            self.app.handle_keypad(key)
        self.app.handle_backspace()
        self.app.handle_keypad('9')
        
        # 4. Submit once, verify that the attempt counter, Guess History, Stack View update exactly once.
        self.app.submit_guess()
        self.assertEqual(self.app.game.guess_stack.size(), 1)
        self.assertEqual(self.app.game.history.size(), 1)
        self.assertEqual(self.app.game.attempts_left, 5)
        self.assertEqual(self.app.game.guess_stack.peek(), "5679")

    def test_scenario_6_undo(self):
        # 6. Press Undo after a valid guess.
        self.app.handle_keypad('5')
        self.app.handle_keypad('6')
        self.app.handle_keypad('7')
        self.app.handle_keypad('8')
        self.app.submit_guess()
        self.assertEqual(self.app.game.attempts_left, 5)
        
        self.app.undo_guess()
        self.assertEqual(self.app.game.guess_stack.size(), 0)
        self.assertEqual(self.app.game.history.size(), 0)
        self.assertEqual(self.app.game.attempts_left, 6)
        self.assertEqual(self.app.current_input, "") # No stale digits

    def test_scenario_7_restart(self):
        # 7. Restart the game after several guesses.
        self.app.handle_keypad('5')
        self.app.handle_keypad('6')
        self.app.handle_keypad('7')
        self.app.handle_keypad('8')
        self.app.submit_guess()
        
        self.app.start_game(4, 6) # Restart
        self.assertEqual(self.app.current_input, "")
        self.assertEqual(self.app.game.guess_stack.size(), 0)
        self.assertEqual(self.app.game.attempts_left, 6)
        self.assertFalse(self.app.game.is_over)

    def test_scenario_8_win_and_loss(self):
        # 8. Test winning and losing. Vault animation doesn't crash. Input blocked. Restart works.
        
        # Test WIN
        self.app.handle_keypad('1')
        self.app.handle_keypad('2')
        self.app.handle_keypad('3')
        self.app.handle_keypad('4')
        self.app.submit_guess() # Winner
        self.assertTrue(self.app.game.is_won)
        self.assertEqual(self.app.current_input, "") # Cleared on win
        
        # Input blocked after end
        self.app.handle_keypad('5')
        self.assertEqual(self.app.current_input, "")
        
        # Restart works
        self.app.start_game(4, 6)
        self.assertFalse(self.app.game.is_won)
        
        # Test LOSS
        self.app.game.secret_code = "1234"
        valid_incorrect_guesses = ["5678", "5679", "5689", "5789", "6789", "0567"]
        for guess in valid_incorrect_guesses:
            for k in guess:
                self.app.handle_keypad(k)
            self.app.submit_guess()
            
        self.assertTrue(self.app.game.is_lost)
        # Input blocked
        self.app.handle_keypad('9')
        self.assertEqual(self.app.current_input, "")
        
    def test_scenario_9_rapid_submit(self):
        # 9. Test rapid Submit clicks and repeated Enter presses.
        self.app.handle_keypad('5')
        self.app.handle_keypad('6')
        self.app.handle_keypad('7')
        self.app.handle_keypad('8')
        
        # Simulate rapid calls
        self.app.submit_guess()
        self.app.submit_guess()
        self.app.submit_guess()
        
        # Should only be processed once
        self.assertEqual(self.app.game.guess_stack.size(), 1)
        self.assertEqual(self.app.game.attempts_left, 5)

if __name__ == '__main__':
    unittest.main()
