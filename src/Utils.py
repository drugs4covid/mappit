import numpy as numpy

class Utilities:
    def levenshteinDistanceDP(token1, token2):
        distances = numpy.zeros((len(token1) + 1, len(token2) + 1))

        for t1 in range(len(token1) + 1):
            distances[t1][0] = t1

        for t2 in range(len(token2) + 1):
            distances[0][t2] = t2
            
        a = 0
        b = 0
        c = 0
        
        for t1 in range(1, len(token1) + 1):
            for t2 in range(1, len(token2) + 1):
                if (token1[t1-1] == token2[t2-1]):
                    distances[t1][t2] = distances[t1 - 1][t2 - 1]
                else:
                    a = distances[t1][t2 - 1]
                    b = distances[t1 - 1][t2]
                    c = distances[t1 - 1][t2 - 1]
                    
                    if (a <= b and a <= c):
                        distances[t1][t2] = a + 1
                    elif (b <= a and b <= c):
                        distances[t1][t2] = b + 1
                    else:
                        distances[t1][t2] = c + 1
        return distances[len(token1)][len(token2)]
        
    #min(1, 1 - abs(t1-t2)/len(token1))

    def string_distance(str1, str2):
        distances = numpy.zeros(len(str1))
        streak = 0
        for x in range(0, len(str1)):
            for y in range(x, len(str2)):
                char1 = str1[x].lower()
                char2 = str2[y].lower()
                if char1 == char2:
                    val = min(1, 1 - abs(x-y)/(max(len(str1), len(str2))))
                    #print(val)
                    if distances[x] < val:
                        distances[x] = val + streak
                    if val == 1:
                        streak += 0.1
                        break
        #print(distances)
        return numpy.sum(distances)/(max(len(str1), len(str2)))

    def jaccard_distance(list1, list2):
        intersection = len(list(set(list1).intersection(list2)))
        union = (len(list1) + len(list2)) - intersection
        return float(intersection) / union

    def jaro_distance(s1,s2):
        if (s1==s2):
            return 1.0

        len1=len(s1)
        len2=len(s2)

        if (len1==0 or len2==0):
            return 0.0

        max_dist=(max(len1, len2)//2)-1

        match=0

        hash_s1=[0]*len1
        hash_s2=[0]*len2

        for i in range(len1):
            for j in range(max(1,i-max_dist),min(len2, i+max_dist+1)):
                if (s1[i]==s2[j] and hash_s2[j]==0):
                    hash_s1[i]==1
                    hash_s2[j]==1
                    match+=1
                    break

        if (match==0):
            return 0.0

        t=0
        point=0

        for i in range(len1):
            if (hash_s1[i]):
                while (hash_s2[point]==0):
                    point+=1
                if (s1[i]!=s2[point]):
                    point+=1
                    t+=1
                else:
                    point+=1
                # global t
                t/=2

        return ((match/len1+match/len2+(match-t)/match)/3.0)
