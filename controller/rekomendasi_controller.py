import json
import base64 # Impor library untuk encoding Base64
from pathlib import Path
from sqlalchemy.orm import Session
from model import makanan as makanan_model, bobot_preferensi as bobot_model
from model.user import Pengguna

CONFIG_FILE_PATH = Path(__file__).parent.parent / "config" / "default_weight.json"

def get_recommendations(db: Session, current_user: Pengguna, timing: str, fase_latihan: str):
    raw_bobot = {}
    custom_weights_query = db.query(bobot_model.BobotPreferensi).filter(bobot_model.BobotPreferensi.id_pengguna == current_user.id_pengguna).all()
    
    if custom_weights_query:
        print(f"Menggunakan bobot kustom dari user ID: {current_user.id_pengguna}")
        raw_bobot = {w.id_kriteria: w.bobot for w in custom_weights_query}
    else:
        print(f"Menggunakan bobot default untuk fase: {fase_latihan}")
        with open(CONFIG_FILE_PATH, 'r') as f:
            all_default_weights = json.load(f)
        bobot_str_keys = all_default_weights.get(fase_latihan, {}).get(timing, {})
        raw_bobot = {int(k.replace('C', '')): v for k, v in bobot_str_keys.items()}

    if not raw_bobot or not any(v > 0 for v in raw_bobot.values()):
        return {"success": False, "message": f"Tidak ditemukan konfigurasi bobot yang valid untuk fase '{fase_latihan}' dan waktu '{timing}'."}

    total_bobot = sum(raw_bobot.values())
    if total_bobot == 0:
        return {"success": False, "message": "Total bobot adalah nol, perhitungan tidak dapat dilanjutkan."}
    normalized_bobot = {k: v / total_bobot for k, v in raw_bobot.items()}
    
    alternatives = db.query(makanan_model.Makanan).all()
    
    kriteria_values = {k_id: [] for k_id in normalized_bobot.keys()}
    for alt in alternatives:
        for gizi in alt.nilai_gizi:
            if gizi.id_kriteria in kriteria_values:
                kriteria_values[gizi.id_kriteria].append(gizi.nilai)

    kriteria_min_max = {k_id: (min(vals), max(vals)) for k_id, vals in kriteria_values.items() if vals}

    scored_results = []
    for alt in alternatives:
        skor_akhir = 0
        for gizi in alt.nilai_gizi:
            kriteria_id = gizi.id_kriteria
            if kriteria_id in normalized_bobot and kriteria_id in kriteria_min_max:
                nilai_alternatif = gizi.nilai
                c_min, c_max = kriteria_min_max[kriteria_id]
                if (c_max - c_min) == 0:
                    utility_value = 1.0
                else:
                    utility_value = (nilai_alternatif - c_min) / (c_max - c_min)
                skor_akhir += utility_value * normalized_bobot[kriteria_id]
        
        # PERBAIKAN GAMBAR: Encode data biner ke Base64
        gambar_base64 = None
        if alt.gambar:
            gambar_base64 = f"data:image/jpeg;base64,{base64.b64encode(alt.gambar).decode('utf-8')}"

        scored_results.append({
            "id": alt.id_makanan,
            "nama": alt.nama,
            "penjelasan": alt.deskripsi, # Menggunakan 'deskripsi'
            "gambar": gambar_base64,     # Menggunakan gambar yang sudah di-encode
            "waktu": timing,             # PERBAIKAN WAKTU: Menggunakan parameter 'timing'
            "skor": skor_akhir
        })

    ranked_results = sorted(scored_results, key=lambda x: x['skor'], reverse=True)
    return {"success": True, "data": ranked_results}