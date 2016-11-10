from selenium import webdriver


class RD2BrowserSession:
    def __init__(self, week, leagueUrl, credentials):
        driver = webdriver.Chrome()
        driver.get(leagueUrl)
        driver.find_element_by_css_selector("input[id=userId]").send_keys(credentials[0])
        driver.find_element_by_css_selector("input[type=password]").send_keys(credentials[1])
        driver.find_element_by_css_selector("input[type=submit]").click()
        self.__leagueUrl = leagueUrl
        self.__week = week
        self.__driver = driver

    def getScoreboardBase(self):
        scoreboardUrl = "{0}/scoring/completed/{1}".format(self.__leagueUrl, self.__week)
        return self.__driver.get(scoreboardUrl).page_source

    def getTopPerformersByPosition(self, position):
        topPerformerUrl = "{0}/stats/data-stats-report/all:{1}/period-{2}/scoring/stats?print_rows=9999".format(
            self.__leagueUrl,
            position,
            self.__week)
        return self.__driver.get(topPerformerUrl).page_source
