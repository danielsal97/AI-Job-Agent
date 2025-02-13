import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ui.user_interface import display_options, get_user_choices


def extract_static_options(driver, container_selector):
    """
    Extract all options from a static dropdown that doesn't require scrolling.

    Args:
        driver (webdriver): Selenium WebDriver instance.
        container_selector (str): CSS selector for the dropdown container.

    Returns:
        dict: Extracted filter options with their IDs.
    """
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    container = soup.select_one(container_selector)

    if not container:
        print(f"Dropdown container not found for selector: {container_selector}.")
        return {}

    filter_mapping = {}
    labels = container.select("label")
    for label in labels:
        filter_id = label.get("for")
        filter_name = label.text.strip()
        filter_name = re.sub(r'\s*\(\d+\)$', '', filter_name)  # Remove counts (e.g., "(1493)")
        if filter_id and filter_name:
            filter_mapping[filter_name] = filter_id

    return filter_mapping


def extract_scrollable_options(driver, fieldset_selector):
    """
    Scroll through a ReactVirtualized grid and extract all options until no more scrolling is possible.

    Args:
        driver (webdriver): Selenium WebDriver instance.
        fieldset_selector (str): CSS selector for the fieldset containing the grid.

    Returns:
        dict: Extracted filter options with their IDs.
    """
    filter_mapping = {}
    try:
        scrollable_container_selector = f"{fieldset_selector} .ReactVirtualized__Grid"
        scrollable_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, scrollable_container_selector))
        )

        last_scroll_top = -1
        end_of_scroll = False

        while not end_of_scroll:
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            fieldset = soup.select_one(fieldset_selector)
            if not fieldset:
                print(f"Fieldset not found for selector: {fieldset_selector}. Skipping.")
                return {}

            labels = fieldset.select("label")
            for label in labels:
                filter_id = label.get("for")
                filter_name = label.text.strip()
                filter_name = re.sub(r'\s*\(\d+\)$', '', filter_name)
                if filter_id and filter_name and filter_name not in filter_mapping:
                    filter_mapping[filter_name] = filter_id

            driver.execute_script("arguments[0].scrollTop += 300;", scrollable_container)
            WebDriverWait(driver, 0.5)

            current_scroll_top = driver.execute_script("return arguments[0].scrollTop;", scrollable_container)
            if current_scroll_top == last_scroll_top:
                end_of_scroll = True
            else:
                last_scroll_top = current_scroll_top

        print(f"Extracted all options for fieldset: {len(filter_mapping)} options.")
    except Exception as e:
        print(f"Error while extracting scrollable options: {e}")

    return filter_mapping


def get_filter_mapping(driver, filter_button_selector, dropdown_selector, query_key=None, fieldset_query_keys=None):
    """
    Extract filter options dynamically for static and scrollable filters.

    Args:
        driver (webdriver): Selenium WebDriver instance.
        filter_button_selector (str): Selector for the filter button.
        dropdown_selector (str): Selector for the dropdown container.
        query_key (str, optional): Key for static dropdown filters.
        fieldset_query_keys (dict, optional): Fieldset query keys for scrollable filters.

    Returns:
        dict: Mapping of query keys to filter options.
    """
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, filter_button_selector))
    )
    button.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, dropdown_selector))
    )

    filter_mapping = {}

    if fieldset_query_keys:
        # Process scrollable filters
        for fieldset_selector, query_key in fieldset_query_keys.items():
            try:
                options = extract_scrollable_options(driver, fieldset_selector)
                filter_mapping[query_key] = options
            except Exception as e:
                print(f"Error processing fieldset for '{query_key}': {e}")
    elif query_key:
        # Process static filters
        try:
            options = extract_static_options(driver, dropdown_selector)
            filter_mapping[query_key] = options
        except Exception as e:
            print(f"Error processing dropdown for '{query_key}': {e}")

    return filter_mapping


def generate_query_string(selected_filters):
    """
    Generate a query string from selected filters.
    """
    query_parts = [
        f"{key}={value}" for key, values in selected_filters.items() for value in values
    ]
    return "&".join(query_parts)


def get_filter_url(base_url, filters):
    """
    Generates a new URL based on multiple selected filters and values.
    """
    driver = webdriver.Chrome()
    driver.get(base_url)

    selected_filters = {}

    while True:
        display_options(filters.keys(), "Available Filters", allow_back=True)
        selected_filter = get_user_choices(filters.keys(), "filter", multiple=False, allow_back=True)

        if selected_filter == "back":
            print("Returning to the previous menu.")
            break

        if not selected_filter:
            print("No valid filter selected. Please try again.")
            continue

        selected_filter = selected_filter[0]
        filter_config = filters[selected_filter]

        filter_mapping = get_filter_mapping(
            driver,
            filter_button_selector=filter_config["filter_button_selector"],
            dropdown_selector=filter_config["dropdown_selector"],
            query_key=filter_config.get("query_key"),
            fieldset_query_keys=filter_config.get("fieldset_query_keys"),
        )

        for query_key, options in filter_mapping.items():
            print(f"\nOptions for Query Key '{query_key}':")
            display_options(options.keys(), "Filter Options", allow_back=True)

            chosen_filters = get_user_choices(options.keys(), "option", multiple=True, allow_back=True)
            if chosen_filters == "back":
                print("Returning to filter selection.")
                continue

            selected_filters.setdefault(query_key, []).extend([options[choice] for choice in chosen_filters])

    query_string = generate_query_string(selected_filters)
    final_url = f"{base_url}?{query_string}"

    print(f"\nGenerated URL: {final_url}")
    driver.quit()
    return final_url