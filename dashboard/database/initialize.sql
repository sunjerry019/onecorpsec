CREATE TABLE `users` (
    sn SERIAL,
    user VARCHAR(50) CHARACTER SET utf8,
    pass VARCHAR(128) CHARACTER SET utf8,
    salt VARCHAR(64) CHARACTER SET utf8,
    tableName VARCHAR(64) CHARACTER SET utf8,
    PRIMARY KEY (sn)
);

CREATE TABLE `main` (
    sn SERIAL,
    coyName VARCHAR(250) CHARACTER SET utf8,        -- Company Name
    coyRegNo VARCHAR(10) UNIQUE CHARACTER SET utf8,        -- Register No = Unique Identifier
    toEmail VARCHAR(250) CHARACTER SET utf8,        -- To Emails (can have multiple, comma separated)
    ccEmail VARCHAR(250) CHARACTER SET utf8,        -- CC Emails (can have multiple, comma separated)
    bccEmail VARCHAR(250) CHARACTER SET utf8,       -- BCC Emails (can have multiple, comma separated)
    addresseeName VARCHAR(250) CHARACTER SET utf8,  -- who the emails should be addressed to
    yearEndMonth TINYINT(2) UNSIGNED,               -- The month in an tiny int format
    yearEndYear YEAR(4) UNSIGNED,               -- The year in which the next ACRA is due
    agmDone BOOLEAN,        -- Flag for whether need to continue sending AGM email
    GSTReq BOOLEAN,         -- Flag for whether company needs to submit GST
    GSTDone BOOLEAN,        -- Flag for whether need to continue sending GST Reminder Email
    auditReq BOOLEAN,       -- Flag for whether company needs to submit GST
    auditDone BOOLEAN,      -- Flag for whether need to continue sending Audit Email
    incomeTaxDone BOOLEAN,  -- Flag for whether need to continue sending Income Tax Email
    PRIMARY KEY (sn)
);


CREATE TABLE `csv_mapping` (
    sn SERIAL,
    tabletext VARCHAR (250) UNIQUE,
    plaintext VARCHAR (250),
    PRIMARY KEY (sn)
)
