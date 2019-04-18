import github_wrapper, webdriver_wrapper, mysql_db_wrapper

BROWSER = "firefox"
URL_TO_SCRAPE = "https://github.com/"
SEARCH_FOR = "selenium"
PAGES_TO_SCRAPE = 5

def scrape_results():
    scraped_results = []
    result_page = 0
    should_stop = False
    while result_page < PAGES_TO_SCRAPE and not should_stop:
        results_list = web_driver_obj.find_element_by("//ul[@class='repo-list']", "xpath")
        results_list = results_list.find_elements_by_tag_name("li")
        for result in results_list:
            obj = webdriver_wrapper.extract_data(result)
            scraped_results.append(obj)
        try:
            web_driver_obj.click_on("//a[@class='next_page']", "xpath")
            web_driver_obj.wait_for_page_load()
        except Exception as e:
            should_stop = True
        result_page += 1

    return scraped_results


if __name__ == "__main__":
    web_driver_obj = webdriver_wrapper.WebDriverObject(BROWSER)
    web_driver_obj.navigate_to_url(URL_TO_SCRAPE)
    web_driver_obj.wait_for("//form[@class='js-site-search-form']//input[@type='text']")

    web_driver_obj.type("//form[@class='js-site-search-form']//input[@type='text']", "xpath", SEARCH_FOR)
    web_driver_obj.press_key("enter")
    web_driver_obj.wait_for("//ul[@class='repo-list']")

    results_objects = scrape_results()

    mysql_db_obj = mysql_db_wrapper.MysqlObject(user="root", password="gitscrape", db_name="results")
    for result_obj in results_objects:
        query = "INSERT INTO github_search_results (title, link, description, tags, datetime, language, stars) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (result_obj.title, result_obj.link, result_obj.description, ", ".join(result_obj.tags), result_obj.datetime, result_obj.language, result_obj.stars)
        insert_id = mysql_db_obj.insert_row(query, val)
        print("insert 1 row to db with ID: {}".format(insert_id))
        web_driver_obj.navigate_to_url(result_obj.link)

    web_driver_obj.close_browser()

    query = 'SELECT * FROM github_search_results'
    db_data = mysql_db_obj.query_db(query)
    for row in db_data:
        result_obj = github_wrapper.ResultObject(row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        result_obj.print()

    mysql_db_obj.close_connection()