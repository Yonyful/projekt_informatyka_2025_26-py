# projekt_informatyka_2025_26 py

Projekt przedstawia symulację kaskadowego układu zbiorników połączonych systemem rur, pomp oraz grzałki.
Celem programu jest odwzorowanie działania prostego systemu SCADA oraz wizualizacja prostych zjawisk w systemie przemysłowym:
- Przepływ cieczy pomiędzy zbiornikami
- Obsługa alarmów
- Sterowanie pompami
- Nagrzewanie cieczy za pomocą grzałki

Układ składa się z czterech zbiorników, ciecz przepływa grawitacyjnie pomiędzy zbiornikami poprzez rury.
Głównym zbiornikiem jest zbiornik nr.1, z niego ciecz przekazywana jest na zbiornik nr.2, który rozdziela ją na zbiornik nr.3 i nr.4 w proporcji 50/50.
W zbiorniku nr.3 ciecz oczekuje na ostygnięcie, gdzie nastepnie jest przekazywana do zbiornika nr.4.
W zbiorniku nr.4 znajduje się grzałka, która podnosi temperaturę cieczy do maksymalnej.
Po uzyskaniu zadanej temperatury, ciecz jest wyciągana spowrotem do zbiornika nr.1 za pomocą pompy.
Dodatkowo układ posiada pompę zewnętrzną, która dopompowuje "porcję" cieczy, gdy jej całkowita ilość w systemie spadnie poniżej określonego poziomu.
Okno alarmów zawiera komunikaty o m.in zbyt wysokiej temperaturze w danym zbiorniku lub niskiej ilości płynu, do okna alarmów dołączony jest również log, w którym znajdują się wszystkie poprzednie alarmy wraz z datą.
Z okna parametrów możemy zmieniać ustawienia elementów, jak np: maksymalną temperaturę w danym zbiorniku, moc grzałek itp.

Program uruchamiany jest poprzez plik symulacja.py, do uruchomienia potrzebna jest biblioteka PyQt5.

