import streamlit as st
from datetime import date
from io import BytesIO
from rpp_generator import generate_docx_rpp

st.set_page_config(page_title="RPP Deep Learning DOCX", layout="centered")
st.title("📘 Generator RPP Deep Learning (Export ke Word)")

fase = st.selectbox("Pilih Fase", ["Fase A - Kelas 1–2 SD", "Fase B - Kelas 3–4 SD", "Fase C - Kelas 5–6 SD"])
mapel = st.selectbox("Mata Pelajaran", ["Matematika", "IPA", "IPS", "Bahasa Indonesia", "PPKn", "TIK / Informatika"])
nama = st.text_input("Nama Guru")
sekolah = st.text_input("Nama Sekolah")
semester = st.selectbox("Semester", ["Ganjil", "Genap"])
alokasi = st.text_input("Alokasi Waktu (JP)", "2 JP")
profil = st.multiselect("Dimensi Profil Lulusan", [
    "Keimanan dan ketakwaan kepada Tuhan Yang Maha Esa", "Kewargaan", "Penalaran kritis",
    "Kreativitas", "Kolaborasi", "Kemandirian", "Kesehatan", "Komunikasi"])

topik_dict = {
    "Matematika": ("Pecahan", "Pecahan Desimal", "Memahami konsep pecahan", "Menjelaskan pecahan desimal dan penggunaannya"),
    "IPA": ("Energi", "Energi Terbarukan", "Menganalisis berbagai bentuk energi", "Membandingkan sumber energi baru dan terbarukan"),
    "IPS": ("Lingkungan", "Perubahan Sosial", "Menjelaskan perubahan sosial", "Mengidentifikasi dampak perubahan sosial"),
    "Bahasa Indonesia": ("Teks Narasi", "Menulis Cerita", "Menulis teks narasi", "Menyusun cerita sederhana dengan struktur teks yang benar"),
    "PPKn": ("Warga Negara", "Hak dan Kewajiban", "Memahami hak dan kewajiban warga negara", "Menjelaskan hak dan kewajiban siswa di sekolah"),
    "TIK / Informatika": ("Algoritma", "Coding Blok", "Mengenal algoritma dasar", "Membuat urutan langkah pemecahan masalah dengan coding blok")
}

topik, materi, cp, tp = topik_dict.get(mapel, ("Topik", "Materi", "CP", "TP"))
tanggal = date.today().strftime('%d-%m-%Y')
fase_label = fase.split(" ")[1]

if st.button("📄 Generate & Download .docx"):
    data = {
        "identitas": {
            "Nama Guru": nama,
            "Sekolah": sekolah,
            "Mata Pelajaran": mapel,
            "Fase": fase,
            "Semester": semester,
            "Topik": topik,
            "Materi": materi,
            "Alokasi Waktu": alokasi,
            "Tanggal": tanggal
        },
        "identifikasi": {
            "Peserta Didik": f"Karakteristik {fase}",
            "Materi Pelajaran": materi,
            "Dimensi Profil Lulusan": ", ".join(profil)
        },
        "desain": {
            "Capaian Pembelajaran": cp,
            "Tujuan Pembelajaran": tp,
            "Lintas Disiplin Ilmu": f"{mapel}, Lingkungan",
            "Topik Pembelajaran": topik,
            "Praktik Pedagogis": "Deep Learning, Problem Solving, Project-Based Learning",
            "Lingkungan Pembelajaran": "Kelas, Luar kelas, Virtual",
            "Pemanfaatan Digital": "Aplikasi simulasi, Google Docs, Video",
            "Kemitraan Pembelajaran": "Orang tua, Komunitas, Guru lain"
        },
        "pengalaman": {
            "Kegiatan Awal": "Apersepsi, motivasi, orientasi",
            "Kegiatan Inti": "Memahami, Mengaplikasi, Merefleksi (diskusi, proyek, refleksi)",
            "Kegiatan Penutup": "Umpan balik, menyimpulkan, perencanaan lanjutan"
        },
        "asesmen": {
            "Asesmen Awal": "Kuis, Tanya jawab",
            "Asesmen Proses": "Observasi, Unjuk kerja",
            "Asesmen Akhir": "Tes, Proyek Mini, Refleksi",
            "Metode": "Tes tertulis/lisan, Portofolio, Peer Review"
        },
        "sumber": "Buku teks, Video, Alat peraga, Lingkungan sekitar, Digital tools",
        "refleksi": "Guru merefleksikan pembelajaran, siswa menulis jurnal pengalaman"
    }

    doc = generate_docx_rpp(data)
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    st.download_button(
        label="📥 Download RPP .docx",
        data=buffer,
        file_name=f"RPP_{mapel}_{fase_label}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
