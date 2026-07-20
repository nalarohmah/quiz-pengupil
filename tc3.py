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

# --- HANYA TC 3 YANG DIJALANKAN ---
def test_tc_reg_03_invalid_email(driver):
    print("\n[INFO] Menjalankan Test Case Register 03 (Email Tidak Valid)...")
    driver.get(f"{BASE_URL}/register.php")
    
    # Isi form, sengaja buat format email menjadi salah (tanpa @)
    driver.find_element(By.NAME, "name").send_keys("Nala Rohmah")
    driver.find_element(By.NAME, "email").send_keys("usercom") # <- Format sengaja disalahkan
    driver.find_element(By.NAME, "username").send_keys("nalarohmah123")
    driver.find_element(By.NAME, "password").send_keys("Password123")
    driver.find_element(By.NAME, "repassword").send_keys("Password123")
    
    # Klik tombol Register
    driver.find_element(By.NAME, "submit").click()
    
    # Menangkap pesan peringatan bawaan browser (HTML5 Validation)
    email_field = driver.find_element(By.NAME, "email")
    validation_message = email_field.get_attribute("validationMessage")
    
    # Ekspektasi: Browser menampilkan peringatan dan form batal terkirim
    assert validation_message != "", "Pesan validasi HTML5 tidak muncul!"
    print(f"\n[SUKSES] Validasi berhasil, pesan error yang muncul: '{validation_message}'")

# --- PEMICU RUN BISA LEWAT TOMBOL PLAY / PYTHON BIASA ---
if __name__ == "__main__":
    pytest.main(["-v", "-s", __file__])