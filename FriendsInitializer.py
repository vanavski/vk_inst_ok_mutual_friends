from vk.exceptions import VkAPIError
from Database import Database
from InstagramDatabase import InstagramDatabase
from ConfigAPI import ConfigAPI
import numpy as np
import numpy.lib.recfunctions as recfunctions
from OkDatabase import OkDatabase

class Initializer(object):
    #
    def vk_refs(self, user_id, reference, api):
        if ('https://vk.com/' in reference):
            if ('id' in reference):
                us_split = reference.split('id')
                vk_us_id = us_split[1]
                #             проверка на ограничения юзера
                if (self.check_account(vk_us_id, api)):
                    friends = api.friends.get(user_id=vk_us_id, extended=1)['items']
                    print('good')
                    if (2767201 in friends):
                        print('Бот в друзьях')
                    else:
                        print('добавьте бота в друзья')
                    db = Database()
                    db.add_vk_user_to_db(user_id, vk_us_id, friends)
                    print('added to db')
                else:
                    print('no fr')


            else:
                us_split = reference.split('/')
                us_nick = us_split[3]
                #             проверка на ограничения юзера, чекнуть можно ли вытащить айди у забаненного, ограниченного, чс юзера
                if (self.check_account(us_nick, api)):
                    user = api.users.get(user_ids=[us_nick])
                    vk_us_id = user[0]['id']
                    friends = api.friends.get(user_id=vk_us_id, extended=1)['items']
                    print('good')
                    if (2767201 in friends):
                        print('true')
                    else:
                        print('добавьте бота в друзья')
                    #             add friends to db
                    db = Database()
                    db.add_vk_user_to_db(user_id, vk_us_id, friends)
                    print('added to db')
                else:
                    print('no fr')
        #             add friends to db
        else:
            print('Некорректная ссылка!')

    #
    def check_account(self, us_id, api):
        try:
            user = api.users.get(user_ids=us_id,
                                 fields='photo_id, verified, sex, bdate, city, country, home_town, has_photo, photo_50, photo_100, photo_200_orig, photo_200, photo_400_orig, photo_max, photo_max_orig, online, domain, has_mobile, contacts, site, education, universities, schools, status, last_seen, followers_count, common_count, occupation, nickname, relatives, relation, personal, connections, exports, activities, interests, music, movies, tv, books, games, about, quotes, can_post, can_see_all_posts, can_see_audio, can_write_private_message, can_send_friend_request, is_favorite, is_hidden_from_feed, timezone, screen_name, maiden_name, crop_photo, is_friend, friend_status, career, military, blacklisted, blacklisted_by_me, can_be_invited_group')

            print('Обрабатывается: {} {}'.format(user[0]['first_name'], user[0]['last_name']))
            if (user[0].get('deactivated') != None):
                print('deactivated account: {}'.format(user[0]['id']))
                return False
            elif (user[0]['is_closed'] == True):
                print('private account: {}'.format(user[0]['id']))
                return False
            elif (user[0].get('blacklisted') != None):
                if (user[0]['blacklisted'] == 1):
                    print('You are in the blacklist: {}'.format(user[0]['id']))
                    return False
                else:
                    return True
            else:
                return True
        except VkAPIError as e:
            if e.code == 18:
                print('account #{} is closed or deactivated!'.format(user[0]['id']))
                #                 self.init(api)
                return False


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

    def insert_mark_friend(self, us_id, friend_id, score):
        if (score == 0 or score == 1):
            db = Database()
            is_contains = db.insert_mark_score_for_friend(us_id, friend_id,score)
            if is_contains == True:
                db.update_mark_score_for_friend(us_id, friend_id, score)
        else:
            print('некорректные данные в score')

# config = ConfigAPI()
# config.init()
init = Initializer()
# init.vk_refs(11, 'https://vk.com/prekrasno', config.api)

init.get_friends_on_site(11)
# init.insert_mark_friend(1, 3, 1)