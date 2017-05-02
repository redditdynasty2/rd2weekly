from selenium import webdriver


class RD2BrowserSession:
    def __init__(self, week, leagueHomeUrl, credentials):
        self.__credentials = credentials
        self.__leagueHomeUrl = leagueHomeUrl
        self.__week = week
        self.__driver = None

    @property
    def credentials(self):
        return self.__credentials

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
        if self.driver.current_url == scoreboardUrl:
            return self.getSource()
        else:
            self.driver.get(scoreboardUrl)
            return self.getSource()

    def clickOnCssElement(self, cssSelector):
        self.driver.find_element_by_css_selector(cssSelector).click()

    def getSource(self):
        return self.driver.page_source

    def getSortedPerformancesByPosition(self, position):
        topPerformerUrl = "{0}/stats/data-stats-report/all:{1}/period-{2}/standard/stats?print_rows=9999".format(
            self.leagueHomeUrl,
            position,
            self.week)
        if self.driver.current_url == topPerformerUrl:
            return self.getSource()
        else:
            self.driver.get(topPerformerUrl)
            return self.getSource()

    def __enter__(self):
        self.__driver = RD2BrowserSession.login(self.credentials, self.leagueHomeUrl)
        return self

    @staticmethod
    def login(credentials, leagueHomeUrl):
        driver = webdriver.Chrome()
        driver.get(leagueHomeUrl)
        driver.find_element_by_css_selector("input[id=userid]").send_keys(credentials[0])
        driver.find_element_by_css_selector("input[type=password]").send_keys(credentials[1])
        driver.find_element_by_css_selector("input[type=submit]").click()
        return driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()
