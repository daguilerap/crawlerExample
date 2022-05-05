
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import os
import shutil
import pyautogui




def download_file(product_name,file_kml):
    try:
        # obtengo el directorio actual
        current_dir = os.getcwd()

        # archivo temporal
        tmp_download_dir = f'{current_dir}\\tmpDownload'

        #si el archivo esta creado lo borra
        if os.path.isdir(tmp_download_dir):
            shutil.rmtree(tmp_download_dir)

        # Crea el archivo temporal
        os.mkdir(tmp_download_dir)

        #carga el chormedirver de selenium
        chromedriver_path = 'resource/chromedriver.exe'
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        options.add_argument("--safebrowsing-disable-download-protection")
        options.add_argument("safebrowsing-disable-extension-blacklist")


        options.add_experimental_option("prefs", {
            'download.default_directory': tmp_download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": False
        })

        browser = webdriver.Chrome(executable_path=chromedriver_path ,options=options)
        browser.implicitly_wait(3)

        #navega a la pagina
        browser.get("http://centrodedescargas.cnig.es/CentroDescargas/index.jsp")

        browser.find_element_by_xpath('//*[@id="menuCddBuscar"]').click()

        browser.find_element_by_xpath('//*[@id="menuCargarShp"]').click()
        sleep(5)

        elm = browser.find_element_by_xpath("//input[@type='file']")

        # el roi lo toma la direccion y lo carga
        elm.send_keys(os.getcwd() + file_kml)
        sleep(3)

        # selecciona el slect y combrueba que el elemento este en el
        select = Select(browser.find_element_by_id('comboProdShape'))
        try:
            select.select_by_visible_text(product_name)
        except:
            print('el elemento no se encuentra en la lista')

        res=select.first_selected_option.get_attribute("value")

        browser.find_element_by_xpath('//*[@id="bDrawGeoFile"]').click()
        sleep(3)

        browser.find_element_by_xpath(f'//*[@id="checkAllFiles_{res}"]').click()
        sleep(10)

        browser.find_element_by_xpath('//*[@id="menuCddDescarga"]').click()
        sleep(3)

        browser.find_element_by_xpath('//*[@id="bInitDesc"]').click()
        sleep(3)

        browser.find_element_by_xpath('//*[@id="bAceptLic"]').click()
        sleep(2)

        browser.find_element_by_xpath('//*[@id="bNoEnviarEnc"]').click()
        sleep(2)

        browser.find_element_by_xpath('//*[@id="bDescAuto0"]').click()
        sleep(2)

        # Selenium no permite saltarme la advertencia de descarga
        # por lo que he usado pyautogui para hacer el click de forma automatica
        sleep(2)

        pyautogui.moveTo(480, 1341)
        pyautogui.click()
    except:
        print('Error en la descarga')
        browser.quit()

if __name__ == '__main__':
    download_file('BTN',"/roi.kml")

