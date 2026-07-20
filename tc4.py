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

# --- HANYA TC 4 YANG DIJALANKAN ---
def test_tc_reg_04_password_mismatch(driver):
    print("\n[INFO] Menjalankan Test Case Register 04 (Password Tidak Sama)...")
    driver.get(f"{BASE_URL}/register.php")
    
    # Isi form, sengaja buat password dan repassword BERBEDA
    driver.find_element(By.NAME, "name").send_keys("Nala Rohmah")
    driver.find_element(By.NAME, "email").send_keys("nala_test@example.com")
    driver.find_element(By.NAME, "username").send_keys("nalarohmah123")
    
    driver.find_element(By.NAME, "password").send_keys("Password123")
    driver.find_element(By.NAME, "repassword").send_keys("Berbeda456") # <- Format sengaja disalahkan
    
    # Klik tombol Register
    driver.find_element(By.NAME, "submit").click()
    
    # Menunggu elemen peringatan dengan class 'text-danger' muncul di halaman
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "text-danger")))
    
    # Menangkap pesan peringatan dari PHP
    error_message = driver.find_element(By.CLASS_NAME, "text-danger").text
    
    # Ekspektasi: Teks peringatan berisi kata-kata password tidak sama
    assert "Password tidak sama" in error_message, "Pesan error password tidak muncul!"
    print(f"\n[SUKSES] Validasi berhasil, pesan error yang muncul: '{error_message}'")

# --- PEMICU RUN BISA LEWAT TOMBOL PLAY / PYTHON BIASA ---
if __name__ == "__main__":
    pytest.main(["-v", "-s", __file__])