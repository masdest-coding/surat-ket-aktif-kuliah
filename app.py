from flask import Flask, render_template, request, make_response  # type: ignore[import]
from fpdf import FPDF  # type: ignore[import]
from datetime import datetime

app = Flask(__name__)

class PDF(FPDF):
    def header(self):
        # Kop Surat
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'KEMENTRIAN PENDIDIKAN TINGGI, SAINS DAN TEKNOLOGI', 0, 1, 'C')
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'UNIVERSITAS MITRA INDONESIA', 0, 1, 'C')
        self.set_font('Arial', '', 10)
        self.cell(0, 5, 'Jl. Zainal Abidin Pagar Alam No.7 Gedung Meneng Rajabasa, Bandar Lampung 35145', 0, 1, 'C')
        self.line(10, 35, 200, 35)
        self.ln(10)

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
    semester = request.form.get('semester')
    alamat = request.form.get('alamat_mhs')
    kecamatan = request.form.get('kec_mhs')
    kota = request.form.get('kota_mhs')
    tujuan = request.form.get('tujuan')

    # Inisialisasi PDF
    pdf = PDF()
    pdf.add_page()
    
    # Judul Surat
    pdf.set_font('Arial', 'BU', 12)
    pdf.cell(0, 10, 'SURAT KETERANGAN AKTIF KULIAH', 0, 1, 'C')
    pdf.set_font('Arial', '', 11)
    pdf.cell(0, 5, 'Nomor: S.05/.... /UM/BAAK/2026', 0, 1, 'C')
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
    pdf.cell(0, 8, semester, 0, 1)

    pdf.cell(40, 8, 'Alamat', 0, 0)
    pdf.cell(5, 8, ':', 0, 0)
    pdf.cell(0, 8, alamat, 0, 1)

    pdf.cell(40, 8, 'Kecamatan', 0, 0)
    pdf.cell(5, 8, ':', 0, 0)
    pdf.cell(0, 8, kecamatan, 0, 1)

    pdf.cell(40, 8, 'Kota', 0, 0)
    pdf.cell(5, 8, ':', 0, 0)
    pdf.cell(0, 8, kota, 0, 1)

    pdf.ln(5)
    isi_penutup = f"Adalah benar berstatus sebagai mahasiswa AKTIF pada semester berjalan di lingkungan Universitas Mitra Indonesia. Surat keterangan ini dibuat untuk keperluan: {tujuan}."
    pdf.multi_cell(0, 8, isi_penutup)
    
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