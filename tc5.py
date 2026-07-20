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

# --- HANYA TC 5 YANG DIJALANKAN (LOGIN VALID) ---
def test_tc_log_01_positive(driver):
    print("\n[INFO] Menjalankan Test Case Login 01 (Login Valid)...")
    driver.get(f"{BASE_URL}/login.php")
    
    # Isi form dengan akun yang sudah terdaftar
    # (Pastikan username ini ada di tabel 'users' pada database Anda)
    driver.find_element(By.NAME, "username").send_keys("nalarohmah123") 
    driver.find_element(By.NAME, "password").send_keys("Password123")
    
    # Klik tombol Sign In
    driver.find_element(By.NAME, "submit").click()
    
    # Menunggu dan memastikan halaman berpindah ke index.php
    WebDriverWait(driver, 5).until(EC.url_contains("index.php"))
    
    # Ekspektasi: URL berubah ke halaman utama/dashboard
    assert "index.php" in driver.current_url
    print("\n[SUKSES] Login berhasil dan diarahkan ke index.php")

# --- PEMICU RUN BISA LEWAT TOMBOL PLAY / PYTHON BIASA ---
if __name__ == "__main__":
    pytest.main(["-v", "-s", __file__])