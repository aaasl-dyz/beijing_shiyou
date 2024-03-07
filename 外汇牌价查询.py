import sys
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import os

import json
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException

currency_dict = {
    "GBP": "英镑",
    "HKD": "港币",
    "USD": "美元",
    "CHF": "瑞士法郎",
    "DEM": "德国马克",
    "FRF": "法国法郎",
    "SGD": "新加坡元",
    "SEK": "瑞典克朗",
    "DKK": "丹麦克朗",
    "NOK": "挪威克朗",
    "JPY": "日元",
    "CAD": "加拿大元",
    "AUD": "澳大利亚元",
    "EUR": "欧元",
    "MOP": "澳门元",
    "PHP": "菲律宾比索",
    "THB": "泰国铢",
    "NZD": "新西兰元",
    "KRW": "韩国元",
    "RUB": "卢布",
    "MYR": "林吉特",
    "TWD": "新台币",
    "ESP": "西班牙比塞塔",
    "ITL": "意大利里拉",
    "NLG": "荷兰盾",
    "BEF": "比利时法郎",
    "FIM": "芬兰马克",
    "INR": "印度卢比",
    "IDR": "印尼卢比",
    "BRL": "巴西里亚尔",
    "AED": "阿联酋迪拉姆",
    "ZAR": "南非兰特",
    "SAR": "沙特里亚尔",
    "TRY": "土耳其里拉"
}




def get_current_rate(date, currency_code):
    try:
        # 设置Chrome选项
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # 无头模式，不显示浏览器界面

        path = r'F:\迅雷下载\chromedriver_win32\chromedriver.exe'
        #driver = webdriver.Chrome()
        # 指定绝对路径的方式（可选）
        service = webdriver.ChromeService(executable_path=path)

        driver = webdriver.Chrome(service=service, options=options)

        driver.get("https://www.boc.cn/sourcedb/whpj/")
        # #打印界面内容
        date_input = driver.find_element("id", "erectDate")
        date_input.click()
        date_input.clear()
        date_input.send_keys(date)

        close_date_button = driver.find_element("id", "calendarClose")
        close_date_button.click()

        code_input = driver.find_element("id", "pjname")
        # 这里是一个选择框，需要先点击选择框，然后选择对应的货币名称
        select = Select(code_input)

        try:
            # 选择选项，根据value属性选择
            select.select_by_value(currency_dict[currency_code])
        except KeyError:
            print("货币代码错误：", currency_code)
            driver.quit()
            exit(1)

        query_button = driver.find_element('xpath', "//input[@onclick='executeSearch()']")
        query_button.click()

        time.sleep(2)

        try:
            element = driver.find_element('xpath', "//tr[@class='odd']/td[4]")
            content = element.text
            print( f"{date} {currency_dict[currency_code]}: {content}")
            with open("output.txt", "a") as file:
                output = f"{date} {currency_dict[currency_code]}: {content}"
                file.write(output + "\n")
        except NoSuchElementException:
            print("找不到查询结果")
        finally:
            time.sleep(3)
            driver.quit()
    except WebDriverException as e:
        if("Message: Cannot locate option" in str(e)):
            print(date,"无法查询到",currency_dict[currency_code],"的交易记录")
        else: print("浏览器操作异常:", str(e))

if __name__ == "__main__":
    date = 20240307
    currency_code = "USD"

    if len(sys.argv) != 3:
        print("Usage: python3 yourcode.py <date> <currency_code>")
        exit(1)

    date = int(sys.argv[1])
    currency_code = sys.argv[2]

    # 调用你的函数，并传递参数
    get_current_rate(date, currency_code)
