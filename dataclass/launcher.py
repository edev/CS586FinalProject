from .sqltypes import *


class Launcher:
    def __init__(self):
        self.organization \
            = self.name \
            = self.founded \
            = self.status \
            = self.firstLaunch \
            = self.launches \
            = self.cost \
            = self.maxLoad \
            = self.launchType \
            = self.isFunded \
            = self.fundingAmt \
            = self.country \
            = None

    def __str__(self):
        """Produces database-ready string output for the given Launcher object."""

        return "({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})".format(
            sqlstr(self.organization),
            sqlstr(self.name),
            sqlbool(self.isFunded),
            sqlint(self.fundingAmt),
            sqlstr(self.launchType),
            sqlstr(self.status),
            sqlint(self.firstLaunch),
            sqlstr(self.country),
            sqlint(self.founded),
            sqlint(self.launches),
            sqlint(self.cost),
            sqlint(self.maxLoad)
        )

    def __repr__(self):
        return self.__str__()
