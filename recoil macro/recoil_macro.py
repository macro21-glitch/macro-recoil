import tkinter as tk
import random
import threading
import keyboard  # Dış kütüphane, tuş dinlemek için

root = tk.Tk()
root.title("Efe Macro")
root.geometry("700x400")
root.resizable(False, False)

bg_color = "#0d0d1a"
root.configure(bg=bg_color)

canvas = tk.Canvas(root, width=700, height=400, bg=bg_color, highlightthickness=0)
canvas.place(x=0, y=0)

stars = []
for _ in range(80):
    x = random.randint(0, 700)
    y = random.randint(0, 400)
    size = random.randint(1, 3)
    star = canvas.create_oval(x, y, x+size, y+size, fill="white", outline="")
    stars.append((star, size))

def animate():
    for star, size in stars:
        canvas.move(star, 0, 0.3 + size*0.1)
        pos = canvas.coords(star)
        if pos[1] > 400:
            new_x = random.randint(0, 700)
            canvas.coords(star, new_x, 0, new_x+size, size)
    root.after(50, animate)

animate()

menu_frame = tk.Frame(root, bg="#1a1a2e", width=150, height=400)
menu_frame.place(x=0, y=0)

# Aktif menüyü izlemek için değişken
current_menu = None

# Recoil macro durumu ve atanan tuş
recoil_active = False
recoil_hotkey = None
waiting_for_key = False

def ana_menu_click():
    global current_menu
    current_menu = "ana_menu"
    content_label.config(text="Menümüze Hoşgeldiniz")
    clear_recoil_menu()

def clear_recoil_menu():
    # Recoil menü altındaki widgetları temizle
    for widget in recoil_menu_frame.winfo_children():
        widget.destroy()

def on_hotkey_pressed(e):
    global recoil_active
    recoil_active = not recoil_active
    status = "Recoil Macro Açık" if recoil_active else "Recoil Macro Aktif Değil"
    recoil_status_label.config(text=status)

def wait_for_key():
    global recoil_hotkey, waiting_for_key

    recoil_status_label.config(text="Kısa tuşu seçin (bir tuşa basın)...")
    waiting_for_key = True

    # Burada keyboard modülü ile tek tuş bekleyeceğiz
    event = keyboard.read_event(suppress=False)
    while event.event_type != keyboard.KEY_DOWN:
        event = keyboard.read_event(suppress=False)

    recoil_hotkey = event.name
    waiting_for_key = False

    recoil_hotkey_label.config(text=f"Aktif Tuş: {recoil_hotkey}")

    # Hotkey ataması: atanan tuşa basıldığında recoil aç/kapa
    keyboard.add_hotkey(recoil_hotkey, on_hotkey_pressed)

    recoil_status_label.config(text="Recoil Macro Aktif Değil")

def recoil_macro_click():
    global current_menu
    current_menu = "recoil_macro"
    content_label.config(text="")

    clear_recoil_menu()

    # Recoil durum etiketi
    global recoil_status_label, recoil_hotkey_label, wait_key_button
    recoil_status_label = tk.Label(recoil_menu_frame, text="Recoil Macro Aktif Değil", font=("Arial", 16), bg=bg_color, fg="white")
    recoil_status_label.pack(pady=(10,5))

    # Kısayol tuş etiketi
    hotkey_text = f"Aktif Tuş: {recoil_hotkey}" if recoil_hotkey else "Aktif Tuş: Yok"
    recoil_hotkey_label = tk.Label(recoil_menu_frame, text=hotkey_text, font=("Arial", 14), bg=bg_color, fg="#bb99ff")
    recoil_hotkey_label.pack(pady=(0,10))

    # Tuş seçme butonu
    wait_key_button = tk.Button(recoil_menu_frame, text="Kısa Tuşu Ayarla", font=("Arial", 14), bg="#2c2f4a", fg="white", relief="flat",
                                command=lambda: threading.Thread(target=wait_for_key, daemon=True).start())
    wait_key_button.pack()

btn_ana_menu = tk.Button(menu_frame, text="Ana Menü", font=("Arial", 14), bg="#2c2f4a", fg="white", relief="flat", command=ana_menu_click)
btn_ana_menu.place(x=10, y=50, width=130, height=40)

btn_recoil_macro = tk.Button(menu_frame, text="Recoil Macro", font=("Arial", 14), bg="#2c2f4a", fg="white", relief="flat", command=recoil_macro_click)
btn_recoil_macro.place(x=10, y=110, width=130, height=40)

title_label = tk.Label(root, text="🛠️ Hile Menüsü", font=("Arial", 28, "bold"), bg=bg_color, fg="#bb99ff")
title_label.place(relx=0.5, y=20, anchor='n')

content_label = tk.Label(root, text="Menümüze Hoşgeldiniz", font=("Arial", 18), bg=bg_color, fg="white")
content_label.place(relx=0.5, y=80, anchor='n')

recoil_menu_frame = tk.Frame(root, bg=bg_color)
recoil_menu_frame.place(x=180, y=130, width=500, height=220)  # İçerik alanı

# Başlangıçta ana menüyü göster
ana_menu_click()

root.mainloop()
