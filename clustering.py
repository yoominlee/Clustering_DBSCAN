## Goal: Perform clustering on a given data set by using DBSCAN
import math
import sys
import copy

def read_input_file(input_file_name):
    input_file = open(input_file_name, 'r') # open(파일 이름, 열기모드(r/w/a))
    raw_data = input_file.readlines() # list 형태임.
    input_file.close()

    datapoint_2dlist=[]

    for one_point in raw_data:
        t = one_point.replace("\n", "").split()

        temp_coord = [] # 한 data point 안의 item 번호, x,y 담는다.
        item_count=0
        for item in t:
            if item_count>2:
                raise("input file ERROR: too many component in one row")
            if item_count==0:
                temp_coord.append(int(item)) # t의 (0번째 값은 index, )1번째 값은 x좌표, 2번째 값은 y좌표
            else:
                temp_coord.append(float(item))

            item_count += 1
        temp_coord.append(int(-1)) # 3번째 값으로 label. -1(undefined)로 초기화. 
        datapoint_2dlist.append(temp_coord)

    ## datapoint_2dlist -> array에 각 datapoint들.
    ## array 각 요소에, [0: input에 있던 index / 1: x좌표 / 2: y좌표 / 3: undefined(-1)로 초기화된 label]    
    return datapoint_2dlist


def range_query(datapoint_2dlist,point_p,input_Eps):
    append_count =0
    neighbors = [] 
    exept_p = datapoint_2dlist
    del exept_p[point_p[0]]
    for neighbor_candidate in exept_p:
        if abs(neighbor_candidate[1]-point_p[1]) > input_Eps or abs(neighbor_candidate[2]-point_p[2]) > input_Eps:
            # print("continue ",neighbor_candidate[0])
            # print("abs(neighbor_candidate[1]-point_p[1]): ",neighbor_candidate[1]," - ",point_p[1]," = ",abs(neighbor_candidate[1]-point_p[1]))
            # print("input_Eps: ",input_Eps)
            continue
        x = neighbor_candidate[1] - point_p[1]
        y = neighbor_candidate[2] - point_p[2]
        dist = math.sqrt((x ** 2) + (y ** 2))
        # print("calc ",neighbor_candidate[0])
        if dist < input_Eps:
            neighbors.append(neighbor_candidate)
            append_count+=1
            # print("app ",neighbor_candidate[0])

    # print("append_count: ",append_count)
    return neighbors

def clustering(datapoint_2dlist, input_Eps, input_MinPts):
    prev_cluster_count = -1
    for p in range(len(datapoint_2dlist)): # Iterate over every point
        #print("p - ", p)
        if datapoint_2dlist[p][3]!=-1: # Skip processed points
            #print("CONTINUE 1")
            continue
        # Find initial neighbors
        neighbors = range_query(copy.deepcopy(datapoint_2dlist),datapoint_2dlist[p],input_Eps)
        if len(neighbors) < input_MinPts:
            datapoint_2dlist[p][3] = -2 # Noise로 우선 분류
            #print("CONTINUE 2")
            continue
        prev_cluster_count += 1
        datapoint_2dlist[p][3] = prev_cluster_count # Start a new cluster
        seed_set = neighbors
        q_count = 0
        #print("before while - ",p)
        while q_count < len(seed_set):
            #print("q_count - ",q_count, "  ", p)
            if seed_set[q_count][3] == -2: # if label(q) == Noise
                #print("===== EDIT 1 =====")
                datapoint_2dlist[seed_set[q_count][0]][3] = prev_cluster_count
            if seed_set[q_count][3] != -1: # if label(q) != Undefined
                q_count += 1
                #print("CONTINUE 3")
                continue
            neighbors1 = range_query(copy.deepcopy(datapoint_2dlist),seed_set[q_count],input_Eps)
            #print("===== EDIT 2 =====")
            datapoint_2dlist[seed_set[q_count][0]][3] = prev_cluster_count
            if len(neighbors1) < input_MinPts: # Core-point check
                q_count += 1
                #print("CONTINUE 4")
                continue
            for i in neighbors1:
                append = True
                for s in seed_set:
                    if s[0] == i[0]:
                        append = False
                if append == True:
                    seed_set.append(i)
            q_count += 1

    return datapoint_2dlist, prev_cluster_count

def write_file(datapoint_2dlist, input_file_name, prev_cluster_count, input_n):
    cluster_objects = []
    # Cluster별로 cluster_objects 안에 저장. (cluster # = cluster_objects의 인덱스)
    # 첫번째 for문은 cluster 개수만큼 빈 array 만들고, 두번째 for문은 모든 데이터 돌면서 cluster_objects에 인덱스 맞춰서 넣음
    for k in range(prev_cluster_count+1):
        cluster_objects.append([])
    for i in datapoint_2dlist:
        cluster_num = i[3]
        if cluster_num >= 0 and cluster_num <= prev_cluster_count: # undefined, noise인 -1, -2와 같이 클러스터 아닌 값들이 들어가는 것 방지. 
            cluster_objects[cluster_num].append(i[0])

    # Optional part - (cluster # > input으로 넣은 n)인 경우, 크기 작은 클러스터부터 제거.
    if prev_cluster_count+1 > input_n:
        cluster_data_count = []
        for l in range(prev_cluster_count):
            cluster_data_count.append(len(cluster_objects[l]))
        while len(cluster_objects) <= input_n:
            remove_index = cluster_data_count.index(min(cluster_data_count))
            del cluster_objects[remove_index]
            del cluster_data_count[remove_index]

    # 클러스터별로 파일 만들기
    for n in range(prev_cluster_count):
        output_file_name = "input" + str(input_file_name[-5]) + "_cluster_"+ str(n) +".txt"
        output_file = open(output_file_name, 'w')

        print(output_file_name)
        objects = cluster_objects[n]
        for o in objects:
            output_file.write(f'{o}\n')
        output_file.close()

    while prev_cluster_count+1 < input_n: # input으로 넣은 클러스터 수보다 적은 수의 클러스터가 존재하는 경우
        output_file_name = "input" + str(input_file_name[-5]) + "_cluster_"+ str(prev_cluster_count+1) +".txt"
        output_file = open(output_file_name, 'w')
        output_file.write('\n')
        output_file.close()
        prev_cluster_count += 1

if __name__ == '__main__':
    input_file_name = sys.argv[1]
    input_n = int(sys.argv[2]) # number of clusters for the corresponding input data
    input_Eps = float(sys.argv[3]) # maximum radius of the neighborhood
    input_MinPts = int(sys.argv[4]) # minimum number of points in an Eps-neighborhood of a given point

    datapoint_2dlist = read_input_file(input_file_name)

    datapoint_2dlist, prev_cluster_count = clustering(datapoint_2dlist, input_Eps, input_MinPts)

    write_file(datapoint_2dlist, input_file_name, prev_cluster_count, input_n)
