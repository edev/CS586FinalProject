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
            self._toint(self.index),
            self._tostr(self.organization),
            self._tostr(self.comment),
            self._toint(self.planned),
            self._toint(self.launched),
            self._toint(self.firstLaunch),
            self._tobool(self.isFunded),
            self._toint(self.fundingAmt)
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

    def _tostr(self, string):
        """Return a string representation of the given string that can be used in a SQL query. string can be None."""
        if string is None:
            return 'NULL'
        else:
            return "'{}'".format(string)

    def _toint(self, integer):
        """Return an integer (or bigint) representation of the given integer that can be used in a SQL query.
        integer can be None."""
        if integer is None:
            return 'NULL'
        else:
            return integer

    def _tobool(self, boolean):
        """Return a boolean representation of the given boolean that can be used in a SQL query. boolean can be None."""
        if boolean is None:
            return "NULL"
        elif boolean is True or boolean is False:
            return str(boolean)
        else:
            # What IS it? Don't know.
            raise TypeError

    def fieldsSql(self):
        """Produces database-ready output for the Constellation object's entries in the junction table joining
        Constellations and Fields. Output is a comma-separated list of parenthesized entries, i.e.

        (ConstellationIndex, Field1Name), (ConstellationIndex, Field2Name), ..., (ConstellationIndex, FieldNName)

        with no trailing comma. It's probably advisable to either insert these entries into the DB as-is or comma-join
        this and other fieldSql() strings from other Constellation objects."""

        if len(self.fields) == 0:
            return None # We might need to change this later.
        formatString = "({}, {})".format(str(self._toint(self.index)), "{}")
        return ", ".join([formatString.format(self._tostr(field)) for field in self.fields])

    def formFactorsSql(self):
        """Produces database-ready output for the Constellation object's entries in the junction table joining
        Constellations and FormFactors. Output is identical to fieldSql() except with FormFactor names rather than
        Field names."""
        if len(self.formFactors) == 0:
            return None # We might need to change this later.
        formatString = "({}, {})".format(str(self._toint(self.index)), "{}")
        return ", ".join([formatString.format(self._tostr(formFactor)) for formFactor in self.formFactors])
