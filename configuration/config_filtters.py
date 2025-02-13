filters= {
    "nvidia":{
            "location": "#mainContent > div > div.css-1wnbqgd > fieldset > div:nth-child(2)",
            "time type" : "#mainContent > div > div.css-1wnbqgd > fieldset > div:nth-child(3)",
            "Job Catagory": "#mainContent > div > div.css-1wnbqgd > fieldset > div:nth-child(4)",
            "More": "#mainContent > div > div.css-1wnbqgd > fieldset > div:nth-child(5)",
            "url_rules": {
                "locationHierarchy1": {},
                "locationHierarchy2": {},
                 "locations": {},


            },
            # Example filters configuration

    "Location": {
        "filter_button_selector": "button[data-automation-id='distanceLocation']",
        "dropdown_selector": "body > div:nth-child(2) > div > div.css-15wisxj > div",  # Adjust if needed
        "query_key": "locationHierarchy1",
        "grid_selector" : "div.ReactVirtualized__Grid__innerScrollContainer"

    },
    
    "Time Type": {
        "filter_button_selector": "button[data-automation-id='employmentType']",
        "dropdown_selector": "fieldset[data-automation-id='employmentTypeCheckboxGroup'] div.ReactVirtualized__Grid__innerScrollContainer",  # Adjust if needed
        "query_key": "TimeType",
    },
    "Job Category": {
        "filter_button_selector": "button[data-automation-id='jobFamilyGroup']",
        "dropdown_selector": "body > div:nth-child(2) > div > div.css-15wisxj > div",  # Adjust if needed
        "query_key": "jobFamilyGroup",
    },
    "More": {
        "filter_button_selector": "button[data-automation-id='more']",
        "dropdown_selector": "body > div:nth-child(2) > div > div.css-15wisxj > div",  # Adjust if needed
        "query_key": "workerSubType",
    },


    }

}