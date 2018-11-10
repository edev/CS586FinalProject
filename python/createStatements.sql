CREATE TABLE Field(
  name VARCHAR(64) PRIMARY KEY
);

CREATE TABLE Organization (
  name VARCHAR(64) PRIMARY KEY
);

CREATE TABLE Constellation (
  index INT PRIMARY KEY,
  orgName VARCHAR(64) REFERENCES Organization(name),
  comment VARCHAR(512),
  planned INT,
  launched INT,
  firstLaunch INT,
  isFunded VARCHAR(16),
  fundingAmt BIGINT
);

CREATE TABLE ConstField (
  constIndex INT REFERENCES Constellation(index),
  fieldName VARCHAR(64) REFERENCES Field(name),
  PRIMARY KEY(constIndex, fieldName)
);

CREATE TABLE FormFactor (
  name VARCHAR(64) PRIMARY KEY
);

CREATE TABLE ConstFF (
  constIndex INT REFERENCES Constellation(index),
  ffName VARCHAR(64) REFERENCES FormFactor(name),
  PRIMARY KEY (constIndex, ffName)
);

CREATE TABLE Launcher (
  orgName VARCHAR(64) REFERENCES Organization(name),
  name VARCHAR(64),
  isFunded VARCHAR(16),
  fundingAmt BIGINT,
  launchType VARCHAR(32),
  status VARCHAR(32),
  firstLaunch INT,
  country VARCHAR(64),
  founded INT,
  launches INT,
  cost BIGINT,
  maxLoad INT,
  UNIQUE (orgName, name)
);

CREATE TABLE Spaceship (
  orgName VARCHAR(64) REFERENCES Organization(name),
  name VARCHAR(64),
  description VARCHAR(512),
  launchYear INT,
  PRIMARY KEY (orgName, name)
);

