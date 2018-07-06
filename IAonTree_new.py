'''
Created on 2017年12月6日
@author: oyzds
'''
import random as ra
import networkx as nx
import matplotlib.pyplot as plt
import time


jCount = 0#jordan成功的节点数
cCount = 0#CC成功的节点数
exception = 0

treeDegree = input("树的度数：")
treeHeight = input("树的高度：")
    
for k in range(100):
    
    print("第" + str(k) + "次执行：")
    p1 = ra.randint(1,100)#p1的概率
    p2 = ra.randint(2,98)#p2的概率
    if p2 <= 100 - p2 :
        minP2 = p2
    else:
        minP2 = 100 - p2    
    r2 = ra.randint(2,minP2)#r2 > r1
    r1 = ra.randint(1,r2-1)
    
    runTime = ra.randint(3,30)
    G = nx.balanced_tree(int(treeDegree),int(treeHeight))
    print("p1:" + str(p1)+ "," + "p2:" + str(p2) + "," + "r2:" + str(r2) + "," + "r1:" + str(r1))
    #pos = nx.spring_layout(G) 
    #nx.draw_networkx(G,pos,with_labels=True,node_color='green')
    
    I_state=[]
    E_state=[]
    R_state=[]
       
    num = nx.number_of_nodes(G) 
    root = ra.randint(0,num-1)
    #nx.draw_networkx_nodes(G,pos,with_labels=True,nodelist=[root],node_color='r',node_size = 550) #画出根节点
    print("根节点为：" + str(root))
    
    G.node[root]['node_state'] = 'I' #设置根节点状态为I
    I_state.append(root)  #把根节点入列表
    
    for i in range(num):
        if i != root:
            G.node[i]['node_state'] = 'S'
  
    print("运行时间：" + str(runTime))
    t = 1
    while(t<=runTime):
        for I_node in I_state:
            I_neighbor_list = nx.all_neighbors(G, I_node)
            for I_neighbor_node in I_neighbor_list:
                if G.node[I_neighbor_node]['node_state'] == 'S':
                    if ra.randint(1,100) <= p1 :
                        #nx.draw_networkx_nodes(G,pos,with_labels=True,nodelist=[I_neighbor_node],node_color='yellow')
                        G.node[I_neighbor_node]['node_state'] = 'E'
                        E_state.append(I_neighbor_node)
                        #print("节点" + str(I_neighbor_node) + "在时刻t = " + str(t) + "接受谣言")
                        E_node = I_neighbor_node #把这个被感染的节点值给予E_node
                        G.node[E_node]['node_time'] = t #给在这个时间由I变为E的节点记录时刻，防止在下面的for循环中这个节点开始活动
            if ra.randint(1,100) <= r1 :
                #nx.draw_networkx_nodes(G,pos,with_labels=True,nodelist=[I_node],node_color='blue')
                G.node[I_node]['node_state'] = 'R'
                R_state.append(I_node)
                I_state.remove(I_node)
                #print("节点" + str(I_node) + "在时刻t = " + str(t) + "恢复！")
                
        for E_node in E_state:
            if G.node[E_node]['node_time'] != t :#判断这个节点收到谣言的时间
                random = ra.randint(1,100)
                if random <= p2 :
                    #nx.draw_networkx_nodes(G,pos,with_labels=True,nodelist=[E_node],node_color='red')
                    G.node[E_node]['node_state'] = 'I'
                    I_state.append(E_node)
                    E_state.remove(E_node)
                    #print("节点" + str(E_node) + "在时刻t = " + str(t) + "被感染！")
                elif random <= r2:
                    #nx.draw_networkx_nodes(G,pos,with_labels=True,nodelist=[E_node],node_color='blue')
                    G.node[E_node]['node_state'] = 'R'
                    R_state.append(E_node)
                    E_state.remove(E_node)
                    #print("节点" + str(E_node) + "在时刻t = " + str(t) + "恢复！")
        t+=1
    
    
    #RI Algorithm
    if I_state and (len(I_state) + len(E_state) + len(R_state)) <= 200 : 
        print("I： " + str(len(I_state)) + ", E: " + str(len(E_state)) + ", R: " + str(len(R_state)))
        
        ecc = 10000000000
        for node in range(num) :
            temp = 0
            for I_node in I_state :
                distanceNodeToINode = 0
                distanceNodeToINode = nx.shortest_path_length(G,node,I_node)
                if distanceNodeToINode > temp :
                    temp = distanceNodeToINode
            G.node[node]['maxValueECC'] = temp
            if temp < ecc :
                ecc = temp

        jNode = 0
        jNodeSet = []
        for node in range(num):
            if G.node[node]['maxValueECC'] == ecc:
                jNode = node
                jNodeSet.append(jNode)
        for NI in jNodeSet:
            print("乔丹节点：" + str(NI) + ", eccentricity : " + str(ecc))
            if NI == root:
                jCount+=1
                print("乔丹节点等于根节点! 目前成功数：" + str(jCount))
            else:
                #distant_jNode = snap.GetShortPath(G5, jNode, root)
                print("乔丹节点距离根节点：" + str(ecc) + " 跳. 目前成功数：" + str(jCount))
    
        print("例外个数：" + str(exception))   
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        
        #CC Algorithm
        temp = 0
        closeness = 0
        for node in range(num) :
            if G.node[node]['node_state'] == 'I' or G.node[node]['node_state'] == 'R' :
                closeness = nx.closeness_centrality(G,node)
                if closeness > temp :
                    temp = closeness
                    maxCentralityNode = node
        print("The node of " + str(maxCentralityNode) + " is maximum, "+ "closeness centrality is " + str(temp))
        if maxCentralityNode != root:
            distant_cNode = nx.shortest_path_length(G,maxCentralityNode, root)
            print("亲密中心性节点距离根节点：" + str(distant_cNode) + " 跳, 目前成功数："  + str(cCount))
            #print("亲密中心性节点成功等于源点个数：" + str(cCount))
        else:
            cCount+=1
            #print("亲密中心性节点成功等于源点个数：" + str(cCount))
            print("亲密中心性节点等于根节点! 目前成功数：" + str(cCount))
    
    #f = open('e:\pythonDate.txt','a')
    #f.write("\n\n\n第" + str(k) + "次执行：\n")
    #f.write("p1:" + str(p1)+ ",  " + "p2:" + str(p2) + ",  " + "r2:" + str(r2) + ",  " + "r1:" + str(r1)+ "\n")
    #f.write("根节点为：" + str(root) + "\n")
    #f.write("运行时间：" + str(runTime)+ "\n")    
    
    #f.write("Jordan Center : " + str(node) + ", eccentricity : " + str(ecc)+ "\n")
    #if jNode != root:
        #distant_jNode = nx.shortest_path_length(G,jNode,root)
        #f.write("乔丹节点距离根节点：" + str(distant_jNode) + " 跳,   " + "成功率：" + str(jCount) + "\n")
        #f.write("乔丹节点成功等于源点个数：" + str(jCount)+"\n")
    #else:
        #f.write("乔丹节点等于根节点!   " + "成功率：" + str(jCount) + "\n")
        #f.write("乔丹节点成功等于源点个数：" + str(jCount)+"\n")
    
    #f.write("The node of " + str(maxCentralityNode) + " is maximum, "+ "closeness centrality is " + str(temp)+ "\n")
    #if maxCentralityNode != root:
        #distant_cNode = nx.shortest_path_length(G,maxCentralityNode,root)
        #f.write("亲密中心性节点距离根节点：" + str(distant_cNode) + " 跳,    " + "成功率：" + str(cCount) + "\n")
        #f.write("亲密中心性节点成功等于源点个数：" + str(cCount)+"\n")
    #else:
        #f.write("亲密中心性节点等于根节点!   " + "成功率：" + str(cCount) + "\n")
        #f.write("亲密中心性节点成功等于源点个数：" + str(cCount)+"\n")
    else:
        exception+=1
        print("==============exception===============" + str(exception))
    
    
    localtime = time.asctime( time.localtime(time.time()))
    print("**********************" + localtime + "**********************")
    
    #f.write("=========" + localtime + "========="+ "\n")
    #f.close()
    
