import vk.api
from pymongo import MongoClient
from .local_vk import find_document, insert_document

service_token = 'your service token'

session = vk.AuthSession(access_token=service_token)
vk_api = vk.API(session, v=5.95)

client = MongoClient('localhost:32769')
db = client.target_base
infos = db.target_collection


def getuser(user_id, fields: list):
    new_fields = ", ".join(fields)
    # country, status, education, universities, bdate, last_seen, site, sex,
    # screen_name, schools, relation, relatives, photo_max_orig, exports, personal,
    # occupation,music, movies, activities, about, books, career, contacts, connections, city

    data = find_document(infos, {"id": int(user_id)}, multiple=False)
    if data is None:
        json_data = vk_api.users.get(user_id=user_id, fields=new_fields)[0]
        if 'deactivated' in json_data:
            return False
        insert_document(infos, json_data)
        return json_data
    del data['_id']
    return data


def print_user(json_data):
    for key, val in json_data.items():
        if key == 'sex' and val == 2:
            print(key, 'male')
        elif key == 'sex' and val == 1:
            print(key, 'female')
        elif val != '':
            print(f'{key}: {val}')


def get_friends(user_id, fields: list):
    friends = vk_api.friends.get(user_id=user_id, order='random')
    friends_info_list = list()
    print("num of friends:", friends["count"])
    for friend_id in friends["items"]:
        user = getuser(str(friend_id), fields)
        if user is not False:
            #print_user(user)
            friends_info_list.append(user)
        else:
            print("deleted id:", friend_id)
    return friends_info_list


def compare_search(users, fields: dict):
    compare_users = list()
    for user in users:
        for field, value in fields.items():
            compare_func = comparing_functions.get(field)
            if user.get(field):
                if compare_func(user.get(field), value):
                    compare_users.append((user["id"], user["first_name"], user["last_name"]))
                    print(user["id"], user["first_name"], user["last_name"], field)
    return compare_users


def city_compare(users_city, comparing_city):
    if users_city['title'] == comparing_city:
        return True


def universities_compare(users_data, comparing_data):
    for university in users_data:
        if university["name"] == comparing_data:
            return True
        if comparing_data in university["name"]:
            return True
    return False


comparing_functions = {
    "city": city_compare,
    "universities": universities_compare
}


def banner():
    banner = """\

       ##                  ##      ,______         __     ____,____    ,_______,        __     ,           ,           ,                                       
      #####            ######      |              /  \        |        |       |       /  \     \         / \         /                                      
      # ######       ##### ##      |             /    \       |        |       |      /    \     \       /   \       /                                      
      #  ################  ##      |            /______\      |        |_______|     /______\     \     /     \     /
      # ################## ##      |           /        \     |        |            /        \     \   /       \   /
      #######################      |______  __/__      __\__  |        |         __/__      __\__   \_/         \_/ 
      ########################                                         
      ########################                                          v.0.1.1
      ###   ### ####  ##    ##                                   OSINT Social Media Tool
      ####      ####       ###                                         ~AmaSus01~       
       ######################                                         
      # ####################  #                                       %###: .####.         
     #    #################    #                                     .##### +####*     
         ##################                                       -+: =###= -####..+*                    
         ##################      ####                            -####.   -+:.   %###=                 
         ####################    ####                            .####% .#####: :####*        
          ##########################                              .=#%.-#######+ *#@-           
            ############     ######                                  -###########+       
            ############                                             %############      
             ####  ####                                              .@####%@####:


    """
    print(banner)