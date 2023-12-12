import time


from selenium.common import TimeoutException
from behave_basics.components.Base import *


class GiftPage(Base):

    def select_option(self, option, section):
        xpath = f"//span[contains(text(), '{section}')]//ancestor::div//span[contains(text(), '{option}')]//ancestor::a"
        locator = (By.XPATH, xpath)
        self.find_element(locator).location_once_scrolled_into_view
        self.click(locator)

    def get_item_name(self, parent):
        time.sleep(0.2)
        item_name_locator = (By.XPATH, f"//{parent}a[@data-test='product-title']")
        txt = self.get_text(item_name_locator)
        self.find_element(item_name_locator).location_once_scrolled_into_view
        return txt

    def get_item_price(self, parent):
        item_price_locator = (By.XPATH, f"//{parent}span[@data-test='current-price']/span[1]")
        txt = self.get_text(item_price_locator)
        return txt

    def get_item_shipping(self, parent):
        item_shipping_locator = (
            By.XPATH, f"//{parent}span[@data-test='LPFulfillmentSectionShippingFA_standardShippingMessage']/span")
        try:
            txt = self.get_text(item_shipping_locator)
        except TimeoutException:
            return None
        else:
            return txt

    def get_item(self):
        time.sleep(0.5)
        item_xpath = (By.XPATH, "//div[@class='styles__StyledCol-sc-fw90uk-0 dOpyUp']")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(item_xpath))
        element = self.driver.find_elements(*item_xpath)
        return element

    def collect_item_features(self):
        item_features = []
        items = self.get_item()
        item_list = []
        item_list.extend(i for i in items)
        for i in range(1, len(item_list)+1):
            xpath = f"div[@class='styles__StyledCol-sc-fw90uk-0 dOpyUp'][" + str(i) + "]//child::"
            item_name = self.get_item_name(xpath)
            item_price = self.get_item_price(xpath)
            item_shipping = self.get_item_shipping(xpath)
            item_features.append({"name": item_name, "price": item_price, "shipment": item_shipping})
        return item_features
    