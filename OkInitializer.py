from OkDatabase import OkDatabase
from Database import Database
from InstagramDatabase import InstagramDatabase
import numpy as np
import numpy.lib.recfunctions as recfunctions

class OkInitializer(object):
    def add_friends_by_link(self, user_id, reference):
        if ('ok.ru/profile/' in reference):

            us_split = reference.split('profile/')
            ok_id = us_split[1]
            # ok_nickname = ok_nickname.replace("/", "")

            friends, ok_us_id = self.get_friends(ok_id)
            #             проверка на ограничения юзера
            if (friends != None and len(friends) != 0):

                db = OkDatabase()
                db.add_ok_user_to_db(user_id, ok_us_id, friends)
                print('added to db')
            else:
                print('private account')




    def get_friends(self, id):
        return 0



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



        ok_db = OkDatabase()
        proposed_fr_list_ok = []

        name_ok_table_with_friends = ok_db.get_table_name_by_user_id(us_id)

        if (name_ok_table_with_friends != None):
            friends_on_site_ok = ok_db.get_friends_us_id_by_table_name(name_vk_table_with_friends)

            if (friends_on_site_ok != None):
                proposed_fr_list_ok = ok_db.check_users_in_confidence_list(friends_on_site_ok, us_id)



        # outer join proposed_fr_list & proposed_fr_list_inst
        if (len(proposed_fr_list) > 0 or len(proposed_fr_list_inst) > 0 or len(proposed_fr_list_ok) > 0):
            friends_array = self.get_joined_array(proposed_fr_list, proposed_fr_list_inst, proposed_fr_list_ok)

            push_list = []
            if (friends_array != None):
                if (len(friends_array) > 0):
                    push_list, us_id = db.push_notifications(us_id, friends_array)

            print(friends_array)
            return friends_array, push_list, us_id
        return None, None, us_id

    def get_joined_array(self, arr1, arr2, arr3):
        # https://stackoverflow.com/questions/23500754/numpy-how-to-outer-join-arrays

        if (len(arr1) > 0):
            box1 = arr1
            if len(arr2) > 0:
                box2 = arr2
            else:
                box2 = [box1[0]]
            if len(arr3) > 0:
                box3 = arr3
            else:
                box3 = [box1[0]]
        else:
            if len(arr2) > 0:
                box2 = arr2
                box1 = [box2[0]]
                if len(arr3) > 0:
                    box3 = arr3
                else:
                    box3 = [box2[0]]
            else:
                if len(arr3) > 0:
                    box3 = arr3
                    box2 = [box3[0]]
                    box1 = [box3[0]]
                else:
                    return None

        a3 = np.array(box1, dtype=[('col1', np.int8)])
        a2 = np.array(box2, dtype=[('col1', np.int8)])
        a1 = np.array(box3, dtype=[('col1', np.int8)])

        result = a1

        for a in (a2, a3):
            cols = list(set(result.dtype.names).intersection(a.dtype.names))
            result = recfunctions.join_by(cols, result, a, jointype='outer')

        pr_fr_l = []
        for item in result:
            pr_fr_l.append(item[0])
        print(pr_fr_l)
        return pr_fr_l

db = OkDatabase()
# db.create_table_ok()