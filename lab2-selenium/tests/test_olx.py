from pages.olx_page import OlxPage


def test_olx(driver):
    olx_page = OlxPage(driver)

    olx_page.open()
    assert "OLX.pl" in driver.title

    olx_page.search_item("iPhone 13")
    assert "iPhone-13" in driver.current_url
    assert "Wybrane dla Ciebie" in driver.page_source
    assert "do negocjacji" in driver.page_source

    olx_page.select_category()
    olx_page.select_fifth_element()

    assert "opis" in driver.page_source
    assert "oferta" in driver.current_url
    assert "Lokalizacja" in driver.page_source
    assert "reklama" in driver.page_source
