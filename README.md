# 🌿 Proyek Akhir Semantik Web: Representasi Naskah Kuno Gandoang

Repositori ini berisi proses dan hasil transformasi digital dari **Naskah Kuno Gandoang** menjadi bentuk terstruktur berbasis semantik web menggunakan CSV, Python, RDF (TTL), dan HTML dengan endpoint SPARQL dari Jena Fuseki.

---

## 📄 Sumber Naskah

Naskah berasal dari:
- 🔗 **[FlipHTML5 - Naskah Kuno Gandoang](https://fliphtml5.com/qqwue/dngu/NASKAH_KUNO_GANDOANG/)**  
- Bentuk asli: *gambar* (bukan teks digital)
- Transkripsi: dilakukan **secara manual ke format CSV**
- Isi naskah dalam aksara Latin, kemudian diterjemahkan ke:
  - Aksara daerah (menggunakan AI)
  - Bahasa Indonesia (hasil AI terlatih)

---

## 🗂️ Struktur Berkas

| Nama Berkas         | Deskripsi                                                                 |
|----------------------|---------------------------------------------------------------------------|
| `naskah-gandoang.csv`| Hasil transkripsi manual dari gambar naskah menjadi teks berstruktur     |
| `konversi.py`        | Script Python untuk membaca CSV dan mengubah ke format RDF `.ttl`        |
| `naskah-gandoang.ttl`| File RDF/Turtle yang dihasilkan dari script Python                       |
| `interface.html`         | Halaman web yang menampilkan data dari Jena Fuseki lewat SPARQL endpoint |

---

## 🛠️ Alur Proses

1. 🔍 **Transkripsi Manual**  
   - Naskah berbentuk gambar → ditulis ulang ke **CSV**
   - Format CSV mencakup: nomor baris, teks Latin, aksara lokal, terjemahan Indonesia

2. 🤖 **Konversi ke RDF**  
   - Dengan `konversi.py`, CSV dikonversi ke **TTL (Turtle RDF)**
   - TTL menggunakan namespace dan struktur sesuai skema semantik

3. 🌐 **Deploy di Jena Fuseki**
   - TTL diunggah ke **Apache Jena Fuseki**
   - Fuseki menghasilkan **SPARQL endpoint** (URL digunakan di HTML)

4. 🖥️ **Visualisasi Web**
   - `interface.html` mengambil data RDF via endpoint SPARQL dan menampilkannya secara interaktif

---

## 🔗 Teknologi yang Digunakan

- 🐍 Python (untuk parsing dan generate RDF)
- 🗃️ CSV (format awal data)
- 🧠 AI (untuk konversi aksara dan bahasa)
- 🐢 RDF/Turtle (format semantik)
- 🔎 Apache Jena Fuseki (SPARQL endpoint)
- 🌐 HTML (visualisasi data)

---

## 🚀 Cara Menjalankan Sendiri

1. Jalankan script Python:
   ```bash
   python naskah_gandoang_rdf_builder.py

2. Jalankan jena fuseki server:
    buka batch file dari jena fuseki yang sudah di download https://jena.apache.org/download/index.cgi

3. Akses localhost 
    buka browser : http://localhost:3030/

4. Tambah dataset di jena fuseki
    pada dataset -> add data upload file ttl 

5. Endpoint untuk interface
    const endpoint : "http://localhost:3030/db_naskah/sparql";

6. Jalankan interface di browser

