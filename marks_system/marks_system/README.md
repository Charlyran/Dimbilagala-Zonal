# Polonnaruwa Zone Term Test Marks System

Web app for managing term test marks of **39 schools** in Polonnaruwa Zone (PL).

## How to run on your computer

### 1. Requirements
- Python 3.8 or newer
- Internet (only for first install)

### 2. Install & Start

**Windows:**
1. Unzip `marks_system.zip`
2. Open Command Prompt inside the `marks_system` folder
3. Run:
```
pip install Flask Flask-SQLAlchemy Flask-Login Werkzeug
python run.py
```
Or double-click `start.bat`

**Mac / Linux:**
```
unzip marks_system.zip
cd marks_system
pip3 install Flask Flask-SQLAlchemy Flask-Login Werkzeug
python3 run.py
```

### 3. Open in browser
http://127.0.0.1:5000

## Logins

| Role | Username | Password |
|------|----------|----------|
| **Zonal Admin** | admin | admin123 |
| **Any School** | (see list) | school123 |

### Admin
- Login → **Zone Results** to see all 39 schools progress, averages and ranking

### School usernames (password for all: school123)
```
wilayayamadh          → PL/WILAYAYA MADHYA MAHA VIDYALAYA
siripuramadh          → PL/SIRIPURA MADHYA MAHA VIDYALAYA
welikandamaha         → PL/WELIKANDA MAHA VIDYALAYA
weheragalamaha        → PL/WEHERAGALA MAHA VIDYALAYA
medagamamaha          → PL/MEDAGAMA MAHA VIDYALAYA
sevanapitiyamaha      → PL/SEVANAPITIYA MAHA VIDYALAYA
nikawathalandamaha    → PL/NIKAWATHALANDA MAHA VIDYALAYA
bogaswewamaha         → PL/BOGASWEWA MAHA VIDYALAYA
leelarathnawijesin    → PL/LEELARATHNA WIJESINGHA MAHA VIDYALAYA
ellewewamaha          → PL/ELLEWEWA MAHA VIDYALAYA
aselapuramaha         → PL/ASELAPURA MAHA VIDYALAYA
nuwaragalamaha        → PL/NUWARAGALA MAHA VIDYALAYA
alawakumburamaha      → PL/ALAWAKUMBURA MAHA VIDYALAYA
nelumwewamaha         → PL/NELUMWEWA MAHA VIDYALAYA
maduruoya             → PL/MADURU OYA MAHA VIDYALAYA
manampitiyasinh       → PL/MANAMPITIYA SINHALA MAHA VIDYALAYA
kashyapamaha          → PL/KASHYAPA MAHA VIDYALAYA
vijayaparakkrama      → PL/VIJAYA PARAKKRAMA KANISHTA VIDYALAYA
damminnamaha          → PL/DAMMINNA MAHA VIDYALAYA
sinhapurakani         → PL/SINHAPURA KANISTA VIDYALAYA
pihitiwewamaha        → PL/PIHITIWEWA MAHA VIDYALAYA
kalingawilakani       → PL/KALINGAWILA KANISHTA VIDYALAYA
kadawathamaduwadha    → PL/KADAWATHAMADUWA DHARMAPALA KANISHTA VIDYALAYA
bandanagalakani       → PL/BANDANAGALA KANISHTA VIDYALAYA
kandegamakani         → PL/KANDEGAMA KANISHTA VIDYALAYA
pahalayakkure         → PL/PAHALA YAKKURE KANISHTA VIDYALAYA
pelatiyawewaseco      → PL/PELATIYAWEWA SECONDARY SCHOOL
kekuluwelamaha        → PL/KEKULUWELA MAHA VIDYALAYA
nawapallegamavidya    → PL/NAWAPALLEGAMA VIDYALAYA
nawaginidamanamaha    → PL/NAWAGINIDAMANA MAHA VIDYALAYA
ihalayakkure          → PL/IHALA YAKKURE KANISHTA VIDYALAYA
maguldamanamaha       → PL/MAGULDAMANA MAHA VIDYALAYA
katuwanwilamusl       → PL/KATUWANWILA MUSLIM KANISHTA VIDYALAYA
senapuraal            → PL/SENAPURA AL AMEEN MUSLIM MAHA VIDYALAYA
manampitiyatami       → PL/MANAMPITIYA TAMIL MAHA VIDYALAYA
hewanpitiyatami       → PL/HEWANPITIYA TAMIL MAHA VIDYALAYA
mutugalatami          → PL/MUTUGALA TAMIL VIDYALAYA
thrikonamaduwamusl    → PL/THRIKONAMADUWA MUSLIM MAHA VIDYALAYA
rotawewatami          → PL/ROTAWEWA TAMIL KANISHTA VIDYALAYA
```

## Features
- Admin sees overall zone results and school ranking
- Each school has private login
- Create classes, add students, enter marks
- Supports "ab" for absent
- Automatic total, average, class rank
- Printable reports
