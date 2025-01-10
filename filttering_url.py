import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from user_interface import display_options, get_user_choices

def get_filter_mapping(driver, filter_button_selector, dropdown_selector):
    """
    Extracts filter options and their IDs from the dropdown triggered by a filter button.
    """
    # Wait for the filter button to be clickable
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, filter_button_selector))
    )

    # Click the filter button to reveal the dropdown
    button.click()

    # Wait for the dropdown content to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, dropdown_selector))
    )

    # Parse the updated page content with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Extract filter labels from the dropdown
    filter_labels = soup.select(f"{dropdown_selector} label")

    # Create a dictionary to store filter mappings
    filter_mapping = {}
    for label in filter_labels:
        full_filter_name = label.text.strip()  # Full filter name
        full_filter_name = re.sub(r'\s*\(\d+\)$', '', full_filter_name)  # Remove count in parentheses
        filter_id = label.get("for")  # The `for` attribute contains the unique filter ID
        
        if full_filter_name and filter_id:
            filter_mapping[full_filter_name] = filter_id

    return filter_mapping

def get_filter_url(base_url, filters):
    """
    Generates a new URL based on multiple selected filters and values.
    """
    # Start Selenium WebDriver
    driver = webdriver.Chrome()
    driver.get(base_url)

    selected_filters = {}

    while True:
        # Display filter options
        display_options(filters.keys(), "Available Filters", allow_back=True)

        # Get user choice (single selection expected)
        selected_filter = get_user_choices(filters.keys(), "filter", multiple=False, allow_back=True)
        if selected_filter == "back":
            print("Returning to the previous menu.")
            break

        if not selected_filter:
            print("No valid filter selected. Please try again.")
            continue

        # `get_user_choices` returns a list, take the first element
        selected_filter = selected_filter[0]

        # Get the selected filter's configuration
        filter_config = filters[selected_filter]

        # Scrape the filter options
        filter_mapping = get_filter_mapping(
            driver,
            filter_button_selector=filter_config["filter_button_selector"],
            dropdown_selector=filter_config["dropdown_selector"],
        )

        # Display extracted filter options
        display_options(filter_mapping.keys(), f"Extracted {selected_filter} Options", allow_back=True)

        # Get user choices for the selected filter
        chosen_filters = get_user_choices(filter_mapping.keys(), "option", multiple=True, allow_back=True)
        if chosen_filters == "back":
            print("Returning to filter selection.")
            continue
        if not chosen_filters:
            print(f"No valid {selected_filter} options selected. Skipping.")
            continue

        for chosen_filter in chosen_filters:
            selected_filters.setdefault(filter_config["query_key"], []).append(filter_mapping[chosen_filter])

    # Generate the final URL with all selected filters
    query_parts = []
    for key, values in selected_filters.items():
        query_parts.extend([f"{key}={value}" for value in values])
    query_string = "&".join(query_parts)
    new_url = f"{base_url}?{query_string}"

    print(f"\nGenerated URL: {new_url}")
    driver.quit()
    return new_url