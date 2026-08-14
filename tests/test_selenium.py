import threading
import time
import requests
import pytest
import sys
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app
import init_db

BASE_URL = 'http://127.0.0.1:5000'


def start_server():
    server = threading.Thread(target=lambda: app.run(host='127.0.0.1', port=5001, debug=False, use_reloader=False))
    server.daemon = True
    server.start()
    time.sleep(1)
    return server


@pytest.fixture(scope='module')
def driver():
    options = ChromeOptions()
    # Use headless mode; if you want visible browser, set headless=False
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-software-rasterizer')
    options.add_argument('--remote-debugging-port=9222')
    # allow overriding the chrome binary via env var (useful for CI/local)
    chrome_env = os.environ.get('CHROME_BINARY')
    if chrome_env and os.path.exists(chrome_env):
        options.binary_location = chrome_env
    else:
        # detect local chrome/chromium binary from common locations
        possible = [
            '/usr/bin/google-chrome',
            '/usr/bin/google-chrome-stable',
            '/usr/bin/chromium-browser',
            '/usr/bin/chromium',
            '/snap/bin/chrome',
        ]
        for p in possible:
            if os.path.exists(p):
                options.binary_location = p
                break
    if hasattr(options, 'binary_location') and options.binary_location:
        print(f"Using Chrome binary: {options.binary_location}")
    else:
        print('Warning: No Chrome/Chromium binary found on common paths. Set CHROME_BINARY to your chrome binary path.')
    service = ChromeService(ChromeDriverManager().install())
    drv = webdriver.Chrome(service=service, options=options)
    yield drv
    drv.quit()


def test_create_comment_get_and_delete(driver):
    # reset database
    init_db.start()

    # using already-running local server on port 5000; do not start test server

    post_id = 'test-post-123'
    # create a post
    driver.get(BASE_URL + '/create')
    time.sleep(0.5)
    driver.find_element(By.NAME, 'id').send_keys(post_id)
    driver.find_element(By.NAME, 'title').send_keys('Test Title')
    driver.find_element(By.NAME, 'link').send_keys('http://example.com')
    driver.find_element(By.CSS_SELECTOR, 'button[type=submit]').click()

    time.sleep(0.5)
    # verify we're on the post page and title is present
    title = driver.find_element(By.CSS_SELECTOR, 'h2 a').text
    assert 'Test Title' in title

    # post a comment/description
    driver.find_element(By.NAME, 'user').send_keys('selenium')
    driver.find_element(By.NAME, 'body').send_keys('This is a description')
    driver.find_element(By.CSS_SELECTOR, 'form button[type=submit]').click()

    time.sleep(0.5)
    # check comment appears
    body_texts = driver.find_elements(By.XPATH, "//p[contains(text(), 'This is a description')]")
    assert len(body_texts) >= 1

    # GET check using requests
    r = requests.get(f"{BASE_URL}/{post_id}")
    assert r.status_code == 200
    assert 'Test Title' in r.text

    # delete the post
    # find delete button and click
    delete_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Delete Post')]")
    delete_btn.click()
    time.sleep(0.5)

    # now GET should return 404
    r2 = requests.get(f"{BASE_URL}/{post_id}")
    assert r2.status_code == 404
 
