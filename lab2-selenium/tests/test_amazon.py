from pages.amazon_page import AmazonPage


def test_amazon(driver):
    amazon_page = AmazonPage(driver)

    amazon_page.open()
    assert "amazon.pl" in driver.current_url
    assert "zakupy internetowe elektroniki" in driver.title

    amazon_page.search_item("Macbook Pro M4")
    amazon_page.click_first_result()

    assert "zł" in driver.page_source
    assert "Apple" in driver.page_source
    assert "MacBook Pro" in driver.page_source
    assert "Kup teraz" in driver.page_source

    amazon_page.add_to_cart()
    amazon_page.go_to_cart()

    assert "cart" in driver.current_url
    assert "Przejdź do finalizacji zakupu" in driver.page_source
    assert "Koszyk" in driver.page_source
