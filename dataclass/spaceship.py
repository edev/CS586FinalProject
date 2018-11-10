from .sqltypes import *


class Spaceship:
    def __init__(self):
        self.organization \
            = self.name \
            = self.launchYear \
            = self.description \
            = None

    def __str__(self):
        """Produces database-ready string output for the given Spaceship object."""

        return "({}, {}, {}, {})".format(
            sqlstr(self.organization),
            sqlstr(self.name),
            sqlstr(self.description),
            sqlint(self.launchYear),
        )

    def __repr__(self):
        return self.__str__()
