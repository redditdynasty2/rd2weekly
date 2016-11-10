from src.scoring.trio import Trio


class BestTrio(Trio):
    def __init__(self, reverse=False):
        super(BestTrio, self).__init__(first=[], second=[], third=[])
        self.__reverse = reverse

    @property
    def first(self):
        return self.__first

    @property
    def second(self):
        return self.__second

    @property
    def third(self):
        return self.__third

    def addIfTopThree(self, newPoints):
        spot = 1
        while spot <= 3:
            if self.__jumpSpotIfAllowed(spot, newPoints):
                self.__pruneToTopThree()
                break

    def __jumpSpotIfAllowed(self, spot, newPoints):
        comparison = self.__pointComparison(spot, newPoints)
        if comparison > 0:
            self.__jumpSpot(spot, newPoints)
        elif comparison == 0:
            self.__addToSpot(spot, newPoints)
        return comparison >= 0


    def __pointComparison(self, spot, newPoints):
        existingPoints = self.first if spot == 1 \
            else self.second if spot == 2 \
            else self.third
        if not existingPoints:
            return 1
        else:
            ourPoints = existingPoints[0]
            multiplier = -1 if self.__reverse else 1
            return multiplier * ((newPoints > ourPoints) - (newPoints < ourPoints))

    def __jumpSpot(self, spot, newPoints):
        i = 3
        while i >= spot:
            if i == 3:
                self.__third = [newPoints]
            elif i == 2:
                self.__third = self.second
                self.__second = [newPoints]
            else:
                self.__second = self.first
                self.__first = [newPoints]
            i-=1


    def __addToSpot(self, spot, newPoints):
        self.__first.append(newPoints) if spot == 1 \
            else self.__second.append(newPoints) if spot == 2 \
            else self.__third.append(newPoints)

    def __pruneToTopThree(self):
        if len(self.first) > 3:
            self.__second = []
        if len(self.first) + len(self.second) > 3:
            self.__third = []
