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

# --- HANYA TC 8 YANG DIJALANKAN (FORM LOGIN KOSONG) ---
def test_tc_log_04_empty_login(driver):
    print("\n[INFO] Menjalankan Test Case Login 04 (Form Kosong)...")
    driver.get(f"{BASE_URL}/login.php")
    
    # Langsung klik tombol Sign In tanpa mengisi username dan password
    driver.find_element(By.NAME, "submit").click()
    
    # Menunggu hingga sistem memunculkan kotak peringatan error (alert-danger)
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "alert-danger")))
    
    # Menangkap pesan error dari PHP
    error_message = driver.find_element(By.CLASS_NAME, "alert-danger").text
    
    # Ekspektasi: Muncul pesan error "Data tidak boleh kosong" sesuai logika di login.php
    assert "Data tidak boleh kosong" in error_message, "Pesan error tidak sesuai atau tidak muncul!"
    print(f"\n[SUKSES] Validasi form kosong berhasil, sistem menampilkan pesan: '{error_message}'")

# --- PEMICU RUN BISA LEWAT TOMBOL PLAY / PYTHON BIASA ---
if __name__ == "__main__":
    pytest.main(["-v", "-s", __file__])