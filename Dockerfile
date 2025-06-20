# (Gunakan Dockerfile yang sama persis seperti sebelumnya)

# Gunakan base image Python yang efisien
FROM python:3.11-slim

# Atur direktori kerja di dalam container
WORKDIR /app

# Salin file requirements.txt terlebih dahulu untuk caching layer
COPY requirements.txt .

# Install dependensi Python
RUN pip install --no-cache-dir -r requirements.txt

# Salin seluruh kode proyek ke dalam direktori kerja di container
COPY . .

# Expose port yang akan digunakan oleh aplikasi FastAPI
EXPOSE 8000

# Perintah untuk menjalankan aplikasi saat container dimulai
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]