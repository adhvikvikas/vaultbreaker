import customtkinter as ctk
import tkinter as tk
import math
import config

class VaultPanel(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=config.PANEL_COLOR, corner_radius=16, border_width=1, border_color=config.BORDER_GLOW)
        
        self.canvas_size = 320
        self.canvas = tk.Canvas(self, width=self.canvas_size, height=self.canvas_size, bg=config.PANEL_COLOR, highlightthickness=0)
        self.canvas.pack(side="left", padx=20, pady=20)
        
        self.right_container = ctk.CTkFrame(self, fg_color="transparent")
        self.right_container.pack(side="left", fill="both", expand=True, padx=20)
        
        self.slots_frame = ctk.CTkFrame(self.right_container, fg_color="transparent")
        self.slots_frame.pack(expand=True, pady=(20, 0))
        
        self.status_lbl = ctk.CTkLabel(self.right_container, text="🔒 LOCKED", font=(config.FONT_SANS, 16, "bold"), text_color=config.AMBER)
        self.status_lbl.pack(pady=(10, 20))
        
        self.slots = []
        self.slot_labels = []
        self.dial_lines_angles = [0, 45, 90, 135, 180, 225, 270, 315]
        self.draw_vault()

    def draw_vault(self):
        self.canvas.delete("all")
        cx, cy = self.canvas_size//2, self.canvas_size//2
        
        radius = 140
        self.canvas.create_oval(cx-radius, cy-radius, cx+radius, cy+radius, outline="#1A2436", width=2, fill="#121824")
        self.canvas.create_oval(cx-radius+10, cy-radius+10, cx+radius-10, cy+radius-10, outline="#2A3B56", width=4, fill="#182236")
        
        self.ring = self.canvas.create_oval(cx-100, cy-100, cx+100, cy+100, outline=config.CYAN, width=4)
        
        for i in range(8):
            angle = math.radians(i * 45 + 22.5)
            bx = cx + 125 * math.cos(angle)
            by = cy + 125 * math.sin(angle)
            self.canvas.create_oval(bx-4, by-4, bx+4, by+4, fill="#506080", outline="")
            
        self.canvas.create_oval(cx-60, cy-60, cx+60, cy+60, fill="#1E293B", outline="#2F3E5A", width=2)
        self.canvas.create_oval(cx-20, cy-20, cx+20, cy+20, fill="#2F3E5A", outline="")
        self.draw_dial(0)

    def draw_dial(self, angle_offset):
        if hasattr(self, 'ring'):
            self.canvas.delete("dial_line")
            cx, cy = self.canvas_size//2, self.canvas_size//2
            for a in self.dial_lines_angles:
                angle = math.radians(a + angle_offset)
                lx1 = cx + 25 * math.cos(angle)
                ly1 = cy + 25 * math.sin(angle)
                lx2 = cx + 55 * math.cos(angle)
                ly2 = cy + 55 * math.sin(angle)
                self.canvas.create_line(lx1, ly1, lx2, ly2, fill="#7B8BA8", width=2, tags="dial_line")

    def animate_win(self, step=0):
        if step > 10:
            return
        self.draw_dial(step * 9)
        self.after(40, lambda: self.animate_win(step+1))

    def setup_slots(self, code_length):
        for w in self.slots_frame.winfo_children():
            w.destroy()
        self.slots = []
        self.slot_labels = []
        
        for i in range(code_length):
            box = ctk.CTkFrame(self.slots_frame, width=64, height=80, corner_radius=10, border_width=2, border_color=config.BORDER_GLOW, fg_color=config.DARK_BLUE)
            box.pack(side="left", padx=5)
            box.pack_propagate(False)
            
            lbl = ctk.CTkLabel(box, text="_", font=(config.FONT_MONO, 40, "bold"), text_color=config.TEXT_MUTED)
            lbl.place(relx=0.5, rely=0.5, anchor="center")
            
            self.slots.append(box)
            self.slot_labels.append(lbl)

    def refresh(self, current_input, is_won, is_lost, secret_code):
        code_length = len(self.slots)
        
        if is_lost:
            for i in range(code_length):
                self.slot_labels[i].configure(text=secret_code[i], text_color=config.RED)
                self.slots[i].configure(border_color=config.RED)
            if hasattr(self, 'ring'):
                self.canvas.itemconfig(self.ring, outline=config.RED)
            self.status_lbl.configure(text="🔒 LOCKED", text_color=config.RED)
        elif is_won:
            for i in range(code_length):
                char = current_input[i] if i < len(current_input) else secret_code[i]
                self.slot_labels[i].configure(text=char, text_color=config.GREEN)
                self.slots[i].configure(border_color=config.GREEN)
            if hasattr(self, 'ring'):
                self.canvas.itemconfig(self.ring, outline=config.GREEN)
            self.status_lbl.configure(text="🔓 UNLOCKED", text_color=config.GREEN)
        else:
            if hasattr(self, 'ring'):
                self.canvas.itemconfig(self.ring, outline=config.CYAN)
            self.status_lbl.configure(text="🔒 LOCKED", text_color=config.AMBER)
            
            for i in range(code_length):
                if i < len(current_input):
                    self.slot_labels[i].configure(text=current_input[i], text_color=config.TEXT_MAIN)
                    self.slots[i].configure(border_color=config.CYAN)
                else:
                    self.slot_labels[i].configure(text="_", text_color=config.TEXT_MUTED)
                    self.slots[i].configure(border_color=config.BORDER_GLOW)
                    
            if len(current_input) < code_length and not is_won and not is_lost:
                self.slots[len(current_input)].configure(border_color=config.CYAN)


class FeedbackPanel(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=config.PANEL_COLOR, corner_radius=16, border_width=1, border_color=config.BORDER_GLOW)
        
        ctk.CTkLabel(self, text="LAST GUESS FEEDBACK", font=(config.FONT_SANS, 11, "bold"), text_color=config.TEXT_MUTED).pack(anchor="w", padx=20, pady=(15, 5))
        
        self.tiles_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.tiles_frame.pack(pady=5)
        
        self.tiles = []
        
        # New feedback panel layout
        self.status_lbl = ctk.CTkLabel(self, text="", font=(config.FONT_SANS, 16, "bold"))
        self.status_lbl.pack(pady=(15, 5))
        
        self.score_lbl = ctk.CTkLabel(self, text="", font=(config.FONT_SANS, 14, "bold"), text_color=config.TEXT_MAIN)
        self.score_lbl.pack(pady=(0, 5))
        
        self.summary_lbl = ctk.CTkLabel(self, text="Awaiting your first guess", font=(config.FONT_SANS, 12), text_color=config.TEXT_MUTED)
        self.summary_lbl.pack(pady=(0, 15))

    def refresh(self, entry, code_length):
        for w in self.tiles_frame.winfo_children():
            w.destroy()
        self.tiles = []
        
        if not entry:
            for _ in range(code_length):
                lbl = ctk.CTkLabel(self.tiles_frame, text="_", font=(config.FONT_MONO, 24, "bold"), width=44, height=54, corner_radius=8, fg_color=config.DARK_BLUE, text_color=config.TEXT_MUTED)
                lbl.pack(side="left", padx=4)
            self.status_lbl.configure(text="")
            self.score_lbl.configure(text="")
            self.summary_lbl.configure(text="Awaiting your first guess", text_color=config.TEXT_MUTED)
            return

        guess = entry["guess"]
        statuses = entry["statuses"]
        
        for i in range(len(guess)):
            color = config.GREEN if statuses[i] == "correct" else (config.AMBER if statuses[i] == "misplaced" else config.BORDER_GLOW)
            text_color = "#000000" if statuses[i] != "absent" else config.TEXT_MUTED
            border = color if statuses[i] != "absent" else config.BORDER_GLOW
            
            lbl = ctk.CTkLabel(self.tiles_frame, text=guess[i], font=(config.FONT_MONO, 24, "bold"), width=44, height=54, corner_radius=8, 
                               fg_color=color if statuses[i] != "absent" else config.DARK_BLUE, 
                               text_color=text_color, border_width=1 if statuses[i]=="absent" else 0, border_color=border)
            lbl.pack(side="left", padx=4)
            
        trend = entry["trend"]
        t_text = ""
        t_color = config.TEXT_MUTED
        msg = ""
        
        if trend == "CORRECT":
            t_text = "CORRECT — VAULT UNLOCKED"
            t_color = config.GREEN
            msg = "You have successfully bypassed the security."
        elif trend == "WARMER":
            t_text = "CLOSE — GETTING WARMER"
            t_color = config.AMBER
            msg = "You're getting closer to the vault code!"
        elif trend == "COLDER":
            t_text = "COLDER — MOVING AWAY"
            t_color = config.RED
            msg = "Your guess is less accurate than the last."
        elif trend == "SAME":
            t_text = "NO CHANGE — TRY AGAIN"
            t_color = config.CYAN
            msg = "Closeness score remains the same."
        elif trend == "INCORRECT":
            t_text = "INCORRECT — FIRST GUESS"
            t_color = config.RED
            msg = "First attempt logged. Keep trying!"
            
        self.status_lbl.configure(text=t_text, text_color=t_color)
        self.score_lbl.configure(text=f"{entry['score']}/{code_length} positions matched")
        self.summary_lbl.configure(text=msg)

    def show_error(self, message):
        self.status_lbl.configure(text="INVALID INPUT", text_color=config.AMBER)
        self.score_lbl.configure(text="")
        self.summary_lbl.configure(text=message, text_color=config.AMBER)


class Keypad(ctk.CTkFrame):
    def __init__(self, master, callback):
        super().__init__(master, fg_color="transparent")
        self.callback = callback
        self.buttons = {}
        
        keys = [
            ('1', '2', '3'),
            ('4', '5', '6'),
            ('7', '8', '9'),
            ('⌫', '0', 'C')
        ]
        
        for r, row in enumerate(keys):
            for c, key in enumerate(row):
                btn = ctk.CTkButton(self, text=key, font=(config.FONT_SANS, 22, "bold"), width=120, height=54, corner_radius=10,
                                    fg_color=config.DARK_BLUE, hover_color=config.BORDER_GLOW, text_color=config.TEXT_MAIN,
                                    border_color=config.CYAN, border_width=1,
                                    command=lambda k=key: self.callback(k))
                btn.grid(row=r, column=c, padx=6, pady=6)
                self.buttons[key] = btn

    def refresh(self, current_input, history_entries, is_over):
        absent_digits = set()
        for entry in history_entries:
            for i, st in enumerate(entry["statuses"]):
                if st == "absent":
                    absent_digits.add(entry["guess"][i])
                    
        for key, btn in self.buttons.items():
            if is_over:
                btn.configure(state="disabled", border_width=1, border_color=config.BORDER_GLOW, fg_color=config.DARK_BLUE)
            else:
                if key.isdigit() and key in current_input:
                    btn.configure(state="disabled", border_width=1, border_color=config.BORDER_GLOW, fg_color=config.BG_COLOR, text_color=config.TEXT_MUTED)
                elif key.isdigit() and key in absent_digits:
                    btn.configure(state="normal", border_width=1, border_color=config.BORDER_GLOW, fg_color=config.DARK_BLUE, text_color=config.BORDER_GLOW)
                else:
                    btn.configure(state="normal", border_width=1, border_color=config.CYAN, fg_color=config.DARK_BLUE, text_color=config.TEXT_MAIN)


class HistoryList(ctk.CTkScrollableFrame):
    def __init__(self, master, max_attempts):
        super().__init__(master, fg_color="transparent", corner_radius=0)
        self.max_attempts = max_attempts

    def refresh(self, history):
        for w in self.winfo_children():
            w.destroy()
            
        if not history:
            ctk.CTkLabel(self, text="Recent attempts appear here", font=(config.FONT_SANS, 12), text_color=config.TEXT_MUTED).pack(pady=20)
            return
            
        for idx, entry in enumerate(reversed(history)):
            attempt_num = len(history) - idx
            is_latest = (idx == 0)
            
            border = config.CYAN if is_latest else config.BORDER_GLOW
            card = ctk.CTkFrame(self, fg_color=config.DARK_BLUE, border_color=border, border_width=1, corner_radius=12)
            card.pack(fill="x", pady=6)
            
            top_row = ctk.CTkFrame(card, fg_color="transparent")
            top_row.pack(fill="x", padx=12, pady=(12, 5))
            
            ctk.CTkLabel(top_row, text=f"#{attempt_num}", font=(config.FONT_SANS, 12), text_color=config.TEXT_MUTED, width=20).pack(side="left")
            
            guess_lbl = ctk.CTkLabel(top_row, text="  ".join(entry["guess"]), font=(config.FONT_MONO, 18, "bold"), text_color=config.TEXT_MAIN)
            guess_lbl.pack(side="left", padx=10)
            
            pegs_frame = ctk.CTkFrame(top_row, fg_color="transparent")
            pegs_frame.pack(side="right")
            
            for st in entry["statuses"]:
                color = config.GREEN if st == "correct" else (config.AMBER if st == "misplaced" else config.TEXT_MUTED)
                ctk.CTkLabel(pegs_frame, text="●", font=(config.FONT_SANS, 14), text_color=color).pack(side="left", padx=2)
                
            bottom_row = ctk.CTkFrame(card, fg_color="transparent")
            bottom_row.pack(fill="x", padx=12, pady=(0, 12))
            
            from hints import get_summary
            summ = get_summary(entry["correct_count"], entry["misplaced_count"])
            if not summ: summ = "0 right, 0 misplaced"
            ctk.CTkLabel(bottom_row, text=summ, font=(config.FONT_SANS, 10), text_color=config.TEXT_MUTED).pack(side="right")

class StackView(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent", corner_radius=0)
        
    def refresh(self, stack_items):
        for w in self.winfo_children():
            w.destroy()
            
        if not stack_items:
            ctk.CTkLabel(self, text="Stack is empty", font=(config.FONT_SANS, 12), text_color=config.TEXT_MUTED).pack(pady=20)
            return
            
        for idx, item in enumerate(reversed(stack_items)):
            is_top = (idx == 0)
            border = config.CYAN if is_top else config.BORDER_GLOW
            
            card = ctk.CTkFrame(self, fg_color=config.DARK_BLUE, border_color=border, border_width=1, corner_radius=8)
            card.pack(fill="x", pady=4, padx=10)
            
            inner = ctk.CTkFrame(card, fg_color="transparent")
            inner.pack(fill="x", padx=10, pady=8)
            
            ctk.CTkLabel(inner, text="☰", font=(config.FONT_SANS, 14), text_color=config.CYAN if is_top else config.TEXT_MUTED).pack(side="left")
            ctk.CTkLabel(inner, text="  ".join(item), font=(config.FONT_MONO, 16, "bold"), text_color=config.TEXT_MAIN).pack(side="left", expand=True)
            
            if is_top:
                ctk.CTkLabel(inner, text="← TOP", font=(config.FONT_SANS, 10, "bold"), text_color=config.CYAN).pack(side="right")
