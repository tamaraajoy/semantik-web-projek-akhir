import pandas as pd
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, RDFS, DCTERMS, FOAF, XSD

# --- 1. Definisi Namespaces (sesuai model sebelumnya) ---
ex = Namespace("http://example.org/naskah-gandoang-ontology#")
g = Graph()

g.bind("ex", ex)
g.bind("dcterms", DCTERMS)
g.bind("foaf", FOAF)
g.bind("xsd", XSD) # Penting untuk tipe data seperti integer

# --- 2. Tambahkan Data Metadata Naskah Umum (seperti sebelumnya) ---
naskah_gandoang = ex.NaskahGandoang
g.add((naskah_gandoang, RDF.type, ex.NaskahKuno))
g.add((naskah_gandoang, DCTERMS.title, Literal("Naskah Gandoang")))
g.add((naskah_gandoang, DCTERMS.description, Literal("Naskah kuno yang berisi surat pengukuhan kekuasaan, silsilah hingga Nabi Adam AS, dan primbon.")))
g.add((naskah_gandoang, DCTERMS.language, Literal("jv"))) # Bahasa Jawa
g.add((naskah_gandoang, DCTERMS.format, Literal("daluwang")))
g.add((naskah_gandoang, DCTERMS.creator, Literal("belum diketahui"))) # Informasi baru

# Informasi kepemilikan dan lokasi
aki_haji_mahmud = ex.AkiHajiMahmud
g.add((aki_haji_mahmud, RDF.type, FOAF.Person))
g.add((aki_haji_mahmud, FOAF.name, Literal("Aki Haji Mahmud")))
g.add((naskah_gandoang, ex.memilikiPemilikSaatIni, aki_haji_mahmud))

juru_kunci = ex.JuruKunciSitusGandoangSebelumnya
g.add((juru_kunci, RDF.type, FOAF.Person))
g.add((juru_kunci, FOAF.name, Literal("Juru Kunci Situs Gandoang (Leluhur)")))
g.add((naskah_gandoang, ex.merupakanWarisanDari, juru_kunci))

lokasi_gandoang = ex.LokasiGandoang
g.add((lokasi_gandoang, RDF.type, ex.LokasiGeografis))
g.add((lokasi_gandoang, DCTERMS.title, Literal("Gandoang")))
g.add((lokasi_gandoang, DCTERMS.spatial, Literal("Wanasigra, Sindangkasih, Ciamis")))
g.add((naskah_gandoang, ex.disimpanDiLokasiFisik, lokasi_gandoang))

# Informasi fisik naskah
g.add((naskah_gandoang, ex.jumlahTotalHalaman, Literal(37, datatype=XSD.integer)))
g.add((naskah_gandoang, ex.jumlahHalamanIsi, Literal(35, datatype=XSD.integer)))
g.add((naskah_gandoang, ex.jumlahHalamanKosong, Literal(2, datatype=XSD.integer)))
g.add((naskah_gandoang, ex.ukuranFisikNaskah, Literal("15.5 x 12.2 cm")))
g.add((naskah_gandoang, ex.ukuranAreaTeks, Literal("12 x 9 cm")))
g.add((naskah_gandoang, ex.jumlahBarisTeksPerHalamanDepan, Literal(10, datatype=XSD.integer)))
g.add((naskah_gandoang, ex.jumlahBarisTeksPerHalamanAkhir, Literal(6, datatype=XSD.integer)))

# --- Definisi Kelas Baru (jika ada) dan Properti Baru ---
# Tambahkan definisi properti 'ex:memuatAksaraJawa' di sini
ex.memuatAksaraJawa = URIRef(ex + "memuatAksaraJawa")
g.add((ex.memuatAksaraJawa, RDF.type, RDF.Property))
g.add((ex.memuatAksaraJawa, RDFS.label, Literal("memuat aksara Jawa")))
g.add((ex.memuatAksaraJawa, RDFS.domain, ex.BarisTeks))
g.add((ex.memuatAksaraJawa, RDFS.range, XSD.string)) # Range-nya string karena ini konten teks

# Tambahkan definisi properti 'ex:memuatBarisTeks' di sini
ex.memuatBarisTeks = URIRef(ex + "memuatBarisTeks")
g.add((ex.memuatBarisTeks, RDF.type, RDF.Property))
g.add((ex.memuatBarisTeks, RDFS.label, Literal("memuat baris teks")))
g.add((ex.memuatBarisTeks, RDFS.domain, ex.HalamanNaskah))
g.add((ex.memuatBarisTeks, RDFS.range, ex.BarisTeks))

# Definisi Aksara (Ini harus tetap di sini dan tidak ditimpa)
aksara_jawa_uri = ex.AksaraJawaCacarakan # Ganti nama variabel agar tidak tertukar!
g.add((aksara_jawa_uri, RDF.type, ex.Aksara))
g.add((aksara_jawa_uri, RDFS.label, Literal("Aksara Jawa (Cacarakan)")))

# Definisi Tokoh dan Entitas Kewenangan yang disebut dalam teks
susuhunan_senapati = ex.SusuhunanSenapatiIngNgalaga
g.add((susuhunan_senapati, RDF.type, ex.Tokoh))
g.add((susuhunan_senapati, FOAF.name, Literal("Susuhunan Senapati Ing Ngalaga")))

sangasar = ex.Sangasar
g.add((sangasar, RDF.type, ex.Tokoh))
g.add((sangasar, FOAF.name, Literal("Sangasar")))

bumi_galuh = ex.BumiGaluh
g.add((bumi_galuh, RDF.type, ex.LokasiGeografis))
g.add((bumi_galuh, DCTERMS.title, Literal("Bumi Galuh")))

dewa = ex.Dewa
g.add((dewa, RDF.type, ex.EntitasKewenangan))
g.add((dewa, RDFS.label, Literal("Dewa (Penguasa yang lebih tinggi)")))

# --- 3. Membaca Data Baris Teks dari CSV ---
try:
    df = pd.read_csv('naskah_gandoang_data.csv', delimiter=';', encoding='utf-8-sig')
    print("Kolom yang Ditemukan di CSV:", df.columns.tolist())    
    # Dictionary untuk menyimpan URI halaman yang sudah dibuat agar tidak dobel
    halaman_uris = {}

    for index, row in df.iterrows():
        halaman_num = int(row['Nomor Halaman'])
        baris_num = int(row['Nomor Baris'])
        
        # Buat URI halaman jika belum ada untuk halaman ini
        if halaman_num not in halaman_uris:
            halaman_uri = ex[f"Halaman_NG_{halaman_num:02d}"]
            g.add((halaman_uri, RDF.type, ex.HalamanNaskah))
            g.add((halaman_uri, DCTERMS.isPartOf, naskah_gandoang))
            g.add((halaman_uri, RDFS.comment, Literal(f"Merupakan halaman ke-{halaman_num} dari Naskah Gandoang.")))
            halaman_uris[halaman_num] = halaman_uri
        else:
            halaman_uri = halaman_uris[halaman_num]

        aksara_jawa_content_str = row['Aksara Jawa']
        teks_latin = row['Teks Latin']
        terjemahan_indonesia = row['Terjemahan Indonesia']

        baris_uri = ex[f"Baris_NG_{halaman_num:02d}_{baris_num:02d}"]

        g.add((baris_uri, RDF.type, ex.BarisTeks))
        g.add((baris_uri, DCTERMS.isPartOf, halaman_uri))
        g.add((baris_uri, ex.lineNumber, Literal(baris_num, datatype=XSD.integer)))
        
        # LINK BARIS KE HALAMAN DENGAN ex:memuatBarisTeks
        g.add((halaman_uri, ex.memuatBarisTeks, baris_uri)) 

        g.add((baris_uri, ex.ditulisDalamAksara, aksara_jawa_uri))
        g.add((baris_uri, ex.memuatAksaraJawa, Literal(aksara_jawa_content_str)))
        g.add((baris_uri, ex.memuatTeksAsliLatin, Literal(teks_latin)))
        g.add((baris_uri, ex.memuatTerjemahanIndonesia, Literal(terjemahan_indonesia)))

        # Tambahkan hubungan semantik yang diekstraksi secara manual dari baris teks ini
        if baris_num == 3: # "ngalaga // gaduh dening sangasar/mar"
            g.add((susuhunan_senapati, ex.memberiKuasaKepada, sangasar))
        if baris_num == 5: # "ngangsar sun gaduhi bumi galuh"
            g.add((sangasar, ex.diberiKuasaAtas, bumi_galuh))
        if baris_num == 8: # "dene wong ratu wong rongewu sanga"
            g.add((sangasar, ex.berkuasaAtasJumlahOrang, Literal(2960, datatype=XSD.integer)))
        if baris_num == 9: # "ngatus sawidak // sapa mahi dé"
            g.add((sangasar, ex.diperolehDari, dewa))


except FileNotFoundError:
    print("Error: File 'naskah_gandoang_data.csv' tidak ditemukan. Pastikan file berada di direktori yang sama dengan script.")
    print("Silakan buat file CSV dengan header: 'Nomor Halaman,Nomor Baris,Aksara Jawa,Teks Latin,Terjemahan Indonesia'")
    exit()

# --- 4. Menyimpan Grafik RDF ke File ---
output_file = "naskah_gandoang_data.ttl"
g.serialize(destination=output_file, format="turtle")
print(f"\nData RDF berhasil disimpan ke: {output_file}")

# --- 5. Contoh Query SPARQL (untuk memverifikasi) ---
print("\n--- Contoh Query SPARQL: Informasi Naskah dan Pemilik ---")
query_naskah_pemilik = """
SELECT ?judulNaskah ?pemilik ?warisanDari ?lokasiFisik
WHERE {
  ?naskah rdf:type ex:NaskahKuno ;
          dcterms:title ?judulNaskah ;
          ex:memilikiPemilikSaatIni ?pemilikUri ;
          ex:merupakanWarisanDari ?warisanUri ;
          ex:disimpanDiLokasiFisik ?lokasiUri .
  ?pemilikUri foaf:name ?pemilik .
  ?warisanUri foaf:name ?warisanDari .
  ?lokasiUri dcterms:title ?lokasiFisik .
}
"""
for row in g.query(query_naskah_pemilik):
    print(f"Judul: {row.judulNaskah}, Pemilik: {row.pemilik}, Warisan dari: {row.warisanDari}, Disimpan di: {row.lokasiFisik}")

print("\n--- Contoh Query SPARQL: Detail Baris Teks dari Halaman 2 ---")
query_baris_halaman_2 = """
SELECT ?lineNumber ?latinText ?indonesianTranslation ?aksaraJawaContent
WHERE {
  ex:Halaman_NG_02 ex:memuatBarisTeks ?baris .
  ?baris ex:lineNumber ?lineNumber ;
         ex:memuatTeksAsliLatin ?latinText ;
         ex:memuatTerjemahanIndonesia ?indonesianTranslation ;
         ex:memuatAksaraJawa ?aksaraJawaContent .
}
ORDER BY ?lineNumber
"""
for row in g.query(query_baris_halaman_2):
    print(f"Baris {row.lineNumber}:")
    print(f"   Latin: {row.latinText}")
    print(f"   Indonesia: {row.indonesianTranslation}")
    print(f"   Jawa: {row.aksaraJawaContent}")

print("\n--- Contoh Query SPARQL: Siapa yang diberi kuasa atas Bumi Galuh? ---")
query_kuasa_galuh = """
SELECT ?tokohName ?jumlahOrang ?sumberKuasa
WHERE {
  ?tokoh rdf:type ex:Tokoh ;
          ex:diberiKuasaAtas ex:BumiGaluh ;
          foaf:name ?tokohName .
  OPTIONAL { ?tokoh ex:berkuasaAtasJumlahOrang ?jumlahOrang . }
  OPTIONAL { ?tokoh ex:diperolehDari ?sumberUri . ?sumberUri rdfs:label ?sumberKuasa . }
}
"""
for row in g.query(query_kuasa_galuh):
    print(f"Tokoh: {row.tokohName}")
    if row.jumlahOrang:
        print(f"   Berkuasa atas: {row.jumlahOrang} orang")
    if row.sumberKuasa:
        print(f"   Diperoleh dari: {row.sumberKuasa}")