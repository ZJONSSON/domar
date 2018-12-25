### Purpose
The `list.js` is a quick script that exports a function that delivers a stream of all court results (metadata and abstracts) from the icelandic court system.  

### Preparation

Install etl-cli globally:

`npm install -g etl-cli`

Then install dependencies in this directory

`npm install`

### Execution

The stream can be processed by the `etl-cli` command line utility as follows:

`etl list.js [output]`

For example, export to a csv file:

`etl list.js list.csv`

or to a line-delimited json file:

`etl list.js list.json`

or directly into mongodb, mysql, elasticsearch (see [etl-cli](https://github.com/ZJONSSON/etl-cli) for details)
