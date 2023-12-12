from behave import *
from selenium.webdriver import Keys

from behave_basics.components.Web_page import *
import time


@step('Print the current url')
def print_current_url(context):
    print(context.browser.current_url)


@step('Navigate to {url}')
def step_impl(context, url):
    context.browser.get(url)
    print_current_url(context)


@step("Search for {search_item}")
def step_impl(context, search_item):
    main_page = Base(context.browser)
    search_field_xpath = "//input[@name='searchTerm']"
    main_page.find_element((By.XPATH, search_field_xpath))
    main_page.input_text_into_field(search_item, (By.XPATH, search_field_xpath))
    main_page.input_text_into_field(Keys.RETURN, (By.XPATH, search_field_xpath))
    time.sleep(1)
    if search_item == 'iphone':
        link1 = "//p[contains(text(),'Explore all iPhone')]//ancestor::a"
        frame1 = "//div[@id='slpespot']//child::iframe[@title='3rd party ad content']"
        context.browser.switch_to.frame(main_page.find_element((By.XPATH, frame1)))
        element = main_page.find_element((By.XPATH, link1))
        element.click()
        context.browser.switch_to.default_content()
        time.sleep(1)


@step("Verify header of the page contains {search_item}")
def step_impl(context, search_item):
    main_page = Base(context.browser)
    header_xpath = "//h1"
    main_page.assert_text(search_item, header_xpath)


@step("Select {option} in {section} section")
def step_impl(context, option, section):
    context.gift_page = GiftPage(context.browser)
    context.gift_page.select_option(option, section)


@step("Collect all items on the first page into {var} on the {level} level")
def step_impl(context, var, level=None):
    items = context.gift_page.collect_item_features()
    if level is not None:
        setattr(context.feature, var, items)
    # assigns the result to the context variable
    else:
        setattr(context, var, items)


@then("Verify all collected results\' {parameter} is {condition}")
def step_impl(context, parameter, condition):
    if any(char in condition for char in {'<', '>', '='}):
        for i in context.feature.collected_items:
            if i[parameter].find('$') < 0:
                print(f"No price available for item {context.feature.collected_items.index(i) + 1}, {i['name']}")
                continue
            item_price = i[parameter].replace("$", "")
            item_price = item_price.split(" - ")
            if len(item_price) > 2:
                item_price.pop()
            try:
                assert eval(f'{item_price[0]} {condition}')
            except AssertionError:
                print(f"Price of item {context.feature.collected_items.index(i) + 1} (${item_price[0]}), {i['name']} doesn't meet condition: '{condition}'")
    else:
        for i in context.feature.collected_items:
            item_parameter = i[parameter]
            if i[parameter] is not None:
                try:
                    assert condition in item_parameter
                except AssertionError:
                    print(f"Parameter of item {context.feature.collected_items.index(i) + 1} {i['name']} doesn't meet condition: '{condition}'")
            else:
                print(f"Parameter of item {context.feature.collected_items.index(i) + 1} {i['name']} doesn't meet condition: '{condition}'")