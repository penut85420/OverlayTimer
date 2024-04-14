import configparser
import time
import tkinter as tk

from pynput.keyboard import Key, Listener


class CountdownApp:
    def __init__(self, root: tk.Tk):
        try:
            parser = configparser.ConfigParser(inline_comment_prefixes="#")
            with open("config.ini", "rt", encoding="UTF-8") as fp:
                content = fp.read().strip()
                parser.read_string(f"[root]\n{content}")
                config = parser["root"]
        except Exception as e:
            print(e)
            config = dict()

        print(dict(config))

        alpha = float(config.get("alpha", 0.6))
        font_name = config.get("font-name", "Consolas")
        font_size = int(config.get("font-size", 24))
        font = (font_name, font_size)
        fg = config.get("foreground", "#333").strip('"').strip("'")
        bg = config.get("background", "#AAA").strip('"').strip("'")
        self.duration = int(config.get("duration", 205))  # 倒數總秒數
        self.x_offset_scale = float(config.get("x-offset-scale", 0.15))
        self.y_offset_scale = float(config.get("y-offset-scale", -0.15))
        self.update_interval = int(config.get("update-interval", 100))

        self.root = root
        self.root.attributes("-alpha", alpha)  # 透明度調整
        self.root.overrideredirect(True)  # 隱藏標題欄
        self.root.attributes("-topmost", True)  # 保持窗口在最上層

        self.turns = 0
        self.label = tk.Label(root, text=str(), font=font, fg=fg, bg=bg)
        self.label.pack()

        self.reset()
        self.update_clock()
        self.center_window()

    def reset(self):
        self.curr_start_time = int(time.time())
        self.life_start_time = int(time.time())

    def reset_curr(self):
        self.curr_start_time = int(time.time()) - self.duration * self.turns

    def set_turn(self, offset):
        self.curr_start_time -= offset * self.duration

    def update_clock(self):
        time_pass = int(time.time() - self.curr_start_time)
        self.turns, time_pass = divmod(time_pass, self.duration)
        time_left = self.duration - time_pass
        mm0, ss0 = divmod(time_left, 60)

        total_time_pass = int(time.time() - self.life_start_time)
        mm1, ss1 = divmod(total_time_pass, 60)
        hh1, mm1 = divmod(mm1, 60)

        timeformat = f"[{self.turns:d}] {mm0:02d}:{ss0:02d}\n{hh1:02d}:{mm1:02d}:{ss1:02d}"
        self.label.config(text=timeformat)

        self.root.after(self.update_interval, self.update_clock)

    def center_window(self):
        self.root.update_idletasks()

        w = self.root.winfo_width()
        h = self.root.winfo_height()

        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()

        x = (sw - w) // 2 + int(self.x_offset_scale * sw)
        y = (sh - h) // 2 + int(self.y_offset_scale * sw)

        self.root.geometry(f"+{x}+{y}")


if __name__ == "__main__":
    root = tk.Tk()
    app = CountdownApp(root)

    def on_press(key):
        if key == Key.home:
            app.reset_curr()
            return True

        if key == Key.end:
            listener.stop()
            root.destroy()
            return False

        if key == Key.insert:
            app.reset()
            return True

        if key == Key.page_up:
            app.set_turn(1)
            return True

        if key == Key.page_down:
            app.set_turn(-1)
            return True

    with Listener(on_press=on_press) as listener:
        root.mainloop()
