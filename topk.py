'''    
1. Implement Fagin method
2. Implement TA method
3. Implement NRA method

Input: num_dim, top_k
    num_dim: Number of dimension
    top_k: Variable k in top-'k' query
Output: uids_result, cnt_access
    uid_result: Result of top-k uids of the scores. 
                The summation function is used 
                for the score function.

                i.e., num_dim = 4, k = 2
                ----------------------------
                 uid    D0   D1    D2    D3
                ----------------------------
                "001"    1    1     1     1
                "002"    2    2     2     2
                "003"    3    3     3     3
                "004"    5    5     5     5
                ----------------------------                
                
                score("001") = 1 + 1 + 1 + 1 = 4
                score("002") = 2 + 2 + 2 + 2 = 8
                score("003") = 3 + 3 + 3 + 3 = 12  --> top-2
                score("004") = 4 + 4 + 4 + 4 = 16  --> top-1
                
                uids_result: ["004", "003"]

    cnt_access: Number of access in each algorithm

Tip: Use Naive method to check your code
     Naive method is the free gift for the code understanding
'''
from collections import defaultdict
from typing import Tuple

def get_score(list_values) -> float:
    result = 0.0
    for v in list_values:
        result += v
    return result

class Algo():
    def __init__(self, list_sorted_entities, uid2dim2value):
        self.list_sorted_entities = list_sorted_entities

        '''
        variable for random access,
        but please do not use this variable directly.
        If you want to get the value of the entity,
        use method 'random_access(uid, dim)'
        '''
        self.__uid2dim2value__ = uid2dim2value
    
    def random_access(cls, uid, dim) -> float:
        return cls.__uid2dim2value__[uid][dim]

    def Naive(cls, num_dim, top_k) -> Tuple[list, int]:
        uids_result = []
        cnt_access = 0

        # read all values from the sorted lists
        uid2dim2value = defaultdict(dict)
        for dim in range(num_dim):            
            for uid,value in cls.list_sorted_entities[dim]:
                uid2dim2value[uid][dim] = value
                cnt_access += 1

        # compute the score and sort it
        uid2score = defaultdict(float)
        for uid, dim2value in uid2dim2value.items():
            list_values = []
            for dim in range(num_dim):
                list_values.append(dim2value[dim])
            score = get_score(list_values)
            uid2score[uid] = score
        
        sorted_uid2score = sorted(uid2score.items(), key = lambda x : -x[1])

        # get the top-k results
        for i in range(top_k):
            uids_result.append(sorted_uid2score[i][0])

        return uids_result, cnt_access


    # Please use random_access(uid, dim) for random access
    def Fagin(cls, num_dim, top_k) -> Tuple[list, int]:
        uids_result = []
        cnt_access = 0

        uid2dim2value = defaultdict(dict)
        for idx in range(len(cls.list_sorted_entities[0])):
            satisfy = 0
            for dim in range(num_dim):
                uid = cls.list_sorted_entities[dim][idx][0]
                value = cls.list_sorted_entities[dim][idx][1]

                uid2dim2value[uid][dim] = value

                cnt_access += 1

            for uid, dic in uid2dim2value.items():
                if len(dic) == num_dim:
                    satisfy += 1

            if satisfy >= top_k:
                break

        uid2score = defaultdict(float)
        for uid, dic in uid2dim2value.items():
            lst = []
            for dim in range(num_dim):
                try:
                    lst.append(dic[dim])

                except:
                    random_value = cls.random_access(uid, dim)
                    lst.append(random_value)
                    cnt_access += 1

            uid2score[uid] = get_score(lst)

        sorted_uid2score = sorted(uid2score.items(), key = lambda x : -x[1])

        for i in range(top_k):
            uids_result.append(sorted_uid2score[i][0])

        return uids_result, cnt_access

    # Please use random_access(uid, dim) for random access
    def TA(cls, num_dim, top_k) -> Tuple[list, int]:
        uids_result = []
        cnt_access = 0

        uid2dim2value = defaultdict(dict)
        uid2score = defaultdict(float)
        for idx in range(len(cls.list_sorted_entities[0])):
            threshold = 0
            for dim in range(num_dim):
                uid = cls.list_sorted_entities[dim][idx][0]
                value = cls.list_sorted_entities[dim][idx][1]

                if uid2dim2value[uid].get(dim) is None:
                    uid2dim2value[uid][dim] = value

                threshold += value

                cnt_access += 1

            for uid, dic in uid2dim2value.items():
                if not (uid in uid2score):
                    lst = []
                    for dim in range(num_dim):
                        if dic.get(dim) is None:
                            random_value = cls.random_access(uid, dim)
                            lst.append(random_value)

                            cnt_access += 1

                        else:
                            lst.append(dic[dim])

                    uid2score[uid] = get_score(lst)

            sorted_uid2score = sorted(uid2score.items(), key = lambda x : -x[1])

            if len(sorted_uid2score) < top_k:
                continue

            else:
                lst = sorted_uid2score[:top_k]

                if lst[-1][1] > threshold:
                    for i in range(top_k):
                        uids_result.append(lst[i][0])

                    break

                else:
                    continue

        return uids_result, cnt_access

    # You cannot use random access in this method
    def NRA(cls, num_dim, top_k) -> Tuple[list, int]:
        uids_result = []
        cnt_access = 0

        uid2dim2value = defaultdict(dict)
        uid2lb2ub = defaultdict(list)
        for idx in range(len(cls.list_sorted_entities[0])):
            lst = []
            for dim in range(num_dim):
                uid = cls.list_sorted_entities[dim][idx][0]
                value = cls.list_sorted_entities[dim][idx][1]

                uid2dim2value[uid][dim] = value

                lst.append(value)

                cnt_access += 1

                if not (uid in uid2lb2ub):
                    uid2lb2ub[uid] = [value, 0]

                else:
                    uid2lb2ub[uid][0] += value

            for uid, dic in uid2dim2value.items():
                uid2lb2ub[uid][1] = uid2lb2ub[uid][0]
                for dim in range(num_dim):
                    if not (dim in uid2dim2value[uid]):
                        uid2lb2ub[uid][1] += lst[dim]

            if len(uid2lb2ub) > top_k:
                sorted_uid2lbub = sorted(uid2lb2ub.items(), key = lambda x : -x[1][0])

                flag = True
                for i in range(top_k, len(sorted_uid2lbub)):
                    if sorted_uid2lbub[top_k-1][1][0] < sorted_uid2lbub[i][1][1]:
                        flag = False
                        break

                if flag:
                    for i in range(top_k):
                        uids_result.append(sorted_uid2lbub[i][0])

                    break

        return uids_result, cnt_access
