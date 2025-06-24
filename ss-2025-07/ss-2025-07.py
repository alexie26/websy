"""Webbasierte Systeme - Gruppe 07
"""
# Import benötigter Flask-Module
from flask import Flask, render_template, request, g, redirect, url_for, session, flash
from functools import wraps
from werkzeug.utils import secure_filename
import os


# Import MySQL-Connector
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

# Import der Verbindungsinformationen zur Datenbank:
# Variable DB_HOST: Servername des MySQL-Servers
# Variable DB_USER: Nutzername
# Variable DB_PASSWORD: Passwort
# Variable DB_DATABASE: Datenbankname
from db.db_credentials import DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE

# extras fur Terminverwaltung
from datetime import datetime, timedelta
from calendar import monthrange
import calendar

app = Flask(__name__)
app.secret_key = "pjfjojefjiejifjiewohfihrieugffuifhoihi"

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

#   Datenbank connection    #
@app.before_request
def before_request():
    """ Verbindung zur Datenbank herstellen """
    g.con = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD,
                                    database=DB_DATABASE)

@app.teardown_request
def teardown_request(exception):
    """ Verbindung zur Datenbank trennen """
    con = getattr(g, 'con', None)
    if con is not None:
        con.close()

#helfer funktionen
def extract_form_data(request):
    return {
        'vorname': request.form.get('vorname', '').strip(),
        'nachname': request.form.get('nachname', '').strip(),
        'email': request.form.get('email', '').strip(),
        'benutzername': request.form.get('benutzername', '').strip(),
        'password': request.form.get('password', '').strip(),
        'telefon': request.form.get('telefon', '').strip(),
        'strasse': request.form.get('strasse', '').strip(),
        'hausnummer': request.form.get('hausnummer', '').strip(),
        'plz': request.form.get('plz', '').strip(),
        'ort': request.form.get('ort', '').strip(),
        'rolle': request.form.get('rolle', '').strip()
    }


def insert_nutzer(cursor, form_data):
    cursor.execute("""
        INSERT INTO Nutzer (
            Vorname, Nachname, EMail, Strasse, 
            Hausnummer, PLZ, ORT, Telefon
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        form_data['vorname'],
        form_data['nachname'],
        form_data['email'],
        form_data['strasse'],
        form_data['hausnummer'],
        form_data['plz'],
        form_data['ort'],
        form_data['telefon']
    ))

    return cursor.lastrowid


def insert_login(cursor, form_data, nutzer_id):
    hashed_password = generate_password_hash(form_data['password'])

    cursor.execute("""
        INSERT INTO Login (
            Benutzername, Passwort, Rolle, FK_Nutzer_ID
        ) VALUES (%s, %s, %s, %s)
    """, (
        form_data['benutzername'],
        hashed_password,
        form_data['rolle'],
        nutzer_id
    ))

    return cursor.lastrowid


def validate_form_data(form_data, required_fields):
    missing_fields = []
    for field in required_fields:
        if not form_data.get(field):
            missing_fields.append(field)

    return missing_fields


def generate_time_slots(start_hour=9, end_hour=17, interval_minutes=30):
    slots = []
    current_time = datetime.strptime(f"{start_hour}:00", "%H:%M")
    end_time = datetime.strptime(f"{end_hour}:00", "%H:%M")

    while current_time < end_time:
        slots.append(current_time.strftime("%H:%M"))
        current_time += timedelta(minutes=interval_minutes)

    return slots


def is_past_date(date_string):
    try:
        date_obj = datetime.strptime(date_string, "%Y-%m-%d").date()
        return date_obj < datetime.now().date()
    except ValueError:
        return True  # Bei ungültigem Datum als "vergangen" betrachten

# decorators
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'nutzer_id' not in session or session.get('rolle') != 'Admin':
            flash('Zugriff verweigert: Nur für Admins!', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'nutzer_id' not in session:
            flash('Bitte einloggen', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ab hier alles routes

@app.route('/')
def startseite():
    cursor = g.con.cursor(dictionary=True)
    cursor.execute("""
    SELECT Titel, Beschreibung, Dauer, Preise, Bild
    FROM Dienstleistungen
    """)
    services = cursor.fetchall()
    cursor.close()
    return render_template('index.html', services=services)

@app.route("/asidiropou")
def asidiropou_profil():
    return render_template("asidiropou.html")

@app.route('/Bsaifo')
def bsaifo():
    cursor = g.con.cursor(dictionary=True)
    cursor.execute('SELECT * FROM Bsaifo')
    daten = cursor.fetchall()
    print(daten)
    cursor.close()
    return render_template('Bsaifo.html', daten=daten)


@app.route('/galkudsy')
def galkudsy():
    cursor = g.con.cursor(dictionary=True)
    cursor.execute('Select id, beschreibung From galkudsy')  # sql Befehl erwarten
    daten = cursor.fetchall()
    cursor.close()
    return render_template('galkudsy.html', daten=daten)

@app.route('/alexandra')
def alexandra():
    cursor = g.con.cursor(dictionary=True)
    cursor.execute('SELECT * FROM mrosu')
    data = cursor.fetchall()
    print(data)
    cursor.close()
    return render_template('alexandra.html', data=data)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        benutzername = request.form['benutzername']
        password = request.form['password']

        try:
            cursor = g.con.cursor(dictionary=True)
            cursor.execute('''
            SELECT l.*, n.Vorname, n.Nachname
            FROM Login l
            JOIN Nutzer n ON l.FK_Nutzer_ID = n.Nutzer_ID
            WHERE l.Benutzername = %s
            ''', (benutzername,))
            user = cursor.fetchone()
        except mysql.connector.Error as err:
            flash('Datenbankfehler', 'danger')
            return redirect(url_for('login'))
        finally:
            cursor.close()

        if user and check_password_hash(user['Passwort'], password):  # Passwort mit dem Hash vergleichen
            session['user_id'] = user['Login_ID']
            session['benutzername'] = user['Benutzername']
            session['rolle'] = user['Rolle']
            session['nutzer_id'] = user['FK_Nutzer_ID']
            session['ganze_name'] = f"{user['Vorname']} {user['Nachname']}"

            flash('Login erfolgreich!', 'success')

            if session['rolle'] == 'Admin':
                return redirect(url_for('admin_dashboard'))
            elif session['rolle'] == 'Anbieter':
                return redirect(url_for('unternehmensprofil'))
            else:
                return redirect(url_for('nutzerprofil'))
        else:
            flash('Benutzername oder Passwort falsch', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('Sie wurden erfolgreich ausgeloggt', "info")
    return redirect(url_for('startseite'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        form_data = extract_form_data(request)
        cursor = g.con.cursor()

        try:
            if not form_data['vorname'] or not form_data['nachname'] or not form_data['email'] or not form_data['benutzername'] or not form_data['password']:
                flash("Bitte alle Pflichtfelder ausfuellen", "danger")
                return redirect(url_for('register'))

            if not form_data['rolle'] or form_data['rolle'] not in ['Nutzer', 'Anbieter']:
                flash("Bitte eine Rolle auswaehlen", "danger")
                return redirect(url_for('register'))

            nutzer_id = insert_nutzer(cursor, form_data)
            insert_login(cursor, form_data, nutzer_id)

            if form_data['rolle'] == 'Anbieter':
                login_id = cursor.lastrowid
                cursor.execute("""
                INSERT INTO Unternehmensprofil (
                Titel, Beschreibung, EMail, Telefonnumer,
                Adresse, Hausnummer, PLZ, Ort, FK_Login_ID
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    f"{form_data['vorname']} {form_data['nachname']}",
                    "Beschreibung wird noch hinzugefugt...",
                    form_data['email'],
                    form_data['telefon'],
                    form_data['strasse'],
                    form_data['hausnummer'],
                    form_data['plz'],
                    form_data['ort'],
                    login_id
                ))
            g.con.commit()

            success_message = "Registrierung erfolgreich"
            if form_data['rolle'] == 'Anbieter':
                success_message += "Sie konnen sich jetzt einlogen und Ihr Unternehmensprofil vervollstandigen"

            flash(success_message, "success")
            return redirect(url_for('login'))

        except mysql.connector.IntegrityError as e:
            g.con.rollback()
            if "Duplicate entry" in str(e):
                if "Benutzername" in str(e):
                    flash("Dieser Benutzername ist bereits gegeben", "danger")
                elif "EMail" in str(e):
                    flash("Diese E-Mail ist bereits registriert", "danger")
                else:
                    flash("Benutzername oder E-Mail bereits existiert", "danger")
            else:
                flash("Registrierung fehler", "danger")
            return redirect(url_for('register'))
        except Exception as e:
            g.con.rollback()
            flash(f"Ein fehler ist aufgetreten: {str(e)}", "danger")
            return redirect(url_for('register'))
        finally:
            cursor.close()
    return render_template('register_auswahl.html')


@app.route('/register/nutzer', methods=['GET', 'POST'])
def register_nutzer():
    if request.method == 'POST':
        form_data = extract_form_data(request)
        form_data['rolle'] = 'Nutzer'

        cursor = g.con.cursor()
        try:
            # Check all required fields including address and phone
            required_fields = ['vorname', 'nachname', 'email', 'benutzername', 'password',
                             'telefon', 'strasse', 'hausnummer', 'plz', 'ort']
            missing_fields = [field for field in required_fields if not form_data.get(field)]

            if missing_fields:
                flash(f"Bitte füllen Sie alle Pflichtfelder aus: {', '.join(missing_fields)}", "danger")
                return redirect(url_for('register_nutzer'))

            nutzer_id = insert_nutzer(cursor, form_data)
            insert_login(cursor, form_data, nutzer_id)

            g.con.commit()
            flash("Registrierung als Nutzer erfolgreich!", "success")
            return redirect(url_for('login'))

        except mysql.connector.IntegrityError as e:
            g.con.rollback()
            if "Duplicate entry" in str(e):
                if "Benutzername" in str(e):
                    flash("Dieser Benutzername ist bereits vergeben", "danger")
                elif "EMail" in str(e):
                    flash("Diese E-Mail ist bereits registriert", "danger")
                else:
                    flash("Benutzername oder E-Mail bereits existiert", "danger")
            else:
                flash("Registrierungsfehler aufgrund von Datenbankbeschränkungen", "danger")
            return redirect(url_for('register_nutzer'))
        except Exception as e:
            g.con.rollback()
            flash(f"Registrierungsfehler: {str(e)}", "danger")
            return redirect(url_for('register_nutzer'))
        finally:
            cursor.close()

    return render_template("register_nutzer.html")


@app.route('/register/anbieter', methods=['GET', 'POST'])
def register_anbieter():
    if request.method == 'POST':
        form_data = extract_form_data(request)
        form_data['rolle'] = 'Anbieter'

        cursor = g.con.cursor()
        try:
            required_fields = ['vorname', 'nachname', 'email', 'benutzername', 'password', 'telefon', 'strasse',
                               'hausnummer', 'plz', 'ort']
            missing_fields = [field for field in required_fields if not form_data.get(field)]

            if missing_fields:
                flash(f"Bitte füllen Sie alle Pflichtfelder aus: {', '.join(missing_fields)}", "danger")
                return redirect(url_for('register_anbieter'))

            nutzer_id = insert_nutzer(cursor, form_data)
            insert_login(cursor, form_data, nutzer_id)

            login_id = cursor.lastrowid
            cursor.execute("""
                INSERT INTO Unternehmensprofil (
                    Titel, Beschreibung, EMail, Telefonnummer, 
                    Adresse, Hausnummer, PLZ, Ort, FK_Login_ID
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                f"{form_data['vorname']} {form_data['nachname']}",
                "Bitte vervollständigen Sie Ihr Unternehmensprofil...",
                form_data['email'],
                form_data['telefon'],
                form_data['strasse'],
                form_data['hausnummer'],
                form_data['plz'],
                form_data['ort'],
                login_id
            ))

            g.con.commit()
            flash("Registrierung als Anbieter erfolgreich! Vervollständigen Sie jetzt Ihr Unternehmensprofil.",
                  "success")
            return redirect(url_for('login'))

        except mysql.connector.IntegrityError:
            g.con.rollback()
            flash("Benutzername oder E-Mail existiert bereits", "danger")
            return redirect(url_for('register_anbieter'))
        except Exception as e:
            g.con.rollback()
            flash(f"Registrierungsfehler: {str(e)}", "danger")
            return redirect(url_for('register_anbieter'))
        finally:
            cursor.close()

    return render_template("register_anbieter.html")



@app.route('/admin')
@admin_required
def admin_dashboard():
    cursor = g.con.cursor(dictionary=True)
    cursor.execute("""
        SELECT l.Login_ID, l.Benutzername, l.Rolle, 
               n.Vorname, n.Nachname, n.Email 
        FROM Login l 
        JOIN Nutzer n ON l.FK_Nutzer_ID = n.Nutzer_ID
    """)
    benutzerliste = cursor.fetchall()
    cursor.close()

    return render_template('admin.html', benutzerliste=benutzerliste)





# ---------- BENUTZER BEARBEITEN ----------------
@app.route('/admin/user/edit/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    cursor = g.con.cursor(dictionary=True)

    if request.method == 'POST':
        rolle = request.form['rolle']
        benutzername = request.form['benutzername']
        vorname = request.form['vorname']
        nachname = request.form['nachname']
        email = request.form['email']
        straße = request.form['straße']
        hausnummer = request.form['hausnummer']
        plz = request.form['plz']
        ort = request.form['ort']
        telefon = request.form['telefon']
        profilbild = request.form.get('profilbild')  # optionales Feld

        cursor.execute("""
            UPDATE Login SET
                Rolle = %s,
                Benutzername = %s,
                Vorname = %s,
                Nachname = %s,
                EMail = %s,
                Straße = %s,
                Hausnummer = %s,
                PLZ = %s,
                Ort = %s,
                Telefon = %s,
                Profilbild = %s
            WHERE Login_ID = %s
        """, (
            rolle,
            benutzername,
            vorname,
            nachname,
            email,
            straße,
            hausnummer,
            plz,
            ort,
            telefon,
            profilbild,
            user_id
        ))

        g.con.commit()
        flash("Benutzer wurde erfolgreich aktualisiert.", "success")
        return redirect(url_for('admin_dashboard'))

    # GET-Request – lade bestehende Daten für das Formular
    cursor.execute("SELECT * FROM Login WHERE Login_ID = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    return render_template('admin Bearbeitung.html', user=user)


# ---------- BENUTZER LÖSCHEN -------------------
@app.route('/admin/user/delete/<int:user_id>', methods=['POST'])
@admin_required
def delete_user(user_id):
    cursor = g.con.cursor()
    cursor.execute("DELETE FROM Login WHERE Login_ID = %s", (user_id,))
    g.con.commit()
    cursor.close()
    flash("Benutzer gelöscht", "info")
    return redirect(url_for('admin_dashboard'))





# ---------- FOTOGALERIE ------------------------
@app.route('/admin/fotos')
@admin_required
def fotos_list():
    cursor = g.con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Fotos")
    fotos = cursor.fetchall()
    cursor.close()
    return render_template('index.html', fotos=fotos)

@app.route('/admin/fotos/neu', methods=['GET', 'POST'])
@admin_required
def foto_neu():
    if request.method == 'POST':
        titel = request.form['titel']
        beschreibung = request.form['beschreibung']
        bild_url = request.form['bild_url']
        cursor = g.con.cursor()
        cursor.execute("INSERT INTO Fotos (Titel, Beschreibung, Bild_URL) VALUES (%s, %s, %s)",
                       (titel, beschreibung, bild_url))
        g.con.commit()
        cursor.close()
        flash("Foto hinzugefügt", "success")
        return redirect(url_for('fotos_list'))
    return render_template('foto_form.html')

services = [
    {"name": "Kosmetikstudio und Hautpflege", "image": "kosmetik.jpg"},
    {"name": "Frisuren und Coloration", "image": "frisur.jpg"},
    {"name": "Massagen", "image": "massage.jpg"},
    {"name": "Lashes und Waxing", "image": "lashes.jpg"},
    {"name": "Hand- und Fußpflege", "image": "handfuss.jpg"},
    {"name": "Wimpern & Augenbrauen", "image": "wimpern.jpg"},
]



"""
@app.route('/nutzerprofil', methods=['GET', 'POST'])
@login_required
def nutzerprofil():
    cursor = g.con.cursor(dictionary=True)
    nutzer_id = session.get('nutzer_id')  # aus der Session
    cursor.execute("SELECT * FROM Nutzer WHERE Nutzer_ID = %s", (nutzer_id,))
    nutzer = cursor.fetchone()
    cursor.close()
    return render_template('nutzerprofil.html', nutzer=nutzer)"""

@app.route('/nutzerprofil', methods=['GET', 'POST'])
@login_required
def nutzerprofil():
    nutzer_id = session.get('nutzer_id')

    if not nutzer_id:
        flash("Nicht eingeloggt", "danger")
        return redirect(url_for('login'))

    try:
        cursor = g.con.cursor(dictionary=True)

        if request.method == 'POST':
            # Neue Daten aus dem Formular holen
            vorname = request.form['Vorname']
            nachname = request.form['Nachname']
            email = request.form['EMail']
            strasse = request.form['Strasse']
            hausnummer = request.form['Hausnummer']
            plz = request.form['PLZ']
            ort = request.form['ORT']
            telefon = request.form['Telefon']

            # Update durchführen
            update_query = '''
                UPDATE Nutzer
                SET Vorname=%s, Nachname=%s, EMail=%s, Strasse=%s,
                    Hausnummer=%s, PLZ=%s, ORT=%s, Telefon=%s
                WHERE Nutzer_ID = %s
            '''
            cursor.execute(update_query, (vorname, nachname, email, strasse,
                                          hausnummer, plz, ort, telefon, nutzer_id))
            g.con.commit()
            flash("Profil erfolgreich aktualisiert!", "success")
            return redirect(url_for('nutzerprofil'))

        # Beim GET: Daten aus der Datenbank holen
        cursor.execute("SELECT * FROM Nutzer WHERE Nutzer_ID = %s", (nutzer_id,))
        nutzer = cursor.fetchone()

    except mysql.connector.Error as err:
        flash("Datenbankfehler beim Laden oder Speichern", "danger")
        nutzer = {}
    finally:
        cursor.close()

    return render_template('nutzerprofil.html', nutzer=nutzer)



@app.route("/unternehmensprofil")
def unternehmensprofil():
    cursor = g.con.cursor(dictionary=True)
    try:
        cursor.execute("""
        SELECT Titel, Beschreibung, EMail, Telefonnummer, Adresse, Hausnummer, PLZ, Ort
        From Unternehmensprofil
        """)
        result = cursor.fetchall()
        profil = result[0] if result else None

        return render_template("unternehmensprofil.html", profil=profil)
    finally:
        cursor.close()

#unternehmensprofil speichern
@app.route('/anbieter/profil_speichern', methods=['POST'])
@login_required
def profil_speichern():
    beschreibung = request.form.get('beschreibung')
    profilbild = request.files.get('profilbild')

    if not beschreibung or not profilbild:
        flash('Bitte alle Felder ausfüllen!', 'danger')
        return redirect(url_for('unternehmensprofil'))

    dateiname = profilbild.filename
    profilbild.save(f'static/uploads/{dateiname}')

    cursor = g.con.cursor()
    cursor.execute("""
        INSERT INTO Unternehmensprofil (Beschreibung, Bild, Nutzer_ID)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE Beschreibung = %s, Bild = %s
    """, (beschreibung, dateiname, session['nutzer_id'], beschreibung, dateiname))
    g.con.commit()
    cursor.close()

    flash('Profil gespeichert!', 'success')
    return redirect(url_for('unternehmensprofil'))

#dienstleistungen speichern
@app.route('/anbieter/dienstleistung/hinzufuegen', methods=['POST'])
@login_required
def dienstleistung_hinzufuegen():
    titel = request.form.getlist('titel[]')
    beschreibung = request.form.getlist('beschreibung[]')
    dauer = request.form.getlist('dauer[]')
    preis = request.form.getlist('preis[]')

    if not all([titel, beschreibung, dauer, preis]) or not all(titel) or not all(beschreibung):
        flash('Bitte alle Felder für jede Dienstleistung ausfüllen!', 'danger')
        return redirect(url_for('unternehmensprofil'))

    cursor = g.con.cursor()
    for i in range(len(titel)):
        cursor.execute("""
            INSERT INTO Dienstleistungen (Titel, Beschreibung, Dauer, Preis, Anbieter_ID)
            VALUES (%s, %s, %s, %s, %s)
        """, (titel[i], beschreibung[i], dauer[i], preis[i], session['nutzer_id']))
    g.con.commit()
    cursor.close()

    flash('Dienstleistungen hinzugefügt!', 'success')
    return redirect(url_for('unternehmensprofil'))


# Zusätzliche Imports (fügen Sie diese zu Ihren bestehenden Imports hinzu)
from datetime import datetime, timedelta
from calendar import monthrange
import calendar


# Route für die Terminverwaltung
@app.route('/terminverwaltung')
@app.route('/terminverwaltung/<int:monat>/<int:jahr>')
@login_required
def terminverwaltung(monat=None, jahr=None):
    if monat is None:
        monat = datetime.now().month
    if jahr is None:
        jahr = datetime.now().year

    cursor = g.con.cursor(dictionary=True)

    try:
        # Kalender-Daten vorbereiten
        kalender_daten = prepare_calendar_data(monat, jahr)

        # Dienstleistungen laden
        if session.get('rolle') == 'Anbieter':
            cursor.execute("""
                SELECT * FROM Dienstleistungen 
                WHERE FK_Login_ID = %s
            """, (session.get('user_id'),))
        else:
            cursor.execute("SELECT * FROM Dienstleistungen")

        dienstleistungen = cursor.fetchall()

        # Termine für den aktuellen Monat laden
        termine_data = load_termine_for_month(cursor, monat, jahr)

        # Template-Daten zusammenstellen
        template_data = {
            'kalender_tage': kalender_daten['tage'],
            'aktueller_monat': kalender_daten['monat_name'],
            'aktuelles_jahr': jahr,
            'vorheriger_monat': kalender_daten['prev_monat'],
            'vorheriges_jahr': kalender_daten['prev_jahr'],
            'naechster_monat': kalender_daten['next_monat'],
            'naechstes_jahr': kalender_daten['next_jahr'],
            'dienstleistungen': dienstleistungen
        }

        # Rollenspezifische Daten
        if session.get('rolle') == 'Anbieter':
            template_data['anbieter_name'] = session.get('ganze_name')
            template_data['aktuelle_termine'] = get_anbieter_termine(cursor)
        else:
            template_data['meine_termine'] = get_nutzer_termine(cursor)

        return render_template('terminverwaltung.html', **template_data)

    finally:
        cursor.close()


def prepare_calendar_data(monat, jahr):
    """Bereitet die Kalenderdaten für die Anzeige vor"""
    monat_name = calendar.month_name[monat]

    # Vorheriger und nächster Monat
    prev_monat = monat - 1 if monat > 1 else 12
    prev_jahr = jahr if monat > 1 else jahr - 1
    next_monat = monat + 1 if monat < 12 else 1
    next_jahr = jahr if monat < 12 else jahr + 1

    # Kalender-Grid erstellen
    cal = calendar.monthcalendar(jahr, monat)

    # Kalender-Daten für Template formatieren
    kalender_tage = []
    for woche in cal:
        woche_data = []
        for tag in woche:
            if tag == 0:
                woche_data.append({'datum': None, 'tag': None, 'termine': [], 'verfuegbare_slots': []})
            else:
                datum = f"{jahr}-{monat:02d}-{tag:02d}"
                woche_data.append({
                    'datum': datum,
                    'tag': tag,
                    'termine': [],  # Wird später gefüllt
                    'verfuegbare_slots': []  # Wird später gefüllt
                })
        kalender_tage.append(woche_data)

    return {
        'tage': kalender_tage,
        'monat_name': monat_name,
        'prev_monat': prev_monat,
        'prev_jahr': prev_jahr,
        'next_monat': next_monat,
        'next_jahr': next_jahr
    }


def load_termine_for_month(cursor, monat, jahr):
    """Lädt alle Termine für den angegebenen Monat"""
    cursor.execute("""
        SELECT 
            t.Termin_ID,
            t.Status,
            t.Uhrzeit,
            t.Datum,
            n.Vorname,
            n.Nachname,
            d.Titel as dienstleistung,
            u.Titel as unternehmen
        FROM Termin t
        LEFT JOIN Nutzer n ON t.FK_Nutzer_ID = n.Nutzer_ID
        LEFT JOIN Dienstleistungen d ON t.FK_Dienstleistung_ID = d.Dienstleistung_ID
        LEFT JOIN Unternehmensprofil u ON d.FK_Login_ID = u.FK_Login_ID
        WHERE YEAR(t.Datum) = %s AND MONTH(t.Datum) = %s
        ORDER BY t.Datum, t.Uhrzeit
    """, (jahr, monat))

    return cursor.fetchall()


def get_anbieter_termine(cursor):
    """Holt aktuelle Termine für Anbieter"""
    cursor.execute("""
        SELECT 
            t.Termin_ID,
            t.Status,
            t.Uhrzeit,
            t.Datum,
            CONCAT(n.Vorname, ' ', n.Nachname) as kunde_name,
            d.Titel as dienstleistung
        FROM Termin t
        JOIN Nutzer n ON t.FK_Nutzer_ID = n.Nutzer_ID
        JOIN Dienstleistungen d ON t.FK_Dienstleistung_ID = d.Dienstleistung_ID
        WHERE d.FK_Login_ID = %s 
        AND t.Datum >= CURDATE()
        ORDER BY t.Datum, t.Uhrzeit
        LIMIT 10
    """, (session.get('user_id'),))

    return cursor.fetchall()


def get_nutzer_termine(cursor):
    """Holt Termine für den aktuellen Nutzer"""
    cursor.execute("""
        SELECT 
            t.Termin_ID,
            t.Status,
            t.Uhrzeit,
            t.Datum,
            d.Titel as dienstleistung,
            u.Titel as unternehmen
        FROM Termin t
        JOIN Dienstleistungen d ON t.FK_Dienstleistung_ID = d.Dienstleistung_ID
        JOIN Unternehmensprofil u ON d.FK_Login_ID = u.FK_Login_ID
        WHERE t.FK_Nutzer_ID = %s
        AND t.Datum >= CURDATE()
        ORDER BY t.Datum, t.Uhrzeit
    """, (session.get('nutzer_id'),))

    return cursor.fetchall()


# Route für Terminbuchung (überarbeitet)
@app.route('/termin_buchen', methods=['POST'])
@login_required
def termin_buchen():
    if session.get('rolle') != 'Nutzer':
        return {'success': False, 'message': 'Nur Nutzer können Termine buchen'}, 403

    dienstleistung_id = request.form.get('dienstleistung_id')
    datum = request.form.get('datum')
    uhrzeit = request.form.get('uhrzeit')
    nutzer_id = session.get('nutzer_id')

    if not all([dienstleistung_id, datum, uhrzeit, nutzer_id]):
        return {'success': False, 'message': 'Alle Felder sind erforderlich'}, 400

    cursor = g.con.cursor()
    try:
        # Prüfen ob der Zeitslot noch verfügbar ist
        # Prüfen ob der Zeitslot noch verfügbar ist (Status NULL = freier Slot)
        cursor.execute("""
                SELECT Termin_ID FROM Termin
                WHERE Datum = %s AND Uhrzeit = %s
                  AND FK_Dienstleistung_ID = %s
                  AND Status IS NULL
                LIMIT 1
            """, (datum, uhrzeit, dienstleistung_id))
        slot = cursor.fetchone()

        if not slot:
            return {'success': False, 'message': 'Der Slot ist nicht mehr verfügbar.'}, 409

        # Termin buchen: Status setzen und Nutzer-ID eintragen
        cursor.execute("""
                UPDATE Termin
                SET Status = 'gebucht',
                    FK_Nutzer_ID = %s
                WHERE Termin_ID = %s
            """, (nutzer_id, slot[0]))

        g.con.commit()
        return {'success': True}, 201

    except Exception as e:
        g.con.rollback()
        return {'success': False, 'message': 'Ein Fehler ist aufgetreten: ' + str(e)}, 500

    finally:
        cursor.close()


# Start der Flask-Anwendung
if __name__ == '__main__':
    app.run(debug=True)
