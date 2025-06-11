import json
from pathlib import Path
from sqlalchemy.orm import Session
from model import makanan as makanan_model, bobot_preferensi as bobot_model, nilai_gizi as nilai_gizi_model, kriteria as kriteria_model
from model.user import Pengguna

CONFIG_FILE_PATH = Path(__file__).parent.parent / "config" / "default_weights.json"

def get_recommendations(db: Session, current_user: Pengguna, timing: str):
    
    # 1. TENTUKAN BOBOT MENTAH (RAW WEIGHTS) DARI USER ATAU DEFAULT
    raw_bobot = {}
    custom_weights = db.query(bobot_model.BobotPreferensi).filter(bobot_model.BobotPreferensi.id_pengguna == current_user.id_pengguna).all()
    
    if custom_weights:
        print("Menggunakan bobot kustom dari user.")
        raw_bobot = {w.id_kriteria: w.bobot for w in custom_weights}
    else:
        print(f"Menggunakan bobot default untuk fase: {current_user.fase_latihan.value}")
        with open(CONFIG_FILE_PATH, 'r') as f:
            all_default_weights = json.load(f)
        fase = current_user.fase_latihan.value
        bobot_str_keys = all_default_weights.get(fase, {}).get(timing, {})
        raw_bobot = {int(k.replace('C', '')): v for k, v in bobot_str_keys.items()}

    if not raw_bobot:
        return {"success": False, "message": "Tidak ditemukan konfigurasi bobot yang sesuai."}

    # LANGKAH A: NORMALISASI BOBOT (SMART)
    total_bobot = sum(raw_bobot.values())
    normalized_bobot = {k: v / total_bobot for k, v in raw_bobot.items()}
    
    # 2. AMBIL SEMUA ALTERNATIF DAN NILAI GIZINYA
    alternatives = db.query(makanan_model.Makanan).all()
    
    # Kumpulkan semua nilai untuk setiap kriteria untuk mencari min & max
    kriteria_values = {k_id: [] for k_id in normalized_bobot.keys()}
    for alt in alternatives:
        for gizi in alt.nilai_gizi:
            if gizi.id_kriteria in kriteria_values:
                kriteria_values[gizi.id_kriteria].append(gizi.nilai)

    # Cari nilai min dan max untuk setiap kriteria
    kriteria_min_max = {k_id: (min(vals), max(vals)) for k_id, vals in kriteria_values.items() if vals}

    # 3. LAKUKAN PERHITUNGAN SKOR (METODE SMART)
    scored_results = []
    for alt in alternatives:
        skor_akhir = 0
        for gizi in alt.nilai_gizi:
            kriteria_id = gizi.id_kriteria
            
            # Pastikan kriteria ini punya bobot dan nilai min/max
            if kriteria_id in normalized_bobot and kriteria_id in kriteria_min_max:
                nilai_alternatif = gizi.nilai
                c_min, c_max = kriteria_min_max[kriteria_id]
                
                # LANGKAH B: HITUNG NILAI UTILITY (SMART)
                # Hindari pembagian dengan nol jika semua nilai sama
                if (c_max - c_min) == 0:
                    utility_value = 1
                else:
                    utility_value = (nilai_alternatif - c_min) / (c_max - c_min)
                
                # Kalkulasi skor akhir: skor = skor + (nilai_utility * bobot_normal)
                skor_akhir += utility_value * normalized_bobot[kriteria_id]
        
        scored_results.append({"makanan": alt, "skor": skor_akhir})

    # 4. URUTKAN HASIL BERDASARKAN SKOR
    ranked_results = sorted(scored_results, key=lambda x: x['skor'], reverse=True)
    
    return {"success": True, "data": ranked_results}