import pytest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = os.getenv("BASE_URL", "http://localhost/quiz-pengupil-main")

# --- PERSIAPAN BROWSER ---
@pytest.fixture
def driver():
    chrome_options = Options()
    # Matikan headless agar proses otomatisasi terlihat di layar
    # chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

# --- HANYA TC 6 YANG DIJALANKAN (USERNAME BELUM TERDAFTAR) ---
def test_tc_log_02_unregistered_user(driver):
    print("\n[INFO] Menjalankan Test Case Login 02 (Username Belum Terdaftar)...")
    driver.get(f"{BASE_URL}/login.php")
    
    # Isi form dengan username asal-asalan yang tidak ada di database
    driver.find_element(By.NAME, "username").send_keys("userpalsu_belum_daftar") 
    driver.find_element(By.NAME, "password").send_keys("Password123")
    
    # Klik tombol Sign In
    driver.find_element(By.NAME, "submit").click()
    
    # Menunggu hingga sistem memunculkan kotak peringatan error (alert-danger)
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "alert-danger")))
    
    # Menangkap pesan error dari PHP
    error_message = driver.find_element(By.CLASS_NAME, "alert-danger").text
    
    # Ekspektasi: Teks peringatan berisi kata 'Gagal' sesuai dengan bug di source code asli
    assert "Gagal" in error_message or "Register User Gagal" in error_message, "Pesan error tidak sesuai!"
    print(f"\n[SUKSES] Validasi berhasil, sistem menolak login dengan pesan: '{error_message}'")

# --- PEMICU RUN BISA LEWAT TOMBOL PLAY / PYTHON BIASA ---
if __name__ == "__main__":
    pytest.main(["-v", "-s", __file__])