from typing import List

from selenium import webdriver


class RD2BrowserSession:
    def __init__(self, week: int, leagueHomeUrl: str, credentials: List[str]):
        self.__credentials = credentials
        self.__leagueHomeUrl = leagueHomeUrl
        self.__week = week
        self.__driver = None

    @property
    def credentials(self) -> List[str]:
        return self.__credentials

    @property
    def leagueHomeUrl(self) -> str:
        return self.__leagueHomeUrl

    @property
    def week(self) -> int:
        return self.__week

    @property
    def driver(self) -> webdriver:
        return self.__driver

    def getScoreboardBase(self) -> str:
        scoreboardUrl = "{0}/scoring/completed/{1}".format(self.leagueHomeUrl, self.week)
        if self.driver.current_url == scoreboardUrl:
            return self.getSource()
        else:
            self.driver.get(scoreboardUrl)
            return self.getSource()

    def clickOnCssElement(self, cssSelector: str) -> None:
        if self.driver:
            self.driver.find_element_by_css_selector(cssSelector).click()

    def getSource(self) -> str:
        if self.driver:
            return self.driver.page_source
        else:
            return ""

    def getSortedPerformancesByPosition(self, position: str) -> str:
        topPerformerUrl = "{0}/stats/data-stats-report/all:{1}/period-{2}/standard/stats?print_rows=9999".format(
            self.leagueHomeUrl,
            position,
            self.week)
        if self.driver.current_url == topPerformerUrl:
            return self.getSource()
        else:
            self.driver.get(topPerformerUrl)
            return self.getSource()

    def __enter__(self) -> "RD2BrowserSession":
        self.__driver = RD2BrowserSession.login(self.credentials, self.leagueHomeUrl)
        return self

    @staticmethod
    def login(credentials: List[str], leagueHomeUrl: str) -> webdriver:
        driver = webdriver.Chrome()
        driver.get(leagueHomeUrl)
        driver.find_element_by_css_selector("input[id=userid]").send_keys(credentials[0])
        driver.find_element_by_css_selector("input[type=password]").send_keys(credentials[1])
        driver.find_element_by_css_selector("input[type=submit]").click()
        return driver

    def __exit__(self, *args, **kwargs) -> None:
        self.driver.close()
