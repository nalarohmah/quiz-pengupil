import pytest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

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

# --- HANYA TC 7 YANG DIJALANKAN (PASSWORD SALAH) ---
def test_tc_log_03_wrong_password(driver):
    print("\n[INFO] Menjalankan Test Case Login 03 (Password Salah)...")
    driver.get(f"{BASE_URL}/login.php")
    
    # Isi form dengan username yang VALID (sudah ada di database)
    driver.find_element(By.NAME, "username").send_keys("nalarohmah123") 
    
    # Isi form dengan password yang SALAH
    driver.find_element(By.NAME, "password").send_keys("PasswordSuperSalah123")
    
    # Klik tombol Sign In
    driver.find_element(By.NAME, "submit").click()
    
    # EKSPEKTASI: Sistem menampilkan pesan error "salah" atau "gagal"
    # KENYATAAN: Karena ada BUG di kode PHP, pesan ini tidak akan pernah muncul, 
    # sehingga script ini akan Timeout dan menghasilkan FAILED.
    page_text = driver.page_source.lower()
    
    assert "salah" in page_text or "gagal" in page_text, "BUG DITEMUKAN: Sistem tidak menampilkan pesan error saat password salah!"
    print("\n[SUKSES] Validasi berhasil, sistem menampilkan pesan error password salah.")

# --- PEMICU RUN BISA LEWAT TOMBOL PLAY / PYTHON BIASA ---
if __name__ == "__main__":
    pytest.main(["-v", "-s", __file__])