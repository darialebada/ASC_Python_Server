### Lebădă Daria-Cristiana, 333CA

# TEMA 1 ASC - Le Stats Sportif

## Organizare

### Structura proiectului
- În directorul app/ se găsește implementarea aplicației, astfel:
  * __init__.py - inițializarea webserverului, crearea directorului pentru scrierea resultatelor
  requesturilor (dacă nu există deja), inițializarea ThreadPool-ului (implicit crearea threadurilor)
  și începerea prelucrării datelor din fișier;
  * data_ingestor.py - preia datele din fișier și le prelucrează, adăugând într-o listă de dicționare
  doar datele de care avem nevoie;
  * task_runner.py - aici se află clasa ThreadPool care se ocupă de organizarea threadurilor (le
  inițializează, adaugă taskuri și la final închide threadurile) și clasa TaskRunner care reprezintă
  clasa threadurilor (funcția run - executarea taskurilor);
  * task_solver.py - funcții care se ocupă de rezolvarea taskurilor (calculează datele cerute);
  * routes.py - inițializarea rutelor pentru momentul în care se primesc requesturi;
  * logging.py - inițializarea logger-ului și handler-ului pentru înregistrarea datelor la rulare.
- În directorul unittests/ se găsesc:
  * TestWebserver.py - clasă în care testez corectitudinea funcțiilor din app/task_solver.py prin
  intermediul a două întrebări;
  * test_data.csv - câteva date luate din fișierul principal pentru a putea testa validitatea datelor.

### Abordarea generală
- Prima dată când pornesc aplicația se vor inițializa automat toate componentele: datele care
trebuie parcurse, ThreadPool-ul și se vor crea threadurile.
- Ideea pentru rute este cam aceeași: în momentul în care primesc un request preiau datele, verific
dacă serverul meu este încă pornit (adică nu a existat un apel de tipul graceful_shutdown) și dacă
este preiau datele, îî dau noului task un job_id unic și îl trimit către ThreadPool pentru a fi
procesat și adăugat în coadă (folosesc Queue - coadă sincronizată).
- ThreadPool doar adaugă taskuri în coadă, iar threadurile vor prelua câte un task (apelul Queue.get()
fiind blocant, vor aștepta până primesc un task în coadă).
- Fiecare task va fi trimis spre rezolvare, iar rezultatul obținut va fi scris într-un fișier cu
numele job_id-ului, iar taskul va fi considerat ”done”.
- Pentru graceful_shutdown folosesc un obiect de tip Event() pentru a notifica ThreaPool-ul să nu
mai adauge taskuri noi în coadă și threadurile să termine când coada este goală.

### Memorarea datelor
- Am ales să mă folosesc în general de dicționare pentru a-mi păstra și prelucra datele, de exemplu
datele citite din fișier le păstrez într-o listă de dicționare, taskurile sunt dicționare care conțin
job_id, tip de request, întrebare și stat (după nevoie). 

### Consideri că tema a fost utilă?
- Da, mi s-a părut ceva des întâlnit în practică (aplicație client server), plus că am avut partea
de unittesting care mi s-a părut interesantă având în vedere că nu prea se pune accentul în facultate
pe partea de testare.

### Consideri implementarea naivă, eficientă, se putea mai bine?
- Consider că am o implementare eficientă, având în cedere că nu prea am mai lucrat cu Python
înainte de semestrul acesta, cred că m-am descurcat destul de bine, dar mereu e loc de mai bine,
poate peste ani aș rezolva diferit.

## Implementare
- Am implementat tot enunțul temei: rute, unittesting, logging.
- Dificultăți întâmpinate: mi-a luat ceva să înțeleg ce trebuie să fac, dar după a mers totul
foarte ușor.
- Lucruri interesante descoperite pe parcurs: chiar consider că am învățat să scriu cod în Python
cu ușurință și să folosesc elemente de sincronizare.

## Resurse utilizate
- Laboratoarele 2 și 3 de Programare concurentă în Python de la ASC.
- Documentația oficiala python pentru sintaxă și pentru folosirea anumitor elemente speciale:
  * Queue: https://docs.python.org/3/library/queue.html
  * Logging: https://docs.python.org/3/library/logging.html
  * Handler: https://docs.python.org/3/library/logging.handlers.html#logging.handlers.RotatingFileHandler
  * unittest: https://docs.python.org/3/library/unittest.html

## Git
https://github.com/darialebada/ASC_Python_Server
