1. Mongo db name: world_data
    
 * collections:    
    1. airports        
    1. cities 
    3. countries
    4. earthquakes
    5. meteorites
    6. states
    7. volcanoes 
2. To run batch file: .\load_mongo.sh or .\load_mongo.bat (Note: geojson may need to be mango\bin)
3. Example queries:

 * query 1 : note ( if radius is too small it will cause an infinite loop ) 
    1. python query1.py LAX CIA 950  
    2. python query1.py IAD RUH 1200 
    3. python query1.py jfk fuk 1000
    
 * query 2 : 
    1. python query2.py meteorites mass 3000 max 3 1000 
    2. python query2.py earthquakes mag 7 min 7 1500  
    3. python query2.py 2000 
    4. python query2.py earthquakes magnitude 5 max 3 2500 (128.320313,46.111326) 
    
* query 3 : note ( dbscan need time to proccess meteorites and earthquakes, can pass a limit to points passed to dbscan( as in ex. iv), default is 5000, if limit is too small it may not find clusters )
    1. python query3.py meteorites 20 25
    2. python query3.py volcanoes 40 30
    3. python query3.py all 70 25
    4. python query3.py all 10 10 7000