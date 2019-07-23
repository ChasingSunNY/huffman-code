import heapq


def getDistribution(arr):
    counts = {}
    for v in arr:
        if v not in counts:
            counts[v] = 1
        else:
            counts[v] += 1

    ps = {x: (c * 1.0 / len(arr)) for x, c in counts.items()}

    return ps

def getEncoding(node, path, dic):
    if node[1] is not None:
        dic[node[1]] = path
        
    else:
        getEncoding(node[2], path + "0", dic)
        getEncoding(node[3], path + "1", dic)
        
def getEncodingRoot(root):
    dic = {}
    getEncoding(root, "", dic)
    return dic

def huffmanEncoding(seq):
    
    ps = getDistribution(seq)
    
    p = [(v, k, None, None) for (k, v) in ps.items()]

    heapq.heapify(p)

    while len(p) > 1:
        l = heapq.heappop(p)
        r = heapq.heappop(p)
        m = (l[0] + r[0], None, l, r)
        heapq.heappush(p, m)

    root = p[0]
    
    dic = getEncodingRoot(root)

    encoded = "".join([dic[x] for x in seq])
    
    encoded = encoded + "0" * (32 - len(encoded) % 32) 
    
    vs = []
    for i in range(0, len(encoded), 32):
        vs.append(int(encoded[i:(i+32)], 2))
    
#     print(len(vs))
#     
    return dic, vs, len(seq)



    
#     s = 

#     #print(len(encoded))
    
# #     v = int(encoded, 2)
    
    

#huffmanEncoding(X)
# huffmanEncoding(Y)
# huffmanEncoding(Z)

def getBinStr(x):
    
    s = bin(x)
    
    s = s[2:]
    
    s = "0" * (32 - len(s)) + s
    
    return s

def huffmanDecode(dic, vs, n):
    revDic = {v:k for k,v in dic.items()}
    s = "".join(getBinStr(x) for x in vs)
    
    cur = ""
    
    seq = []
    for i in range(len(s)):
        cur = cur + s[i]
        
        if cur in revDic:
            seq.append(revDic[cur])
            cur = ""
            
            if len(seq) == n:
                break
            
    
    return seq
            
encode("566.bin", 1, "1.encoded")
decode("1.encoded", 1, "1.decode")
encode("566.bin", 2, "2.encoded")
decode("2.encoded", 2, "2.decode")
encode("566.bin", 3, "3.encoded")
decode("3.encoded", 3, "3.decode")
