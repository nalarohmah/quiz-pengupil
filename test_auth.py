import pytest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# URL dinamis yang bisa mendeteksi apakah berjalan di lokal atau di GitHub Actions
BASE_URL = os.getenv("BASE_URL", "http://localhost/quiz-pengupil-main")

@pytest.fixture
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # Tambahkan 2 baris ini agar ukuran layar server virtual pas dan elemen tidak tersembunyi:
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10) # Naikkan sedikit waktu tunggu dari 5 ke 10 detik
    yield driver
    driver.quit()

# ================= MODUL REGISTER =================

def test_tc_reg_01_positive(driver):
    driver.get(f"{BASE_URL}/register.php")
    driver.find_element(By.NAME, "name").send_keys("Nala Rohmah")
    driver.find_element(By.NAME, "email").send_keys("nala_test@example.com")
    driver.find_element(By.NAME, "username").send_keys("nalarohmah123")
    driver.find_element(By.NAME, "password").send_keys("Password123")
    driver.find_element(By.NAME, "repassword").send_keys("Password123")
    driver.find_element(By.NAME, "submit").click()
    WebDriverWait(driver, 5).until(EC.url_contains(".php"))
    assert "register.php" not in driver.current_url

def test_tc_reg_02_empty_fields(driver):
    driver.get(f"{BASE_URL}/register.php")
    driver.find_element(By.NAME, "submit").click()
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "alert-danger")))
    error_message = driver.find_element(By.CLASS_NAME, "alert-danger").text
    assert "Data tidak boleh kosong" in error_message

def test_tc_reg_03_invalid_email(driver):
    driver.get(f"{BASE_URL}/register.php")
    driver.find_element(By.NAME, "name").send_keys("Nala Rohmah")
    driver.find_element(By.NAME, "email").send_keys("usercom") 
    driver.find_element(By.NAME, "username").send_keys("nalarohmah123")
    driver.find_element(By.NAME, "password").send_keys("Password123")
    driver.find_element(By.NAME, "repassword").send_keys("Password123")
    driver.find_element(By.NAME, "submit").click()
    email_field = driver.find_element(By.NAME, "email")
    validation_message = email_field.get_attribute("validationMessage")
    assert validation_message != ""

def test_tc_reg_04_password_mismatch(driver):
    driver.get(f"{BASE_URL}/register.php")
    driver.find_element(By.NAME, "name").send_keys("Nala Rohmah")
    driver.find_element(By.NAME, "email").send_keys("nala_test@example.com")
    driver.find_element(By.NAME, "username").send_keys("nalarohmah123")
    driver.find_element(By.NAME, "password").send_keys("Password123")
    driver.find_element(By.NAME, "repassword").send_keys("Berbeda456") 
    driver.find_element(By.NAME, "submit").click()
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "text-danger")))
    error_message = driver.find_element(By.CLASS_NAME, "text-danger").text
    assert "Password tidak sama" in error_message

# ================= MODUL LOGIN =================

def test_tc_log_01_positive(driver):
    driver.get(f"{BASE_URL}/login.php")
    driver.find_element(By.NAME, "username").send_keys("nalarohmah123") 
    driver.find_element(By.NAME, "password").send_keys("Password123")
    driver.find_element(By.NAME, "submit").click()
    WebDriverWait(driver, 5).until(EC.url_contains("index.php"))
    assert "index.php" in driver.current_url

def test_tc_log_02_unregistered_user(driver):
    driver.get(f"{BASE_URL}/login.php")
    driver.find_element(By.NAME, "username").send_keys("userpalsu_belum_daftar") 
    driver.find_element(By.NAME, "password").send_keys("Password123")
    driver.find_element(By.NAME, "submit").click()
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "alert-danger")))
    error_message = driver.find_element(By.CLASS_NAME, "alert-danger").text
    assert "Gagal" in error_message or "Register User Gagal" in error_message

def test_tc_log_03_wrong_password(driver):
    driver.get(f"{BASE_URL}/login.php")
    driver.find_element(By.NAME, "username").send_keys("nalarohmah123") 
    driver.find_element(By.NAME, "password").send_keys("PasswordSuperSalah123")
    driver.find_element(By.NAME, "submit").click()
    page_text = driver.page_source.lower()
    
    # Catatan: Test case ini akan FAILED secara natural karena bug pada login.php yang sudah kita analisis
    assert "salah" in page_text or "gagal" in page_text

def test_tc_log_04_empty_login(driver):
    driver.get(f"{BASE_URL}/login.php")
    driver.find_element(By.NAME, "submit").click()
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "alert-danger")))
    error_message = driver.find_element(By.CLASS_NAME, "alert-danger").text
    assert "Data tidak boleh kosong" in error_message