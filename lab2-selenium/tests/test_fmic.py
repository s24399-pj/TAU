from pages.fmic_page import FmicPage


def test_fmic(driver):
    fmic_page = FmicPage(driver)

    fmic_page.open()

    assert "fmic.pl" in driver.current_url

    fmic_page.go_to_category()

    assert "silnik-i-turbo" in driver.current_url

    fmic_page.go_to_turbo_category()

    assert "turbosprezarki" in driver.current_url

    fmic_page.select_maker("Garrett")

    assert "Garrett" in driver.current_url

    fmic_page.select_third()

    assert "garrett" in driver.current_url
    assert "garrett" in driver.page_source
    assert "Dodaj do koszyka" in driver.page_source
    assert "Producent" in driver.page_source
    assert "SKU" in driver.page_source

    print("elo")