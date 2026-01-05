import pytest
from playwright.sync_api import Page, Browser, sync_playwright, TimeoutError
import random
import string
from playwright.sync_api import Page
from time import sleep

# =========================
# Fixtures
# =========================

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            slow_mo=150  # Zpomalení akcí o 150 ms pro lepší viditelnost testů (chtěla jsem si vyzkoušet)
        )
        yield browser
        browser.close()


@pytest.fixture
def page(browser: Browser):
    page = browser.new_page()
    yield page
    page.close()


# =========================
# Pomocné funkce
# =========================

def refuse_cookies(page: Page):
    """
    Odmítne cookies pomocí ID tlačítka.
    Pokud se banner nezobrazí, test pokračuje dál.
    """
    try:
        page.wait_for_selector("#cookiescript_reject", timeout=3000)
        btn_refuse = page.locator("#cookiescript_reject")

        if btn_refuse.is_visible():
            btn_refuse.click()
    except TimeoutError:
        pass


# =========================
# Testy
# =========================

# ===První test - Otevření Testing Akademie========================
def test_open_testing_academy_from_menu(page: Page):
    # Otevření stránky
    page.goto("https://engeto.cz")
    refuse_cookies(page)

    # Hover nad desktopovou položku Kurzy
    kurzy = page.locator("a[href='https://engeto.cz/prehled-kurzu/']:has-text('Kurzy')")
    kurzy.wait_for(state="visible")
    kurzy.hover()

    # Počkáme, až se zobrazí položka Testing Akademie v submenu
    testing_akademie = page.locator(
        "ul.sub-menu li.menu-item-type-custom a[href='https://engeto.cz/testovani-softwaru/'] span.menu-item-title"
    )
    testing_akademie.wait_for(state="visible")

    # Kliknutí na Testing Akademie
    testing_akademie.click()

    # Počkáme na načtení stránky
    page.wait_for_load_state("domcontentloaded")

    # Ověření, že nadpis H1 je správný
    heading = page.locator("h1:has-text('Testing Akademie')")
    assert heading.is_visible()

# ===Druhý test - Odebírání newsletteru========================

def generate_random_email():
    return "test_" + "".join(random.choices(string.ascii_lowercase + string.digits, k=6)) + "@example.com"

def test_newsletter_subscription(page: Page):
    # Otevření stránky
    page.goto("https://engeto.cz")
    refuse_cookies(page)

    # Vyplnění náhodného emailu
    random_email = generate_random_email()
    email_input = page.locator("input[name='newsletter-form-email']")
    email_input.wait_for(state="visible")
    email_input.fill(random_email)

    # Kliknutí na tlačítko Odebírat
    submit_btn = page.locator("a:has-text('Odebírat')")
    submit_btn.wait_for(state="visible")
    submit_btn.click()

    # Počkáme na potvrzení
    confirmation = page.locator("span.thank-you-message")
    confirmation.wait_for(state="visible")

    # Ověření, že potvrzení obsahuje správný text
    assert "Děkujeme, už se můžeš těšit na čerstvou dávku novinek!" in confirmation.inner_text()

# ===Třetí test - Zrušení filtru ========================

def test_filter_courses(page: Page):
    # Otevření stránky
    page.goto("https://engeto.cz", wait_until="load")
    refuse_cookies(page)

    #Hover nad Kurzy (dropdown)
    kurzy = page.locator("a[href='https://engeto.cz/prehled-kurzu/']:has-text('Kurzy')")
    kurzy.wait_for(state="visible")
    kurzy.hover()

    # Kliknutí na "Zobrazit termíny kurzů"
    menu_buttons = page.locator("li.menu-buttons")
    show_dates_btn = menu_buttons.locator("a:has-text('Zobrazit termíny kurzů')").first
    show_dates_btn.wait_for(state="visible")
    show_dates_btn.click()

    # Počkáme, až se zobrazí konkrétní sekce technologie
    tech_section = page.locator("div.dates-filter.dates-filter-technology-section")
    tech_section.wait_for(state="visible")

    # Checkboxy Python a Testování softwaru
    python_checkbox = tech_section.locator(
        "div.dates-filter-row:has(label[for='technology-python']) input"
    ).first
    testovani_checkbox = tech_section.locator(
        "div.dates-filter-row:has(label[for='technology-testovani-softwaru']) input"
    ).first

    python_checkbox.wait_for(state="visible")
    testovani_checkbox.wait_for(state="visible")

    # Kliknutí na filtry
    python_checkbox.check()
    testovani_checkbox.check()

    # Kliknutí na "Zrušit filtry"
    reset_btn = page.locator("a.dates-filter-reset-fields:has-text('Zrušit filtry')").first
    reset_btn.wait_for(state="visible")
    reset_btn.click()

    # Ověření, že filtry byly zrušeny
    assert not python_checkbox.is_checked()
    assert not testovani_checkbox.is_checked()
