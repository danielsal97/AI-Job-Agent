from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Function to scrape filter mapping
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
        filter_id = label.get("for")  # The `for` attribute contains the unique filter ID
        
        if full_filter_name and filter_id:
            filter_mapping[full_filter_name] = filter_id

    return filter_mapping

# Function to get the filter URL with multiple filters
def get_filter_url(base_url, filters):
    """
    Generates a new URL based on multiple selected filters and values.
    """
    # Start Selenium WebDriver
    driver = webdriver.Chrome()
    driver.get(base_url)

    selected_filters = {}

    while True:
        # Display available filters to the user
        print("\nAvailable Filters:")
        for key in filters.keys():
            print(f"- {key}")

        # Ask user to select a filter key or type "done" to finish
        filter_key = input("Enter the filter key (or type 'done' to finish): ").strip()
        if filter_key.lower() == 'done':
            break

        if filter_key not in filters:
            print("Invalid filter key selected.")
            continue

        # Get the selected filter's configuration
        filter_config = filters[filter_key]

        # Scrape the filter options
        filter_mapping = get_filter_mapping(
            driver,
            filter_button_selector=filter_config["filter_button_selector"],
            dropdown_selector=filter_config["dropdown_selector"],
        )

        # Display the extracted options for the selected filter
        print(f"\nExtracted {filter_key} Options:")
        for name, filter_id in filter_mapping.items():
            print(f"{name}: {filter_id}")

        # Ask user to choose multiple options for the filter
        chosen_filters = input(f"Choose one or more {filter_key} options ('+'-separated): ").strip().split('+')

        for chosen_filter in chosen_filters:
            chosen_filter = chosen_filter.strip()
            if chosen_filter in filter_mapping:
                selected_filters.setdefault(filter_config["query_key"], []).append(filter_mapping[chosen_filter])
            else:
                print(f"Invalid {filter_key} option: {chosen_filter}")

    # Generate the final URL with all selected filters
    query_parts = []
    for key, values in selected_filters.items():
        query_parts.extend([f"{key}={value}" for value in values])
    query_string = "&".join(query_parts)
    new_url = f"{base_url}?{query_string}"

    print(f"\nGenerated URL: {new_url}")
    driver.quit()
    return new_url


# Example usage
filters = {
    "Job Type": {
        "filter_button_selector": "button[data-automation-id='JobTypeFilter']",
        "dropdown_selector": "fieldset[data-automation-id='JobType-checkboxgroup'] div.ReactVirtualized__Grid__innerScrollContainer",
        "query_key": "job_type"
    },
    "Job Family": {
        "filter_button_selector": "button[data-automation-id='JobFamilyFilter']",
        "dropdown_selector": "fieldset[data-automation-id='jobFamilyGroupCheckboxGroup'] div.ReactVirtualized__Grid__innerScrollContainer",
        "query_key": "job_family"
    }
}

# # Base URL for the job site
# base_url = "https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite"

# # Generate a URL for the selected filters
# new_url = get_filter_url(base_url, filters)

# if new_url:
#     print(f"\nFinal URL: {new_url}")