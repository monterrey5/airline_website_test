from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# DEFINING INPUT VARIABLES / VALUES
DEPARTURE_FROM_COUNTRIES_LI = ["Alemania", "Croacia", "Dinamarca", "Italia", "Montenegro", "Polonia", "Suiza"]
DEPARTURE_CITY = "Madrid"
ARRIVAL_CITY = "Prague"
DEPARTURE_TABLE_HEADER = "País de origen"
ARRIVAL_TABLE_HEADER = "Elegir un país de destino"
SUBMIT_BTN = "Buscar"
line_phr = 20*"-"

# DRIVER AND WEBSITE SETUP
PATH = Service("C:\Program Files (x86)\chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(service=PATH, options=options)
driver.get("https://www.ryanair.com/es/es")

# ACCEPT_COOKIES
def accept_cookies():
    accept_cookies = driver.find_element(By.XPATH, '//*[@id="cookie-popup-with-overlay"]/div/div[3]/button[2]')
    accept_cookies.click()
    return


# ********************************************
# TEST CASES START
def test_departure_header_texts():
    departure_cell = driver.find_element(By.ID, "input-button__departure")
    departure_cell.click()
    try:
        departure_header = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="ry-tooltip-1"]/div[2]/hp-app-controls-tooltips/fsw-controls-tooltips-container/fsw-controls-tooltips/fsw-origin-container/fsw-airports/fsw-countries/div[1]'))).text
    except:
        print("DEPARTURE HEADER NOT FOUND")
        return "FAIL"

    if departure_header != DEPARTURE_TABLE_HEADER:
        print("INCORRECT DEPARTURE HEADER")
        return "FAIL"
    return "PASS"


def test_arrival_header_texts():
    arrival_cell = driver.find_element(By.ID, "input-button__destination")
    arrival_cell.click()
    try:
        arrival_header = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="ry-tooltip-3"]/div[2]/hp-app-controls-tooltips/fsw-controls-tooltips-container/fsw-controls-tooltips/fsw-destination-container/fsw-airports/fsw-countries/div[1]'))).text
    except:
        print("ARRIVAL HEADER NOT FOUND")
        return "FAIL"

    if arrival_header != ARRIVAL_TABLE_HEADER:
        print("INCORRECT ARRIVAL HEADER")
        return "FAIL"
    return "PASS"


def test_check_if_departure_arrival_cities_found():
    departure_cell = driver.find_element(By.ID, "input-button__departure")
    departure_cell.click()
    departure_cell.clear()
    departure_cell.send_keys(DEPARTURE_CITY)

    arrival_cell = driver.find_element(By.ID, "input-button__destination")
    arrival_cell.click()
    arrival_cell.clear()
    arrival_cell.send_keys(ARRIVAL_CITY)
    try:
        prg_dest = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="ry-tooltip-3"]/div[2]/hp-app-controls-tooltips/fsw-controls-tooltips-container/fsw-controls-tooltips/fsw-destination-container/fsw-airports/div/fsw-airports-list/div[2]/div[1]/fsw-airport-item[2]/span/span')))
        prg_dest.click()
    except:
        print("ARRIVAL CITY NOT FOUND")
        return "FAIL"
    return "PASS"


def test_check_if_ryanair_departs_from_given_countries():
    pf_result = "PASS"
    all_countries_to_departure_li = []
    to_departure_country = driver.find_elements(By.CLASS_NAME, "countries__country-inner")
    for item in to_departure_country:
        all_countries_to_departure_li.append(item.text.strip())

    missing_countries_li = []
    for country in DEPARTURE_FROM_COUNTRIES_LI:
        if country not in all_countries_to_departure_li:
            missing_countries_li.append(country)
            if pf_result == "PASS":
                pf_result = "FAIL"
    if pf_result == "FAIL":
        print("COUNTRIES MISSING IN LIST OF COUNTRIES RYANAIR DEPARTS FROM")
        print(missing_countries_li)
    return pf_result


def test_check_departure_return_dates_entry():
    try:
        departure_date = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="ry-tooltip-7"]/div[2]/hp-app-controls-tooltips/fsw-controls-tooltips-container/fsw-controls-tooltips/fsw-flexible-datepicker-container/fsw-datepicker/ry-datepicker-desktop/div[1]/calendar[2]/calendar-body/div[5]/div[1]/div')))
        departure_date.click()
    except:
        print("DEPARTURE DATE NOT FOUND")
        return "FAIL"
    try:
        return_date = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="ry-tooltip-8"]/div[2]/hp-app-controls-tooltips/fsw-controls-tooltips-container/fsw-controls-tooltips/fsw-flexible-datepicker-container/fsw-datepicker/ry-datepicker-desktop/div[1]/calendar[2]/calendar-body/div[6]/div[1]/div')))
        return_date.click()
    except:
        print("RETURN DATE NOT FOUND")
        return "FAIL"
    return "PASS"


def test_check_submit_flight_button_present_and_correct():
    try:
        submit_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/hp-app-root/hp-home-container/hp-home/hp-search-widget-container/hp-search-widget/div/hp-flight-search-widget-container/fsw-flight-search-widget-container/fsw-flight-search-widget/div/div/div/button')))
        submit_btn_text = driver.find_element(By.XPATH, '/html/body/hp-app-root/hp-home-container/hp-home/hp-search-widget-container/hp-search-widget/div/hp-flight-search-widget-container/fsw-flight-search-widget-container/fsw-flight-search-widget/div/div/div/button/span').text
        submit_btn.click()
    except:
        print("SUBMIT BUTTON NOT FOUND")
        return "FAIL"

    if submit_btn_text != SUBMIT_BTN:
        print("INCORRECT NAME OF SUBMIT BUTTON")
        return "FAIL"
    return "PASS"


def test_flight_route_info_headlines_correct():
    try:
        departure_header = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/app-root/flights-root/div/div/div/div/flights-lazy-content/flights-summary-container/flights-summary/div/div[1]/journey-container/journey/div/div[1]/h3'))).text
        return_header = driver.find_element(By.XPATH, '/html/body/app-root/flights-root/div/div/div/div/flights-lazy-content/flights-summary-container/flights-summary/div/div[2]/journey-container/journey/div/div[1]/h3').text
    except:
        print("DEPARTURE OR RETURN HEADLINES NOT FOUND")
        return "FAIL"

    departure_header_exp = "{} a {}".format(DEPARTURE_CITY, ARRIVAL_CITY)
    return_header_exp = "{} a {}".format(ARRIVAL_CITY, DEPARTURE_CITY)
    if departure_header != departure_header_exp or return_header != return_header_exp:
        print("INCORRECT DEPARTURE OR RETURN HEADLINES")
        return "FAIL"
    driver.back()
    return "PASS"


def test_recent_search_present_and_correct():
    try:
        recent_search = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/hp-app-root/hp-home-container/hp-home/hp-search-widget-container/hp-search-widget/div/hp-flight-search-widget-container/hp-recent-searches-container/hp-recent-search/div/div[1]'))).text
    except:
        print("RECENT SEARCH NOT FOUND")
        return "FAIL"
    if  recent_search != "{} - {}".format(DEPARTURE_CITY, ARRIVAL_CITY):
        print("INCORRECT RECENT SEARCH ROUTE INFO")
        return "FAIL"
    return "PASS"


# CALLING TEST CASES AND PRINTING DESCRIPTION AND RESULT OF EACH TEST CASE
def run_test_cases_count_results():

    pass_fail_dict = {"PASS": 0, "FAIL": 0}
    print("\n{}\n{}\n".format(line_phr, line_phr))


    print("\nTEST CASE 1: CHECK HEADER TEXTS ON DEPARTURE TABLE\n{}".format(line_phr))
    pf_phr = test_departure_header_texts()
    pass_fail_dict[pf_phr] += 1
    print("{}\n{}\n".format(pf_phr, line_phr))

    print("\nTEST CASE 2: CHECK IF RYANAIR DEPARTS FROM GIVEN COUNTRIES\n{}".format(line_phr))
    pf_phr = test_check_if_ryanair_departs_from_given_countries()
    pass_fail_dict[pf_phr] += 1
    print("{}\n{}\n".format(pf_phr, line_phr))

    print("\nTEST CASE 3: CHECK HEADER TEXTS ON ARRIVAL TABLE\n{}".format(line_phr))
    pf_phr = test_arrival_header_texts()
    pass_fail_dict[pf_phr] += 1
    print("{}\n{}\n".format(pf_phr, line_phr))

    print("\nTEST CASE 4: CHECK DEPARTURE AND ARRIVAL CITIES PRESENT\n{}".format(line_phr))
    pf_phr = test_check_if_departure_arrival_cities_found()
    pass_fail_dict[pf_phr] += 1
    print("{}\n{}\n".format(pf_phr, line_phr))

    print("\nTEST CASE 5: CHECK IF DEPARTURE / RETURN DATES ENTRY WORKS\n{}".format(line_phr))
    pf_phr = test_check_departure_return_dates_entry()
    pass_fail_dict[pf_phr] += 1
    print("{}\n{}\n".format(pf_phr, line_phr))

    print("\nTEST CASE 6: CHECK IF SUBMIT BUTTON PRESENT WITH CORRECT NAME\n{}".format(line_phr))
    pf_phr = test_check_submit_flight_button_present_and_correct()
    pass_fail_dict[pf_phr] += 1
    print("{}\n{}\n".format(pf_phr, line_phr))

    print("\nTEST CASE 7: CHECK IF FLIGHT FOUND AND ITS ROUTE INFO HEADLINES CORRECT\n{}".format(line_phr))
    pf_phr = test_flight_route_info_headlines_correct()
    pass_fail_dict[pf_phr] += 1
    print("{}\n{}\n".format(pf_phr, line_phr))

    print("\nTEST CASE 8: CHECK IF RECENT SEARCH PRESENT AND CORRECT\n{}".format(line_phr))
    pf_phr = test_recent_search_present_and_correct()
    pass_fail_dict[pf_phr] += 1
    print("{}\n{}\n".format(pf_phr, line_phr))

    return pass_fail_dict

# PRINT FINAL RESULTS
def show_results(pass_fail_dict):
    pass_count = pass_fail_dict["PASS"]
    fail_count = pass_fail_dict["FAIL"]
    print("\n\n{}\n{}\nTOTAL\n{}".format(line_phr, line_phr, line_phr))
    print("PASS: ", pass_count)
    print("FAIL: ", fail_count)
    print("PASSING %: ", (pass_count / (pass_count + fail_count))*100)
    return


if __name__ == "__main__":
    accept_cookies()
    results_dict = run_test_cases_count_results()
    driver.close()
    show_results(results_dict)
    print("\nTest Complete\n")
