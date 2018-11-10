from dataclass.sqltypes import sqlstr, sqlint, sqlbool


class Constellation:
    def __init__(self):
        self.index \
            = self.organization \
            = self.launched \
            = self.planned \
            = self.isFunded \
            = self.fundingAmt \
            = self.comment \
            = self.firstLaunch \
            = None
        self.fields = list()
        self.formFactors = list()

    def __str__(self):
        """Produces database-ready string output for the given Constellation object. Fields and FormFactors
        are not included; see fieldSql() and formFactorsSql()."""

        return "({}, {}, {}, {}, {}, {}, {}, {})".format(
            sqlint(self.index),
            sqlstr(self.organization),
            sqlstr(self.comment),
            sqlint(self.planned),
            sqlint(self.launched),
            sqlint(self.firstLaunch),
            sqlbool(self.isFunded),
            sqlint(self.fundingAmt)
        )

    def __repr__(self):
        return "{" + \
               ", ".join(
                   [
                    self.__str__(),
                    str(self.fields),
                    str(self.formFactors)
                   ]
                ) \
                + "}"

    def fieldsSql(self):
        """Produces database-ready output for the Constellation object's entries in the junction table joining
        Constellations and Fields. Output is a comma-separated list of parenthesized entries, i.e.

        (ConstellationIndex, Field1Name), (ConstellationIndex, Field2Name), ..., (ConstellationIndex, FieldNName)

        with no trailing comma. It's probably advisable to either insert these entries into the DB as-is or comma-join
        this and other fieldSql() strings from other Constellation objects."""

        if len(self.fields) == 0:
            return None # We might need to change this later.
        formatString = "({}, {})".format(str(sqlint(self.index)), "{}")
        return ", ".join([formatString.format(sqlstr(field)) for field in self.fields])

    def formFactorsSql(self):
        """Produces database-ready output for the Constellation object's entries in the junction table joining
        Constellations and FormFactors. Output is identical to fieldSql() except with FormFactor names rather than
        Field names."""
        if len(self.formFactors) == 0:
            return None # We might need to change this later.
        formatString = "({}, {})".format(str(sqlint(self.index)), "{}")
        return ", ".join([formatString.format(sqlstr(formFactor)) for formFactor in self.formFactors])

    @classmethod
    def sqlInsertHeader(cls):
        """Returns the first line of an INSERT statement for Constellation, i.e. INSERT ... VALUE\n"""

        return "INSERT INTO Constellation(index, orgName, comment, planned, launched, firstLaunch, isFunded, fundingAmt) VALUES\n"
