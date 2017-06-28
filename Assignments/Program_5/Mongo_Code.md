#Windows 10   
##added mongoDB\bin folder to path Environment variables:   
1. edit PATH in Environment variables in Control Panel\System and Security\System\Advanced System Settings
2. add mongoDB bin folder
##Commands:   
1. mongod	(open connection)
2. mongo
3. mongoimport --jsonArray --db [name_to_call_db]--collection [name_to_call_collection]--file [file_name]
4. mongorestore -d [name_to_call_db] [path_to_db]