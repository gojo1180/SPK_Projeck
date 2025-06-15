# controllers/makanan_controller.py

from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException, status
from model.makanan import Makanan
from model.nilai_gizi import NilaiGizi
from model.hasil import Hasil   # <-- TAMBAHKAN impor ini
from schema.makanan_schemas import MakananCreate
import base64
import json # <-- TAMBAHKAN impor ini

async def create_makanan(db: Session, makanan: MakananCreate, gambar: UploadFile, nilai_gizi_json: str): # <-- TAMBAHKAN parameter
    existing = db.query(Makanan).filter(Makanan.nama == makanan.nama).first()
    if existing:
        raise HTTPException(status_code=400, detail="Makanan dengan nama tersebut sudah ada")

    gambar_bytes = await gambar.read()

    new_makanan = Makanan(
        nama=makanan.nama,
        deskripsi=makanan.deskripsi,
        gambar=gambar_bytes
    )

    # --- LOGIKA BARU UNTUK NILAI GIZI ---
    if nilai_gizi_json:
        try:
            nilai_gizi_data = json.loads(nilai_gizi_json) # Parse string JSON
            for item in nilai_gizi_data:
                if item.get('nilai') is not None: # Hanya simpan jika ada nilainya
                    gizi = NilaiGizi(
                        id_kriteria=item['id_kriteria'],
                        nilai=item['nilai']
                    )
                    new_makanan.nilai_gizi.append(gizi)
        except (json.JSONDecodeError, KeyError) as e:
            raise HTTPException(status_code=400, detail=f"Format data nilai gizi tidak valid: {e}")
    # --- AKHIR LOGIKA BARU ---

    db.add(new_makanan)
    db.commit()
    db.refresh(new_makanan)
    return new_makanan

# ... (get_all_makanan tidak perlu diubah) ...

async def update_makanan_controller(
    db: Session,
    makanan_id: int,
    nama: str,
    deskripsi: str,
    nilai_gizi_json: str, # <-- TAMBAHKAN parameter
    gambar: UploadFile = None
):
    makanan = db.query(Makanan).filter(Makanan.id_makanan == makanan_id).first()

    if not makanan:
        raise HTTPException(status_code=404, detail="Makanan tidak ditemukan")

    makanan.nama = nama
    makanan.deskripsi = deskripsi

    if gambar:
        content = await gambar.read()
        makanan.gambar = content

    # --- LOGIKA BARU UNTUK UPDATE NILAI GIZI ---
    # 1. Hapus nilai gizi lama
    db.query(NilaiGizi).filter(NilaiGizi.id_makanan == makanan_id).delete(synchronize_session=False)

    # 2. Tambahkan nilai gizi baru dari form
    if nilai_gizi_json:
        try:
            nilai_gizi_data = json.loads(nilai_gizi_json)
            for item in nilai_gizi_data:
                 if item.get('nilai') is not None and str(item.get('nilai')).strip() != '':
                    gizi = NilaiGizi(
                        id_makanan=makanan_id,
                        id_kriteria=item['id_kriteria'],
                        nilai=float(item['nilai'])
                    )
                    db.add(gizi)
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            raise HTTPException(status_code=400, detail=f"Format data nilai gizi tidak valid: {e}")
    # --- AKHIR LOGIKA BARU ---


    db.commit()
    db.refresh(makanan)

    # ... (sisa kode tidak berubah) ...
    encoded_gambar = (
        base64.b64encode(makanan.gambar).decode("utf-8") if makanan.gambar else None
    )

    return {
        "id_makanan": makanan.id_makanan,
        "nama": makanan.nama,
        "deskripsi": makanan.deskripsi,
        "gambar": encoded_gambar
    }


def get_all_makanan(db: Session):
    """
    Mengambil semua data makanan dan meng-encode gambar ke Base64
    agar aman dikirim sebagai JSON.
    """
    makanan_list = db.query(Makanan).all()
    
    result = []
    for makanan in makanan_list:
        # Siapkan variabel untuk gambar yang sudah di-encode
        encoded_gambar = None
        if makanan.gambar:
            # Ubah data biner gambar menjadi string base64
            encoded_gambar = base64.b64encode(makanan.gambar).decode("utf-8")
        
        # Buat dictionary dengan format yang benar
        result.append({
            "id_makanan": makanan.id_makanan,
            "nama": makanan.nama,
            "deskripsi": makanan.deskripsi,
            "gambar": encoded_gambar  # Gunakan gambar yang sudah di-encode
        })
        
    return result

def force_delete_makanan(db: Session, makanan_id: int):
    """
    Menghapus makanan dan semua data terkaitnya secara paksa.
    Ini termasuk menghapus data dari tabel 'hasil' yang merujuk ke makanan ini.
    """
    # 1. Cari makanan berdasarkan ID
    makanan_to_delete = db.query(Makanan).filter(Makanan.id_makanan == makanan_id).first()
    if not makanan_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Makanan tidak ditemukan")

    # 2. Hapus semua entri di tabel 'hasil' yang terkait dengan makanan ini
    db.query(Hasil).filter(Hasil.id_makanan == makanan_id).delete(synchronize_session=False)

    # 3. Hapus makanan itu sendiri.
    #    Data NilaiGizi akan terhapus secara otomatis karena cascade="all, delete-orphan".
    db.delete(makanan_to_delete)

    # 4. Commit semua perubahan ke database
    db.commit()

    return {"message": f"Makanan dengan ID {makanan_id} dan semua data terkaitnya berhasil dihapus."}