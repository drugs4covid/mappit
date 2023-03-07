# Mappit

**Mappit** is a tool that automatically generates mappings making correspondences between the target ontology and heterogeneous source data (i.e. JSON, CSV, XML and RDBs). It relies on the ontology constructs to build the mapping structure and distance metrics for making the correspondences to the data, producing both RML and R2RML mappings.

## Getting started

Mappit can be executed from CLI first installing the requirements:

```
python3 install -r requirements.txt
```

Then, you can run the tool giving as input a `properties` file. 

```
./mappit properties/properties_json.json
```

### Properties file
recieves as input a `properties` file written in JSON with information about the mapping language to be used, the data source and the input ontology. This file is then read by the tool in order to set the environment, load the ontology and load the data source. You can see examples of `properties` file in the `./properties` folder. This file contains the following information:

*  `main-ontology`: Path to the ontology file, either in turtle or owl, or the ontology's IRI.
*  `distance-metric`: Method used to compare the difference between strings inside the tool. The metrics included in Mappit are the _Levehnstein_ distance, _Jaro_ distance, the _Jaccard_ distance and the _Longest Common Subset (LCS)_.
*  `compare-system`: Mappit uses either the ontology or the database as the main structure for the mappings. This system establishes the direction in which the comparison is going to be done: ontology or data-source. `ontology` uses the ontology as the main structure of the mappings and searchs for suitable elements in the database to do the matchings. `data-source` employs the database as the main structure and tries to find classes and properties that match with its own tables and columns.
*  `map-language`: The mapping language in which the mapper is going to write the mappigns. It can be either `R2RML` or `RML`.
*  `data`: Contains information about the location and type of data source that is going to be used. Depending on the format data source, it contains different information:`
   -  `Database`: If the data source is a relational database, this element contains the following information:`
       1.  `format`: Data format, in this case, a `database`.
       2.  `type`: Type of database used. It can be either a `mysql` database or a `postgres` database.
       3.  `database`: Name of the database.
       4.  `user`: Name of the user used to access to the database.
       5.  `password`: Pasword for the user's account.
       6.  `port`: Port at which the user is going to connect.
       7.  `host`: Host of the database.`
   -  `Non-database formats`: All other formats, such as JSON, CSV or XML, Include the same elements:`
       1.  `format`: Data format, could be either JSON, CSV or XML.
       2.  `folder`: Path to the folder in which all the data files are located. It is necessary that all the files are located in the same folder. The Input data must be located inside the `Inputs folder` inside the tool folders.
       3.  `separator`: Separator used to divide columns and elements inside the data (`,` `-` `;` ...). `
   -  `output`: Name for the output file in which the mapping is going to be written.
   -  `base`: Base URI for the ontology. It is included the `URI` for the ontology and its `prefix`.
