def flight_scrape_task(preferences, url):
    return f"""Follow these steps in order:
    Go to {url}

            }}
        }}

    5. Important:
        - Make sure to capture BOTH outbound and return flight details
        - Each flight should have its own complete set of details
        - Store the duration in the format "Xh Ym" (e.g., "2h 15m")
        - Return the total price of the flight, which is the maximum of the two prices listed
    """