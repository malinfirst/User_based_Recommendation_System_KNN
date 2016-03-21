# -*- coding: utf-8 -*-
"""
Mining Assignment 1
Cohort A - Team 1
Ryan Krieger, Raul Molina, Lin Ma, Chaitra Prabhakar
"""

import math

#################################################
# recommender class does user-based filtering and recommends items 
class UserBasedFilteringRecommender:
    
    # class variables:    
    # none
    
    ##################################
    # class instantiation method - initializes instance variables
    #
    # usersItemRatings:
    # users item ratings data is in the form of a nested dictionary:
    # at the top level, we have User Names as keys, and their Item Ratings as values;
    # and Item Ratings are themselves dictionaries with Item Names as keys, and Ratings as values
    # Example: 
    #     {"Angelica":{"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0},
    #      "Bill":{"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0}}
    #
    # metric:
    # metric is in the form of a string. it can be any of the following:
    # "minkowski", "cosine", "pearson"
    #     recall that manhattan = minkowski with r=1, and euclidean = minkowski with r=2
    # defaults to "pearson"
    #
    # r:
    # minkowski parameter
    # set to r for minkowski, and ignored for cosine and pearson
    #
    # k:
    # the number of nearest neighbors
    # defaults to 1
    #
    def __init__(self, usersItemRatings, metric='pearson', r=1, k=1):
        
        # set self.usersItemRatings
        self.usersItemRatings = usersItemRatings

        # set self.metric and self.similarityFn
        if metric.lower() == 'minkowski':
            self.metric = metric
            self.similarityFn = self.minkowskiFn
        elif metric.lower() == 'cosine':
            self.metric = metric
            self.similarityFn = self.cosineFn
        elif metric.lower() == 'pearson':
            self.metric = metric
            self.similarityFn = self.pearsonFn
        else:
            print ("    (DEBUG - metric not in (minkowski, cosine, pearson) - defaulting to pearson)")
            self.metric = 'pearson'
            self.similarityFn = self.pearsonFn
        
        # set self.r
        if (self.metric == 'minkowski'and r > 0):
            self.r = r
        elif (self.metric == 'minkowski'and r <= 0):
            print ("    (DEBUG - invalid value of r for minkowski (must be > 0) - defaulting to 1)")
            self.r = 1
            
        # set self.k
        if k > 0:   
            self.k = k
        else:
            print ("    (DEBUG - invalid value of k (must be > 0) - defaulting to 1)")
            self.k = 1
            
    
    #################################################
    # minkowski distance (dis)similarity - most general distance-based (dis)simialrity measure
    # notation: if UserX is Angelica and UserY is Bill, then:
    # userXItemRatings = {"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0}
    # userYItemRatings = {"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0}
    def minkowskiFn(self, userXItemRatings, userYItemRatings):
        
        distance = 0
        commonRatings = False 
        
        for item in userXItemRatings:
            # inlcude item rating in distance only if it exists for both users
            if item in userYItemRatings:
                distance += pow(abs(userXItemRatings[item] - userYItemRatings[item]), self.r)
                commonRatings = True
                
        if commonRatings:
            return round(pow(distance,1/self.r), 2)
        else:
            # no ratings in common
            return -2

    #################################################
    # cosince similarity
    # notation: if UserX is Angelica and UserY is Bill, then:
    # userXItemRatings = {"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0}
    # userYItemRatings = {"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0}
    def cosineFn(self, userXItemRatings, userYItemRatings):
        
        sum_xy = 0
        sum_x2 = 0
        sum_y2 = 0
        
        for item in userXItemRatings:
            if item in userYItemRatings:
                x = userXItemRatings[item]
                y = userYItemRatings[item]
                sum_xy += x * y
                sum_x2 += pow(x, 2)
                sum_y2 += pow(y, 2)
        
        denominator = math.sqrt(sum_x2) * math.sqrt(sum_y2)
        if denominator == 0:
            return -2
        else:
            return round(sum_xy / denominator, 3)

    #################################################
    # pearson correlation similarity
    # notation: if UserX is Angelica and UserY is Bill, then:
    # userXItemRatings = {"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0}
    # userYItemRatings = {"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0}
    def pearsonFn(self, userXItemRatings, userYItemRatings):
        
        sum_xy = 0
        sum_x = 0
        sum_y = 0
        sum_x2 = 0
        sum_y2 = 0
        n = 0
        
        for item in userXItemRatings:
            if item in userYItemRatings:
                n += 1
                x = userXItemRatings[item]
                y = userYItemRatings[item]
                sum_xy += x * y
                sum_x += x
                sum_y += y
                sum_x2 += pow(x, 2)
                sum_y2 += pow(y, 2)
       
        if n == 0:
            return -2
        
        denominator = math.sqrt(sum_x2 - pow(sum_x, 2) / n) * math.sqrt(sum_y2 - pow(sum_y, 2) / n)
        if denominator == 0:
            return -2
        else:
            return round((sum_xy - (sum_x * sum_y) / n) / denominator, 2)
            
    ###################################################
    def getDistanceDict(self, ratingDict, userX):
        distanceDD = {}
        for names in ratingDict.keys():
            distanceD = {}
            for name1 in ratingDict.keys():
                distance = round(self.similarityFn(ratingDict[names],ratingDict[name1]),3)
                distanceD[name1] = distance
            
            distanceDD[names] = distanceD
        
        return distanceDD
    
    
    
    ####################################################
    # This creates a tuple list of recommend items based off of a nested dictionary of
    # relationship measurements, nested dictionary of user ratings, and the specified
    # user.
    def weightedAVG(self, distanceDict, ratingsDict, userX):
        userDistance = distanceDict[userX]     #retrieving distance vector associated with userX
        del userDistance[userX]   #removing userX from the measurments
        userDistance = [(v,k) for k,v in userDistance.items()]   #separating dictionary into list of tuple pairs
        
        #separates sorted names and measurements based off of specified metric
        if self.metric.lower() == 'minkowski':
            userDistance.sort(key= lambda tup: tup[0])
            userNames = [v for k,v in userDistance]
            userDistance = [k for k,v in userDistance]
            
        elif self.metric.lower() == 'cosine':
            userDistance.sort(key= lambda tup: tup[0], reverse=True)   #need reverse order because larger values are more signifigant for cosine
            userNames = [v for k,v in userDistance]
            userDistance = [k for k,v in userDistance]
            
        else:
            userDistance.sort(key= lambda tup: tup[0], reverse=True)   #need reverse order because larger values are more signifigant for pearson corellation
            userNames = [v for k,v in userDistance]
            userDistance = [k for k,v in userDistance]
            userDistance = [(userDistance[i]+1)/2 for i in range(len(userDistance))]   #correction to remove the possibility of negative numbers, correlation scale is now 0 to 1
        
        #selecting the k nearest neighbors and calculating the weighted average
        userNames = userNames[0:self.k]   
        userDistance = userDistance[0:self.k]
        totalDistance = sum(userDistance)
        userDistance = [userDistance[i]/totalDistance for i in range(len(userDistance))]
        
        
        recDD = {}   #creating new nested dictionary for recommendation values
        
        recD = {}
        for k,v in zip(userNames, userDistance):
            recL = [v*float(i) for i in ratingsDict[k].values()]   #multiplying weighted average value for given user by their rating scores for each song        
            recD = dict(zip(ratingsDict[k].keys(), recL))   #recreating a dictionary to store all values as a nested dictionary
            recDD[k] = recD
        

        
                
        finalrec = {}  #creating new nested dictionary for final recommendation values
        
        #This block will sum the recommendation values from all nearest neighbors for songs that the specified user hasn't listened to
        for names in recDD.keys():
            for song in recDD[names].keys():
                if song not in ratingsDict[userX].keys():
                    if song not in finalrec.keys():
                        finalrec[song] = recDD[names][song]
                    else:    
                        finalrec[song] += recDD[names][song]
                    
        return finalrec
                
                
    #################################################
    # make recommendations for userX from the most similar k nearest neigibors (NNs)
    def recommendKNN(self, userX):
        
        # YOUR CODE HERE
        relation = self.getDistanceDict(self.usersItemRatings, userX)  #getting distance relations dictionary
        
        recommendation = self.weightedAVG(relation, self.usersItemRatings, userX)  #getting the recommended songs and values
        
        rounded = [(k,round(v,2)) for k,v in recommendation.items()]  #rounding recommended values to 2 decimal places
        rounded.sort(key=lambda tup: tup[1], reverse=True)   #sorting recommended songs highest to lowest
        
        return rounded
        
        
        
        # for given userX, get the sorted list of users - by most similar to least similar        
        
        # calcualte the weighted average item recommendations for userX from userX's k NNs
        
        # return sorted list of recommendations (sorted highest to lowest ratings)
        # example: [('Broken Bells', 2.64), ('Vampire Weekend', 2.2), ('Deadmau5', 1.71)]
        
        # once you are done coding this method, delete the pass statement below
        



        
