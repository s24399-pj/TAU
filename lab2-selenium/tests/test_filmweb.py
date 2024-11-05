from pages.filmweb_page import FilmwebPage


def test_filmweb(driver):
    filmweb_page = FilmwebPage(driver)

    filmweb_page.open()

    assert "Filmweb" in driver.title
    assert "filmy takie jak Ty" in driver.page_source

    filmweb_page.go_to_ranking()

    assert "film" in driver.current_url.lower(), "URL should contain 'ranking'"

    filmweb_page.open_first_movie()

    assert "Skazani na Shawshank" in driver.title
    assert "Zobacz pełną obsadę i twórców" in driver.page_source
    assert "Zobacz wszystkie zdjęcia" in driver.page_source
    assert "Ciekawostki" in driver.page_source

    filmweb_page.scroll_to_cast()
    filmweb_page.go_to_cast()

    assert "obsada" in driver.page_source
