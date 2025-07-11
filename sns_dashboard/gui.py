import tkinter as tk
from tkinter import ttk
import threading

import typer


def start_app(channel_var, log_text):
    log_text.insert(tk.END, "Starting update...\n")
    typer.run(lambda: None)  # placeholder


def main():
    root = tk.Tk()
    root.title("SNS Dashboard")

    tk.Label(root, text="YouTube Channel URL").pack()
    channel_var = tk.StringVar()
    tk.Entry(root, textvariable=channel_var, width=40).pack()

    tk.Button(root, text="Instagram 로그인", command=lambda: None).pack()
    tk.Button(root, text="TikTok 로그인", command=lambda: None).pack()

    tk.Button(root, text="저장&시작", command=lambda: threading.Thread(target=start_app, args=(channel_var.get(), log_box)).start()).pack()

    log_box = tk.Text(root, height=10)
    log_box.pack(fill="both", expand=True)

    root.mainloop()


if __name__ == "__main__":
    main()
