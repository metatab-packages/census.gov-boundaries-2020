# Census Cartographic Boundary Files, 2020 Vintage

This data package collects a selection of the US Census cartographic shape
files, which are designed to be used in creating maps. For each type of region,
they come in a varity of resolutions, so they are more suitable for creating
web maps than the much larger TIGER files.

<center><img src="http://library.metatab.org/census.gov-boundaries-2018-1.2.4/notebooks/continental.png" width='600'/></center>

These files have been processed to all have the same schema and use ACS style
Geoids. The original files have AFF style geoids, which have extra '00'
characters in them.

The use of a single schema means that in some files, some columns are
consistently empty. For instance, ZCTA ( which are similar to ZIP code regions)
may not be entirely within a single state or county, so they don't have a
well-defined state and county. In these cases, the ``state_fips`` ``stusab``
and ``county_fips`` columns will be empty.

