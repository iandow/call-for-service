# Loading data - Calls

## Data format

CFS Analytics loads data from CSV files with one call per line. These files
must have the following headers:

- Internal ID
- Time Received
- Time Dispatched
- Time Arrived
- Time Closed

Each internal ID should be unique. If one is encountered that has been seen
before, it is ignored.

(There is a current bug around this. If the same ID is in the same file more
than once, an error can occur.)

The files should have some or all of the following headers. Note that headers
that end in "Code" and "Text" come in pairs and must be matched.

- Street Address
- City
- Zip
- Latitude
- Longitude
- Priority
- Source
- Beat
- District
- Nature Code
- Nature Text
- Close Code
- Close Text

Having additional headers is fine.

## Running the load command

From the command line, in the top level directory of this repository, run:

    ./cfs/manage.py load_call_csv <name of your CSV file>

This will load not only the individual calls in your CSV file but will also
create the priorities, districts, beats, natures, sources, and close codes from your source
file.

If no agency code is provided, new calls will be assigned to the first agency in the database.
If you are using the application with multiple agencies, you can load data for an individual agency with the
following command:

    ./cfs/manage.py load_call_csv <name of your CSV file> --agency <code of your agency, ex. CPD>



# Loading data - Officer Allocation

The officer allocation plugin is an optional addition to the main CFS app that allows you to explore
how your officers are spending their time during the day.  It requires files with the following data:

 - a "call log" CSV file, containing a timestamped row for each unit's actions on a call (for example, "Dispatched", "Arrived", "Cleared", etc)
 - a "shift" CSV file, containing start and end timestamps for each unit on duty

More specifically, the "call log" file should contain the following fields (again, Code/Text fields must match up):

 - Internal ID (should map to a call in your calls file)
 - Transaction Code (Arrived, Dispatched, etc)
 - Transaction Text
 - Timestamp
 - Unit

And the "shift" file should contain the following fields:

 - Unit
 - In Timestamp
 - Out Timestamp

You will also need to do some configuration through the admin interface in order for the officer allocation view to work properly.  **NOTE**: You must perform these steps _after_ your call data is loaded but _before_ you load any officer allocation data; the officer allocation configuration must be set up correctly before its data is loaded for the loading scripts to work correctly.

1. Log in to the admin interface as described in [the Configuration docs](config.md).
2. Click on "Call sources".  Identify which call sources correspond to "Self Initiated" calls (i.e., calls initiated by officers rather than civilians).  For each such source, click on its description to access the detailed edit page.  Click the checkbox labeled "Is self initiated" and click "Save".  You should be returned to the call source list, and the source you just edited should now have a green check mark in the "Is self initiated column".  Repeat as needed.  Once this is done for all "Self Initiated" sources, return to the main admin page.
3. Click on "Natures".  Repeat the process outlined in 2. but for natures corresponding to "Directed Patrols" (i.e., officers patrolling a specific area).  Mark each such nature accordingly and save your changes.  Return to the main admin page when done.
4. Click on "Transactions".  For all transactions in your data associated with an officer's involvement "starting" on a call (ex. "Dispatched"), click "Add transaction", enter the corresponding code (must be an exact, case-sensitive match) and the description, and check "Is start".  Then, for all transactions associated with an officer's involvement "ending" on a call (ex. "Cleared", "Canceled"), do the same; click "Add transaction", enter the exact code and description, and check "Is end".  Save and return to the main admin page.  You do not need to enter _all_ the transactions in your data; you only need to create these special ones ahead of time so the system knows which ones they are.  The remaining transactions will be created in the database during data load.

Once you have correctly configured the site for your data **and have loaded your call data** as described above, run the following command from the top level directory of this repository:

    ./cfs/manage.py load_ofc_alloc --call-log-file <location of your call log CSV file> \
        --shift-file <location of your shift CSV file>

This will load and transform the call log and shift data in order to generate the officer allocation chart in
the dashboard.

As before, officer allocation will be assigned to the first agency in the database by default.  If you have multiple agencies,
you may load data for each separately with the following command:

    ./cfs/manage.py load_ofc_alloc --call-log-file <location of your call log CSV file> \
        --shift-file <location of your shift CSV file> \
        --agency <code of your agency ex. CPD>

**NOTE**: Since there are no primary keys in the call log or shift files, our loading script has no way to determine whether you're loading duplicate data (whereas with calls, the duplicate data is ignored based on the primary key).  Therefore, if you try to re-load files you already loaded, duplicate data will be created, and the resulting charts will be inaccurate.
