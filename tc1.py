import pytest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = os.getenv("BASE_URL", "http://localhost/quiz-pengupil-main")

@pytest.fixture
def driver():
    chrome_options = Options()
    # Matikan headless sementara agar Anda bisa melihat prosesnya
    # chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_tc_reg_01_positive(driver):
    print("\n[INFO] Menjalankan Test Case Register 01...")
    driver.get(f"{BASE_URL}/register.php")
    
    # Mengisi form sesuai dengan atribut 'name' asli di kode sumber
    driver.find_element(By.NAME, "name").send_keys("Nala Rohmah")
    driver.find_element(By.NAME, "email").send_keys("nala_test@example.com")
    driver.find_element(By.NAME, "username").send_keys("nalarohmah123")
    driver.find_element(By.NAME, "password").send_keys("Password123")
    driver.find_element(By.NAME, "repassword").send_keys("Password123")
    
    # Klik tombol Register
    driver.find_element(By.NAME, "submit").click()
    
    # Menunggu dan memastikan halaman berpindah setelah register
    WebDriverWait(driver, 5).until(EC.url_contains(".php"))
    assert "register.php" not in driver.current_url