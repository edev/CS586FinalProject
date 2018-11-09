import re
from decimal import Decimal, getcontext
from reader.tsvreader import TsvReader
from dataclass.constellation import Constellation

# Initial setup.
getcontext().prec = 10 # we'll probably need no more than 2, but we DEFINITELY won't need more than 10.

# Data structures representing information to give to the DB
organizations = list()
formFactors = list()
fields = list()
constellations = list()

index = 1
with TsvReader('constellations.tsv') as reader:
    for line in reader:
        # Each line is a list of tokens to be processed.
        # In a Constellation, the tokens are:

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
            organizations.append(line[0]) # inefficient but we're only doing it 100 times.
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

        # print("{}\t\t{}\t\t{}".format(c, c.formFactorsSql(), c.fieldsSql()))
        constellations.append(c)

# Print our various lists.
print("Organizations:", organizations)
print("Form Factors:", formFactors)
print("Fields:", fields)
print("Constellations:", constellations)

