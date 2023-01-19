import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(name='driver')
def driver():
    driver = webdriver.Chrome('/windriverfortests/chromedriver.exe')
    driver.implicitly_wait(10)
    driver.set_window_size(1700, 980)

    yield driver

    driver.quit()


def test_pet_friends(driver):
    # Open PetFriends main page:
    driver = driver
    driver.get("https://petfriends.skillfactory.ru/")

    # click register button
    btn_new_user = driver.find_element(by=By.XPATH, value="//button[@onclick=\"document.location='/new_user';\"]")
    btn_new_user.click()

    # I have an account
    btn_exist_acc = driver.find_element(by=By.LINK_TEXT, value="У меня уже есть аккаунт")
    btn_exist_acc.click()

    # email
    field_email = driver.find_element(by=By.ID, value="email")
    field_email.clear()
    field_email.send_keys("ChuchundraIvanovna@mail.com")

    # password
    field_pass = driver.find_element(by=By.ID, value="pass")
    field_pass.clear()
    field_pass.send_keys("ChuchundraIvanovna")

    # click submit button
    btn_submit = driver.find_element(by=By.XPATH, value="//button[@type='submit']")
    btn_submit.click()

    # check PetFriends "all pets" page
    assert driver.current_url == 'https://petfriends.skillfactory.ru/all_pets'

    # "my pets" page
    btn_my_pets = driver.find_element(by=By.LINK_TEXT, value="Мои питомцы")
    btn_my_pets.click()

    images = WebDriverWait(driver, 3).until(
        EC.presence_of_all_elements_located((By.XPATH, '//*[@scope="row"]/img')))
    names = WebDriverWait(driver, 3).until(
        EC.presence_of_all_elements_located((By.XPATH, '//*[@scope="row"]/following-sibling::td[1]')))
    descriptions = WebDriverWait(driver, 3).until(
        EC.presence_of_all_elements_located((By.XPATH, '//*[@scope="row"]/following-sibling::td[2]')))

    count_pets = driver.find_element(by=By.XPATH, value="//*[@class='.col-sm-4 left']").text.split('\n')[1].split(' ')[-1]

    # check all the pets have names and descriptions
    for i in range(len(names)):
        assert names[i].text != ''
        assert descriptions[i].text != ''

    my_list = []
    for i in range(len(names)):
        my_list.append(driver.find_element(by=By.XPATH,
                                           value='//*[@id="all_my_pets"]/table/tbody/tr['+str(i+1)+']/td[1]').text)

    # check all the pets are at "my pets" page
    assert int(count_pets) == len(names)
    # check at least the half of pets has images
    assert len(images) >= int(count_pets)/2
    # check all the pets existing at the page have names and descriptions
    assert int(count_pets) == len(names) == len(descriptions)

    # check all the pets have different names
    my_list_unique = set(my_list)
    assert len(my_list_unique) == len(my_list)
