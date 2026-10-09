import unittest
from test_logic import TestAppIntegration

class TestDebug(TestAppIntegration):
    def test_submission_and_undo(self):
        self.app.handle_keypad('1')
        self.app.handle_keypad('2')
        print("Before incomplete submit. is_submitting:", getattr(self.app, '_is_submitting', False))
        self.app.submit_guess()
        print("After incomplete:", self.app.game.guess_stack.size())
        
        self.app.clear_input()
        for key in ['5', '6', '7', '8']:
            self.app.handle_keypad(key)
        print("Current input before valid submit:", self.app.current_input)
        print("is_submitting before valid submit:", getattr(self.app, '_is_submitting', False))
        self.app.submit_guess()
        print("Stack size:", self.app.game.guess_stack.size())
        print("is_submitting after valid submit:", getattr(self.app, '_is_submitting', False))

if __name__ == '__main__':
    unittest.main()
