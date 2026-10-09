import customtkinter as ctk
import config
import messages
from game_logic import Game
from ui_components import VaultPanel, FeedbackPanel, Keypad, HistoryList, StackView

class VaultBreakerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("VaultBreaker")
        self.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")
        self.minsize(config.WINDOW_MIN_WIDTH, config.WINDOW_MIN_HEIGHT)
        self.configure(fg_color=config.BG_COLOR)
        ctk.set_appearance_mode("dark")

        self.game = Game(config.DEFAULT_CODE_LENGTH, config.DEFAULT_MAX_ATTEMPTS)
        self.current_input = ""
        
        self.setup_ui()
        
        self.bind("<Key>", self.handle_keypress)
        self.bind("<Return>", lambda e: self.submit_guess())
        self.bind("<BackSpace>", lambda e: self.handle_backspace())
        self.bind("<Delete>", lambda e: self.handle_backspace())
        self.bind("<Escape>", lambda e: self.clear_input())
        self.bind("<Control-z>", lambda e: self.undo_guess())
        self.bind("<Command-z>", lambda e: self.undo_guess())
        self._is_submitting = False

        self.start_game(config.DEFAULT_CODE_LENGTH, config.DEFAULT_MAX_ATTEMPTS)

    def start_game(self, length, attempts):
        self.game.restart(length, attempts)
        self.current_input = ""
        
        self.vault.setup_slots(length)
        self.vault.refresh(self.current_input, False, False, self.game.secret_code)
        
        for w in self.pips_frame.winfo_children():
            w.destroy()
        self.pips = []
        for i in range(attempts):
            pip = ctk.CTkLabel(self.pips_frame, text="●", font=(config.FONT_SANS, 16), text_color=config.CYAN)
            pip.pack(side="left", padx=3)
            self.pips.append(pip)
            
        self.history_title_lbl.configure(text=f"0 / {attempts} ATTEMPTS")
        
        self.refresh_all()

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0, minsize=340)
        self.grid_rowconfigure(0, weight=1)

        self.left_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.left_frame.grid_columnconfigure(0, weight=1)

        header = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        left_h = ctk.CTkFrame(header, fg_color="transparent")
        left_h.pack(side="left")
        ctk.CTkLabel(left_h, text="V A U L T  B R E A K E R", font=(config.FONT_SANS, 34, "bold"), text_color=config.CYAN).pack(anchor="w")
        ctk.CTkLabel(left_h, text="S E C U R I T Y   T E R M I N A L   0 1", font=(config.FONT_SANS, 10, "bold"), text_color=config.TEXT_MUTED).pack(anchor="w")
        
        right_h = ctk.CTkFrame(header, fg_color="transparent")
        right_h.pack(side="right")
        pill = ctk.CTkFrame(right_h, fg_color="#0A2416", border_color=config.GREEN, border_width=1, corner_radius=16)
        pill.pack(anchor="e", pady=2)
        ctk.CTkLabel(pill, text="● SYSTEM ONLINE", font=(config.FONT_SANS, 10, "bold"), text_color=config.GREEN).pack(padx=12, pady=4)
        
        mid = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        mid.grid(row=1, column=0, sticky="nsew", pady=10)
        mid.grid_columnconfigure(0, weight=1)
        mid.grid_columnconfigure(1, weight=1)

        self.vault = VaultPanel(mid)
        self.vault.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        bottom_mid = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        bottom_mid.grid(row=2, column=0, sticky="nsew", pady=10)
        bottom_mid.grid_columnconfigure(0, weight=1)
        bottom_mid.grid_columnconfigure(1, weight=1)
        
        self.keypad = Keypad(bottom_mid, self.handle_keypad)
        self.keypad.grid(row=0, column=0, sticky="nw")
        
        self.feedback = FeedbackPanel(bottom_mid)
        self.feedback.grid(row=0, column=1, sticky="ne", padx=(20, 0))

        self.btn_submit = ctk.CTkButton(self.left_frame, text="ENTER 4 DIGITS", font=(config.FONT_SANS, 20, "bold"), height=56,
                                        fg_color=config.PANEL_COLOR, text_color=config.TEXT_MUTED, hover_color=config.BORDER_GLOW,
                                        command=self.submit_guess)
        self.btn_submit.grid(row=3, column=0, sticky="ew", pady=(20, 10))

        att_cont = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        att_cont.grid(row=4, column=0)
        self.lbl_att_count = ctk.CTkLabel(att_cont, text="ATTEMPTS LEFT: 6", font=(config.FONT_SANS, 14, "bold"), text_color=config.TEXT_MAIN)
        self.lbl_att_count.pack(pady=5)
        self.pips_frame = ctk.CTkFrame(att_cont, fg_color="transparent")
        self.pips_frame.pack()
        self.pips = []

        self.right_frame = ctk.CTkFrame(self, fg_color=config.PANEL_COLOR, corner_radius=16, border_width=1, border_color=config.BORDER_GLOW)
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 20), pady=20)
        self.right_frame.grid_rowconfigure(2, weight=3)
        self.right_frame.grid_rowconfigure(4, weight=2)

        hist_h = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        hist_h.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 5))
        ctk.CTkLabel(hist_h, text="G U E S S  H I S T O R Y", font=(config.FONT_SANS, 14, "bold"), text_color=config.TEXT_MAIN).pack(side="left")
        self.history_title_lbl = ctk.CTkLabel(hist_h, text="0 / 6 ATTEMPTS", font=(config.FONT_SANS, 10, "bold"), text_color=config.TEXT_MUTED)
        self.history_title_lbl.pack(side="right")
        
        ctk.CTkLabel(self.right_frame, text="● right place  ○ wrong place", font=(config.FONT_SANS, 10), text_color=config.TEXT_MUTED).grid(row=1, column=0, sticky="w", padx=20)

        self.history_list = HistoryList(self.right_frame, config.DEFAULT_MAX_ATTEMPTS)
        self.history_list.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

        stack_h = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        stack_h.grid(row=3, column=0, sticky="ew", padx=20, pady=(10, 5))
        ctk.CTkLabel(stack_h, text="S T A C K  V I E W  ( U N D O )", font=(config.FONT_SANS, 14, "bold"), text_color=config.TEXT_MAIN).pack(side="left")
        ctk.CTkLabel(stack_h, text="ⓘ LIFO", font=(config.FONT_SANS, 14), text_color=config.TEXT_MUTED).pack(side="right")
        
        self.stack_view = StackView(self.right_frame)
        self.stack_view.grid(row=4, column=0, sticky="nsew", padx=10, pady=(0, 10))

        actions = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        actions.grid(row=5, column=0, sticky="ew", padx=20, pady=(10, 20))
        actions.grid_columnconfigure(0, weight=1)
        actions.grid_columnconfigure(1, weight=1)
        
        self.btn_undo = ctk.CTkButton(actions, text="⟲ UNDO", font=(config.FONT_SANS, 14, "bold"), height=44,
                                      fg_color="transparent", border_color=config.AMBER, border_width=1, text_color=config.AMBER,
                                      hover_color="#332500", command=self.undo_guess)
        self.btn_undo.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        
        self.btn_restart = ctk.CTkButton(actions, text="↻ RESTART", font=(config.FONT_SANS, 14, "bold"), height=44,
                                         fg_color="transparent", border_color=config.RED, border_width=1, text_color=config.RED,
                                         hover_color="#330F15", command=lambda: self.start_game(self.game.code_length, self.game.max_attempts))
        self.btn_restart.grid(row=0, column=1, sticky="ew", padx=(5, 0))

    def handle_keypad(self, key):
        if self.game.is_over:
            return
        if key == '⌫':
            self.handle_backspace()
        elif key == 'C' or key == 'CLEAR':
            self.clear_input()
        else:
            if len(self.current_input) < self.game.code_length and key not in self.current_input:
                self.current_input += key
                self.refresh_all()

    def handle_keypress(self, event):
        if self.game.is_over:
            return
        char = event.char
        if char.isdigit():
            if len(self.current_input) < self.game.code_length and char not in self.current_input:
                self.current_input += char
                self.refresh_all()

    def handle_backspace(self):
        if len(self.current_input) > 0:
            self.current_input = self.current_input[:-1]
            self.refresh_all()

    def clear_input(self):
        self.current_input = ""
        self.refresh_all()

    def submit_guess(self):
        if self.game.is_over or len(self.current_input) != self.game.code_length:
            return
            
        if getattr(self, "_is_submitting", False):
            return
        self._is_submitting = True
            
        try:
            res = self.game.make_guess(self.current_input)
            
            if res["valid"]:
                self.current_input = ""
                if res["won"]:
                    self.vault.animate_win()
                self.refresh_all()
            else:
                self.refresh_all()
                self.feedback.show_error(res["message"])
        finally:
            self._is_submitting = False

    def undo_guess(self):
        if self.game.guess_stack.is_empty():
            return
        self.current_input = ""
        res = self.game.undo()
        self.refresh_all()

    def refresh_all(self):
        h_all = self.game.history.get_all()
        s_all = self.game.guess_stack.to_list()
        last_entry = self.game.history.get_last()
        is_won = self.game.is_won
        is_lost = self.game.is_lost
        is_over = self.game.is_over
        c_len = self.game.code_length
        a_left = self.game.attempts_left

        self.vault.refresh(self.current_input, is_won, is_lost, self.game.secret_code)
        self.feedback.refresh(last_entry, c_len)
        self.keypad.refresh(self.current_input, h_all, is_over)
        self.history_list.refresh(h_all)
        self.history_title_lbl.configure(text=f"{len(h_all)} / {self.game.max_attempts} ATTEMPTS")
        self.stack_view.refresh(s_all)
        
        self.lbl_att_count.configure(text=f"ATTEMPTS LEFT: {a_left}")
        for i, pip in enumerate(self.pips):
            if i < a_left:
                color = config.CYAN if a_left > 1 or i < a_left - 1 else config.RED
                if a_left == 1 and i == 0:
                    color = config.RED
                else:
                    color = config.CYAN
                pip.configure(text_color=color)
            else:
                pip.configure(text_color=config.BORDER_GLOW)
                
        if is_over:
            self.btn_submit.configure(state="disabled", text="GAME OVER", fg_color=config.PANEL_COLOR, text_color=config.TEXT_MUTED)
            self.btn_undo.configure(state="disabled")
        else:
            if len(self.current_input) == c_len:
                self.btn_submit.configure(state="normal", text="SUBMIT GUESS", fg_color=config.CYAN, text_color="#000000")
            else:
                self.btn_submit.configure(state="disabled", text=f"ENTER {c_len} DIGITS", fg_color=config.PANEL_COLOR, text_color=config.TEXT_MUTED)
                
            if len(s_all) > 0:
                self.btn_undo.configure(state="normal")
            else:
                self.btn_undo.configure(state="disabled")

if __name__ == "__main__":
    app = VaultBreakerApp()
    app.mainloop()
