# python -m pytest -v --driver Chrome --driver-path C:\chromedriver\chromedriver.exe practice25.py
import pytest
from selenium import webdriver
driver = webdriver.Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(autouse=True)
def testing():
   pytest.driver = webdriver.Chrome('C:\chromedriver\chromedriver.exe')
   # Переход на страницу авторизации:
   pytest.driver.get('http://petfriends.skillfactory.ru/login')

   yield

   pytest.driver.quit()

def test_show_my_pets():
    # Вводим email:
    pytest.driver.find_element_by_id('email').send_keys('engine87@mail.ru')
    # Вводим пароль:
    pytest.driver.find_element_by_id('pass').send_keys('121212')
    # Нажимаем на кнопку входа в аккаунт:
    pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя:
    assert pytest.driver.find_element_by_tag_name('h1').text == "PetFriends"

# Тест на определение количества питомцев в спике.
def test_count_my_pets():
    # Вводим email:
    pytest.driver.find_element_by_id('email').send_keys('engine87@mail.ru')
    # Вводим пароль:
    pytest.driver.find_element_by_id('pass').send_keys('121212')
    # Нажимаем на кнопку входа в аккаунт:
    pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя:
    WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "card-deck")))
    # Проверяем, есть ли питомцы на странице
    pytest.driver.get('http://petfriends.skillfactory.ru/my_pets')
    pytest.driver.implicitly_wait(5)
    names = pytest.driver.find_elements_by_css_selector('#all_my_pets table tbody tr')
    cnt = pytest.driver.find_element_by_xpath('/html/body/div[1]/div/div[1]').text
    lines = cnt.split()
    print(lines[2])
    print(len(names))
    assert int(lines[2]) == len(names)

# Тест на определение уникальности имён питомцев.
def test_my_pets_with_uniq_names():
    # Вводим email:
    pytest.driver.find_element_by_id('email').send_keys('engine87@mail.ru')
    # Вводим пароль:
    pytest.driver.find_element_by_id('pass').send_keys('121212')
    # Нажимаем на кнопку входа в аккаунт:
    pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя:
    WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "card-deck")))
    assert pytest.driver.find_element_by_tag_name('h1').text == "PetFriends"
    # Проверяем, что мы имена питомцев уникальны:
    pytest.driver.get('http://petfriends.skillfactory.ru/my_pets')
    pytest.driver.implicitly_wait(5)
    names = pytest.driver.find_elements_by_xpath('//td[1]')
    x = 0
    for i in range(len(names) - 1):
        for j in range(i + 1, len(names)):
            if names[i].text == names[j].text:
                x = 1
                quit()
    assert x == 0

# Проверка параметров карточек питомцев:
def test_card_my_pets():
    # Вводим email:
    pytest.driver.find_element_by_id('email').send_keys('engine87@mail.ru')
    # Вводим пароль:
    pytest.driver.find_element_by_id('pass').send_keys('121212')
    # Нажимаем на кнопку входа в аккаунт:
    pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
    # Проверяем наличие информации о питомцах:
    WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "card-deck")))
    assert pytest.driver.find_element_by_tag_name('h1').text == "PetFriends"
    images = pytest.driver.find_elements_by_xpath('//th/img')
    names = pytest.driver.find_elements_by_xpath('//td[1]')
    types = pytest.driver.find_elements_by_xpath('//td[2]')
    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert types[i].text != ''
        assert ', ' in types[i]
        parts = types[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0

# Проверка что у всех питомцев есть фото.
def test_all_my_pets_have_photo():
    # Вводим email:
    pytest.driver.find_element_by_id('email').send_keys('engine87@mail.ru')
    # Вводим пароль:
    pytest.driver.find_element_by_id('pass').send_keys('121212')
    # Нажимаем на кнопку входа в аккаунт:
    pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
    # Проверяем наличие информации о питомцах:
    WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "card-deck")))
    assert pytest.driver.find_element_by_tag_name('h1').text == "PetFriends"
    pytest.driver.get('http://petfriends.skillfactory.ru/my_pets')
    pytest.driver.implicitly_wait(5)
    pets_text = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class=".col-sm-4 left"]')))
    assert 'Питомцев:' in pets_text.text
    amount_of_pets = int(pets_text.text.split('\n')[1].split(':')[1])
    lines = WebDriverWait(pytest.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@id="all_my_pets"]/table[@class="table table-hover"]/tbody/tr')))
    lines_amount = len(lines)
    assert amount_of_pets == lines_amount
    lines = WebDriverWait(pytest.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@id="all_my_pets"]/table[@class="table table-hover"]/tbody/tr/th/img')))
    pets_with_photo = 0
    for line in lines:
        if line.get_attribute('src') != '':
            pets_with_photo += 1
    assert pets_with_photo == amount_of_pets
