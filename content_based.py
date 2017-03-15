
from __future__ import division

import MySQLdb as mdb 
import datetime, time
#import pandas as pd
import os
import numpy as np
from math import sqrt
import math

def run_sql_file(filename, connection):
    '''
    The function takes a filename and a connection as input
    and will run the SQL query on the given connection  
    '''
    start = time.time()
    #connection.commit()
    file = open(filename, 'r')
    sql = s = " ".join(file.readlines())
    #print("Start executing: " + str(filename) + " at " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")) + "\n" ) 
    cursor = connection.cursor()
    
    #cursor.execute(sql) 

    flags_sql = "SELECT `flag_id` FROM `logs`"
    users_sql = "SELECT `user_id` FROM `logs`"
    match_sql = "SELECT `match` FROM `logs`"
    cursor.execute(flags_sql)
    flags = cursor.fetchall()

    cursor.execute(users_sql)
    users = cursor.fetchall()

    cursor.execute(match_sql)
    match = cursor.fetchall()

    chal_sql = "SELECT `id_chal` FROM `challenges`"
    flag_sql = "SELECT `flag_id_chal` FROM `challenges`"
    
    cursor.execute(chal_sql)
    chals = cursor.fetchall()
    cursor.execute(flag_sql)
    flag = cursor.fetchall()

    def problem_list(id_user):
        id_flag = []
        length = len(flags)
        i = 0
    
        while(i<length):
            if users[i][0]==id_user:
                if match[i][0]==1:
                    id_flag.append(int(flags[i][0]))
            i = i+1


        chal =[]
        length_flag = len(id_flag)
        length_chal = len(chals)
        i = 0
        while(i<length_flag):
            j = 0
            while(j<length_chal):
                if id_flag[i]==flag[j][0]:
                    chal.append(chals[j][0])
                j = j+1
            i = i+1
        return chal
        

    points_sql = "SELECT `points` FROM `flags`"
    flags_p_sql = "SELECT `id_flag` FROM `flags`"
    cursor.execute(points_sql)
    point = cursor.fetchall()
    cursor.execute(flags_p_sql)
    flag_p = cursor.fetchall()
    
    """
    point_new = []
    k = 0
    while(k<len(id_flag)):
        l = 0
        while(l<len(flag_p)):
            if id_flag[k]==flag_p[l][0]:
                point_new.append(point[l][0])
            l = l+1
        k = k+1
    chal_point = np.column_stack((chal,point_new))

    chal_sorted = []
    sort_chal = sorted(chal_point,key=lambda x: x[1])[0:5]
    i = 0
    while(i<5):
        chal_sorted.append(sort_chal[i][0])
        i = i+1

    """
    chal_t_sql = "SELECT `challenge_id` FROM `challenge_tag_maps`"
    tag_sql = "SELECT `tag_id` FROM `challenge_tag_maps`"
    cursor.execute(chal_t_sql)
    chal_t = cursor.fetchall()
    cursor.execute(tag_sql)
    tag = cursor.fetchall()

    tags_sql = "SELECT `id_tag` FROM `tags`"
    cursor.execute(tags_sql)
    tags_t = cursor.fetchall()

    def tags(p_id):
        tag_id = []
        i = 0
        while(i<len(chal_t)):
            if chal_t[i][0]==p_id:
                tag_id.append(tag[i][0])
            i = i+1
        return tag_id

    def create_tag_matrix(p_id):
        i = 0
        chals_tag = []
        while(i<len(tags_t)):
            if tags_t[i][0] in tags(p_id):
                chals_tag = np.append(chals_tag,1)
            else:
                chals_tag = np.append(chals_tag,0)
            i = i+1
        return chals_tag


    def tag_dict():
        
        dict_tag = {}
        for i in chals:
            dict_tag[i[0]] = {}
            k = 0
            for j in tags_t:
                dict_tag[i[0]][j[0]] = create_tag_matrix(i[0])[k]
                k = k+1
        return dict_tag



    def create_challenge_vector(u_id):
        i = 0
        users_list = []
        while(i<len(chals)):
            if chals[i][0] in problem_list(u_id):
                users_list = np.append(users_list,1)
            else:
                users_list = np.append(users_list,0)
            i = i+1
        return users_list




    def user_matrix():
        user_matrix = np.zeros((np.amax(users)+1, len(chals)))
        i = 0
        while(i<len(users)):
            user_matrix[i] = problem_list(users[i][0])
            i = i+1
        return user_matrix

    
    dict = {'Name': 'Zara', 'Age': 7, 'Class': 'First'}
    print(dict[Name])



    def sim_pearson(create_tag_matrix,p1,p2):
        # Get the list of mutually rated items
        si={}
        for item in create_tag_matrix[p1]:
            if item in create_tag_matrix[p2]: si[item]=1
        # Find the number of elements
        n=len(si)

        # if they are no ratings in common, return 0
        if n==0: return 0
        # Add up all the preferences
        sum1=sum([create_tag_matrix[p1][it] for it in si])
        sum2=sum([create_tag_matrix[p2][it] for it in si])
        # Sum up the squares
        sum1Sq=sum([pow(create_tag_matrix[p1][it],2) for it in si])
        sum2Sq=sum([pow(create_tag_matrix[p2][it],2) for it in si])
        # Sum up the products
        pSum=sum([create_tag_matrix[p1][it]*create_tag_matrix[p2][it] for it in si])
        # Calculate Pearson score
        num=pSum-(sum1*sum2/n)
        den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
        if den==0: return 0
        r=num/den
        return r
 

    # Returns the best matches for person from the prefs dictionary.
    # Number of results and similarity function are optional params.
    def topMatches(create_tag_matrix,person,n,similarity = sim_pearson):
        scores=[(similarity(create_tag_matrix,person,other[0]),other[0])
        for other in chals if other[0]!=person]
            # Sort the list so the highest scores appear at the top
        scores.sort( )
        scores.reverse( )
        return scores[0:n]
    a = topMatches(tag_dict(),5,3)
    for b in a:
        print(b[0])

    challenges_sql = "SELECT `id_comp_chal` FROM `competition_challenges`"
    cursor.execute(challenges_sql)
    chal_list = cursor.fetchall()

    def tag_match_score(p_id1 = 5):

        tag1 = tags(p_id1)
        score = []
        for prob in chals:
            tag2 = tags(prob[0])
            #print(float(len(list(set(tag1).intersection(tag2)))/np.maximum(len(tag2),len(tag1))))
            score.append(len(set(tag1).intersection(tag2))/np.maximum(len(tag2),len(tag1)))
        chal_score = np.column_stack((chals,score))
        #chal_score_sort = [np.argsort(chal_score[:,0])]
        chal_score_sort = sorted(chal_score,key=lambda x: x[1], reverse=True)[0:6]
        i = 0
        score_sort_chal = []
        while(i<6):
            if chal_score_sort[i][0]!= p_id1 :
                score_sort_chal.append(chal_score_sort[i][0])
            i = i+1
        return score_sort_chal

    end = time.time()
    cursor.close()

  


 
def main():    
    connection = mdb.connect('localhost', 'root', 'ahsin0710', 'backdoor_db25')
    #conn = mdb.connect('localhost', 'root', 'ahsin0710', 'backdoor_db2','competition_challenges')
    run_sql_file("backdoor.sql", connection)    
    connection.close()
    
main()