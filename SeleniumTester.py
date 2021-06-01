# from Test import Test
# import selenium.common.exceptions
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
import openpyxl


class SeleniumTester:
    logged_in = False  # Nesne için sadece ilk girişte login fonksiyonu çalışmalı. Diğer girişler için çalıştırmıyoruz bu değişken ile.

    probationary_period_letter = False  # Deneme süreniz bitecek yazıcı çıkıyorsa sayfanın xpath'leri değişiyor.

    # Bu yüzden çoğu click'ler çalışmıyor. Henüz geliştirilmedi. Buna özel olarak birçok xpath değişmeli.

    def __init__(self, username, password):
        optionsHeadless = Options()
        optionsHeadless.headless = True  # True olursa webdriver görünürde çalışmaz
        # headless True olduğunda ubuntu serverda hata veriyor.
        dir_path = os.path.dirname(os.path.realpath(__file__))
        chromedriver_path = dir_path + "/chromedriver"
        optionsHeadless.add_argument("disable-infobars")
        optionsHeadless.add_argument("--disable-extensions")
        optionsHeadless.add_argument("--disable-gpu")
        optionsHeadless.add_argument('--no-sandbox')
        optionsHeadless.add_argument('--disable-dev-shm-usage')
        optionsHeadless.add_argument("--window-size=1920,1080")
        optionsHeadless.add_argument("start-maximized")
        self.driver = webdriver.Chrome(executable_path=chromedriver_path,options=optionsHeadless)  # İçerdeki parametreyi kaldırırsak pencerede olanları izleyebiliriz.
        self.actions = ActionChains(self.driver)
        #self.driver.maximize_window()  # arka planda pencere küçük açılıyor, butonları bulamayıp hata veriyordu. Bu yüzden eklendi.
        # Headless=true ile kullanıldığında element not interactable hatası veriyor kullanma yukarıyı.
        self.username = username  # Sitemize gireceğimiz kullanıcı adı
        self.password = password  # Sitemize gireceğimiz parola

    def get_driver(self):
        return self.driver

    def check_on_page(self, word):
        if word in self.driver.page_source:  # Yazı sayfada varsa True döndürüyor.
            Result = True
        else:
            Result = False
        return Result

    def check_has_xpath(self, xpath):
        if self.driver.find_element_by_xpath(xpath) is None:  # Genelde ürün eklendi uyarısı için
            Result = False  # kullanıyoruz bu fonksiyonu
        else:
            Result = True
        return Result

    # Url karşılaştırması yapmak için url'yi bölüyoruz.
    def get_first_38_characters(self, string):
        x = ""
        for i in range(0, 38):  # URL son kısmı değişkenlik gösterebileceğinden
            x = x + string[i]  # İlk 38 karakterini karşılaştırıyoruz.
        return x

    # Gönderilen url ile mevcut url aynımı kontrol ediyor.
    # Genelde Ürün eklendikten sonra bir sayfaya atıyorsa, bu sayfadamıyız diye kontrol ediyor.
    def check_on_url(self, url):
        z = self.get_first_38_characters(self.driver.current_url)
        if (z == url):
            return True
        else:
            return False

    # Ekleme sonrası eleman sayısını, ekleme öncesi eleman sayısı ile karşılaştırıyoruz.
    # Bu denklem eşitse eleman ekleme başarılı olmuş demektir.
    # Eleman eklendiğinde sayfa dolmuşsa yeni sayfaya eklenir ve son sayfada 1 eleman olur.
    # dolayısıyla 15 ve 1 eşit olmayınca fonksiyon başarısız sanmasın diye bu kontrol elifte yapılıyor.
    def check_element_add_count(self, number_of_previous_element, number_of_next_element):
        if (number_of_previous_element + 1 == number_of_next_element):
            return True
        elif number_of_previous_element == 15 and number_of_next_element == 1:
            return True
        else:
            return False

    # Yukardakinin eleman silme durumu için.
    def check_element_sub_count(self, number_of_previous_element, number_of_next_element):
        if (number_of_previous_element == number_of_next_element + 1):
            return True
        elif number_of_previous_element==1 and number_of_next_element==15:
            return True # Son sayfadan kalan tek eleman silinince önceki sayfaya geliyorsa eleman silinmiştir.
        else:
            return False

    # Bu fonksiyon, staging.dopigo sitesine bir hesapla girmemizi sağlıyor.
    def click_login(self):
        if (self.logged_in == True):
            return
        self.driver.get("http://staging.dopigo.com/")
        # self.driver.get("https://www.youtube.com")
        # time.sleep(1)

        username = self.driver.find_element_by_name("username")
        password = self.driver.find_element_by_name("password")
        username.send_keys(self.username)  # username kısmına parametredeki kullanici adı gönderildi.
        password.send_keys(self.password)  # Aynı şekilde password gönderildi.

        login_button = self.driver.find_element_by_xpath("//*[@id='login-form']/div[4]/button")
        login_button.click()  # Kullanıcı adı ve parola girildikten sonra giriş yap butonuna basıyoruz.
        # time.sleep(2)
        self.logged_in = True
        return

    def click_orders(self):
        Orders = self.driver.find_element_by_xpath("/html/body/div[3]/header/nav/div/div[2]/ul/li[2]/a")
        Orders.click()
        return

        # Bu fonksiyon bir hesapla siteye girdikten sonra ürünler'e girmemizi sağlıyor.

    def click_products(self):
        Products = self.driver.find_element_by_xpath("/html/body/div[3]/header/nav/div/div[2]/ul/li[3]/a")
        Products.click()
        return

    def click_income_and_expense(self):
        income_expense = self.driver.find_element_by_xpath("/html/body/div[3]/header/nav/div/div[2]/ul/li[4]/a")
        income_expense.click()

    def click_customers(self):
        customers = self.driver.find_element_by_xpath("/html/body/div[5]/header/nav/div/div[2]/ul/li[2]/ul/li[2]")
        customers.click()
        return

    def click_supplier(self):
        self.driver.find_element_by_xpath("/html/body/div[5]/header/nav/div/div[2]/ul/li[2]/ul/li[4]/a").click()
        return

    def click_warehause(self):
        Warehause = self.driver.find_element_by_xpath("/html/body/div[3]/header/nav/div/div[2]/ul/li[3]/ul/li[7]")
        Warehause.click()
        return

    def click_welcome(self):
        welcome_button = self.driver.find_element_by_xpath("/html/body/div[3]/header/nav/div/div[1]/div[2]/div[3]")
        welcome_button.click()
        return

    def click_settings(self):
        setting_button = self.driver.find_element_by_xpath(
            "/html/body/div[3]/header/nav/div/div[1]/div[2]/div[2]/button")
        setting_button.click()
        return

    # Mause ile üzerine gelinen gruplar Hover grubudur.
    def hover_batch_operations(self):
        batch_operations = self.driver.find_element_by_xpath(
            '/html/body/div[3]/header/nav/div/div[2]/ul/li[3]/ul/li[3]')
        self.actions.move_to_element(batch_operations).perform()

    # Ürün seçme dropdown'undan bir tanesini seçiyoruz.
    def select_product(self):
        product = self.driver.find_element_by_id("select2-id_product-container")
        product.click()
        # Dropdown içerisinden birini seçiyoruz.
        # Bu dropdown başka bir yerden verileri alıp içine koyuyor. Normal select komutuyla içinden birini seçemiyoruz.
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH,  # Message: Select only works on <select> elements, not on <ul>
                                        "//*[@id='select2-id_product-results']/li[2]"))).click()  # Yukarıdaki hata Select komutuyla açıldığında geliyordu.
        # Bu haliyle dropdown'dan seçebildik. li[2] Burada sayıyı değiştirsek ürünü değiştiririz.
        # li[1] birinci elemanı seçemiyoruz neden olduğuna bakmadım. diğer elemanalar seçilebiliyor.
        return

    def select_supplier(self):
        supplier = self.driver.find_element_by_id("select2-id_supplier-container")
        supplier.click()
        x = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH,
                                        '//*[@id="select2-id_supplier-results"]/li[2]'))).click()
        return

    # Bu fonksiyon bir ürün eklenmesinin başarılı olup olmadığını kontrol ediyor.
    # Ürün başarıyle eklenmişse True, aksi takdirde False döndürür.
    def is_product_add(self):
        self.click_login()  # "111111111111"
        self.click_products()

        new_product_add = self.driver.find_element_by_xpath(
            "/html/body/div[3]/div/div/div[3]/div/div[1]/div/a[1]/button")
        new_product_add.click()  # Yeni Ürün ekle butonuna basıyoruz.

        username = self.driver.find_element_by_name("pm-name")
        username.send_keys(time.strftime("%H-%M-%S"))  # Ürün ismi girildi.

        """
            # Katogori kısmı yapılamadı fakat bu kısım olmadanda ürün eklenebiliyor.
            # kategori2 = self.driver.find_element_by_xpath("//*[@id='select2-id_pm-category-container']")
            # kategori2.click()
            eklenmeyen başka ürün özellikleri var. parametreler ile birlikte artırılabilir.
        """

        # Barkod ekleniyor.
        barcode = self.driver.find_element_by_name("p-barcode")
        barcode.send_keys("111111111111") # barkod numaralı ürünü oluşturduk.
        time.sleep(2)

        stock = self.driver.find_element_by_name("p-price")
        stock.send_keys("1000")

        product_subhead = self.driver.find_element_by_name("pm-subheading")
        product_subhead.send_keys("aaaaaaaaaaaaa")

        # Eğer aynı barkodlu ürün girilmişse bir uyarı mesajı çıkacak.
        # Dolayısıyla program ürün kaydet butonuna erişemeyecek ve hata verecek.
        # Hata veriyorsa ayın barkodlu 2 ürün yaratılamaz ve except'de False döndürür.
        try:
            product_save_button = self.driver.find_element_by_xpath(
                "//*[@id='add-product']/div[1]/div/div[4]/div[7]/div/button")
            product_save_button.click()
        except:
            #print("111111111111", "Bu barkodu başka üründe de kullandınız.")
            return False
        # time.sleep(1)

        # Burada Yeni ürün yaratıldı yazısı geldimi kontrol ediyoruz.
        if self.driver.find_element_by_xpath("//*[@id='top-message-container']/div") is not None:
            Result = self.check_on_page("Yeni ürün yaratıldı")
        else:
            # print("Element is not present")
            Result = False
        return Result
        # finish isProductAdd()

    def is_stock_add(self):
        self.click_login()
        self.click_products()
        self.click_warehause()

        warehause_in = self.driver.find_element_by_xpath(
            "/html/body/div[3]/header/nav/div/div[2]/ul/li[3]/ul/li[7]/ul/li[1]/a")
        warehause_in.click()

        barcode = self.driver.find_element_by_name("barcode")
        barcode.send_keys("111111111111")
        # Barkod ve Stok giriş çıkış'ın text kısmını doldurduk.
        warehause_stock_in_out = self.driver.find_element_by_name("warehouse_stock_in_out")
        warehause_stock_in_out.send_keys("2")

        warehause_in_button = self.driver.find_element_by_xpath(
            "/html/body/div[3]/div/div/form/div[2]/div[3]/div/button")
        warehause_in_button.click()

        return self.check_has_xpath("//*[@id='top-message-container']/div")  # Ürün eklendi uyarısını kontrol ediyoruz.

    def is_stock_sub(self):
        self.click_login()
        self.click_products()
        self.click_warehause()

        warehuase_out = self.driver.find_element_by_xpath(
            "/html/body/div[3]/header/nav/div/div[2]/ul/li[3]/ul/li[7]/ul/li[2]/a")
        warehuase_out.click()

        barcode = self.driver.find_element_by_name("barcode")
        barcode.send_keys("111111111111")  # Barkod nolu ürünü güncelliyoruz.
        # Barkod ve Stok giriş çıkış'ın text kısmını doldurduk.
        warehause_stock_in_out = self.driver.find_element_by_name("warehouse_stock_in_out")
        warehause_stock_in_out.send_keys("2")  # Her seferde 2 adet stokdan çıkaracak.

        warehuase_out_button = self.driver.find_element_by_xpath(
            "/html/body/div[3]/div/div/form/div[2]/div[3]/div/button")
        warehuase_out_button.click()

        return self.check_has_xpath("//*[@id='top-message-container']/div")  # Ürün eklendi uyarısını kontrol ediyoruz.

    def is_customer_add(self):
        self.click_login()
        self.click_orders()

        current_time = time.strftime("%H:%M:%S")
        customers = self.driver.find_element_by_xpath("/html/body/div[5]/header/nav/div/div[2]/ul/li[2]/ul/li[2]")
        # /html/body/div[5]/header/nav/div/div[2]/ul/li[2]/ul/li[2]
        customerAdd = self.driver.find_element_by_xpath(
            "/html/body/div[5]/header/nav/div/div[2]/ul/li[2]/ul/li[2]/ul/li/a")
        self.actions.move_to_element(customers).perform()  # Mause ile müşterilerin üzerine geliyor. (Mause hover)
        self.actions.move_to_element(customerAdd)  # Müşteri eklenin üzerine geliyor.
        customerAdd.click()  # Müşteri ekleye tıklıyor.

        account_type = self.driver.find_element_by_name("account_type")
        drp = Select(account_type)  # Dropdown. Aşağı açılan seçeneceklerden biri seçildi.
        drp.select_by_visible_text('Şirket')  # Şirket veya Şahıs

        # Text kutucukları gelen girdiler ile dolduruluyor.
        company_name_text = self.driver.find_element_by_name("company_name")
        company_name_text.send_keys(current_time)

        email_text = self.driver.find_element_by_name("email")
        email_text.send_keys(time.strftime("%H-%M-%S") + "@hotmail.com")

        phone_number_text = self.driver.find_element_by_name("phone_number")
        phone_number_text.send_keys("555" + time.strftime("%H%M%S") + "0")

        tax_id_text = self.driver.find_element_by_name("tax_id")
        tax_id_text.send_keys(time.strftime("%H%M%S%H%M"))  # Vergi numarası 10 haneli olmalı

        full_adress_text = self.driver.find_element_by_name("full_address")
        full_adress_text.send_keys(current_time)

        city_text = self.driver.find_element_by_name("city")
        city_text.send_keys(current_time)

        district_text = self.driver.find_element_by_name("district")
        district_text.send_keys(current_time)

        # Butona tıklıyoruz.
        add_customer_button = self.driver.find_element_by_xpath("//*[@id='add_customer_form']/div/div[3]/div/button")
        add_customer_button.click()

        self.click_orders()  # Siparişlere tıklıyoruz.
        self.click_customers()  # Müşteri eklendikten sonra yeniden müşteriler sayfasına gelip, burada isimle kontrol ediyoruz.
        # WARNİNG! Eğer aynı isme sahip kişiler varsa bu sorun yaratacaktır. Henüz dikkate alınmadı. ve düzeltilmeli.

        return self.check_on_page(current_time)  # current_time aslında şirket yada şahıs adı.

    # Tedarikçi
    def is_supplier_add(self):
        self.click_login()
        self.click_orders()

        current_time = time.strftime("%H:%M:%S")
        suppliers = self.driver.find_element_by_xpath("/html/body/div[5]/header/nav/div/div[2]/ul/li[2]/ul/li[4]/a")
        supplierAdd = self.driver.find_element_by_xpath("/html/body/div[5]/header/nav/div/div[2]/ul/li[2]/ul/li[4]/ul/li/a")
        self.actions.move_to_element(suppliers).perform()  # Mause ile müşterilerin üzerine geliyor. (Mause hover)
        self.actions.move_to_element(supplierAdd)  # Müşteri eklenin üzerine geliyor.
        supplierAdd.click()  # Müşteri ekleye tıklıyor.

        account_type = self.driver.find_element_by_name("account_type")
        drp = Select(account_type)  # Dropdown. Aşağı açılan seçeneceklerden biri seçildi.
        drp.select_by_visible_text('Şirket')  # Şirket veya Şahıs

        # Text kutucukları gelen girdiler ile dolduruluyor.
        company_name_text = self.driver.find_element_by_name("company_name")
        company_name_text.send_keys(current_time)

        email_text = self.driver.find_element_by_name("email")
        email_text.send_keys(time.strftime("%H-%M-%S") + "@hotmail.com")

        phone_number_text = self.driver.find_element_by_name("phone_number")
        phone_number_text.send_keys("555" + time.strftime("%H%M%S") + "0")

        tax_id_text = self.driver.find_element_by_name("tax_id")
        tax_id_text.send_keys(time.strftime("%H%M%S%H%M"))  # Vergi numarası 10 haneli olmalı

        full_adress_text = self.driver.find_element_by_name("full_address")
        full_adress_text.send_keys(current_time)

        city_text = self.driver.find_element_by_name("city")
        city_text.send_keys(current_time)

        district_text = self.driver.find_element_by_name("district")
        district_text.send_keys(current_time)

        id_tax_office_text = self.driver.find_element_by_id("id_tax_office")
        id_tax_office_text.send_keys("Ege Vergi Dairesi")

        # Butona tıklıyoruz.
        add_customer_button = self.driver.find_element_by_xpath("//*[@id='add_supplier_form']/div/div[3]/div/button")
        add_customer_button.click()
        time.sleep(1)

        # tedarikçi eklendikten sonra yeniden tedarikçiler sayfasına gelip, burada isimle kontrol ediyoruz.
        # WARNİNG! Eğer aynı isme sahip kişiler varsa bu sorun yaratacaktır. Henüz dikkate alınmadı. ve düzeltilmeli.

        try:  # Aynı sayfadaysa şirket ismini siliyoruz, isimle aratma başarısız olmasın
            company_name_text2 = self.driver.find_element_by_name("company_name")
            company_name_text2.clear()
        except:  # Hata fırlatmışsa tedarilkçi eklenmiş, tedarikçiler sayfasına gelmiş demektir. Burada isimle kontrol yapıyoruz.
            return self.check_on_page(current_time)  # current_time aslında şirket yada şahıs adı.
        else:
            return False  # Hala mevcut sayfadaysak tedarikçi eklenmemiş demektir.

    def is_log_out(self):
        self.click_login()
        self.click_welcome()

        # Çıkış butonuna tıklanıyor.
        log_out = self.driver.find_element_by_xpath("/html/body/div[3]/header/nav/div/div[1]/div[2]/div[3]/ul/li[2]/a")
        log_out.click()
        # Çıkış sayfasına gelindimi kontrol ediyor.
        return self.check_on_url(
            self.get_first_38_characters("http://staging.dopigo.com/accounts/login/?next=/users/dashboard/"))

    def is_setting_company(self):
        self.click_login()
        self.click_settings()

        # Şirket ayarlarına tıkladık.
        company_setting = self.driver.find_element_by_xpath(
            "/html/body/div[3]/header/nav/div/div[1]/div[2]/div[2]/ul/li[2]/a")
        company_setting.click()

        cargo = self.driver.find_element_by_xpath(
            "//*[@id='update-service-config']/div/div/div/div/div/div[1]/nav/ul/li[4]")
        cargo.click()

        cargo_company_dropdown = self.driver.find_element_by_xpath(
            "//*[@id='shipment']/div[2]/div[2]/div/div/div/button")
        cargo_company_dropdown.click()
        by_express = self.driver.find_element_by_xpath("//*[@id='shipment']/div[2]/div[2]/div/div/div/ul/li[1]/a/label")
        by_express.click()

        save_button = self.driver.find_element_by_xpath(
            "//*[@id='update-service-config']/div/div/div/div/div/div[2]/div/div/div/div[9]/div/button")
        save_button.click()  # Kayıt butonuna tıklandı ve aşağıda
        # Şirket ayarları kaydedildi yazısını kontrol ediyoruz.

        return self.check_has_xpath("//*[@id='top-message-container']/div")

    def is_change_password(self):
        self.click_login()
        self.click_settings()
        change_password = self.driver.find_element_by_xpath(
            "/html/body/div[3]/header/nav/div/div[1]/div[2]/div[2]/ul/li[1]/a")
        change_password.click()

        # Eski ve yeni parolalar girildi.
        old_password = self.driver.find_element_by_id("id_old_password")
        old_password.send_keys("123456qwe")
        new_password = self.driver.find_element_by_id("id_new_password1")
        new_password.send_keys("123456qwe")
        new_password_again = self.driver.find_element_by_id("id_new_password2")
        new_password_again.send_keys("123456qwe")

        change_password_button = self.driver.find_element_by_xpath(
            "/html/body/div[3]/div/div/div[3]/div[2]/div/form/div[4]/button")
        change_password_button.click()

        # Yazı ekranda çıktımı kontrol edip sonucu döndürüyor.
        return self.check_on_page("Parolanız değiştirildi.")

        # Bu fonksiyon çalışmıyor. Ürün seçme dropdown'unda Select komutu çalışmadı.
        # Select yerine farklı yöntemlerle ürün seçilemedi.

    def is_order_add(self):
        self.click_login()
        self.click_orders()

        orders = self.driver.find_element_by_xpath("/html/body/div[5]/header/nav/div/div[2]/ul/li[2]/ul/li[1]")
        orders_add = self.driver.find_element_by_xpath(
            "/html/body/div[5]/header/nav/div/div[2]/ul/li[2]/ul/li[1]/ul/li/a")
        self.actions.move_to_element(orders).perform()  # Siparişler'e mause ile üzerine geliyoruz.
        self.actions.move_to_element(orders_add)
        orders_add.click()  # Sipariş ekleye tıklıyoruz.

        self.select_product()  # Dropdown'dan bir kutucuğu seçtik.

        sales_channel = self.driver.find_element_by_id("select2-id_sales_channel-container")
        sales_channel.click()
        # Satış kanalı içerisinden n11 seçtik.
        n11_for_example = self.driver.find_element_by_xpath("/html/body/span/span/span[2]/ul/li[2]")
        n11_for_example.click()

        # 2. sıradaki müşteriyi seçtik
        customer = self.driver.find_element_by_id("select2-id_customer-container")
        customer.click()
        WebDriverWait(self.driver, 20).until(  # Henüz çalışmıyor.
            EC.element_to_be_clickable((By.XPATH, "/html/body/span/span/span[2]/ul/li[2]"))).click()
        time.sleep(2)

        save_button = self.driver.find_element_by_xpath(
            "/html/body/div[3]/div/div[1]/div[3]/div[2]/form/div[7]/div/button")
        save_button.click()
        # Kaydetme işleminden sonra Orders sayfasına atıyor. Bu sayfaya geldikmi kontrol ediyoruz.
        # Sipariş kodunu önceki sayfadan göremiyoruz. Yeni sayfada ürünün varlığı kontrol edilebilir.
        time.sleep(1)

        # ilk 38 karakteri gönderiyoruz. Fonksiyon o şekilde karşılaştırma yapıyor.
        ilk_38_karakter = self.get_first_38_characters(
            "http://staging.dopigo.com/orders/order/?service_created__gte=01%2F02%2F2021")
        return self.check_on_url(ilk_38_karakter)

    def is_delete_customer(self):
        self.click_login()
        self.click_orders()
        self.click_customers()

        # Müşterilerden birinin yanındaki silme butonuna tıklıyoruz.
        delete = self.driver.find_element_by_xpath('//*[@id="result_list"]/tbody/tr[2]/td[5]/a[2]/span')
        delete.click()

        # Bir alert geliyor. Eminmisiniz?, Normal alert bu şekilde çözülüyor fakat sitede çalışmadı.
        # time.sleep(4)
        # alert = self.driver.switch_to_alert      # alert.accept() alert sistemi burada çalışmıyor.
        # alert.accept()  # AttributeError: 'function' object has no attribute 'accept'   sitedeki alert accept kabul etmiyor.

        time.sleep(1)  # Alert ekranında bekleme olmazsa yanlış çalışıyor. Zaman beklemeli
        alert_are_you_sure = self.driver.find_element_by_xpath("/ html / body / div[13] / div[7] / div / button")
        alert_are_you_sure.click()
        time.sleep(1)  # Başarılı oldu yazısı hemen gelmiyor. Zaman beklemeli.
        return self.check_on_page("Müşteri silindi, ")

    def is_search_and_find_customer(self):
        self.click_login()
        self.click_orders()
        self.click_customers()

        searchbar_text = self.driver.find_element_by_id("searchbar")
        searchbar_text.send_keys("Melih Yılmaz")

        search_button = self.driver.find_element_by_xpath("//*[@id='sample_1_filter']/button")
        search_button.click()

        searchbar_text2 = self.driver.find_element_by_id(
            "searchbar")  # Arama yaptıktan sonra text bölgesinden girdiğimiz String'i siliyoruz.
        searchbar_text2.clear()  # Çünki, yeniden sayfada bu string'i aradığımızda burayı bulmayalım.

        time.sleep(1)
        return self.check_on_page("Melih Yılmaz")

    # Yeni gelir gider ekle
    # Burada kontrol olarak veri eklenmeden önceki eleman sayısı ile veri eklendikten sonraki eleman sayısını karşılaştırıyoruz.
    def is_income_and_expense_add(self):
        self.click_login()
        self.click_income_and_expense()

        self.click_last_page_in_element_list_control()
        number_of_previous_element = len(self.driver.find_elements_by_xpath("//*[@id='transactions_table']/tbody/tr"))

        new_transaction_button = self.driver.find_element_by_id("add-new-transaction-button")
        new_transaction_button.click()

        self.select_product()  # Ürün seçme dropdown'undan birini seçiyor.

        save_button = self.driver.find_element_by_xpath("//*[@id='add_form']/div/div[5]/div/button")
        save_button.click()

        self.click_last_page_in_element_list_control()
        number_of_next_element = len(self.driver.find_elements_by_xpath("//*[@id='transactions_table']/tbody/tr"))
        return self.check_element_add_count(number_of_previous_element, number_of_next_element)

        # Listenin başındaki tedarikçiyi silmeyi kontrol eder.

    def is_delete_supplier(self):
        self.click_login()
        self.click_orders()
        self.click_supplier()  # Tedarikçilere tıkladık.

        # mevcut tedarikçi sayısını not ettik.
        number_of_pre_element_lenght = len(self.driver.find_elements_by_xpath('//*[@id="result_list"]/tbody/tr'))

        # Birinciyi siliyoruz.
        first_supplier = self.driver.find_element_by_xpath('//*[@id="result_list"]/tbody/tr[1]/th/a')
        first_supplier.click()

        delete_supplier_button = self.driver.find_element_by_id("delete-button")
        delete_supplier_button.click()

        time.sleep(1)  # Alert çıktığı için bu satır durmalı
        alert_okey_button = self.driver.find_element_by_xpath('/html/body/div[12]/div[7]/div/button')
        alert_okey_button.click()

        time.sleep(1)  # Bu satır durmalı
        number_of_next_element_lenght = len(self.driver.find_elements_by_xpath('//*[@id="result_list"]/tbody/tr'))
        # Yukarıda son haldeki eleman sayısı aldık, aşağıda karşılaştırıyoruz.
        return self.check_element_sub_count(number_of_pre_element_lenght, number_of_next_element_lenght)

    def is_delete_order(self):
        self.click_login()
        self.click_orders()
        number_of_pre_element_lenght = len(self.driver.find_elements_by_xpath('//*[@id="result_list"]/tbody/tr'))

        first_order = self.driver.find_element_by_xpath('//*[@id="result_list"]/tbody/tr[1]/td[2]')
        first_order.click()

        delete_order_button = self.driver.find_element_by_id('delete-button')
        delete_order_button.click()

        time.sleep(1)  # Alert çıkıyorsa kullanılmalı.
        are_you_sure_alert_button = self.driver.find_element_by_xpath('/html/body/div[15]/div[7]/div')
        are_you_sure_alert_button.click()

        time.sleep(1)
        number_of_next_element_lenght = len(self.driver.find_elements_by_xpath('//*[@id="result_list"]/tbody/tr'))

        # Eleman silindikten sonra eleman eleman sayısına 1 eklerdiğimizde silinmeden önceki eleman
        # sayısını buluyorsak True döndürüyoruz.
        if (number_of_next_element_lenght + 1 == number_of_pre_element_lenght):
            return True
        else:
            return False

    # Buradaki elemanlar sayfalara ayrılmıyor. Dolayısıyla tek sayfadan eleman sayısı öğreniyoruz.
    # son sayfaya gelmeye gerek kalmıyor.
    def is_purchase_order_add(self):
        self.click_login()
        self.click_orders()

        purchases = self.driver.find_element_by_xpath("/html/body/div[5]/header/nav/div/div[2]/ul/li[2]/ul/li[3]/a")
        purchases.click()

        number_of_pre_elements = len(self.driver.find_elements_by_xpath('//*[@id="result_list"]/tbody/tr'))
        # önceki eleman sayısını aldık. sonrakiyle karşılaştırıp kontrol yapacağız.

        purchases = self.driver.find_element_by_xpath("/html/body/div[3]/header/nav/div/div[2]/ul/li[2]/ul/li[3]/a")
        purchasAdd = self.driver.find_element_by_xpath("/html/body/div[3]/header/nav/div/div[2]/ul/li[2]/ul/li[3]/ul/li/a")
        self.actions.move_to_element(
            purchases).perform()  # Mause ile satın alma siparişlerinin üzerine geliyor. (Mause hover)
        self.actions.move_to_element(purchasAdd)  # Satın alma siparişi eklenin üzerine geliyor.
        purchasAdd.click()  # Satın alma siparişi ekleye tıklıyor.

        self.select_supplier()
        self.select_product()

        save_button = self.driver.find_element_by_xpath('//*[@id="add_purchase_order_form"]/div/div[4]/div/button')
        save_button.click()

        number_of_next_elements = len(self.driver.find_elements_by_xpath('//*[@id="result_list"]/tbody/tr'))
        return self.check_element_add_count(number_of_pre_elements, number_of_next_elements)

    # Henüz çalışmıyor.
    # Siteye kullanıcı kayıt eder.
    # Fonksiyon kontrol yapmakla birlikte bir array döndürür.
    # Bu arrayin 1 ve 2. elemanı kullanıcı adi ve şifredir. 3. elemanı ise kontrol sonucudur.
    def is_register_dopigo(self):
        self.driver.get("http://staging.dopigo.com/")
        register_button = self.driver.find_element_by_xpath('//*[@id="register-btn"]')
        register_button.click()

        email = self.driver.find_element_by_name('email')
        username = time.strftime("%H-%M-%S") + '@hotmail.com'
        email.send_keys(username)

        password = '123456qwe'
        self.driver.find_element_by_name('password1').send_keys(password)
        self.driver.find_element_by_name('password2').send_keys(password)
        email_and_password = [username, password]


        self.driver.find_element_by_xpath('//*[@id="login-form"]/div[5]/button').click()  # kayıt olma butonu
        time.sleep(5)




        # Çalışmamakta recaptcha çıkartılmalı
        if self.check_has_xpath('//*[@id="recaptcha-anchor"]/div[1]'): # Recaptcha çıkmış ise:
            WebDriverWait(self.driver, 20).until(EC.frame_to_be_available_and_switch_to_it(
                (By.XPATH, '//*[@id="recaptcha-anchor"]')))
            WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH,  # Message: Select only works on <select> elements, not on <ul>
                                            '//*[@id="recaptcha-anchor"]'))).click()
            time.sleep(5) # recaptcha çıkma süresi için durmalı
        if self.check_has_xpath('//*[@id="login-form"]/div[6]/button'):
            self.driver.find_element_by_xpath('//*[@id="login-form"]/div[6]/button').click()
        time.sleep(100)

        self.driver.find_element_by_xpath('//*[@id="sq_100"]/div/label[2]').click() # Kısacık bir anketimiz var :) hayır.
        self.driver.find_element_by_xpath('//*[@id="survey"]/div/div[2]/input').click() #Devam tık
        self.driver.find_element_by_xpath('//*[@id="login-form"]/div[6]/span/a').click()
        result_company = self.is_setting_company() # giriş ekranından itibaren şirket ayarlarını yapıyoruz.

        time.sleep(100)
        return False


    def is_income_and_expense_delete(self):
        self.click_login()
        self.click_income_and_expense()

        number_of_previous_element = len(self.driver.find_elements_by_xpath("//*[@id='transactions_table']/tbody/tr"))

        self.driver.find_element_by_id('delete-button').click()
        time.sleep(1)  # Alert olunca olması zorunludur.
        self.driver.find_element_by_xpath('/html/body/div[18]/div[7]/div/button').click()  # Alert'e tamam diyoruz.
        time.sleep(1)
        number_of_next_element = len(self.driver.find_elements_by_xpath("//*[@id='transactions_table']/tbody/tr"))
        return self.check_element_sub_count(number_of_previous_element, number_of_next_element)

    def is_income_and_expense_repeat(self):
        self.click_login()
        self.click_income_and_expense()



        self.click_last_page_in_element_list_control()
        number_of_previous_element = len(self.driver.find_elements_by_xpath("//*[@id='transactions_table']/tbody/tr"))


        self.driver.find_element_by_id('duplicate-button').click() # tekrarlaya tık.
        time.sleep(1)  # Alert olunca olması zorunludur.
        self.driver.find_element_by_xpath('/html/body/div[19]/div[7]/div/button').click()  # Alert'e tamam diyoruz.
        time.sleep(1) # durmalı
        self.click_last_page_in_element_list_control() # ekleme yaptıktan sonra son sayfaya geliyoruz.
        number_of_next_element = len(self.driver.find_elements_by_xpath("//*[@id='transactions_table']/tbody/tr"))

        return self.check_element_add_count(number_of_previous_element, number_of_next_element)

    # Eleman sayısı artmışmı veya azalmışmı diye kontrol edeceğimiz noktalarda sayfa sayısı eğer varsa,
    # son sayfaya gelmemiz lazım. Eleman sayısı kontrolünde her daim bu fonksiyon çağırılmalı.
    # 6 ve 10. karakterler eşit mi ? ör:gelir/gider listesinde son sayfadamıyız bunu kontrol edeceğiz.
    # ürün sayısını sadece son sayfadan kontrol ediyoruz. ilk sayfalar sabit 15 elemanlı oluyor.
    # Ör 32 eleman varsa 15+15+2 = 3 sayfada oluyor. son sayfaya gelip kontrol yapıyoruz.
    # Son elemanın 15. veya 1. olma durumları kontrol ediliyor check_element_add_count()'de.
    def click_last_page_in_element_list_control(self):
        page_info = self.driver.find_element_by_xpath('//*[@id="actions-space"]/div/span/span').text
        # ör: page_info = Sayfa 1 / 2.
        # buradaki 1 ve 2 eşitmi bunu kontrol ediyoruz. eşitse son sayfadayız demektir.
        while (page_info[6] != page_info[10]):  # Sonraki var olduğu sürece ilerliyor. Son sayfaya geliyor.
            #print( page_info[6], page_info[10], page_info )
            if page_info[6]=='1': # Birinci sayfada önceki yok. sonrakine tık. direk
                self.driver.find_element_by_xpath('//*[@id="actions-space"]/div/span/a').click()  # sonraki sayfasına tık.
            else: # ara sayfalarda önceki ve sonraki var. sonraki sayfaya tıklıyoruz.
                self.driver.find_element_by_xpath('//*[@id="actions-space"]/div/span/a[2]').click()  # sonraki sayfasına tık.
            time.sleep(1)
            page_info = self.driver.find_element_by_xpath('//*[@id="actions-space"]/div/span/span').text
        return

    # isBatchProductDownloadAndUpdate fonksiyonu kullansın diye bu var.
    def batch_product_download(self):
        self.click_login()
        self.click_products()
        self.hover_batch_operations()  # Toplu işlemlerin mause ile üzerine geldik. Alt segmeyi açtık.

        batch_product_download_update = self.driver.find_element_by_xpath(
            '/html/body/div[3]/header/nav/div/div[2]/ul/li[3]/ul/li[3]/ul/li[1]/a')
        self.actions.move_to_element(batch_product_download_update)
        batch_product_download_update.click()

        self.driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/div[2]/form/div[1]/a').click()
        time.sleep(1)
        self.driver.find_element_by_xpath(
            '/html/body/div[3]/div/div/div[3]/div[2]/table/tbody/tr[1]/td[4]/a').click()  # Dosyayı indirdik.
        time.sleep(2)  # Dosya indirme işlemi için

        # İndirdiğimiz dosyanın adını değiştiriyoruz. Böylelikle ona heryerden kolay erişeceğiz.
        # Virgülden öncesi son indirilen dosyanın özel yolunu yolluyor, sonrası yeni dosya yolu ve ismi.
        os.rename(max(glob.glob("C:/Users/batma/Downloads/*.*"), key=os.path.getmtime),
                  'C:/Users/batma/Downloads/1.xlsx')
        return

    # isBatchProductDownloadAndUpdate fonksiyonu kullansın diye bu var.
    # Bu fonksiyon belirli bir excel dosyasının 1. elemanının stoğunu artırıp kaydediyor.
    # Dosya oluşturulan yerde 1 isimli başka dosya varsa hata verecektir. kontrol edilmeli.
    def batch_product_file_manipulation(self):
        #import openpyxl
        xfile = openpyxl.load_workbook("C:\\Users\\batma\\Downloads\\1.xlsx")
        sheet = xfile["Tablib Dataset"]
        if sheet['I2'].value == None:  # Birinci ürünün stoğu boş ise 1 yapıyoruz. Dolu ise 1 artıracağız.
            sheet['I2'] = 1
        else:
            sheet['I2'] = sheet['I2'].value + 1
        xfile.save(
            "C:\\Users\\batma\\Downloads\\1.xlsx")  # Aynı isimle kaydediyoruz. Farklı isimle kaydedince eskiyi silmiyor.
        return

    # WARNING fonksiyon bilgisayara özel path içermekte. Bu kısım pc değiştiğinde vs çalışmayacaktır.
    # Bu fonksiyon dosya indiren ve indirilen dosyayı update eden başka fonksiyonlar içeriyor.
    # Bu fonksiyon dosya yükleyerek toplu ürün indirme/güncelleme yapıyor.
    def is_batch_product_download_and_update(self):
        self.batch_product_download()  # Login vs burada yapılıyor. önce dosya indirilecek.
        self.batch_product_file_manipulation()  # Burada indirilen dosyaya müdahale edip değiştiriyoruz.
        # Dosyada yolundaki \ işaretini 2şer yapıyoruz.
        self.driver.find_element_by_name('imported_file').send_keys('C:\\Users\\batma\\Downloads\\1.xlsx')
        # Dosyayı yükledik.

        self.driver.find_element_by_xpath(
            '/html/body/div[3]/div/div/div[3]/div[2]/form/div[2]/div[2]/button').click()  # Excel yükle butonu.
        time.sleep(1)  # Burada kalmalı.

        check_successful_post = self.driver.find_element_by_xpath(
            '/html/body/div[3]/div/div/div[3]/div[2]/table/tbody/tr[1]/td[3]/h4/span').text
        # Tablodaki ilk sıradaki elemanın durumunu kontrol ediyoruz. Başarılı yazısı döndürüyorsa True.
        return 'tamamlandı' == check_successful_post

    def is_change_price_tracker_per_day(self):
        self.click_login()
        self.click_products()

        self.driver.find_element_by_xpath(
            '/html/body/div[3]/header/nav/div/div[2]/ul/li[3]/ul/li[4]/a').click()  # Otomatik fiyat
        self.driver.find_element_by_xpath(
            '/html/body/div[3]/div/div/div[3]/div/div[1]/div[1]/div[3]/div[1]/div[1]/a').click()  # Ayarlara tık.

        id_price_tracker_per_day_input_boxes = self.driver.find_element_by_id('id_price_tracker_per_day')
        id_price_tracker_per_day_input_boxes.clear()
        id_price_tracker_per_day_input_boxes.send_keys('3')
        self.driver.find_element_by_xpath(
            '//*[@id="pt-settings"]/div/div/div/div/div[2]/div[2]/button').click()  # kaydet tik.
        time.sleep(2)
        return self.check_has_xpath('//*[@id="top-message-container"]/div')

    def is_ware_hause_stock_list_change(self):
        self.click_login()
        self.click_products()
        self.click_warehause()

        self.driver.find_element_by_xpath(
            '/html/body/div[3]/header/nav/div/div[2]/ul/li[3]/ul/li[7]/ul/li[3]/a').click()  # Stok list tık.
        first_element = self.driver.find_element_by_id('id_form-0-warehouse_stock')
        first_element.clear()
        first_element.send_keys(10)  # 0 id'li 1. sıradaki elemanın kutusuna 10
        self.driver.find_element_by_name('_save').click()  # Kaydet butonu
        time.sleep(4)
        return self.check_on_page('başarılı olarak değiştirildi.')

    # Bu fonksiyon 2 aşağıdaki fonksiyon kullansın diye var.
    def order_downdload(self):
        self.click_login()
        self.click_orders()
        drp = Select(self.driver.find_element_by_id('id_file_format')) # Dropdown'da indirmek istediğimiz dosya şeklini seçiyoruz.
        drp.select_by_visible_text('Excel')
        time.sleep(1) # Burada kalması lazım dosya oluşturuluyor.
        # '/html/body/div[5]/div/div/div[3]/div/div[1]/div[3]/div/ul/li[1]/a'
        self.driver.find_element_by_xpath('/html/body/div[5]/div/div/div[3]/div/div[1]/div[3]/div/ul/li[1]/a').click()
        time.sleep(2)

        # İndirdiğimiz dosyanın adını değiştiriyoruz. Böylelikle ona heryerden kolay erişeceğiz.
        # Virgülden öncesi son indirilen dosyanın özel yolunu yolluyor, sonrası yeni dosya yolu ve ismi.
        os.rename(max(glob.glob("C:/Users/batma/Downloads/*.*"), key=os.path.getmtime),
                  'C:/Users/batma/Downloads/siparisler.xlsx')
        return False

    # Bu fonksiyon aşağıdaki fonksiyon kullansın diye var.
    def update_mass_order_cargo_information_file_manipulation(self):
        xfile = openpyxl.load_workbook("C:\\Users\\batma\\Downloads\\siparisler.xlsx")
        sheet = xfile["Tablib Dataset"]
        if sheet['AG2'].value == None:  # Birinci sipariş kargo takip no boş ise 1 yapıyoruz. Dolu ise 1 artıracağız.
            sheet['AG2'] = '11111111111'
        else:
            sheet['AG2'] = str(int(sheet['AG2'].value) + 1)
        if sheet['AH2'].value == None:  # Birinci sipariş kargo cari no boş ise 1 yapıyoruz. Dolu ise 1 artıracağız.
            sheet['AH2'] = '11111111111'
        else:
            sheet['AH2'] = str(int(sheet['AH2'].value) + 1)
        xfile.save(
            "C:\\Users\\batma\\Downloads\\siparisler.xlsx")  # Aynı isimle kaydediyoruz. Farklı isimle kaydedince eskiyi silmiyor.
        return

    # indirilen klasörde aynı dosya olmamasına özen gösterilmeli aksi takdirde: [WinError 183] Halen varolan bir dosya oluşturulamaz:
    # WARNING Siteden dosya excel olarak indiriliyor. Excel dosyayı açtığında sipariş kodunun başında eğer 0 varsa,
    # bunları siliyor. dosyayı bu haliyle yüklemeye çalıştığımızda sistem kabul etmiyor ve hata veriyor.
    # Bu durum dikkate alınmalı, excel dosyası düzeltilmeli.
    # Gerçek sitedede eğer başında 0 olan bir ürün olursa aynı sorun yaşanır. fakat bu durum gerçekleşmezmiş
    def is_update_mass_order_cargo_information(self):
        self.order_downdload() # Sipariş bilgilerin bilgisara indirdir.
        self.update_mass_order_cargo_information_file_manipulation() # Dosyayı değiştirdik.
         #Kargo takip kodu ve kargo cari kodunu değiştiriyoruz.

        # self.click_login()
        #self.click_orders()

        self.driver.find_element_by_xpath('/html/body/div[5]/header/nav/div/div[2]/ul/li[2]/ul/li[8]/a').click() #Toplu Sipariş Kargo Bilgisi Güncelleme tık
        # self.driver.find_element_by_name('imported_file').send_keys('')
        self.driver.find_element_by_name('imported_file').send_keys(
            'C:\\Users\\batma\\Downloads\\siparisler.xlsx')  # Dosyamızı yüklüyoruz.

        self.driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/div[2]/form/div[2]/div[2]/button').click() # Excel yükle butonu

        time.sleep(1)  # Burada kalmalı.

        check_successful_post = self.driver.find_element_by_xpath(
            '/html/body/div[3]/div/div/div[3]/div[2]/table/tbody/tr[1]/td[3]/h4/span').text
        # Tablodaki ilk sıradaki elemanın durumunu kontrol ediyoruz. Başarılı yazısı döndürüyorsa True.
        time.sleep(1)
        return 'tamamlandı' == check_successful_post

    # Dosya indirme ve manipule kısımları yok mevcut bir toplu_urun_gonderme.xlsx dosyasını yolluyor.
    # Gösterilen yolda bir toplu_urun_gonderme.xlsx isimli dosya olması lazım çalışabilmesi için.
    # Dosya indirme kısmında varolan dosyaları indirmediği için sadece bu kısım yapıldı.
    def is_batch_product_download_and_send(self):
        self.click_login()
        self.click_products()
        self.hover_batch_operations()

        self.driver.find_element_by_xpath('/html/body/div[3]/header/nav/div/div[2]/ul/li[3]/ul/li[3]/ul/li[2]/a').click() # Toplu ürün gönderme dropdown seçeneği tık
        self.driver.find_element_by_name('imported_file').send_keys('C:\\Users\\batma\\Downloads\\toplu_urun_gonderme.xlsx')
        self.driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/div[2]/form/div[2]/div[2]/button').click() # Excel yükle butonu

        check_successful_post = self.driver.find_element_by_xpath(
            '/html/body/div[3]/div/div/table/tbody/tr/td[3]').text
        # Tablodaki ilk sıradaki elemanın durumunu kontrol ediyoruz. Başarılı yazısı döndürüyorsa True.
        return 'ürün yaratma işlemi başlatıldı' == check_successful_post

