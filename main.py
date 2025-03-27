import tkinter as tk
import os

timer_id = None


"""уведомление о перерыве"""
def show_fullscreen(message, break_minutes):
    notification = tk.Toplevel()
    notification.attributes("-fullscreen", True)
    notification.attributes("-topmost", True)
    notification.attributes("-alpha", 0.6)
    notification.configure(bg="black")

    lbl_notification = tk.Label(
        notification,
        text=f"{message}\n\nОсталось: {break_minutes} мин.",
        font=("Arial", 30),
        bg="black",
        fg="#398ff9"
    )
    lbl_notification.pack(expand=True, fill=tk.BOTH)


    btn_close = tk.Button(
        notification,
        text="Закрыть",
        command=notification.destroy,
        font=("Arial", 20),
        bg="black",
        fg="white",
        relief=tk.RIDGE
    )
    btn_close.pack(pady=20)

    countdown(notification, lbl_notification, break_minutes * 60)

"""Таймер обратного отсчета."""
def countdown(notification, label, remaining_seconds):
    global is_running
    if not is_running or remaining_seconds <= 0:
        notification.destroy()  
        return

    minutes, seconds = divmod(remaining_seconds, 60)
    label.config(text=f"Время перерыва!\n\nОсталось: {minutes} мин {seconds} сек")

    notification.after(1000, countdown, notification, label, remaining_seconds - 1)


"""Основное окно"""
def start_program():
    global work_value, break_value, is_running
    try:
        work_value = int(entry_work.get())
        break_value = int(entry_break.get())

        if work_value >= 0 and break_value >= 0:
            if work_value > 120 or break_value > 120:
                lbl_work.config(text="Максимум 120 минут!")
                lbl_break.config(text="Максимум 120 минут!")
                return
            lbl_work.config(text=f"Интервал работы: {work_value} минут")
            lbl_break.config(text=f"Интервал перерыва: {break_value} минут")

            is_running = True
            btn_break.config(state=tk.DISABLED)
            run_timer(work_value, break_value)
        else:
            lbl_work.config(text="Введите положительные числа!")
            lbl_break.config(text="Введите положительные числа!")
    except ValueError:
        lbl_work.config(text="Некорректный ввод!")
        lbl_break.config(text="Некорректный ввод!")

"""Начало работы"""
def run_timer(work_minutes, break_minutes):
    global is_running, timer_id
    if not is_running:
        return

    timer_id = window.after(work_minutes * 60000, start_break, break_minutes)

'''начало перерыва'''
def start_break(break_minutes):
    global is_running, timer_id
    if not is_running:
        return
    show_fullscreen(f"Пора дать глазам отдохнуть!", break_minutes)
    timer_id = window.after(break_minutes * 60000, run_timer, work_value, break_value)


"""Остановка таймера"""
def stop_program():
    global is_running, timer_id
    is_running = False
    if timer_id:
        window.after_cancel(timer_id)
        timer_id = None
    btn_break.config(state=tk.NORMAL)
    lbl_work.config(text="Интервал работы: не установлен")
    lbl_break.config(text="Интервал перерыва: не установлен")

work_value = 0
break_value = 0
is_running = False

window = tk.Tk()

window.title("EyesCare v1.0")
window.iconbitmap(os.path.join(os.path.dirname(__file__), "icon.ico"))
window.geometry('620x360')
window.configure(bg="#95aca7")

lbl1 = tk.Label(
    window,
    text="Добро пожаловать в EyesCare",
    bg="#95aca7",
    fg="#333333",
    font=("Montserrat", 16, "bold")
)
lbl1.pack(pady=20, padx=10, anchor="center")

lbl_work = tk.Label(window,
                    text="Введите время работы (минуты):",
                    bg="#95aca7", font=("Arial", 11))
lbl_work.pack(pady=5)
entry_work = tk.Entry(window, font=("Arial", 11), width=10)
entry_work.pack(pady=5)

lbl_break = tk.Label(window,
                     text="Введите время перерыва (минуты):",
                     bg="#95aca7", font=("Arial", 11))
lbl_break.pack(pady=5)
entry_break = tk.Entry(window, font=("Arial", 11), width=10)
entry_break.pack(pady=5)


btn_break = tk.Button(
    text="Запустить",
    command=start_program,
    font=("Arial", 12),
    bg="#4CAF50",
    fg="white",
    relief=tk.RAISED,
    width=15
)
btn_break.pack(pady=10)

btn_stop = tk.Button(
    text="Остановить",
    command=stop_program,
    font=("Arial", 12),
    bg="#f44336",
    fg="white",
    relief=tk.RAISED,
    width=15
)
btn_stop.pack(pady=10)

window.mainloop()
