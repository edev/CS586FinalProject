import re
from decimal import Decimal, getcontext
from reader.tsvreader import TsvReader
from dataclass.constellation import Constellation
from dataclass.launcher import Launcher
from dataclass.spaceship import Spaceship


# Initial setup.
getcontext().prec = 10 # we'll probably need no more than 2, but we DEFINITELY won't need more than 10.

# Data structures representing information to give to the DB
organizations = list()
formFactors = list()
fields = list()
constellations = list()
launchers = list()
spaceships = list()

# Process Constellations.
index = 1
with TsvReader('constellations.tsv') as reader:
    for line in reader:
        # Each line is a list of tokens to be processed.

        # Test code: prints everything with its column number.
        #for i in list(range(len(line))):
            # print("{}:  {}".format(i, line[i]))

        # Make sure we have the right number of tokens; otherwise, skip.
        if len(line) != 7:
            continue

        # Perform some initial clean-up.
        line = [e.strip() for e in line]
        line = [e.replace('"', '') for e in line]
        line = [e.replace('\t', ' ') for e in line]

        # The constellation we're setting up.
        c = Constellation()

        # 0: organization. See if it exists already. If not, add it to the list. Either way, set it.
        if line[0] not in organizations:
            organizations.append(line[0]) # inefficient but we're only doing it 200 times.
        c.organization = line[0]

        # 1. Launched / Planned. Either one might be '?'
        # Split on '/' and trim whitespace.
        tokens = [token.strip() for token in line[1].split('/')]
        if len(tokens) == 2:
            # Note: if we don't have 2 tokens, then we don't know what to do! Leave them at default.
            # But here we're able to parse 2 tokens. Either might be a number or '?' and WILL have spaces around it.
            if tokens[0] != '?':
                c.planned = tokens[0]
            if tokens[1] != '?':
                c.launched = tokens[1]

        # 2: first launch (year).
        # Now, this can be a numeric year, '?', or 'Cancelled'. The latter 2 translate to None.
        if line[2] == '?' or line[2] == 'Cancelled':
            c.firstLaunch = None
        else:
            c.firstLaunch = line[2]

        # 3: Form Factors.
        # This is a comma-separated list of form factors, so we'll split by commas and trim again,
        # and then we'll register any new ones in the overall list and save our list so that we can later
        # produce junction table entries.
        # For clarity in our DB, we will strip out any question marks as well.
        tokens = [token.replace('?', '').strip() for token in line[3].split(',')]
        for token in tokens:
            if token == '':
                continue
            if token not in formFactors:
                formFactors.append(token)
            c.formFactors.append(token)
        
        # 4: Fields.
        # This works just like Form Factor.
        tokens = [token.replace('?', '').strip() for token in line[4].split(',')]
        for token in tokens:
            if token == '':
                continue
            if token not in fields:
                fields.append(token)
            c.fields.append(token)

        # 5. Funding.
        # This field is one of a few types of values:
        #   1. "Yes" -> isFunded = True, fundingAmt = None
        #   2. "?" -> isFunded = None, fundingAmt = None
        #   3. "$### million" ->  isFunded = True, fundingAmt = ### * 1,000,000
        #   4. #3 but with "billion"
        #   5. "Seed" -> same as 1
        # We'll strip out "+" indicators that have no meaning in our DB. We'll also strip out "?" to clean up parsing,
        # which means when checking for #2, we'll actually look for "" rather than "?".
        line[5] = line[5].replace("?", "").replace("+", "")
        if line[5] == "Yes" or line[5] == "Seed":
            c.isFunded = True
            c.fundingAmt = None
        elif line[5] == "": # "?", but we stripped out question marks.
            c.isFunded = None
            c.fundingAmt = None
        elif "million" in line[5]:
            c.isFunded = True

            # 1. Find the number with a regular expression search. Might have a decimal point, even though it's a
            #    very large number.
            # 2. Convert to Decimal to preserve accuracy and allow us to do math.
            # 3. Multiply as needed.
            # 4. Convert to int to get rid of the decimal point.
            # 5. Convert to string for SQL.
            c.fundingAmt = \
                str(
                    int(
                        Decimal(
                            re.search(r'\d+(?:\.\d+)?', line[5]).group()
                        ) * 1000000))
        elif "billion" in line[5]:
            c.isFunded = True

            # 1. Find the number with a regular expression search. Might have a decimal point, even though it's a
            #    very large number.
            # 2. Convert to Decimal to preserve accuracy and allow us to do math.
            # 3. Multiply as needed.
            # 4. Convert to int to get rid of the decimal point.
            # 5. Convert to string for SQL.
            c.fundingAmt = \
                str(
                    int(
                        Decimal(
                            re.search(r'\d+(?:\.\d+)?', line[5]).group()
                        ) * 1000000000))

        # 6. Comment. Straight text copy, or None if empty.
        if line[6] is None:
            c.comment = None
        else:
            c.comment = line[6]

        # Finally, set the index.
        c.index = index
        index += 1

        # Print for testing, if desired.
        # print("{}\t\t{}\t\t{}".format(c, c.formFactorsSql(), c.fieldsSql()))

        constellations.append(c)

# For safety.
c = None

# Process Launchers.
with TsvReader('launchers.tsv') as reader:
    for line in reader:
        # Each line is a list of tokens to be processed.

        # Test code: prints everything with its column number.
        # for i in list(range(len(line))):
        #     print("{}:  {}".format(i, line[i]))

        # Make sure we have the right number of tokens; otherwise, skip.
        if len(line) != 11:
            continue

        # Perform some initial clean-up.
        line = [e.strip() for e in line]
        line = [e.replace('"', '') for e in line]
        line = [e.replace('\t', ' ') for e in line]

        # The constellation we're setting up.
        l = Launcher()

        # 0: organization. See if it exists already. If not, add it to the list. Either way, set it.
        if line[0] not in organizations:
            organizations.append(line[0]) # inefficient but we're only doing it 200 times.
        l.organization = line[0]

        # 1. name
        # Either "-" or a valid value. If "-" then set None.
        if line[1] == "-":
            l.name = None
        else:
            l.name = line[1]

        # 2: founded
        # The year the launcher was founded, i.e. the year work began.
        # Either a 4-digit integer (e.g. 2010) or "-".
        if line[2] == "-":
            l.founded = None
        else:
            l.founded = line[2]

        # 3: status
        # A text description of a status value. No missing values, so direct copy.
        l.status = line[3]

        # 4: first launch
        # One of three value types:
        #   1. A 4-digit year -> direct copy
        #   2. "-" -> None
        #   3. "Never?" -> None (but we'll match any occurrence of "Never" for safety)
        if line[4] == "-" or "Never" in line[4]:
            l.firstLaunch = None
        else:
            l.firstLaunch = line[4]

        # 5: launches
        # The number of launches that a launcher has had. An integer. Straight copy.
        l.launches = line[5]

        # 6: cost
        # We'll adapt code from Constellation's funding field, since it's similar.

        # This field is one of a few types of values:
        #   1. "-" -> None
        #   3. "$###M" where ### is a decimal number -> ### times 1,000,000
        # We'll strip out "?" to clean up parsing. It only occurs a couple of times, and we have no way of
        # intelligently interpreting this information anyway.

        line[6] = line[6].replace("?", "")
        if line[6] == "-":
            l.cost = None
        elif "M" in line[6]:

            # 1. Find the number with a regular expression search. Might have a decimal point, even though it's a
            #    very large number.
            # 2. Convert to Decimal to preserve accuracy and allow us to do math.
            # 3. Multiply as needed.
            # 4. Convert to int to get rid of the decimal point.
            # 5. Convert to string for SQL.
            l.cost = \
                str(
                    int(
                        Decimal(
                            re.search(r'\d+(?:\.\d+)?', line[6]).group()
                        ) * 1000000))

        # 7: maxLoad
        # All figures are in kg, if specified, so we have one of the following cases:
        #   1. "-" -> None
        #   2. "" -> None
        #   3. "### kg" (where ### is an integer)-> ###
        if "kg" in line[7]:
            l.maxLoad = re.search(r'\d+(?:\.\d+)?', line[7]).group()
        else:
            l.maxLoad = None

        # 8: launchType
        # A launchType is one of two types of values:
        #   1. "-" -> None
        #   2. A launchType we copy directly.
        if line[8] == "-":
            l.launchType = None
        else:
            l.launchType = line[8]

        # 9: funding
        # This field is nearly the same as Constellation funding, with a few, small differences:
        #   1. Instead of "million", this field uses "M".
        #   2. There are no billion-dollar launchers.
        #   3. We have no "?" but do have lots of "-".
        # So we'll simply adapt the Constellation funding code minimally to these changed conditions.

        # This field is one of a few types of values:
        #   1. "Yes" -> isFunded = True, fundingAmt = None
        #   2. "-" -> isFunded = None, fundingAmt = None
        #   3. "$###M" ->  isFunded = True, fundingAmt = ### * 1,000,000
        #   5. "Seed" -> same as 1
        # We'll strip out "+" indicators that have no meaning in our DB. We'll also strip out "?" to clean up parsing,
        # which means when checking for #2, we'll actually look for "" rather than "?".
        line[9] = line[9].replace("?", "").replace("+", "")
        if line[9] == "Yes" or line[9] == "Seed":
            l.isFunded = True
            l.fundingAmt = None
        elif line[9] == "-":
            l.isFunded = None
            l.fundingAmt = None
        elif "M" in line[9]:
            l.isFunded = True

            # 1. Find the number with a regular expression search. Might have a decimal point, even though it's a
            #    very large number.
            # 2. Convert to Decimal to preserve accuracy and allow us to do math.
            # 3. Multiply as needed.
            # 4. Convert to int to get rid of the decimal point.
            # 9. Convert to string for SQL.
            l.fundingAmt = \
                str(
                    int(
                        Decimal(
                            re.search(r'\d+(?:\.\d+)?', line[9]).group()
                        ) * 1000000))

        # 10: country
        # Direct copy.
        l.country = line[10]

        # Print for testing, if desired.
        # print(l)

        launchers.append(l)

# For safety.
l = None

# Process Spaceships.
with TsvReader('spaceships.tsv') as reader:
    for line in reader:
        # Each line is a list of tokens to be processed.

        # Test code: prints everything with its column number.
        # for i in list(range(len(line))):
        #     print("{}:  {}".format(i, line[i]))

        # Make sure we have the right number of tokens; otherwise, skip.
        if len(line) != 4:
            continue

        # Perform some initial clean-up.
        line = [e.strip() for e in line]
        line = [e.replace('"', '') for e in line]
        line = [e.replace('\t', ' ') for e in line]

        # The constellation we're setting up.
        s = Spaceship()

        # 0: organization. See if it exists already. If not, add it to the list. Either way, set it.
        if line[0] not in organizations:
            organizations.append(line[0]) # inefficient but we're only doing it 200 times.
        s.organization = line[0]

        # 1. name
        # Direct copy.
        s.name = line[1]

        # 2: launchYear
        # The year the ship first launched. Direct copy.
        s.launchYear = line[2]

        # 3: description
        # A text description of the spaceship. Direct copy.
        s.description = line[3]

        spaceships.append(s)

# Print our various lists, for testing purposes.
# print("Organizations:", organizations)
# print("Form Factors:", formFactors)
# print("Fields:", fields)
# print("Constellations:", constellations)
# print("Launchers:", launchers)
# print("Spaceships:", spaceships)

# And, finally, we'll output SQL files.
# Constellations
strings = [str(c) for c in constellations]
with open("insertConstellations.sql", "w") as f:
    f.write(Constellation.sqlInsertHeader())
    f.write("\t")
    f.write(",\n\t".join(strings))
    f.write(";")

# Launchers
strings = [str(l) for l in launchers]
with open("insertLaunchers.sql", "w") as f:
    f.write(Launcher.sqlInsertHeader())
    f.write("\t")
    f.write(",\n\t".join(strings))
    f.write(";")

# Spaceships
strings = [str(s) for s in spaceships]
with open("insertSpaceships.sql", "w") as f:
    f.write(Launcher.sqlInsertHeader())
    f.write("\t")
    f.write(",\n\t".join(strings))
    f.write(";")

# Now we're on to the simple tables for which we only have lists of strings.
# Organizations
strings = ["('{}')".format(o) for o in organizations]
with open("insertOrganizations.sql", "w") as f:
    f.write("INSERT INTO Organization(name) VALUES\n\t")
    f.write(",\n\t".join(strings))
    f.write(";")

# Fields
strings = ["('{}')".format(f) for f in fields]
with open("insertFields.sql", "w") as f:
    f.write("INSERT INTO Field(name) VALUES\n\t")
    f.write(",\n\t".join(strings))
    f.write(";")

# FormFactors
strings = ["('{}')".format(f) for f in formFactors]
with open("insertFormFactors.sql", "w") as f:
    f.write("INSERT INTO FormFactor(name) VALUES\n\t")
    f.write(",\n\t".join(strings))
    f.write(";")

# And finally, we have two junction tables to output from Constellations.
# TODO
