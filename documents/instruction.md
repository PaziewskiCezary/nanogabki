Cały potrzebny sprzęt znajduje się w budynku Wydziału Fizyki w części A w laboratorium Zakładu Fizyki Biomedycznej sali 4.62

Podłączenie układu - wszystkie oznaczenia zgodne z tymi ze schematu przedstawionego na Rysunku 1a:
  1. Urządzenie TiePie Handyscope HS5 należy połączyć ze sobą za pomocą kabla mini HDMI - HDMI i przejściówki HDMI-mini HDMI (wejścia w urządzeniach są mini HDMI)
  2. Wyjście (generator) z urządzenia TiePie Handyscope HS5 urządzenie1 należy podłączyć do wejścia na płytce drukowanej Gen1
  3. Kanał 1 (Ch1 - napięcie U1 po wejściu do układu) należy połączyć z urządzeniem TiePie Handyscope HS5 urządzenie1 CH1
  4. Kanał 2 (Ch2 - napięcie U2 po przejściu przez pierwszy opornik R1) należy połączyć z urządzeniem TiePie Handyscope HS5 urządzenie1 CH2
  5. Kanał 3 (Ch3 - napięcie U3 po przejściu przez elektrodę gąbkową) należy połączyć z urządzeniem TiePie Handyscope HS5 urządzenie2 CH1
  6. Do wejść radiowych R1 i R2 należy włożyć dwa oporniki (standardowo około 400Ohm)
  7. Wejścia radiowe Nano1 należy połączyć za pomocą kabelków z elektrod z tłokiem, w którym znajduje się elektroda gąbkowa

W przypadku innego połączenia trzeba przekazać do inicjalizatora klasy `Experiment` słownik mapujący wyjścia urządzenia z nazwami kanałów
```py
channels = {
            'ch1' : 0,
            'ch2' : 1,
            'ch3' : 3,
            'gen' : 0,
            }
```

Uruchomienie eksperymentu:
  1. Należy uruchomić plik examples/run.py po ówczesnym uzupełnieniu wartości startowych zgodnie z dokumentacją
