import tkinter as tk
from tkinter import messagebox
import sqlite3

DB_NAME = "nilai_siswa.db"

# ====== WARNA ======
BG = "#5B5FC7"          # latar ungu-biru
BG_ENTRY = "#7B7FE0"    # kotak input
PINK = "#FF6FB5"        # judul
BTN = "#A5A9F0"         # tombol
BTN_HOVER = "#E5EFA7"   # tombol saat disentuh mouse


# ====== DATABASE ======
def create_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT NOT NULL,
            biologi INTEGER NOT NULL,
            fisika INTEGER NOT NULL,
            inggris INTEGER NOT NULL,
            prediksi_fakultas TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def prediksi_fakultas(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris:
        return "Kedokteran"
    elif fisika > biologi and fisika > inggris:
        return "Teknik"
    elif inggris > biologi and inggris > fisika:
        return "Bahasa"
    else:
        return "Tidak Dapat Ditentukan"


def submit_nilai():
    nama = entry_nama.get().strip()
    if not nama:
        messagebox.showerror("Error", "Nama siswa tidak boleh kosong!")
        return

    try:
        bio = int(entry_bio.get())
        fis = int(entry_fis.get())
        ing = int(entry_ing.get())
    except ValueError:
        messagebox.showerror("Error", "Nilai harus berupa angka!")
        return

    if not all(0 <= n <= 100 for n in (bio, fis, ing)):
        messagebox.showerror("Error", "Nilai harus antara 0 - 100!")
        return

    hasil = prediksi_fakultas(bio, fis, ing)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    """, (nama, bio, fis, ing, hasil))
    conn.commit()
    conn.close()

    messagebox.showinfo("Hasil Prediksi", f"{nama} diprediksi masuk: {hasil}")

    for e in (entry_nama, entry_bio, entry_fis, entry_ing):
        e.delete(0, tk.END)
    entry_nama.focus()


def on_enter(e):
    btn_submit["bg"] = BTN_HOVER


def on_leave(e):
    btn_submit["bg"] = BTN


# ====== TAMPILAN TKINTER ======
create_db()

root = tk.Tk()
root.title("Prediksi Fakultas Siswa")
root.geometry("340x420")
root.configure(bg=BG)
root.resizable(False, False)

tk.Label(root, text="📝 Prediksi Fakultas", bg=BG, fg=PINK,
         font=("Segoe UI", 16, "bold")).pack(pady=(20, 15))


def buat_input(teks):
    tk.Label(root, text=teks, bg=BG, fg="white",
             font=("Segoe UI", 10)).pack(pady=(8, 2))
    entry = tk.Entry(root, width=28, bg=BG_ENTRY, fg="white",
                     insertbackground="white", relief="flat",
                     justify="center", font=("Segoe UI", 10))
    entry.pack(ipady=4)
    return entry


entry_nama = buat_input("Nama Siswa")
entry_bio = buat_input("Nilai Biologi")
entry_fis = buat_input("Nilai Fisika")
entry_ing = buat_input("Nilai Inggris")

btn_submit = tk.Button(root, text="Submit Nilai", command=submit_nilai,
                       bg=BTN, fg="black", relief="flat", width=22,
                       font=("Segoe UI", 10), cursor="hand2")
btn_submit.pack(pady=25, ipady=4)
btn_submit.bind("<Enter>", on_enter)
btn_submit.bind("<Leave>", on_leave)

root.mainloop()