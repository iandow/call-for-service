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

# Loading data - Officer Allocation

The officer allocation plugin is an optional addition to the main CFS app that allows you to explore
how your officers are spending their time during the day.  It requires files with the following data:

 - a "call log" CSV file, containing a timestamped row for each unit's actions on a call (for example, "Dispatched", "Arrived", "Cleared", etc)
 - a "shift" CSV file, containing start and end timestamps for each unit on duty
 
More specifically, the "call log" file should contain the following fields (again, Code/Text fields must match up):

 - Internal ID (**MUST** map to a call in your calls file)
 - Transaction Code (Arrived, Dispatched, etc)
 - Transaction Text
 - Timestamp
 - Unit

And the "shift" file should contain the following fields:

 - Unit
 - Officer ID
 - In Timestamp
 - Out Timestamp
 
You will also need to do some configuration through the admin interface in order for the officer allocation view to work properly.  **NOTE**: You must perform this step _before_ you load any data; the officer allocation configuration must be set up correctly before data is loaded for the loading scripts to work correctly.

1. Log in to the admin interface as described in [the Configuration docs](config.md).
2. Click on "Call sources".  Identify which call sources correspond to "Self Initiated" calls (i.e., calls initiated by officers rather than civilians).  For each such source, click on its description to access the detailed edit page.  Click the checkbox labeled "Is self initiated" and click "Save".  You should be returned to the call source list, and the source you just edited should now have a green check mark in the "Is self initiated column".  Repeat as needed.  Once this is done for all "Self Initiated" sources, return to the main admin page.
3. Click on "Natures".  Repeat the process outlined in 2. but for natures corresponding to "Directed Patrols" (i.e., officers patrolling a specific area).  Mark each such nature accordingly and save your changes.
 
Once you have correctly configured the site for your data and have loaded your call data as described above, run the following command from the top level directory of this repository:

    ./cfs/manage.py load_ofc_alloc --call-log-file <location of your call log CSV file> --shift-file <location of your shift CSV file>
    
This will load and transform the call log and shift data in order to generate the officer allocation chart in
the dashboard.

**NOTE**: Since there are no primary keys in the call log or shift files, our loading script has no way to determine whether you're loading duplicate data (whereas with calls, the duplicate data is ignored based on the primary key).  Therefore, if you try to re-load files you already loaded, duplicate data will be created, and the resulting charts will be inaccurate.
