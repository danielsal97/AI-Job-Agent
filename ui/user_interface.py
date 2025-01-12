def display_options(options, title="Options", allow_back=False, allow_quit=False):
    """
    Display numbered options to the user, with an optional "Go Back" or "Quit" option.
    
    Parameters:
        options (list): List of options to display.
        title (str): Title of the options menu.
        allow_back (bool): If True, adds a "Go Back" option as the default (0).
        allow_quit (bool): If True, adds a "Quit" option as the default (0).
    """
    print(f"\n{title}:")
    if allow_back:
        print("0. Go Back")
    elif allow_quit:
        print("0. Quit")
    for idx, option in enumerate(options, start=1):
        print(f"{idx}. {option}")

def get_user_choices(options, item_name="item", multiple=False, allow_back=False, allow_quit=False):
    """
    Prompt the user to choose one or more options, with an optional "Go Back" or "Quit" default.
    
    Parameters:
        options (list): List of options to display.
        item_name (str): Name of the item(s) being chosen.
        multiple (bool): If True, allows selecting multiple options.
        allow_back (bool): If True, adds a "Go Back" option as the default (0).
        allow_quit (bool): If True, adds a "Quit" option as the default (0).
    
    Returns:
        list or str: Selected options, or "back"/"quit" for special cases.
    """
    try:
        user_input = input(
            f"Enter the number(s) corresponding to the {item_name}(s) you'd like to choose"
            f" ({'comma-separated for multiple' if multiple else 'a single number'}): "
        ).strip()

        if not user_input:
            print(f"No {item_name} selected.")
            return None

        selected_indices = [int(choice.strip()) for choice in user_input.split(',')]

        # Handle "Go Back" or "Quit" if enabled
        if allow_back and 0 in selected_indices:
            return "back"
        elif allow_quit and 0 in selected_indices:
            return "quit"

        if not multiple:
            selected_indices = selected_indices[:1]

        selected_options = [
            list(options)[idx - 1] for idx in selected_indices if 1 <= idx <= len(options)
        ]
        return selected_options

    except (ValueError, IndexError):
        print("Invalid input. Please enter valid numbers.")
        return None