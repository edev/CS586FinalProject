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

    @classmethod
    def sqlInsertHeader(cls):
        """Returns the first line of an INSERT statement for Spaceship, i.e. INSERT ... VALUE\n"""

        return "INSERT INTO Spaceship(orgName, name, description, launchYear) VALUES\n"
