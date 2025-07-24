# Budgetin

Budgetin adalah aplikasi desktop sederhana untuk menghitung estimasi biaya transportasi bulanan menggunakan moda KRL dan KRD. Aplikasi dibuat dengan Python menggunakan modul `tkinter` dan dapat menampilkan grafik apabila `matplotlib` terpasang.

## Fitur

- Form pemilihan tahun dan bulan dengan widget `Combobox` untuk menentukan periode perhitungan.
- Tab **Summary**, **Details**, dan **Charts** untuk menampilkan ringkasan total biaya, rincian per hari, serta grafik distribusi biaya.
- Perhitungan otomatis dilakukan oleh kelas `BudgetCalculator` yang menjumlahkan tarif harian dari file `constants.py`.
- Dukungan opsional grafik dengan `matplotlib`.
- Skrip `build.bat` untuk membangun aplikasi menjadi satu file eksekusi menggunakan PyInstaller.

## Persyaratan

- Python 3.8 atau lebih baru.
- `tkinter` (biasanya sudah tersedia di instalasi Python standar).
- `matplotlib` (opsional, hanya untuk tampilan grafik).

## Cara Menjalankan

Clone repository ini kemudian jalankan `main.py`:

```bash
python main.py
```

Aplikasi akan menampilkan jendela berisi pilihan tahun dan bulan. Tekan tombol **Generate** untuk melihat rekapitulasi biaya.

## Pembuatan Paket Windows

Untuk membuat file exe pada Windows, jalankan `build.bat` yang telah tersedia. Skrip tersebut akan memanggil PyInstaller dengan menyalin seluruh modul yang dibutuhkan.

## Lisensi

Proyek ini menggunakan lisensi MIT. Lihat file `LICENSE` untuk informasi lebih lanjut.
