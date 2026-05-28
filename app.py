from flask import Flask, render_template, request, make_response  # type: ignore[import]
from fpdf import FPDF  # type: ignore[import]
from datetime import datetime

app = Flask(__name__)

class PDF(FPDF):
    def header(self):
        # 1. Tambahkan Logo UMITRA (Pastikan file logo_umitra.png ada di folder)
        self.image('Logo_umitra.png', 15, 10, 22) 
        
        # 2. Atur Teks Kop Surat Resmi (Diperbarui ke Kementerian Baru)
        self.set_xy(45, 11)
        self.set_font('Arial', 'B', 10) # Ukuran font 10 agar teks panjang tetap rapi dalam satu baris
        self.cell(0, 6, 'KEMENTERIAN PENDIDIKAN TINGGI, SAINS, DAN TEKNOLOGI', 0, 1, 'L')
        
        self.set_x(45)
        self.set_font('Arial', 'B', 14)
        self.cell(0, 8, 'UNIVERSITAS MITRA INDONESIA', 0, 1, 'L')
        
        self.set_x(45)
        self.set_font('Arial', '', 9)
        self.cell(0, 5, 'Jl. Z.A. Pagar Alam No. 7, Gedong Meneng, Rajabasa, Bandar Lampung, Lampung 40115', 0, 1, 'L')
        
        # 3. Garis Pembatas Kop Surat
        self.set_line_width(0.6) 
        self.line(10, 40, self.w - 10, 40) 
        self.ln(12) 

    
    def footer(self):
        self.set_y(-15)
        self.set_line_width(0.2)
        self.line(10, 282, self.w - 10, 282) 
        self.set_font('Arial', 'I', 8)
        teks_footer = 'Telepon: (0721) 701418 | Website: www.umitra.ac.id | Email: info@umitra.ac.id'
        self.cell(0, 10, teks_footer, 0, 0, 'C')

# Fungsi Logika untuk Mendeteksi Tahun Akademik & Semester Berjalan secara Otomatis
def hitung_semester_berjalan():
    sekarang = datetime.now()
    bulan = sekarang.month
    tahun = sekarang.year
    
    # Jika bulan Maret (3) sampai Agustus (8) -> Masuk Genap
    if 3 <= bulan <= 8:
        tahun_akademik = f"{tahun-1}/{tahun} Genap"
    # Jika bulan September (9) sampai Desember (12) -> Masuk Ganjil (Tahun ini/Tahun depan)
    elif bulan >= 9:
        tahun_akademik = f"{tahun}/{tahun+1} Ganjil"
    # Jika bulan Januari (1) atau Februari (2) -> Masuk Ganjil (Tahun lalu/Tahun ini)
    else:
        tahun_akademik = f"{tahun-1}/{tahun} Ganjil"
        
    return tahun_akademik

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_pdf():
    # Mengambil data dari form
    nama = request.form.get('nama')
    npm = request.form.get('npm')
    ttl = request.form.get('ttl_mhs')
    fakultas = request.form.get('fakultas')
    prodi = request.form.get('prodi')
    semester_angka = request.form.get('semester')
    alamat = request.form.get('alamat_mhs')
    kecamatan = request.form.get('kec_mhs')
    kota = request.form.get('kota_mhs')
    tujuan = request.form.get('tujuan')

    alamat_lengkap = f"{alamat}, Kec. {kecamatan}, {kota}"

    # Memanggil fungsi otomatis untuk mendapatkan string misal: "2025/2026 Genap"
    semester_berjalan = hitung_semester_berjalan()
    tahun_sekarang = datetime.now().year

    # Inisialisasi PDF
    pdf = PDF(format='Legal')  # Ukuran kertas Legal (8.5 x 14 inch)
    pdf.add_page()
    
    # Judul Surat
    pdf.set_font('Arial', 'BU', 14)
    pdf.cell(0, 10, 'SURAT KETERANGAN AKTIF KULIAH', 0, 1, 'C')
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 5, 'Nomor: S.01/.... /UMITRA/BAAK/2026', 0, 1, 'C')
    pdf.ln(10)

    # Isi Surat
    pdf.set_font('Arial', '', 11)
    pdf.multi_cell(0, 8, 'Yang bertanda tangan di bawah ini, Kepala Biro Administrasi Akademik dan Kemahasiswaan (BAAK) Universitas Mitra Indonesia, menerangkan dengan sesungguhnya bahwa:')
    
    # Data Mahasiswa
    pdf.ln(5)
    pdf.cell(40, 8, 'Nama', 0, 0)
    pdf.cell(5, 8, ':', 0, 0)
    pdf.cell(0, 8, nama, 0, 1)
    
    pdf.cell(40, 8, 'NPM', 0, 0)
    pdf.cell(5, 8, ':', 0, 0)
    pdf.cell(0, 8, npm, 0, 1)
    
    pdf.cell(40, 8, 'Tempat Tanggal Lahir', 0, 0)
    pdf.cell(5, 8, ':', 0, 0)
    pdf.cell(0, 8, ttl, 0, 1)

    pdf.cell(40, 8, 'Fakultas', 0, 0)
    pdf.cell(5, 8, ':', 0, 0)
    pdf.cell(0, 8, fakultas, 0, 1)

    pdf.cell(40, 8, 'Program Studi', 0, 0)
    pdf.cell(5, 8, ':', 0, 0)
    pdf.cell(0, 8, prodi, 0, 1)
    
    pdf.cell(40, 8, 'Semester', 0, 0)
    pdf.cell(5, 8, ':', 0, 0)
    pdf.cell(0, 8, semester_angka, 0, 1)

    pdf.cell(40, 8, 'Alamat', 0, 0)
    pdf.cell(5, 8, ':', 0, 0)
    pdf.cell(0, 8, alamat, 0, 1)

    pdf.cell(40, 8, 'Kecamatan', 0, 0)
    pdf.cell(5, 8, ':', 0, 0)
    pdf.cell(0, 8, kecamatan, 0, 1)

    pdf.cell(40, 8, 'Kota', 0, 0)
    pdf.cell(5, 8, ':', 0, 0)
    pdf.cell(0, 8, kota, 0, 1)

    pdf.cell(40, 8, 'Alamat Lengkap', 0, 0)
    pdf.cell(5, 8, ':', 0, 0)
    pdf.cell(0, 8, alamat_lengkap, 0, 1, 'L')

    pdf.ln(5)
    isi_penutup = f"Adalah benar berstatus sebagai mahasiswa AKTIF pada semester {semester_berjalan} di lingkungan Universitas Mitra Indonesia. Surat keterangan ini dibuat untuk keperluan: {tujuan}."
    pdf.multi_cell(0, 8, isi_penutup, 0, 'J')
    
    pdf.ln(5)
    pdf.multi_cell(0, 8, 'Demikian surat keterangan ini dibuat agar dapat dipergunakan sebagaimana mestinya. Dokumen ini wajib divalidasi dan ditandatangani secara langsung di loket BAAK.')

    # Tanda Tangan BAAK
    pdf.ln(15)
    tanggal_sekarang = datetime.now().strftime("%d %B %Y")
    pdf.cell(120)
    pdf.cell(0, 6, f'Bandar Lampung, {tanggal_sekarang}', 0, 1, 'L')
    pdf.cell(120)
    pdf.cell(0, 6, 'Kepala BAAK,', 0, 1, 'L')
    pdf.cell(120)
    pdf.cell(0, 6, 'Universitas Mitra Indonesia,', 0, 1, 'L')
    pdf.ln(20)
    pdf.cell(120)
    pdf.set_font('Arial', 'BU', 11)
    pdf.cell(0, 6, 'Dr. Yudhinanto CN, SE., MM', 0, 1, 'L')
    pdf.cell(120)
    pdf.set_font('Arial', '', 11)
    pdf.cell(0, 6, 'NPP.2222144 ', 0, 1, 'L')

    # Output PDF
    pdf_output = pdf.output(dest='S').encode('latin1')
    response = make_response(pdf_output)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename=Surat_Aktif_{npm}.pdf'
    
    return response

if __name__ == '__main__':
    app.run(debug=True)