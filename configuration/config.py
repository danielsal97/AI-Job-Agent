websites = {
  "nvidia": {
        "url": "https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite",
        "selectors": {
            "job_card": "li.css-1q2dra3",
            "job_title": "h3 a[data-automation-id='jobTitle']",
            "job_title_detail": "h2[data-automation-id='jobPostingHeader']",
            "job_location": "div[data-automation-id='locations']",
            "job_date": "div[data-automation-id='postedOn']",
            "job_description": "div[data-automation-id='jobPostingDescription']",
            "next_button": "//button[@aria-label='next']",
            "next_button_type": "button"
        },
        "filters": {
            "Location": {
                "filter_button_selector": "button[data-automation-id='distanceLocation']",
                "dropdown_selector": "div[aria-label='grid']", 
                "fieldset_query_keys": {
                    "fieldset[data-automation-id='Location Type-container']": "locationHierarchy2",
                    "fieldset[data-automation-id='Locations-container']": "locationHierarchy1",
                    "fieldset[data-automation-id='Sites-container']": "locations"
        },
            },
            "Time Type": {
                "filter_button_selector": "button[data-automation-id='employmentType']",
                "dropdown_selector": "fieldset[data-automation-id='employmentTypeCheckboxGroup'] div.ReactVirtualized__Grid__innerScrollContainer", 
                "query_key": "timeType"
            },
            "Job Category": {
                "filter_button_selector": "button[data-automation-id='jobFamilyGroup']",
                "dropdown_selector": "fieldset[data-automation-id='jobFamilyGroupCheckboxGroup'] div.ReactVirtualized__Grid__innerScrollContainer",  # Adjusted to match the provided HTML
                "query_key": "jobFamilyGroup"
            },
            "More": {
                "filter_button_selector": "button[data-automation-id='more']",
                "dropdown_selector": "fieldset[data-automation-id='Job Type-checkboxgroup'] div.ReactVirtualized__Grid__innerScrollContainer", 
                "query_key": "workerSubType" 
            }
        }
    },


        # "apple": {
        #     "url": "https://jobs.apple.com/en-il/search?location=israel-ISR",
        #     "job_card": "tbody[id^='accordion_PIPE']",
        #     "job_title": "a.table--advanced-search__title",
        #     "job_title_detail": "h1.jd__header--title",
        #     "job_location": "span[itemprop='addressRegion']",
        #     "job_date": "time#jobPostDate",
        #     "job_description": "div[itemprop='description']",
        #     "next_button": "li.pagination__next a"
        # },

    "apple": {
        "url": "https://jobs.apple.com/en-il/search?sort=relevance&key=graduate&location=israel-ISR",
        "selectors": {
        "job_card": "tbody[id^='accordion_PIPE']",
        "job_title": "tbody[id^='accordion_PIPE'] a.table--advanced-search__title",
        "job_title_detail": "h1.jd__header--title",
        "job_location": "span[itemprop='addressRegion']",
        "job_date": "time#jobPostDate",
        "job_description": "div[itemprop='description']",
        "next_button": "li.pagination__next a[aria-disabled='false']",
        "next_button_type": "link"
        },
        "filters": {
            "Location": {
                "filter_button_selector": "#locations-filter-acc",
                "dropdown_selector": "fieldset.selected-filters-section ul.auto-suggest-list",
                "query_key": ["location"]
            },
            # "Time Type": {
            #     "filter_button_selector": "button[data-automation-id='employmentType']",
            #     "dropdown_selector": "fieldset[data-automation-id='employmentTypeCheckboxGroup'] div.ReactVirtualized__Grid__innerScrollContainer", 
            #     "query_key": "timeType"
            # },
            # "Job Category": {
            #     "filter_button_selector": "button[data-automation-id='jobFamilyGroup']",
            #     "dropdown_selector": "fieldset[data-automation-id='jobFamilyGroupCheckboxGroup'] div.ReactVirtualized__Grid__innerScrollContainer",  # Adjusted to match the provided HTML
            #     "query_key": "jobFamilyGroup"
            # },
            # "More": {
            #     "filter_button_selector": "button[data-automation-id='more']",
            #     "dropdown_selector": "fieldset[data-automation-id='Job Type-checkboxgroup'] div.ReactVirtualized__Grid__innerScrollContainer", 
            #     "query_key": "workerSubType" 
            # }
        }
    },

    # "alljobs": {
    #     "url": "https://www.alljobs.co.il/SearchResultsGuest.aspx?page=1&position=&type=&city=&region=",
    #     "selectors": {
    #     "job_card": "div.open-board",
    #     "job_title": "a[title][href*='UploadSingle.aspx']",
    #     "job_title_detail": "a[title][href*='UploadSingle.aspx']",
    #     "job_location": "a[style*='text-decoration: none']",
    #     "job_date": "div.job-content-top-date",
    #     "job_description": "a[title][href*='UploadSingle.aspx'] h2",
    #     "next_button": "None",
    #     "next_button_type": "link"
    #     }
    # },
    #     "indeed": {
    #     "url": "https://il.indeed.com/jobs?q=&l=israel&from=searchOnHP&vjk=4ebb26071350a151&advn=452171920771710",
    #     "job_card": "li.css-1ac2h1w.eu4oa1w0",
    #     "job_title": "h2.jobTitle a.jcs-JobTitle",
    #     "job_title_detail": "h2[data-testid='simpler-jobTitle']",
    #     "job_location": "div[data-testid='jobsearch-JobInfoHeader-companyLocation'] span",
    #     "job_date": "span[data-testid='myJobsStateDate']",
    #     "job_description": "a[title][href*='UploadSingle.aspx'] h2",
    #     "next_button": "None"
    # },
    # "drushim": {
    #     "url": "https://www.drushim.co.il/jobs/cat5/",
    #     "selectors": {
    #     "job_card": "div.pt-0.mb-6.jobList_vacancy",  # Correctly identifies the container for job postings
    #     "job_title": "div.job-header a[target='_blank']",
    #      "job_title_detail": "div.job-header a[target='_blank']",  # Targets the job title and its associated link    "job_title_detail": "span.job-url.primary--text.font-weight-medium",  # For job detail view, if needed
    #     "job_location": "div.layout.job-details-sub span.display-18:not(.px-1)",  # Refined location selector
    #     "job_date": "span.display-18.inline-flex",  # Correctly targets the job posting date
    #     "job_description": "div.job-item-main",  # Targets the job description text
    #     "next_button": "None", # If there’s no pagination or next button
    #     "next_button_type": "link"  # Specify the type of next button (link or button)
    #     }
    # }
    

}