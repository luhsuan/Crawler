# Cosmetics Forum Crawler
This Python script is a web crawler designed to collect data from a beauty forum's user blog https://fgblog.fashionguide.com.tw/category/4/last_posts. Collecting data is the aim of training the matching learning model to recommend products. The script uses libraries such as Requests, BeautifulSoup, Selenium, and more to scrape articles and comments from the forum.
Below is a breakdown of the script's main functions and how to use it:

## Prerequisites
* Python 3.x
* Required Python libraries (Requests, BeautifulSoup, Selenium, etc.)
* Web driver (Chrome or PhantomJS)
* Set the web driver executable path in the script (chrome_path or p_path variable)

## How to Use
1. Start by configuring the web driver:
 Modify the chrome_path or p_path variable to point to your Chrome or PhantomJS web driver executable.
2. Run the script:
Run the main() function to initiate the data collection process.
3. Specify the forum pages:
   You can specify the forum pages you want to scrape by changing the url variable in the main() function.

## Functionality
The script's functions are as follows:

* getHtml(url, retry): Fetches the HTML content of a given URL. It uses random user agents for requests and handles errors gracefully.
* singlePage(url): Extracts information from a single blog post page, including board name, date range, article type, article title, author, content, and comments (if needed).
* getIndex(index_url): Collects and organizes data from a forum index page. It retrieves information about articles such as title, date, author, and links to individual posts.
* main(): The main function that initiates the data collection process. You can specify the forum pages you want to scrape here.

## Data Storage
The script creates JSON files to store the scraped data. The data is organized by category and date range, and an "error.json" file keeps track of any problematic URLs.

Note
* You need to have the necessary web drivers (e.g., ChromeDriver) installed and configured for the script to run successfully.
The script may need adjustments or additional error handling depending on the specific website structure.
* Please ensure that you have the required libraries installed and the web driver configured before using this script. Also, be aware of website policies and web scraping laws when using this crawler on any specific website.
