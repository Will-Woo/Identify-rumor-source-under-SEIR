import snap#第三方库
#import networkx as nx
#import matplotlib.pyplot as plt
#import graphviz as gr
import random as ra
import time
import math

jCount = 0#jordan成功的节点数
cCount = 0#CC成功的节点数
exception = 0#例外的节点数

oneHopNum_J = 0
twoHopNum_J = 0
threeHopNum_J = 0

oneHopNum_C = 0
twoHopNum_C = 0
threeHopNum_C  = 0
    
G5 = snap.LoadEdgeList(snap.PNEANet,"facebook.txt", 0, 1)
num = G5.GetNodes()


for k in range(100):
    
    print("第" + str(k) + "次执行：")
    print("节点总数：" + str(num))
    p1 = ra.randint(1,100)#p1的概率
    p2 = ra.randint(2,98)#p2的概率
    if p2 <= 100 - p2 :
        minP2 = p2
    else:
        minP2 = 100 - p2
        
    r2 = ra.randint(2,minP2)
    r1 = ra.randint(1,r2-1)
    print("p1:" + str(p1)+ "," + "p2:" + str(p2) + "," + "r2:" + str(r2) + "," + "r1:" + str(r1)) 
    
    I_state=[]
    E_state=[]
    R_state=[]
    
    root = G5.GetRndNId()
    print "根节点是: " + str(root)
    
    G5.AddStrAttrDatN(root, "I", "node_state")
    I_state.append(root)
    
    for NI in G5.Nodes():
        if NI.GetId() != root:
            G5.AddStrAttrDatN(NI.GetId(), "S", "node_state")
            
    runTime = ra.randint(3,200)#时间
    print("Time ：" + str(runTime))
    t = 1
    while(t<=runTime):
        #I_node = 0
        for I_node in I_state:
            I_neighbor_list = G5.GetNI(I_node).GetOutEdges()
            for I_neighbor_node in I_neighbor_list :
                if G5.GetStrAttrDatN(I_neighbor_node, "node_state") == 'S':
                    if ra.randint(1,100) <= p1 :
                        #nx.draw_networkx_nodes(G,pos,with_labels=True,nodelist=[I_neighbor_node],node_color='yellow')
                        G5.AddStrAttrDatN(I_neighbor_node, "E", "node_state")
                        E_state.append(I_neighbor_node)
                        #print("节点" + str(I_neighbor_node) + "在时刻t = " + str(t) + "接受谣言")
                        E_node = I_neighbor_node #把这个被感染的节点值给予E_node
                        G5.AddIntAttrDatN(E_node, t, "node_time")#给在这个时间由I变为E的节点记录时刻，防止在下面的for循环中这个节点开始活动 
            if ra.randint(1,100) <= r1 :
                #nx.draw_networkx_nodes(G,pos,with_labels=True,nodelist=[I_node],node_color='blue')
                G5.AddStrAttrDatN(I_node, "R", "node_state")
                R_state.append(I_node)
                I_state.remove(I_node)
                #print("节点" + str(I_node) + "在时刻t = " + str(t) + "恢复！")
                
        for E_node in E_state:
            if G5.GetIntAttrDatN(E_node, "node_time") != t :#判断这个节点收到谣言的时间
                random = ra.randint(1,100)
                if random <= p2 :
                    #nx.draw_networkx_nodes(G,pos,with_labels=True,nodelist=[E_node],node_color='red')
                    G5.AddStrAttrDatN(E_node, "I", "node_state")
                    I_state.append(E_node)
                    E_state.remove(E_node)
                    #print("节点" + str(E_node) + "在时刻t = " + str(t) + "被感染！")
                elif random <= r2:
                    #nx.draw_networkx_nodes(G,pos,with_labels=True,nodelist=[E_node],node_color='blue')
                    G5.AddStrAttrDatN(E_node, "R", "node_state")
                    R_state.append(E_node)
                    E_state.remove(E_node)
                    #print("节点" + str(E_node) + "在时刻t = " + str(t) + "恢复！")
        t+=1
    
    #RI Algorithm
    if I_state :
        print("I： " + str(len(I_state)) + ", E: " + str(len(E_state)) + ", R: " + str(len(R_state)))    
        tempMaxValueECC = 10000000000000        
        for node in G5.Nodes():
            temp = 0
            for I_node in I_state :
                distanceNodeToINode = 0
                distanceNodeToINode = snap.GetShortPath(G5, node.GetId(), I_node)
                if distanceNodeToINode > temp :
                    temp = distanceNodeToINode
            G5.AddIntAttrDatN(node.GetId(), temp, "maxValueECC")
            if temp < tempMaxValueECC:
                tempMaxValueECC = temp            

        jNode = 0
        jNodeSet = []
        for node in G5.Nodes():
            if G5.GetIntAttrDatN(node.GetId(), "maxValueECC") == tempMaxValueECC:
                jNode = node.GetId()
                jNodeSet.append(jNode)
        for NI in jNodeSet:
            print("乔丹节点是: " + str(NI) + ", 偏心距 : " + str(tempMaxValueECC))
            if NI == root:
                jCount+=1
                print("乔丹节点等于根节点! 目前成功个数：" + str(jCount))
                #print("例外个数：" + str(exception))
            else:
                #distant_jNode = snap.GetShortPath(G5, jNode, root)
                print("乔丹节点距离根节点 " + str(tempMaxValueECC) + " 跳 ， 目前成功个数：" + str(jCount))
                #print("例外个数：" + str(exception))
        if tempMaxValueECC == 1:
            oneHopNum_J+=1
            print("1 hop : " + str(oneHopNum_J) + ", 2 hops : " + str(twoHopNum_J) + ", 3 hops : " + str(threeHopNum_J))
        elif tempMaxValueECC == 2:
            twoHopNum_J+=1
            print("1 hop : " + str(oneHopNum_J) + ", 2 hops : " + str(twoHopNum_J) + ", 3 hops : " + str(threeHopNum_J))
        elif tempMaxValueECC == 3:
            threeHopNum_J+=1
            print("1 hop : " + str(oneHopNum_J) + ", 2 hops : " + str(twoHopNum_J) + ", 3 hops : " + str(threeHopNum_J))
        print("例外个数：" + str(exception))    
        
        
        print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        #CC Algorithm
        temp = 0.0
        ccNodeSet = []
        for node in G5.Nodes():
            if G5.GetStrAttrDatN(node.GetId(),"node_state") == 'I' or G5.GetStrAttrDatN(node.GetId(),"node_state") == 'R' :
                ccNodeSet.append(node.GetId())
                CCvalue = 0.0
                CCvalue = snap.GetClosenessCentr(G5,node.GetId())
                G5.AddFltAttrDatN(node.GetId(), CCvalue, "CC")
                if CCvalue > temp :
                    temp = CCvalue
   
        for NI in ccNodeSet:
            if G5.GetFltAttrDatN(NI,"CC") == temp:
                print("节点" + str(NI) + " 亲密中心性最大, "+ "值为：  " + str(temp))
                if NI == root:
                    cCount+=1
                    print("亲密中心性节点等于根节点! 目前成功个数：" + str(cCount))
                else:
                    distant_cNode = snap.GetShortPath(G5, NI, root)
                    print("亲密中心性节点距离根节点：" + str(distant_cNode) + " 跳， 目前成功个数："  + str(cCount))
                    if distant_cNode == 1 :
                        oneHopNum_C+=1
                        print("1 hop : " + str(oneHopNum_C) + ", 2 hops : " + str(twoHopNum_C) + ", 3 hops : " + str(threeHopNum_C))
                    elif distant_cNode == 2 :
                        twoHopNum_C+=1
                        print("1 hop : " + str(oneHopNum_C) + ", 2 hops : " + str(twoHopNum_C) + ", 3 hops : " + str(threeHopNum_C))
                    elif distant_cNode == 3 :
                        threeHopNum_C+=1
                        print("1 hop : " + str(oneHopNum_C) + ", 2 hops : " + str(twoHopNum_C) + ", 3 hops : " + str(threeHopNum_C))        
    else:
        exception+=1
        print("==============exception===============" + str(exception))
            
    localtime = time.asctime( time.localtime(time.time()) )
    print("**********************" + localtime + "**********************")
    
