# constants.py

# Tarif harian berdasarkan hari (dalam rupiah)
TARIF = {
    'senin':  {'krl': 8000, 'krd': 4000},
    'selasa': {'krl': 6000, 'krd':    0},
    'rabu':   {'krl': 6000, 'krd':    0},
    'kamis':  {'krl': 6000, 'krd':    0},
    'jumat':  {'krl': 8000, 'krd': 3000},
    'sabtu':  {'krl':    0, 'krd':    0},
    'minggu': {'krl':    0, 'krd':    0}
}

# Mapping weekday() ke nama hari Indonesia
MAP_HARI = {
    0: 'senin',
    1: 'selasa',
    2: 'rabu',
    3: 'kamis',
    4: 'jumat',
    5: 'sabtu',
    6: 'minggu'
}
