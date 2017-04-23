from selenium import webdriver


class RD2BrowserSession:
    def __init__(self, week, leagueHomeUrl, credentials):
        driver = webdriver.Chrome()
        driver.get(leagueHomeUrl)
        driver.find_element_by_css_selector("input[id=userId]").send_keys(credentials[0])
        driver.find_element_by_css_selector("input[type=password]").send_keys(credentials[1])
        driver.find_element_by_css_selector("input[type=submit]").click()
        self.__leagueHomeUrl = leagueHomeUrl
        self.__week = week
        self.__driver = driver

    @property
    def leagueHomeUrl(self):
        return self.__leagueHomeUrl

    @property
    def week(self):
        return self.__week

    @property
    def driver(self):
        return self.__driver

    def getScoreboardBase(self):
        scoreboardUrl = "{0}/scoring/completed/{1}".format(self.leagueHomeUrl, self.week)
        return self.driver.get(scoreboardUrl).page_source

    def getSortedPerformancesByPosition(self, position):
        topPerformerUrl = "{0}/stats/data-stats-report/all:{1}/period-{2}/standard/stats?print_rows=9999".format(
            self.leagueHomeUrl,
            position,
            self.week)
        return self.driver.get(topPerformerUrl).page_source
