# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import os
import glob
"""
import selenium.common.exceptions
from SeleniumTester import SeleniumTester
from Test import Test
import smtplib


selenium_tester_1 = SeleniumTester("09-58-31@hotmail.com", "123456qwe")
# bütün fonksiyonlar bu arrayde tutuluyor.
# Array'i gezip fonksiyonları çağıracağız.
# Array'e fonksiyonları çağırmadan koyduk. () olmaksızın.
array_of_test_functions = [
#selenium_tester_1.is_customer_add,
#selenium_tester_1.is_product_add,
selenium_tester_1.is_stock_add
#selenium_tester_1.is_stock_sub,
#selenium_tester_1.is_ware_hause_stock_list_change,
#selenium_tester_1.is_log_out,
#selenium_tester_1.is_setting_company,
#selenium_tester_1.is_change_password,
#selenium_tester_1.is_order_add,
#selenium_tester_1.is_delete_customer,
#selenium_tester_1.is_search_and_find_customer,
#selenium_tester_1.is_supplier_add,  # Burada sayı olarak olabiliriz sayfalara bölünmüyor.
#selenium_tester_1.is_income_and_expense_add,
#selenium_tester_1.is_delete_supplier,
#selenium_tester_1.is_delete_order,
#selenium_tester_1.is_purchase_order_add,
        #selenium_tester_1.is_register_dopigo, # Henüz çalışmamakta. Robot kontrolü var.
#selenium_tester_1.is_income_and_expense_delete,
#selenium_tester_1.is_income_and_expense_repeat,
#selenium_tester_1.is_change_price_tracker_per_day,
#selenium_tester_1.is_batch_product_download_and_update,
        #selenium_tester_1.is_update_mass_order_cargo_information, # Excelden kaynaklanan sorunlar var. Staging'de çalışmıyor.
#selenium_tester_1.is_batch_product_download_and_send
]
array_of_test_object = [Test()] * len(array_of_test_functions) # Sonuçlara başlangıçta boş nesne atadık.

# Bu döngü her seferinde test arrayinden bir test çağırıyor. Sonucunu sonuç array'ine yazıyor.
# Hata olursa fırlatıyor ve diğer testler bitene kadar devam ediyor.
#for i,test_function in enumerate(array_of_test_functions_results):
i=0
while (i < len(array_of_test_functions) ):
    #array_of_test_object[i].set_result(array_of_test_functions[i]())  # Fonksiyonu çağırdık. bool sonucunu set ettik.
    try:
        array_of_test_object[i].set_test_name( array_of_test_functions[i].__name__ ) # nesneye testin adını string olarak gönderdik.
        # bu listede test nesnelerini tuturoyuruz. İlk olarak isimleri yazdık sonralıkla sonucu ve varsa hataları atıyoruz.
        array_of_test_object[i].set_result( array_of_test_functions[i]() ) # Fonksiyonu çağırdık. bool sonucunu set ettik.
        # array_of_test_functions[i] Burası bir fonksiyon adı döndürüyor
        # Örnek olarak selenium_tester_1.is_order_add
        # () koyup çağırıyoruz.
        if array_of_test_object[i].get_result() == False:
            array_of_test_object[i].set_error_page( selenium_tester_1.get_driver().current_url )
            # Buraya artı olarak hatanın ne olduğunu yazdırabiliriz.
    except selenium.common.exceptions.NoSuchElementException as error:
        # Aranan şey sitede yoksa bu hatayı verir. Sitede bir sorun olmuş olabilir.
        array_of_test_object[i].set_result(False)
        array_of_test_object[i].set_error(error)
        array_of_test_object[i].set_error_page(selenium_tester_1.get_driver().current_url)
    except Exception as e:
        array_of_test_object[i].set_result(False)
        array_of_test_object[i].set_error(e)
        array_of_test_object[i].set_error_page(selenium_tester_1.get_driver().current_url)
    finally:
        i+=1



test_results_string="" # çalıştırılan bütün test sonuçlarını tuttuğumuz string
# arraydeki her eleman bir test nesnesidir. Bu nesne teste dair bilgileri tutuyor.
for i,test_object in enumerate(array_of_test_object):
    test_results_string += test_object.__str__()
    if i != len(array_of_test_object)-1: # nesnelerin arasına çentik koyduk.
        # Sadece sonuncuya koymadık. estetik sebeplerden.
        test_results_string += "-------------------------------------"
    else:
        test_results_string+="This email was sent automatically."

#melih@dopigo.com hedef email
# batman.fatih7@hotmail.com deneme için kullanılan
# sonuçları email atıyoruz.
server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
server.login("selenium.tester.dopigo@gmail.com", "X6cMn7Yc")
server.sendmail("selenium.tester.dopigo@gmail.com",
                "batman.fatih7@hotmail.com", "Hello.\n" + str(test_results_string))
server.quit()

selenium_tester_1.driver.close()
quit()