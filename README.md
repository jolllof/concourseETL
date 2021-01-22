# concourseETL
grabbing syllabi data from concourse api to be loaded into the WareHouse
extract.py requests a list of ids for the intial call and then for each id grabs the course details.
transform.py parses details into pandas dataframe to be loaded.
still working on load.py which would then load each table into WH
