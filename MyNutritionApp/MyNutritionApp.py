import nutritionix
import sqlite3
import sys

def get_food_items(min_calorie, max_calorie, start, end):
    obj = nix.search().nxql(
		offset=start_index,
	  	limit=50,
		filters={
		    "nf_calories": {
		        "from": min_calorie,
                "to":max_calorie
		    }
		},
		fields=["item_name", "item_id", "nf_calories"]
	).json()
    limit=50
    end = start+limit
    return (obj['total'], end, start+end, obj)  


if __name__ == "__main__":

    MAX_ITEMS_TO_FETCH = 10000
    MIN_CALORIE = 80
    MAX_CALORIE = 600

    #fetch APP ID and API key from APP_CREDENTIALS file
    lines = open("APP_CREDENTIALS","r").readlines()
    app_id = lines[0].split("=")[1].strip("\r\n")
    app_key = lines[1].split("=")[1].strip("\r\n")
    nix = nutritionix.Nutritionix(app_id=app_id, api_key=app_key)
    (start_index, end_index)=(0,0)
    
    #Write this data to database
    conn = sqlite3.connect("NutritionDatabase.db")
    conn.text_factory = str
    conn.execute("create table FoodsAndCalories(Food TEXT, Calorie REAL)")
    print "Start"
    sys.stdout.flush()
    while(True):
		#keep calling until we get all results or end_index>100
        if end_index>MAX_ITEMS_TO_FETCH:
            break
        (total_no_results, start_index, end_index, obj) = get_food_items(MIN_CALORIE, MAX_CALORIE ,start_index ,end_index)
        
        if total_no_results<end_index:
            break

        for hit in obj['hits']:
            food = hit['fields']['item_name']
            calorie = float(hit['fields']['nf_calories'])
        #print "start:",start_index," and end:",end_index
            #write
            conn.execute("insert into FoodsAndCalories values (?,?)",(food, calorie))
    
    conn.commit()
    conn.close()
    print "Done"

    
