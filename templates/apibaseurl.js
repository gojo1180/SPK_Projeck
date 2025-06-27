// apibaseurl.js
const isProduction = true; // GANTI sesuai environment

export const API_BASE_URL = isProduction
  ? 'https://b712-110-138-89-247.ngrok-free.app/' // Ngrok aktif
  : 'http://192.168.1.102/';
