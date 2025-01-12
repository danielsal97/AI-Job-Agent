import os
import sys
from ui.user_interface import display_options, get_user_choices
from core.process import show_data, run_scraping
from configuration.config import websites
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))
# Suppress tokenizers parallelism warning
os.environ["TOKENIZERS_PARALLELISM"] = "false"

def main():
    """TODO: Implement the main function
        1. fix bugs with go back -> when im scarping can make an errors with sellenium -> going to differnet page 
        2. scrping dyinmacly with scrolling down
        3. add more websites
        4. use asincio for scrapping ( websites and jobs)
        5. improve runtime
    """
    while True:
        # Top-Level Options
        main_menu_options = ["Show jobs in database", "Run job scraping"]
        display_options(main_menu_options, title="Main Menu", allow_quit=True)

        main_choice = get_user_choices(main_menu_options, "option", multiple=False, allow_quit=True)
        if main_choice == "quit":
            print("Exiting the application. Goodbye!")
            break

        if main_choice[0] == "Show jobs in database":
            print("\nDisplaying jobs in the database...")
            show_data()  # Calls the function to display database content
        elif main_choice[0] == "Run job scraping":
            while True:
                print("\nRunning job scraping...")
                display_options(websites, title="Available Websites", allow_back=True)
                selected_websites = get_user_choices(websites, "website", multiple=True, allow_back=True)

                if selected_websites == "back":
                    print("Returning to Main Menu.")
                    break
                if not selected_websites:
                    print("No valid websites selected. Please try again.")
                    continue

                run_scraping(selected_websites)
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()