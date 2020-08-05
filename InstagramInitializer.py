from instagram_private_api import Client, ClientCompatPatch
from InstagramDatabase import InstagramDatabase
from Database import Database

import numpy as np
import numpy.lib.recfunctions as recfunctions

class InstagramInitializer(object):
    def add_friends_by_link(self, user_id, reference):
        if ('instagram.com/' in reference):

            us_split = reference.split('com/')
            inst_nickname = us_split[1]
            inst_nickname = inst_nickname.replace("/", "")

            friends, inst_us_id = self.get_friends(inst_nickname)
            #             проверка на ограничения юзера
            if (friends != None and len(friends) != 0):

                db = InstagramDatabase()
                db.add_inst_user_to_db(user_id, inst_us_id, friends)
                print('added to db')
            else:
                print('private account')

    def get_friends(self, nickname):
        user_name = ''
        password = ''

        api = Client(user_name, password)
        results = api.username_info(nickname)
        id = results['user']['pk']
        followings = self.get_followings(id, api)
        followers = self.get_followers(id, api)
        if (len(followings) == 0 and len(followers) == 0 and results['user']['is_private'] == True):
            print('Account is private. Follow to account')
            #         api.friendships_create(id)
            return None, id
        friend_list = list(set(followings) & set(followers))
        return friend_list, id

    def get_followings(self, id, api):
        token = api.generate_uuid()
        followers = api.user_following(id, token)
        follow_list = []
        for i in range(len(followers['users'])):
            follow_list.append(followers['users'][i]['pk'])
        return follow_list

    def get_followers(self, id, api):
        token = api.generate_uuid()
        followers = api.user_followers(id, token)
        follow_list = []
        for i in range(len(followers['users'])):
            follow_list.append(followers['users'][i]['pk'])
        return follow_list



    def get_friends_on_site(self, us_id):
        db = Database()

        proposed_fr_list = []

        name_vk_table_with_friends = db.get_table_name_by_user_id(us_id)

        if (name_vk_table_with_friends != None):
            friends_on_site_vk = db.get_friends_us_id_by_table_name(name_vk_table_with_friends)

            if (friends_on_site_vk != None):
                proposed_fr_list = db.check_users_in_confidence_list(friends_on_site_vk, us_id)



        inst_db = InstagramDatabase()
        proposed_fr_list_inst = []

        name_vk_table_with_friends = inst_db.get_table_name_by_user_id(us_id)

        if (name_vk_table_with_friends != None):
            friends_on_site_inst = inst_db.get_friends_us_id_by_table_name(name_vk_table_with_friends)

            if (friends_on_site_inst != None):
                proposed_fr_list_inst = inst_db.check_users_in_confidence_list(friends_on_site_inst, us_id)


        # outer join proposed_fr_list & proposed_fr_list_inst
        if (len(proposed_fr_list) > 0 or len(proposed_fr_list_inst) > 0):
            friends_array = self.get_joined_array(proposed_fr_list, proposed_fr_list_inst)

            push_list = []
            if (friends_array != None):
                if (len(friends_array) > 0):
                    push_list, us_id = db.push_notifications(us_id, friends_array)

            print(friends_array)
            return friends_array, push_list, us_id
        return None, None, us_id

    def get_joined_array(self, arr1, arr2):
        # https://stackoverflow.com/questions/23500754/numpy-how-to-outer-join-arrays

        if (len(arr1) > 0):
            box1 = arr1
            if len(arr2) > 0:
                box2 = arr2
            else:
                box2 = [box1[0]]
        else:
            if len(arr2) > 0:
                box2 = arr2
                box1 = [box2[0]]
            else:
                return None

        a3 = np.array(box1, dtype=[('col1', np.int8)])
        a2 = np.array(box2, dtype=[('col1', np.int8)])
        a1 = a3[0]

        result = a1

        for a in (a2, a3):
            cols = list(set(result.dtype.names).intersection(a.dtype.names))
            result = recfunctions.join_by(cols, result, a, jointype='outer')

        pr_fr_l = []
        for item in result:
            pr_fr_l.append(item[0])
        print(pr_fr_l)
        return pr_fr_l

iner = InstagramInitializer()
# iner.add_friends_by_link(3, 'https://www.instagram.com/blabla/')

iner.get_friends_on_site(3)