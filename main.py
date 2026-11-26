from datetime import datetime
from fastapi import FastAPI
import sqlite3
from fastapi.responses import FileResponse

connection = sqlite3.connect("database.db")
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS sessies (id INTEGER PRIMARY KEY AUTOINCREMENT, datum TEXT, start_tijd TEXT, eind_tijd TEXT, duur_minuten INTEGER)")

app = FastAPI()

@app.get("/")
def home():
    return FileResponse("index.html")

@app.post("/start")
def start():
    nu = datetime.now()
    datum = nu.strftime("%Y-%m-%d")
    tijd = nu.strftime("%H-%M-%S")
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM sessies")
    rij = cursor.fetchall()
    if len(rij) > 0 and rij[-1][-1] is None:
        connection.close()
        return {"bericht": "Er loopt al een timer! Druk eerst op Stop."}
    cursor.execute("INSERT INTO sessies (datum, start_tijd) VALUES (?, ?)", (datum, tijd))
    connection.commit()
    connection.close()
    return {"bericht": f"Timer gestart om {tijd}!"}

@app.post("/stop")
def stop():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM sessies")
    rijen = cursor.fetchall()
    if len(rijen) == 0:
        connection.close()
        return {"bericht": "Geen lopende timer!"}
    else:
        laatste_rij = rijen[-1]
        sessie_id = laatste_rij[0]
        start_tijd = laatste_rij[2]
        nu = datetime.now()
        eind_tijd = nu.strftime("%H-%M-%S")
        t1 = datetime.strptime(start_tijd, "%H-%M-%S")
        t2 = datetime.strptime(eind_tijd, "%H-%M-%S")
        minuten = int((t2- t1).total_seconds() // 60)
        cursor.execute("UPDATE sessies SET  eind_tijd = ?, duur_minuten = ? WHERE id = ?", (eind_tijd, minuten, sessie_id))
        connection.commit()
        connection.close()
        return {"bericht": f"Gestopt om {eind_tijd}. Duur: {minuten} minuten.!"}

@app.get("/overzicht")
def overzicht():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM sessies")
    rijen = cursor.fetchall()
    connection.close()
    totaal_minuten = 0
    for rij in rijen:
        if rij[4] is not None:
            totaal_minuten += rij[4]
    totaal_uren = round(totaal_minuten / 60, 2)
    return {"bericht": f"Totaal uren: {totaal_uren}, totaal minuten: {totaal_minuten}", "alle_sessies": rijen}
