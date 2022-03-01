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