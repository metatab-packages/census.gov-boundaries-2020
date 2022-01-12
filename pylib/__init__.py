""" Example pylib functions"""



def process_geo(resource, doc, env, *args, **kwargs):
    """ An example row generator function.

    Reference this function in a Metatab file as the value of a Datafile:

            Datafile: python:pylib#row_generator

    The function must yield rows, with the first being headers, and subsequenct rows being data.

    :param resource: The Datafile term being processed
    :param doc: The Metatab document that contains the term being processed
    :param args: Positional arguments passed to the generator
    :param kwargs: Keyword arguments passed to the generator
    :return:


    The env argument is a dict with these environmental keys:

    * CACHE_DIR
    * RESOURCE_NAME
    * RESOLVED_URL
    * WORKING_DIR
    * METATAB_DOC
    * METATAB_WORKING_DIR
    * METATAB_PACKAGE

    It also contains key/value pairs for all of the properties of the resource.

    """

    from geoid.aff import AffGeoid

    ref = doc.reference(resource.name+'_source')
    
    def county(g):
        try:
            return g.county
        except:
            return None
            
    def state(g):
        try:
            return g.state
        except:
            return None
            
    def stateab(g):
        try:
            return g.stusab
        except:
            return None

    if 'zcta' in ref.name:
        geoid_name = 'AFFGEOID10'
        name_name = 'ZCTA5CE10'
        land_name = 'ALAND10'
        water_name = 'AWATER10'
    else:
        geoid_name = 'AFFGEOID'
        name_name = 'NAME'
        land_name = 'ALAND'
        water_name = 'AWATER'
        

    yield 'geoid name stusab state_fips county_fips land_area water_area geometry'.split()
    

    for row in ref.iterrows:

        g =  AffGeoid.parse(row[geoid_name]).as_acs()

        yield [
            g, 
            row[name_name],
            stateab(g),
            state(g),
            county(g),
            row.get(land_name),
            row.get(water_name),
            row.geometry
        ]
        
    


def custom_update(doc, args):
    """Custom update function, run with `mp update -U`

    The args argument will recieve any remainder arguments from the call, for instance

        mp update -U -- --foo bar

    """


    from metapack.cli.core import prt



    for rf in doc.references():
        
        resource_name = rf['name'].value.replace('_source','')
        
        rs = doc.resource(resource_name)
        
        if not rs:
            rs = doc['Resources'].new_term('Root.Datafile', name=resource_name)
        
        rs.value = 'python:pylib#process_geo'
        rs['description'] = rf['description'].value
        

    doc.write()
