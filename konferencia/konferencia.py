from tkinter import *
from tkinter import messagebox
import hashlib
from tkinter import ttk
import mysql.connector
from PIL import *
from mysql.connector.errors import IntegrityError
import csv
import pygame
import configparser
from datetime import datetime

# Fő alkalmazás ablak
app = Tk()
app.title("Konferencia Rendszer")
app.iconbitmap('konfico.ico')
app.geometry("650x650")

global bejelentkezett
bejelentkezett = 0

def handle_integrity_error(exception):
    messagebox.showerror("Integritás Hiba", f"Adatbázis integritás hibát találtam: {exception}")

# pygame mixer
pygame.mixer.init()

def play():
    pygame.mixer.music.load("audio/beep.wav")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(loops=0)

# Kapcsolódás a MySQL adatbázishoz
config = configparser.ConfigParser()
config.read('config.ini')

db = mysql.connector.connect(
    host=config['MySQL']['host'],
    user=config['MySQL']['user'],
    passwd=config['MySQL']['passwd'],
    database=config['MySQL']['database'],
)

# Sikerült csatlakozni a MySQL-hez?
print(db)

# Cursort létrehoz
cursor = db.cursor(buffered=True)

# DB törlése
# cursor.execute("DROP DATABASE IF EXISTS Konferencia")

# DBt létrehoz
# cursor.execute("""CREATE DATABASE IF NOT EXISTS Konferencia
#	DEFAULT CHARACTER SET utf8
#	COLLATE utf8_hungarian_ci;""")
# Sikerült létrehozni a DBt?
#cursor.execute("SHOW DATABASES")
#for db in my_cursor:
#	print(db)

# Write To CSV Excel Fgv.-k
def write_to_csv_felhasznalok():
    cursor.execute("SELECT id, felhasznalonev, elotag, nev, szerepkor, email, intezmeny FROM felhasznalok")
    result = cursor.fetchall()
    justdoit(result)
def justdoit(result):
    with open("csvk/felhasznalok.csv", "w", newline="") as csvfile:
        w = csv.writer(csvfile)
        w.writerow(["Felhasználó ID", "Felhasználónév", "Előtag", "Név", "Szerepkör", "Email", "Intézmény"])
        w.writerows(result)
def write_to_csv_cikkek(result):
    with open("csvk/cikkek.csv", "w", newline="") as csvfile:
        w = csv.writer(csvfile)
        w.writerow(["Cikk ID", "Cikk Címe", "Szerző"])
        w.writerows(result)
def write_to_csv_eloadasok(result):
    with open("csvk/eloadasok.csv", "w", newline="") as csvfile:
        w = csv.writer(csvfile)
        w.writerow(["Előadás ID", "Cikk ID", "Cikk Cím", "Szekció ID", "Kezdés Időpont", "Előadó Név", "Előadó ID", "Előadás Hossz"])
        w.writerows(result)
def write_to_csv_szekciok(result):
    with open("csvk/szekciok.csv", "w", newline="") as csvfile:
        w = csv.writer(csvfile)
        w.writerow(["ID", "Szekció Név", "Kezdési Időpont", "Levezető Elnök ID"])
        w.writerows(result)
def write_to_csv_osszetett_1(result):
    with open("csvk/osszetett_lekerdezes_1.csv", "w", newline="") as file:
        w = csv.writer(file)
        w.writerow(["Szekció Név", "Előadások Száma"])
        w.writerows(result)
def write_to_csv_osszetett_2(result):
    with open("csvk/osszetett_lekerdezes_2.csv", "w", newline="") as file:
        w = csv.writer(file)
        w.writerow(["Szerző Neve", "Cikkek Száma"])
        w.writerows(result)
def write_to_csv_osszetett_3(result):
    with open("csvk/osszetett_lekerdezes_3.csv", "w", newline="") as file:
        w = csv.writer(file)
        w.writerow(["Szerző Neve"])
        w.writerows(result)
def write_to_csv_nem_lett_eloadas(result):
    with open("csvk/nem_lett_eloadas.csv", "w", newline="") as file:
        w = csv.writer(file)
        w.writerow(["Szekció ID", "Szekció Név"])
        w.writerows(result)

# Lista a cikkek megtekintéséhez
# Létrehozunk egy Frame-et a görgetősáv és a lista számára
frame = Frame(app)
frame.grid(row=3, column=0, columnspan=2)
# Létrehozunk egy görgetősávot
scrollbar = Scrollbar(frame, orient=VERTICAL)

# Létrehozunk egy Listbox-ot a lista számára és hozzáadjuk a görgetősávot
cikk_lista = Listbox(frame, yscrollcommand=scrollbar.set, selectmode=EXTENDED, width=70, height=10)
scrollbar.config(command=cikk_lista.yview)

# Elhelyezzük a Listbox-ot és a görgetősávot a Frame-ben
cikk_lista.grid(row=0, column=0)
scrollbar.grid(row=0, column=1, sticky="ns")

# Függvény a cikkek betöltéséhez és megjelenítéséhez
def cikkek_betoltes():
    cikk_lista.delete(0, END)
    cursor.execute("SELECT cikkek.id, cikkek.cikk_cim, felhasznalok.nev FROM cikkek JOIN felhasznalok ON cikkek.szerzo_id = felhasznalok.id ORDER BY cikkek.id")
    cikkek = cursor.fetchall()
    for sor in cikkek:
        cikk_lista.insert(END, f"Cikk ID: {sor[0]} - Cikk Címe: {sor[1]} - Szerző: {sor[2]}")

# Gomb a cikkek betöltéséhez
cikkek_betoltes_gomb = Button(app, text="Cikkek Betöltése", command=lambda:[play(),cikkek_betoltes()])
cikkek_betoltes_gomb.grid(row=4, column=0, columnspan=2)

# Űrlap mezők és címkék a cikk törléséhez és frissítéséhez
cikk_id_label = Label(app, text="Cikk ID:")
cikk_id = Entry(app)

uj_cikk_cim_label = Label(app, text="Új Cikk Címe:")
uj_cikk_cim = Entry(app)

# Függvény a cikk törléséhez
def cikk_torles():
    cikk_id_text = cikk_id.get()
    cursor.execute("DELETE FROM cikkek WHERE id = %s", (cikk_id_text,))
    db.commit()
    cikk_id.delete(0, END)
    cikkek_betoltes()

# Gomb a cikk törléséhez
cikk_torles_gomb = Button(app, text="Cikk Törlése", command=lambda:[play(),cikk_torles()])

# Előadás törlése ablak fgv.-ek
def get_deletable_eloadasok():
    cursor.execute("SELECT * FROM eloadasok")
    deletable_eloadasok = cursor.fetchall()
    return deletable_eloadasok

def delete_eloadas(eloadas_id):
    cursor.execute("DELETE FROM eloadasok WHERE id = %s", (eloadas_id,))
    db.commit()
    messagebox.showinfo("Sikeres törlés", "Az előadás sikeresen törölve lett.")

def eloadas_torlese_ablak():
    eloadas_deletion_query = Tk()
    eloadas_deletion_query.title("Előadás Törlése")
    eloadas_deletion_query.geometry("800x400")

    # Létrehozunk egy Frame-et a görgetősáv és a lista számára
    frame = Frame(eloadas_deletion_query)
    frame.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

    # Létrehozunk egy görgetősávot
    scrollbar = Scrollbar(frame, orient=VERTICAL)

    # Létrehozunk egy Treeview-ot a lista számára és hozzáadjuk a görgetősávot
    tree = ttk.Treeview(frame, columns=("ID", "Cikk ID", "Cikk Cím", "Szekció ID", "Kezdés Időpont", "Előadó Név", "Előadó ID", "Előadás Hossz"), show="headings", selectmode=EXTENDED)
    scrollbar.config(command=tree.yview)

    # Oszlopok beállítása
    tree.heading("ID", text="ID")
    tree.heading("Cikk ID", text="Cikk ID")
    tree.heading("Cikk Cím", text="Cikk Cím")
    tree.heading("Szekció ID", text="Szekció ID")
    tree.heading("Kezdés Időpont", text="Kezdés Időpont")
    tree.heading("Előadó Név", text="Előadó Név")
    tree.heading("Előadó ID", text="Előadó ID")
    tree.heading("Előadás Hossz", text="Előadás Hossz")
    tree.column("ID", anchor=W, width=40)
    tree.column("Cikk ID", anchor=W, width=60)
    tree.column("Cikk Cím", anchor=W, width=140)
    tree.column("Szekció ID", anchor=W, width=70)
    tree.column("Kezdés Időpont", anchor=W, width=115)
    tree.column("Előadó Név", anchor=W, width=140)
    tree.column("Előadó ID", anchor=W, width=60)
    tree.column("Előadás Hossz", anchor=W, width=90)

    # Adatok feltöltése a Treeview-be
    deletable_eloadasok = get_deletable_eloadasok()
    for row in deletable_eloadasok:
        tree.insert("", "end", values=row)

    # Elhelyezzük a Treeview-ot és a görgetősávot a Frame-ben
    tree.grid(row=0, column=0)
    scrollbar.grid(row=0, column=1, sticky="ns")

    def delete_selected_eloadasok():
        selected_items = tree.selection()
        if not selected_items:
            messagebox.showwarning("Nincs kiválasztva", "Kérem, válassza ki a törölni kívánt előadásokat.")
            return

        for item in selected_items:
            eloadas_id = int(tree.item(item, "values")[0])
            delete_eloadas(eloadas_id)

        # Frissítjük a Treeview-t az új adatokkal (esetlegesen már törölt előadásokkal)
        tree.delete(*tree.get_children())
        deletable_eloadasok = get_deletable_eloadasok()
        for row in deletable_eloadasok:
            tree.insert("", "end", values=row)

    # Törlés gomb
    delete_button = Button(eloadas_deletion_query, text="Kiválasztott előadások törlése", command=lambda:[play(),delete_selected_eloadasok()])
    delete_button.grid(row=0, column=0, padx=10, pady=10)

    # Quit Button már megint
    quit_button = Button(eloadas_deletion_query, text="Kilépés", command=lambda:[play(),eloadas_deletion_query.destroy()])
    quit_button.grid(row=0, column=1, padx=10, pady=10)

# Gomb az eloadas törléséhez
eloadas_torlese_gomb = Button(app, text="Előadás Törlése", command=lambda:[play(),eloadas_torlese_ablak()])

# Függvény a cikk frissítéséhez
def cikk_frissites():
    cikk_id_text = cikk_id.get()
    uj_cikk_cim_text = uj_cikk_cim.get()
    cursor.execute("UPDATE cikkek SET cikk_cim = %s WHERE id = %s", (uj_cikk_cim_text, cikk_id_text))
    db.commit()
    cikk_id.delete(0, END)
    uj_cikk_cim.delete(0, END)
    cikkek_betoltes()

# Gomb a cikk frissítéséhez
cikk_frissites_gomb = Button(app, text="Cikk Frissítése", command=lambda:[play(),cikk_frissites()])

# Listázás
def list_felhasznalok():
    list_felhasznalo_query = Tk()
    list_felhasznalo_query.title("Listázás")
    list_felhasznalo_query.iconbitmap('konfico.ico')
    list_felhasznalo_query.geometry("950x650")
    
    # DB-t lekérdez
    cursor.execute("SELECT * FROM Felhasznalok")
    result = cursor.fetchall()

    # Létrehozunk egy Frame-et a görgetősáv és a lista számára
    frame = Frame(list_felhasznalo_query)
    frame.grid(row=1, column=0, padx=10, pady=10, columnspan=33)
    
    # Létrehozunk egy görgetősávot
    scrollbar = Scrollbar(frame, orient=VERTICAL)
    
    # Létrehozunk egy Listbox-ot a lista számára és hozzáadjuk a görgetősávot
    listbox = Listbox(frame, yscrollcommand=scrollbar.set, selectmode=EXTENDED, width=150, height=35)
    scrollbar.config(command=listbox.yview)
    
    # Elhelyezzük a Listbox-ot és a görgetősávot a Frame-ben
    listbox.grid(row=0, column=0)
    scrollbar.grid(row=0, column=1, sticky="ns")
    
    for y in result:
        listbox.insert(END, f"{y}")
    
    csv_button = Button(list_felhasznalo_query, text="Excel-be mentés (felhasznalok.csv)", command=lambda: [play(), write_to_csv_felhasznalok()])
    csv_button.grid(row=0, column=30, padx=10, pady=10)
    
    # Quit Button már megint
    quit_button = Button(list_felhasznalo_query, text="Kilépés", command=lambda: [play(), list_felhasznalo_query.destroy()])
    quit_button.grid(row=0, column=32, padx=10, pady=10)

def list_cikkek():
    list_cikk_query = Tk()
    list_cikk_query.title("Listázás")
    list_cikk_query.iconbitmap('konfico.ico')
    list_cikk_query.geometry("800x650")

    # DB-t lekérdez
    cursor.execute("SELECT cikkek.id, cikkek.cikk_cim, felhasznalok.nev FROM cikkek JOIN felhasznalok ON cikkek.szerzo_id = felhasznalok.id ORDER BY cikkek.id")
    result = cursor.fetchall()

    # Létrehozunk egy Frame-et a görgetősáv és a lista számára
    frame = Frame(list_cikk_query)
    frame.grid(row=1, column=0, padx=10, pady=10, columnspan=33)

    # Létrehozunk egy görgetősávot
    scrollbar = Scrollbar(frame, orient=VERTICAL)

    # Létrehozunk egy Listbox-ot a lista számára és hozzáadjuk a görgetősávot
    listbox = Listbox(frame, yscrollcommand=scrollbar.set, selectmode=EXTENDED, width=120, height=35)
    scrollbar.config(command=listbox.yview)

    # Elhelyezzük a Listbox-ot és a görgetősávot a Frame-ben
    listbox.grid(row=0, column=0)
    scrollbar.grid(row=0, column=1, sticky="ns")

    for cikk in result:
        # Hozzáadjuk a cikkeket a Listbox-hoz formázott szövegként
        listbox.insert(END, f"Cikk ID: {cikk[0]} - Cikk Címe: {cikk[1]} - Szerző: {cikk[2]}")

    csv_button = Button(list_cikk_query, text="Excel-be mentés (cikkek.csv)", command=lambda: [play(), write_to_csv_cikkek(result)])
    csv_button.grid(row=0, column=30, padx=10, pady=10)

    # Quit Button már megint
    quit_button = Button(list_cikk_query, text="Kilépés", command=lambda: [play(), list_cikk_query.destroy()])
    quit_button.grid(row=0, column=32, padx=10, pady=10)

def list_eloadasok():
    list_eloadas_query = Tk()
    list_eloadas_query.title("Listázás")
    list_eloadas_query.iconbitmap('konfico.ico')
    list_eloadas_query.geometry("800x650")
    
    # DB-t lekérdez
    cursor.execute("SELECT * FROM Eloadasok")
    result = cursor.fetchall()

    # Létrehozunk egy Frame-et a görgetősáv és a lista számára
    frame = Frame(list_eloadas_query)
    frame.grid(row=1, column=0, padx=10, pady=10, columnspan=33)
    
    # Létrehozunk egy görgetősávot
    scrollbar = Scrollbar(frame, orient=VERTICAL)
    
    # Létrehozunk egy Listbox-ot a lista számára és hozzáadjuk a görgetősávot
    listbox = Listbox(frame, yscrollcommand=scrollbar.set, selectmode=EXTENDED, width=120, height=35)
    scrollbar.config(command=listbox.yview)
    
    # Elhelyezzük a Listbox-ot és a görgetősávot a Frame-ben
    listbox.grid(row=0, column=0)
    scrollbar.grid(row=0, column=1, sticky="ns")
    
    for y in result:
        # Módosítjuk a dátumot egyedi formátumra
        formatted_date = y[4].strftime("%Y-%m-%d %H:%M")
        
        # Hozzáadjuk az elemet a Listbox-hoz a formázott dátummal
        listbox.insert(END, f"{y[0]}, {y[1]}, {y[2]}, {y[3]}, {formatted_date}, {y[5]}, {y[6]}, {y[7]}")
    
    csv_button = Button(list_eloadas_query, text="Excel-be mentés (eloadasok.csv)", command=lambda: [play(), write_to_csv_eloadasok(result)])
    csv_button.grid(row=0, column=30, padx=10, pady=10)
    
    # Quit Button már megint
    quit_button = Button(list_eloadas_query, text="Kilépés", command=lambda: [play(), list_eloadas_query.destroy()])
    quit_button.grid(row=0, column=32, padx=10, pady=10)
    
def list_szekciok():
    list_szekcio_query = Tk()
    list_szekcio_query.title("Listázás")
    list_szekcio_query.iconbitmap('konfico.ico')
    list_szekcio_query.geometry("800x650")
    
    # DB-t lekérdez
    cursor.execute("SELECT * FROM Szekciok")
    result = cursor.fetchall()

    # Létrehozunk egy Frame-et a görgetősáv és a lista számára
    frame = Frame(list_szekcio_query)
    frame.grid(row=1, column=0, padx=10, pady=10, columnspan=33)
    
    # Létrehozunk egy görgetősávot
    scrollbar = Scrollbar(frame, orient=VERTICAL)
    
    # Létrehozunk egy Listbox-ot a lista számára és hozzáadjuk a görgetősávot
    listbox = Listbox(frame, yscrollcommand=scrollbar.set, selectmode=EXTENDED, width=120, height=35)
    scrollbar.config(command=listbox.yview)
    
    # Elhelyezzük a Listbox-ot és a görgetősávot a Frame-ben
    listbox.grid(row=0, column=0)
    scrollbar.grid(row=0, column=1, sticky="ns")
    
    for y in result:
        # Módosítjuk a dátumot egyedi formátumra
        formatted_date = y[2].strftime("%Y-%m-%d %H:%M")
        
        # Hozzáadjuk az elemet a Listbox-hoz a formázott dátummal
        listbox.insert(END, f"{y[0]}, {y[1]}, {formatted_date}, {y[3]}")
    
    csv_button = Button(list_szekcio_query, text="Excel-be mentés (szekciok.csv)", command=lambda: [play(), write_to_csv_szekciok(result)])
    csv_button.grid(row=0, column=30, padx=10, pady=10)
    
    # Quit Button már megint
    quit_button = Button(list_szekcio_query, text="Kilépés", command=lambda: [play(), list_szekcio_query.destroy()])
    quit_button.grid(row=0, column=32, padx=10, pady=10)

# Összetettségek
def osszetett_lekerdezes_1():
    cursor.execute("SELECT szekciok.szekcio_nev, COUNT(eloadasok.id) AS eloadasok_szama FROM szekciok LEFT JOIN eloadasok ON szekciok.id = eloadasok.szekcio_id GROUP BY szekciok.szekcio_nev")
    eredmeny = cursor.fetchall()

    # Új ablak létrehozása eredményekkel
    ossz1_query = Tk()
    ossz1_query.title("Eredmények - Összetett Lekérdezés 1")
    ossz1_query.iconbitmap('konfico.ico')
    ossz1_query.geometry("700x700")

    # Létrehozunk egy Frame-et a görgetősáv és a lista számára
    frame = Frame(ossz1_query)
    frame.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

    # Létrehozunk egy görgetősávot
    scrollbar = Scrollbar(frame, orient=VERTICAL)

    # Létrehozunk egy Listbox-ot a lista számára és hozzáadjuk a görgetősávot
    listbox = Listbox(frame, yscrollcommand=scrollbar.set, selectmode=EXTENDED, width=100, height=35)
    scrollbar.config(command=listbox.yview)

    # Elhelyezzük a Listbox-ot és a görgetősávot a Frame-ben
    listbox.grid(row=0, column=0)
    scrollbar.grid(row=0, column=1, sticky="ns")

    # Az eredményeket megjelenítjük a Listbox-ban
    for i, sor in enumerate(eredmeny):
        szekcio_nev = sor[0]
        eloadasok_szama = sor[1]
        listbox.insert(END, f"Eredmény #{i + 1}: Szekció Neve: {szekcio_nev}, Előadások Száma: {eloadasok_szama}")

    # Excel-be mentés gomb
    csv_button = Button(ossz1_query, text="Excel-be mentés (osszetett_lekerdezes_1.csv)", command=lambda: [play(), write_to_csv_osszetett_1(eredmeny)])
    csv_button.grid(row=0, column=0, padx=10, pady=10)

    # Kilépés gomb
    quit_button = Button(ossz1_query, text="Kilépés", command=lambda: [play(), ossz1_query.destroy()])
    quit_button.grid(row=0, column=1, padx=10, pady=10)

# Gomb az összetett lekérdezés #1 futtatásához
osszetett_lekerdezes_1_gomb = Button(app, text="Összetett Lekérdezés #1", command=lambda:[play(),osszetett_lekerdezes_1()])
osszetett_lekerdezes_1_gomb.grid(row=11, column=0, columnspan=2, padx=10)

# Funkció az összetett lekérdezés #2 megvalósításához
def osszetett_lekerdezes_2():
    cursor.execute("SELECT felhasznalok.nev, COUNT(cikkek.id) AS cikkek_szama FROM felhasznalok INNER JOIN cikkek ON felhasznalok.id = cikkek.szerzo_id GROUP BY felhasznalok.nev")
    eredmeny = cursor.fetchall()

    # Új ablak létrehozása eredményekkel
    ossz2_query = Tk()
    ossz2_query.title("Eredmények - Összetett Lekérdezés 2")
    ossz2_query.iconbitmap('konfico.ico')
    ossz2_query.geometry("700x700")

    # Létrehozunk egy Frame-et a görgetősáv és a lista számára
    frame = Frame(ossz2_query)
    frame.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

    # Létrehozunk egy görgetősávot
    scrollbar = Scrollbar(frame, orient=VERTICAL)

    # Létrehozunk egy Listbox-ot a lista számára és hozzáadjuk a görgetősávot
    listbox = Listbox(frame, yscrollcommand=scrollbar.set, selectmode=EXTENDED, width=100, height=35)
    scrollbar.config(command=listbox.yview)

    # Elhelyezzük a Listbox-ot és a görgetősávot a Frame-ben
    listbox.grid(row=0, column=0)
    scrollbar.grid(row=0, column=1, sticky="ns")

    # Az eredményeket megjelenítjük a Listbox-ban
    for i, sor in enumerate(eredmeny):
        szerzo_nev = sor[0]
        cikkek_szama = sor[1]
        listbox.insert(END, f"Eredmény #{i + 1}: Szerző Neve: {szerzo_nev}, Cikkek Száma: {cikkek_szama}")

    # Excel-be mentés gomb
    csv_button = Button(ossz2_query, text="Excel-be mentés (osszetett_lekerdezes_2.csv)", command=lambda: [play(), write_to_csv_osszetett_2(eredmeny)])
    csv_button.grid(row=0, column=0, padx=10, pady=10)

    # Kilépés gomb
    quit_button = Button(ossz2_query, text="Kilépés", command=lambda: [play(), ossz2_query.destroy()])
    quit_button.grid(row=0, column=1, padx=10, pady=10)

# Gomb az összetett lekérdezés #2 futtatásához
osszetett_lekerdezes_2_gomb = Button(app, text="Összetett Lekérdezés #2", command=lambda:[play(),osszetett_lekerdezes_2()])
osszetett_lekerdezes_2_gomb.grid(row=12, column=0, columnspan=2, padx=10)

# Funkció az összetett lekérdezés #3 megvalósításához
def osszetett_lekerdezes_3():
    ossz3_query = Tk()
    ossz3_query.title("Eredmények - Összetett Lekérdezés 3")
    ossz3_query.iconbitmap('konfico.ico')
    ossz3_query.geometry("500x500")

    cursor.execute("SELECT felhasznalok.nev FROM felhasznalok INNER JOIN cikkek ON felhasznalok.id = cikkek.szerzo_id GROUP BY felhasznalok.id, felhasznalok.nev HAVING COUNT(cikkek.id) = (SELECT MAX(CountCikkek) FROM (SELECT COUNT(cikkek2.id) AS CountCikkek FROM cikkek cikkek2 GROUP BY cikkek2.szerzo_id) AS MaxCikkek)")
    eredmeny = cursor.fetchall()

    # Létrehozunk egy Frame-et a görgetősáv és a lista számára
    frame = Frame(ossz3_query)
    frame.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

    # Létrehozunk egy görgetősávot
    scrollbar = Scrollbar(frame, orient=VERTICAL)

    # Létrehozunk egy Listbox-ot a lista számára és hozzáadjuk a görgetősávot
    listbox = Listbox(frame, yscrollcommand=scrollbar.set, selectmode=EXTENDED, width=50, height=15)
    scrollbar.config(command=listbox.yview)

    # Elhelyezzük a Listbox-ot és a görgetősávot a Frame-ben
    listbox.grid(row=0, column=0)
    scrollbar.grid(row=0, column=1, sticky="ns")

    # Az eredményeket megjelenítjük a Listbox-ban
    eredmeny_label = Label(ossz3_query, text="A legtöbb cikket író szerző(k) neve(i): ")
    for i, sor in enumerate(eredmeny):
        nev = sor[0]
        listbox.insert(END, nev)
        # Ha ez nem az utolsó sor, adj hozzá egy vesszőt
        if i < len(eredmeny) - 1:
            eredmeny_label["text"] += ", "

    # Excel-be mentés gomb
    csv_button = Button(ossz3_query, text="Excel-be mentés (osszetett_lekerdezes_3.csv)", command=lambda: [play(), write_to_csv_osszetett_3(eredmeny)])
    csv_button.grid(row=0, column=0, padx=10, pady=10)

    # Kilépés gomb
    quit_button = Button(ossz3_query, text="Kilépés", command=lambda: [play(), ossz3_query.destroy()])
    quit_button.grid(row=0, column=1, padx=10, pady=10)

# Gomb az összetett lekérdezés #3 futtatásához
osszetett_lekerdezes_3_gomb = Button(app, text="Összetett Lekérdezés #3", command=lambda:[play(),osszetett_lekerdezes_3()])
osszetett_lekerdezes_3_gomb.grid(row=13, column=0, columnspan=2, padx=10)

def nem_lett_eloadas_rendelve():
    nler_query = Tk()
    nler_query.title("Eredmények - Nem Lett Előadás Rendelve")
    nler_query.iconbitmap('konfico.ico')
    nler_query.geometry("800x700")

    cursor.execute("SELECT szekciok.id, szekciok.szekcio_nev FROM szekciok LEFT JOIN eloadasok ON szekciok.id = eloadasok.szekcio_id WHERE eloadasok.szekcio_id IS NULL")
    eredmeny = cursor.fetchall()

    # Létrehozunk egy Frame-et a görgetősáv és a lista számára
    frame = Frame(nler_query)
    frame.grid(row=1, column=0, padx=10, pady=10, columnspan=2)
    
    # Létrehozunk egy görgetősávot
    scrollbar = Scrollbar(frame, orient=VERTICAL)
    
    # Létrehozunk egy Listbox-ot a lista számára és hozzáadjuk a görgetősávot
    listbox = Listbox(frame, yscrollcommand=scrollbar.set, selectmode=EXTENDED, width=105, height=35)
    scrollbar.config(command=listbox.yview)
    
    # Elhelyezzük a Listbox-ot és a görgetősávot a Frame-ben
    listbox.grid(row=0, column=0)
    scrollbar.grid(row=0, column=1, sticky="ns")
    
    # Az eredmények megjelenítése a Listbox-ban
    for eredmeny_sor in eredmeny:
        listbox.insert(END, f"Nem lett előadás rendelve: {eredmeny_sor}")

    csv_button = Button(nler_query, text="Excel-be mentés (nem_lett_eloadas.csv)", command=lambda: [play(), write_to_csv_nem_lett_eloadas(eredmeny)])
    csv_button.grid(row=0, column=0, padx=10, pady=10)

    # Quit Button már megint
    quit_button = Button(nler_query, text="Kilépés", command=lambda: [play(), nler_query.destroy()])
    quit_button.grid(row=0, column=2, padx=10, pady=10)

# nler gomb
nem_lett_eloadas_rendelve_gomb = Button(app, text="Szekciók, ahol nincs előadás", command=lambda:[play(),nem_lett_eloadas_rendelve()])
nem_lett_eloadas_rendelve_gomb.grid(row=14, column=0, columnspan=2, padx=10)

# Listázás gombok
list_felhasznalo_button = Button(app, text="Listázás (Felhasználók)", command=lambda:[play(),list_felhasznalok()])
list_felhasznalo_button.grid(row=4, column=4, padx=10)

list_cikk_button = Button(app, text="Listázás (Cikkek)", command=lambda:[play(),list_cikkek()])
list_cikk_button.grid(row=5, column=4, padx=10)

list_eloado_button = Button(app, text="Listázás (Előadások)", command=lambda:[play(),list_eloadasok()])
list_eloado_button.grid(row=6, column=4, padx=10)

list_szekcio_button = Button(app, text="Listázás (Szekciók)", command=lambda:[play(),list_szekciok()])
list_szekcio_button.grid(row=7, column=4, padx=10)

szekcio_torlese_button = Button(app, text="Szekcio törlése", command=lambda:[play(),szekcio_torlese_ablak()])

# Kilépés gomb
quit_button = Button(app, text="Kilépés", command=lambda:[app.quit()])
quit_button.grid(row=18, column=1, sticky=W, padx=10)

# Szekció törlése ablak fgv.-ek
# Törölhető szekciók lekérdezése
def get_deletable_sections():
    cursor.execute("SELECT id, szekcio_nev FROM szekciok WHERE id NOT IN (SELECT szekcio_id FROM cikkek UNION SELECT szekcio_id FROM eloadasok)")
    deletable_sections = cursor.fetchall()
    return deletable_sections

def can_delete_section(section_id):
    cursor.execute("SELECT 1 FROM cikkek WHERE szekcio_id = %s", (section_id,))
    has_articles = cursor.fetchone()

    cursor.execute("SELECT 1 FROM eloadasok WHERE szekcio_id = %s", (section_id,))
    has_presentations = cursor.fetchone()

    return not has_articles and not has_presentations

def delete_section(section_id):
    if can_delete_section(section_id):
        cursor.execute("DELETE FROM szekciok WHERE id = %s", (section_id,))
        db.commit()
        messagebox.showinfo("Sikeres törlés", "A szekció sikeresen törölve lett.")
    else:
        messagebox.showwarning("Törlés nem engedélyezett", "A szekciót nem lehet törölni, mert tartozik hozzá cikk vagy előadás.")

def szekcio_torlese_ablak():
    section_deletion_query = Tk()
    section_deletion_query.title("Szekció Törlése")
    section_deletion_query.geometry("600x400")

    # Létrehozunk egy Frame-et a görgetősáv és a lista számára
    frame = Frame(section_deletion_query)
    frame.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

    # Létrehozunk egy görgetősávot
    scrollbar = Scrollbar(frame, orient=VERTICAL)

    # Létrehozunk egy Treeview-ot a lista számára és hozzáadjuk a görgetősávot
    tree = ttk.Treeview(frame, columns=("ID", "Szekció"), show="headings", selectmode=EXTENDED)
    scrollbar.config(command=tree.yview)

    # Oszlopok beállítása
    tree.heading("ID", text="ID")
    tree.heading("Szekció", text="Szekció")

    # Adatok feltöltése a Treeview-be
    deletable_sections = get_deletable_sections()
    for row in deletable_sections:
        tree.insert("", "end", values=row)

    # Elhelyezzük a Treeview-ot és a görgetősávot a Frame-ben
    tree.grid(row=0, column=0)
    scrollbar.grid(row=0, column=1, sticky="ns")

    def delete_selected_sections():
        selected_items = tree.selection()
        if not selected_items:
            messagebox.showwarning("Nincs kiválasztva", "Kérem, válassza ki a törölni kívánt szekciókat.")
            return

        for item in selected_items:
            section_id = int(tree.item(item, "values")[0])
            delete_section(section_id)

        # Frissítjük a Treeview-t az új adatokkal (esetlegesen már törölt szekciókkal)
        tree.delete(*tree.get_children())
        deletable_sections = get_deletable_sections()
        for row in deletable_sections:
            tree.insert("", "end", values=row)

    # Törlés gomb
    delete_button = Button(section_deletion_query, text="Kiválasztott szekciók törlése", command=lambda:[play(),delete_selected_sections()])
    delete_button.grid(row=0, column=0, padx=10, pady=10)

    # Quit Button már megint
    quit_button = Button(section_deletion_query, text="Kilépés", command=lambda:[play(),section_deletion_query.destroy()])
    quit_button.grid(row=0, column=1, padx=10, pady=10)

# Függvény a felhasználó regisztrációjához
def regisztracio():
    app2 = Tk()
    app2.title("Konferencia Rendszer - Regisztráció")
    app2.iconbitmap('konfico.ico')
    app2.geometry("500x500")

    # Űrlap mezők és címkék a felhasználó regisztrációjához
    reg_felhnev_label = Label(app2, text="Felhasználónév:")
    reg_felhnev_label.grid(row=9, column=0, padx=10)
    reg_felhnev = Entry(app2)
    reg_felhnev.grid(row=9, column=1, padx=10)

    reg_jelszo_label = Label(app2, text="Jelszó:")
    reg_jelszo_label.grid(row=10, column=0, padx=10)
    reg_jelszo = Entry(app2, show="*")  # A jelszó mező tartalmát csillagokkal jelenítjük meg
    reg_jelszo.grid(row=10, column=1, padx=10)

    reg_jelszo_megerosites_label = Label(app2, text="Jelszó megerősítése:")
    reg_jelszo_megerosites_label.grid(row=11, column=0, padx=10)
    reg_jelszo_megerosites = Entry(app2, show="*")
    reg_jelszo_megerosites.grid(row=11, column=1, padx=10)

    # Űrlap mezők és címkék a felhasználó regisztrációjához
    reg_nev_label = Label(app2, text="Teljes Név:")
    reg_nev_label.grid(row=12, column=0, padx=10)
    reg_nev = Entry(app2)
    reg_nev.grid(row=12, column=1, padx=10)

    reg_elotag_label = Label(app2, text="Előtag (például: Dr.):")
    reg_elotag_label.grid(row=13, column=0, padx=10)
    reg_elotag = Entry(app2)
    reg_elotag.grid(row=13, column=1, padx=10)

    reg_intezmeny_label = Label(app2, text="Intézmény:")
    reg_intezmeny_label.grid(row=14, column=0, padx=10)
    reg_intezmeny = Entry(app2)
    reg_intezmeny.grid(row=14, column=1, padx=10)

    reg_email_label = Label(app2, text="Email:")
    reg_email_label.grid(row=15, column=0, padx=10)
    reg_email = Entry(app2)
    reg_email.grid(row=15, column=1, padx=10)

    def regisztracio_rendben():
        felhasznalonev = reg_felhnev.get()
        jelszo = reg_jelszo.get()
        jelszo_megerosites = reg_jelszo_megerosites.get()
        elotag = reg_elotag.get()
        teljes_nev = reg_nev.get()
        email = reg_email.get()
        intezmeny = reg_intezmeny.get()

        # Jelszó ellenőrzése
        if jelszo == jelszo_megerosites:
            # Jelszó titkosítása
            titkos_jelszo = hashlib.sha256(jelszo.encode()).hexdigest()

            # Felhasználó regisztrálása az adatbázisban
            cursor.execute("INSERT INTO felhasznalok (felhasznalonev, elotag, nev, email, intezmeny, hashed_jelszo) VALUES (%s, %s, %s, %s, %s, %s)", (felhasznalonev, elotag, teljes_nev, email, intezmeny, titkos_jelszo))
            db.commit()

            # Űrlap mezők ürítése
            reg_felhnev.delete(0, END)
            reg_jelszo.delete(0, END)
            reg_jelszo_megerosites.delete(0, END)
            reg_elotag.delete(0, END)
            reg_nev.delete(0, END)
            reg_email.delete(0, END)
            reg_intezmeny.delete(0, END)
            

            # Sikeres regisztráció üzenet
            messagebox.showinfo("Sikeres Regisztráció", "A regisztráció sikeres volt!")
        else:
            # Sikertelen regisztráció üzenet
            messagebox.showerror("Hiba", "A jelszavak nem egyeznek meg!")
    # Gomb a regisztrációhoz
    regisztracio_gomb = Button(app2, text="Regisztráció", command=lambda: [play(), regisztracio_rendben()])
    regisztracio_gomb.grid(row=18, column=0, padx=10)

    # Quit Button már megint
    quit_button = Button(app2, text="Kilépés", command=lambda: [play(), app2.destroy()])
    quit_button.grid(row=20, column=0, padx=10, pady=10)

# Bejelentkezes fgv.-ek
def is_admin(username):
    cursor.execute("SELECT szerepkor FROM felhasznalok WHERE felhasznalonev = %s", (username,))
    result = cursor.fetchone()
    if result and result[0] == "adminisztrátor":  # A szerepkor mező értéke admin, ha a felhasználó admin
        return True
    return False

def bejelentkezes():
    app3 = Tk()
    app3.title("Konferencia Rendszer - Bejelentkezés")
    app3.iconbitmap('konfico.ico')
    app3.geometry("500x300")

    # Űrlap mezők és címkék a bejelentkezéshez
    bejelentkezes_nev_label = Label(app3, text="Felhasználónév:")
    bejelentkezes_nev_label.grid(row=0, column=0, padx=10)
    bejelentkezes_nev = Entry(app3)
    bejelentkezes_nev.grid(row=0, column=1, padx=10)

    bejelentkezes_jelszo_label = Label(app3, text="Jelszó:")
    bejelentkezes_jelszo_label.grid(row=1, column=0, padx=10)
    bejelentkezes_jelszo = Entry(app3, show="*")  # A jelszó mező tartalmát csillagokkal jelenítjük meg
    bejelentkezes_jelszo.grid(row=1, column=1, padx=10)

    def bejelentkezes_rendben():
        felhasznalonev = bejelentkezes_nev.get()
        jelszo = bejelentkezes_jelszo.get()

        # Jelszó titkosítása
        titkos_jelszo = hashlib.sha256(jelszo.encode()).hexdigest()

        # Felhasználó ellenőrzése
        cursor.execute("SELECT * FROM felhasznalok WHERE felhasznalonev = %s AND hashed_jelszo = %s", (felhasznalonev, titkos_jelszo))
        regisztralt_felhasznalo = cursor.fetchone()

        if regisztralt_felhasznalo:
            # Sikeres bejelentkezés üzenet
            bejelentkezett = 1
            regisztracio_gomb.config(state="disabled")
            regisztracio_gomb.grid_forget()
            bejel_gomb.config(state="disabled")
            bejel_gomb.grid_forget()         
            # Kijelentkezés gomb, stb.
            if bejelentkezett == 1:
                cikk_hozzaadas_gomb.config(state="normal")
                cikk_hozzaadas_gomb.grid(row=2, column=0, columnspan=3, padx=10)

                cikk_cim_label.config(state="normal")
                cikk_cim_label.grid(row=0, column=0, padx=10)

                cikk_cim.config(state="normal")
                cikk_cim.grid(row=0, column=1, padx=10)

                szerzo_label.config(state="normal")
                szerzo_label.grid(row=1, column=0, padx=10)

                szerzo_id.config(state="normal")
                szerzo_id.grid(row=1, column=1, padx=10)

                cikk_id_label.config(state="normal")
                cikk_id_label.grid(row=5, column=0, padx=10)

                cikk_id.config(state="normal")
                cikk_id.grid(row=5, column=1, padx=10)

                uj_cikk_cim_label.config(state="normal")
                uj_cikk_cim_label.grid(row=6, column=0, padx=10)

                uj_cikk_cim.config(state="normal")
                uj_cikk_cim.grid(row=6, column=1, padx=10)

                cikk_torles_gomb.config(state="normal")
                cikk_torles_gomb.grid(row=7, column=0, columnspan=2, padx=10)

                cikk_frissites_gomb.config(state="normal")
                cikk_frissites_gomb.grid(row=8, column=0, columnspan=2, padx=10)

                eloadas_torlese_gomb.config(state="normal")
                eloadas_torlese_gomb.grid(row=12, column=4, padx=10)

                kijel_gomb.config(state="normal")
                kijel_gomb.grid(row=16, column=4, padx=10)

            messagebox.showinfo("Sikeres Bejelentkezés", "A bejelentkezés sikeres volt! " + str(bejelentkezett))
            if is_admin(felhasznalonev):
                print("Az adminisztrátor bejelentkezett.")
                szekcio_torlese_button.config(state="normal")
                szekcio_torlese_button.grid(row=8, column=4, padx=10)
            else:
                print("Nem adminisztrátor jelentkezett be.")
            app3.destroy()
        else:
            # Sikertelen bejelentkezés üzenet
            bejelentkezett = 0
            messagebox.showerror("Hiba", "Hibás felhasználónév vagy jelszó! " + str(bejelentkezett))

    # Gomb a bejelentkezéshez
    bejelentkezes_gomb = Button(app3, text="Bejelentkezés", command=lambda: [play(), bejelentkezes_rendben()])
    bejelentkezes_gomb.grid(row=2, column=0, pady=10)

    # Quit Button már megint
    quit_button = Button(app3, text="Kilépés", command=lambda: [play(), app3.destroy()])
    quit_button.grid(row=4, column=0, padx=10, pady=10)

# Kijelentkezes Fgv.
def kijelentkezes():
    bejelentkezett = 0

    cikk_hozzaadas_gomb.config(state="disabled")
    cikk_hozzaadas_gomb.grid_forget()

    cikk_cim_label.config(state="disabled")
    cikk_cim_label.grid_forget()

    cikk_cim.config(state="disabled")
    cikk_cim.grid_forget()

    szerzo_label.config(state="disabled")
    szerzo_label.grid_forget()

    szerzo_id.config(state="disabled")
    szerzo_id.grid_forget()

    cikk_id_label.config(state="disabled")
    cikk_id_label.grid_forget()

    cikk_id.config(state="disabled")
    cikk_id.grid_forget()

    uj_cikk_cim_label.config(state="disabled")
    uj_cikk_cim_label.grid_forget()

    uj_cikk_cim.config(state="disabled")
    uj_cikk_cim.grid_forget()

    cikk_torles_gomb.config(state="disabled")
    cikk_torles_gomb.grid_forget()

    cikk_frissites_gomb.config(state="disabled")
    cikk_frissites_gomb.grid_forget()

    szekcio_torlese_button.config(state="disabled")
    szekcio_torlese_button.grid_forget()

    eloadas_torlese_gomb.config(state="disabled")
    eloadas_torlese_gomb.grid_forget()

    regisztracio_gomb.config(state="normal")
    regisztracio_gomb.grid(row=9, column=4, padx=10)

    bejel_gomb.config(state="normal")
    bejel_gomb.grid(row=12, column=4, padx=10)

    kijel_gomb.config(state="disabled")
    kijel_gomb.grid_forget()
    messagebox.showinfo("Sikeres Kijelentkezés", "A kijelentkezés sikeres volt! " + str(bejelentkezett))

# Gomb a regisztráció kezdéséhez
regisztracio_gomb = Button(app, text="Regisztráció", command=lambda: [play(), regisztracio()])
regisztracio_gomb.grid(row=12, column=4, padx=10)

# Gomb a bejelentkezéshez
bejel_gomb = Button(app, text="Bejelentkezes", command=lambda: [play(), bejelentkezes()])
bejel_gomb.grid(row=15, column=4, padx=10)


kijel_gomb = Button(app, text="Kijelentkezés", command=lambda: [play(), kijelentkezes()])

# Űrlap mezők és címkék a cikk hozzáadásához
cikk_cim_label = Label(app, text="Cikk Címe:")
cikk_cim = Entry(app)

szerzo_label = Label(app, text="Szerző ID:")
szerzo_id = Entry(app)

# Függvény az új cikk hozzáadásához
def uj_cikk():
    try:
        cikk_cim_text = cikk_cim.get()
        szerzo_id_text = szerzo_id.get()
        cursor.execute("INSERT INTO cikkek (cikk_cim, szerzo_id) VALUES (%s, %s)", (cikk_cim_text, szerzo_id_text))
        db.commit()
        cikk_cim.delete(0, END)
        szerzo_id.delete(0, END)
        cikkek_betoltes()
    except IntegrityError as e:
        # Handle IntegrityError
        handle_integrity_error(e)

# Gomb a cikk hozzáadásához
cikk_hozzaadas_gomb = Button(app, text="Cikk Hozzáadása", command=lambda:[play(),uj_cikk()])

app.mainloop()

# Kapcsolat lezárása a program befejezése után
cursor.close()
db.close()
