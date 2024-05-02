# Porkbun Domains Data Extractor

The Porkbun Domains Data Extractor is a Python script that extracts domain information from the Porkbun website and generates a JSON file containing the domain data. The script uses Selenium WebDriver to automate the process of navigating through the website, extracting relevant domain information, and updating the JSON file.

## Features

- Automatically navigates to the Porkbun domains page (assumes you're logged in manually via Chrome in debug mode)
- Scrolls through the domain management page to load all available domains
- Extracts domain information such as domain name, price, sales blurb, and minimum offer (if available)
- Checks if a domain already exists in the JSON file before adding it to avoid duplicates
- Updates the JSON file with the extracted domain data, preserving existing data between runs
- Handles various exceptions and edge cases to ensure smooth execution
- Provides informative console output to track the progress and status of the extraction process

## Prerequisites

Before running the script, make sure you have the following prerequisites installed:

- Python (version 3.6 or above)
- Selenium WebDriver
- Chrome WebDriver (compatible with your Chrome browser version)

## Installation

1. Clone the repository or download the source code files.

2. Install the required dependencies by running the following command:
   Activate your virtual environment if desired
   ```
   pip install selenium
   ```

3. Download the appropriate version of the Chrome WebDriver from the official website: [Chrome WebDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads)

4. Place the downloaded Chrome WebDriver executable place it somewhere (e.g. `/usr/local/bin/chromedriver` on macOS)

## Configuration

1. Open the `config.py` file and provide the location used for your Chrome web driver.

## Usage

1. Open Chrome in debug mode with port 9222 listening. On macOS the command to run is

   ```bash
   /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
   ```

2. In Chrome that was just opened navigate to [porkbun.com](https://porkbun.com) and log in.
3. Run the script by executing the following command:

   ```bash
   python main.py
   ```

4. The script will navigate to or refresh your domain page and start extracting domain information.

5. The extracted domain data will be added to domains.json one at a time until the script completes. If a domain already exists in the file it will be skipped. To refresh all domains, delete the file.

6. The script will display progress and status updates in the console.

## Troubleshooting

- If the script encounters any issues during execution, it will display error messages in the console. Review the error messages and take appropriate action based on the specific issue.

- If the script fails to locate certain elements on the website, ensure that the HTML structure of the Porkbun website has not changed. You may need to update the CSS selectors or XPaths used in the script to match the current website structure.

- If the script times out at launch double-check that you have the correct version of the Chrome web driver for your Chrome version.

## License

This project is licensed under the [MIT License](LICENSE).

## Disclaimer

This script is provided as-is without any warranty. Use it at your own risk. The authors are not responsible for any consequences arising from the use of this script.

Please ensure that you comply with the terms of service and usage policies of the Porkbun website when using this script. Use it responsibly and respect the website's guidelines and restrictions.