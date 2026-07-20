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

# --- HANYA TC 2 YANG DIJALANKAN ---
def test_tc_reg_02_empty_fields(driver):
    print("\n[INFO] Menjalankan Test Case Register 02 (Form Kosong)...")
    driver.get(f"{BASE_URL}/register.php")
    
    # Langsung klik tombol Register tanpa mengisi satu pun kotak input
    driver.find_element(By.NAME, "submit").click()
    
    # Menunggu hingga sistem merespons dan menampilkan kotak peringatan bahaya (alert-danger)
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "alert-danger")))
    
    # Mengambil teks dari kotak peringatan tersebut
    error_message = driver.find_element(By.CLASS_NAME, "alert-danger").text
    
    # Ekspektasi: Sistem menolak form dan menampilkan pesan error PHP yang sesuai
    assert "Data tidak boleh kosong" in error_message