
import os, sys
import xml
import traci
import networkx as nx
import pandas as pd
import pyomo.environ as pyomo
import random
import matplotlib.pyplot as plt
import math
import plotly.express as px
import numpy as np
import copy

class vehicle():
    
    def __init__(self,veh_id,depart,route_id):
        self.veh_id=veh_id
        self.depart=depart
        self.route=route_id
        self.departLane="best"
        
#                    new_element = xml.etree.ElementTree.Element('vehicle')
#                    new_element.attrib['id']= 'vehicle_'+route_ID+'_'+str(flag)+'_'+str(depart)  
#                    new_element.attrib['depart'] =str(depart) 
#                    new_element.attrib['route'] =route_ID  
#                    new_element.attrib['departLane']="best"
class basic_information():
    traci=''
    sumo_config_file_path=''
    
    G=''
    
    
    edge_route=''
    network=''
    route_dir=''
    edge_route=''
    edge_routeIDs=''

    origin_list=''
    destination_list=''
    O_D_route_IDs=''  
    
    edge_list=[]
    edge_length={}
    edge_lanes={}
    edge_lane_IDs={}
    
    lane_list={}
    lane_length={}
    
    
    
    edge_flow={}
    veh_dir={}
    
    total_lane_length=0
    
    detector_list=[]   
    detector_data=''

    route_flow_list={}
    edge_cal_flow={}

    new_add_name=''
    new_rou_name=''
    
#    def __init__(self):
#        self.edge_lanes={}
#        self.edge_length={}
#        self.edge_list=[]
        
    @classmethod    
    def interface(cls,traci,sumo_GUI_EXE_Path,sumo_config_file_path,sumo_config_name):
        
        if 'SUMO_HOME' in os.environ:
             tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
             sys.path.append(tools)
        else:
             sys.exit("please declare environment variable 'SUMO_HOME'")
        #sumoBinary = "C:"+os.sep+"Sumo"+os.sep+"bin"+os.sep+"sumo-gui.exe"
        
        sumoBinary = sumo_GUI_EXE_Path+"sumo-gui.exe"
        #sumoBinary = "sumo-gui"
        sumoCmd = [sumoBinary, "-c", sumo_config_file_path+sumo_config_name,"--start"] ##,
        
        
        traci.start(sumoCmd)
        print("Starting SUMO")
#        conn1 = traci.getConnection("sim1")
        
        traci.gui.setSchema("View #0", "real world")
        
#        cls.traci=traci
        cls.sumo_config_file_path=sumo_config_file_path
#        cls.traci.close()
#        
    @classmethod        
    def get_edge_information(cls,traci):    
        edge_list=[]
        lane_list=[]
        
        
        edge_list_all=traci.edge.getIDList()
        
        for edge in edge_list_all:
            if edge[0]==':':
                continue
            edge_list.append(edge)
            cls.edge_lanes[edge]=traci.edge.getLaneNumber(edge)
            cls.edge_lane_IDs[edge]=[]
            
        lane_list_all=traci.lane.getIDList() 
        total_lane_length=0
        
        seperator='_'
        for lane in lane_list_all:
            if lane[0]==':':
                continue
            
            lane_list.append(lane)
            lane_c=lane.split('_')
            edge=seperator.join(lane_c[0:(len(lane_c)-1)])
            cls.edge_length[edge]=traci.lane.getLength(lane)
            cls.edge_lane_IDs[edge].append(lane)
            
            
        total_lane_length=0
        for edge in edge_list:
            total_lane_length=total_lane_length+cls.edge_length[edge]*len(cls.edge_lane_IDs[edge])
            
        cls.edge_list= edge_list
        cls.total_lane_length=total_lane_length
        
        
    @classmethod        
    def get_edge_information_from_osm_file(cls,sumo_config_file_path,sumo_net_name):    
        edge_list=[]
        lane_list=[]
        lane_length={}
        total_lane_length=0
        
        
        et = xml.etree.ElementTree.parse(sumo_config_file_path+sumo_net_name)
        root = et.getroot()
     
        for edge in root.findall('edge'):  
            if edge.attrib['id'][0]!=':' :             ## To remove the internal edges marked as"function="internal"
                
                edge_ID= edge.attrib['id']
                edge_list.append(edge_ID)
                
                edge_lane_num= len(edge)                
                cls.edge_lanes[edge_ID]=edge_lane_num
                cls.edge_length[edge_ID]=float(edge[0].attrib['length'])
                
                lanes=[]
                for lane in edge.findall('lane'):
                    lane_ID=lane.attrib['id']
                    lanes.append(lane_ID)
                    lane_list.append(lane_ID)
                    lane_length[lane_ID]=float(edge[0].attrib['length'])
                cls.edge_lane_IDs[edge_ID]=lanes 

        
        for edge in edge_list:
            total_lane_length=total_lane_length+cls.edge_length[edge]*len(cls.edge_lane_IDs[edge])
            
        cls.edge_list= edge_list
        cls.total_lane_length=total_lane_length
        cls.lane_list=lane_list
        cls.lane_length=lane_length
            
        


    @classmethod
    def measure_data_to_edgeflow(cls,sumo_config_file_path,sumo_add_name,measure_data):
        cls.detector_data=pd.read_csv(sumo_config_file_path+measure_data,index_col=[0])      # SUMO-calibration 需要的检测器数据
        lane_detector={}
        et = xml.etree.ElementTree.parse(sumo_config_file_path+sumo_add_name)
        
        detector_root=et.getroot()
        
        for detector in detector_root.findall('e1Detector'):
            
            de_Id=detector.attrib['id']
            de_lane=detector.attrib['lane']
            lane_detector[de_lane]=de_Id
     
        detector_flow=dict(zip(cls.detector_data.index.tolist(),
                                cls.detector_data['qPKW'].tolist() ))
         
        edge_flow={}
         
        for edge in cls.edge_lane_IDs.keys():
             
             edge_flow[edge]=0
             for lane in cls.edge_lane_IDs[edge]:
                 try:
                     detect_id=lane_detector[lane]
                     
                     edge_flow[edge]=edge_flow[edge]+detector_flow[detect_id]
                 except KeyError:
                     
                     print(lane+" does not exist a detector")     
        cls.edge_flow={x:y for x,y in edge_flow.items() if y!=0}
        
        
    @classmethod
    def Create_network(cls,sumo_config_file_path,sumo_net_name):
        et = xml.etree.ElementTree.parse(sumo_config_file_path+sumo_net_name)
        root = et.getroot()
        G = nx.DiGraph()
        node_o_count={}
        node_d_count={}
        node_list=[]
        edge_list=[]
        
        for edge in root.findall('edge'):  
            if edge.attrib['id'][0]!=':' :             ## To remove the internal edges marked as"function="internal"
                
           
                print(edge.attrib)

                edge_o=edge.attrib['from']
                edge_d=edge.attrib['to']
                
                node_list.append(edge_o)
                node_list.append(edge_d)
                
                G.add_edge(edge_o, edge_d)
                G[edge_o][edge_d]['length']= float(edge[0].attrib['length'])
                G[edge_o][edge_d]['speed']= float(edge[0].attrib['speed'])
                G[edge_o][edge_d]['id']= edge.attrib['id']
                G[edge_o][edge_d]['lanes_num']= len(edge)
                
                edge_list.append(G[edge_o][edge_d]['id'])
                lanes=[]
                for lane in edge.findall('lane'):
                    lanes.append(lane.attrib['id'])
                
                G[edge_o][edge_d]['lanes']=lanes 
                
                try:
                    node_o_count[edge_o]= node_o_count[edge_o]+1
                except KeyError:
                    node_o_count[edge_o]=1

                try:
                    node_d_count[edge_d]= node_d_count[edge_d]+1
                except KeyError:
                    node_d_count[edge_d]=1
                    
                print(edge.tag)
        connect_two_egde={}
        
        for edge in edge_list:
            connect_two_egde[edge]={}
            
        for connect in root.findall('connection'):
            
                    if connect.attrib['from'][0]==':' :       
                        continue
                    if connect.attrib['to'][0]==':' :       
                        continue
                    
#                    transfer_dir=connect_two_egde[edge]
#                    transfer_dir[]
                    
                    edge_A=connect.attrib['from']
                    edge_B=connect.attrib['to']
                    connect_two_egde[edge_A][edge_B]=1
         
            
        for node in root.findall('junction'):
            if node.attrib['type']!="internal" :
#                print('-----')
                node_id=node.attrib['id']

                G.nodes[node_id]['id'] = node_id
                
                G.nodes[node_id]['type'] = node.attrib['type']  
#                print(G.nodes[node_id]['type'])

                node_x=float(node.attrib['x'])
                node_y=float(node.attrib['y'])
                print(node_id)
                G.add_node(node_id,x=node_x,y=node_y)
                            
        origin_list=[]
        destination_list=[]    
#----------------------------               (very good, sumo 还有信号点属性之说)   
        for node in node_o_count.keys():
            if (node_o_count[node]<=1) and  (G.nodes[node]['type']=="dead_end"):
                
                origin_list.append(node)
        for node in node_d_count.keys() :
            if node_d_count[node]<=1 and  (G.nodes[node]['type']=="dead_end"):
                destination_list.append(node)
        
##---------------------------one-way network for VISSIM               
#        node_list=list(dict.fromkeys(node_list))                    
#        origin_list=list(set(node_list.copy())-set(list(node_d_count.keys())))
#        destination_list=list(set(node_list.copy())-set(list(node_o_count.keys())))          
#       
                
#        origin_list=['gneJ5','8851499-AddedOnRampNode','64226680','8853422#1-AddedOnRampNode','1190368509','64190138','1039725892','7606429243','cluster_1039818681_5796719989','cluster_5729084836_5730665989','gneJ37','gneJ47','gneJ33','cluster_1039748801_1039779011','gneJ22','gneJ17','7606429243','cluster_1039818681_5796719989','cluster_5729084836_5730665989','gneJ37','gneJ47','gneJ33','cluster_1039748801_1039779011','gneJ22','gneJ17']        
#        destination_list=['gneJ6','64207080','1039676797','4997534207','8849236#0-AddedOffRampNode','gneJ8','1039767895','1039690553','207114431#27-AddedOffRampNode','cluster_1039818681_5796719989','cluster_5729084836_5730665989','gneJ37','gneJ47','gneJ33','cluster_1039748801_1039779011','gneJ22','gneJ17','gneJ6','64207080','1039676797','4997534207','8849236#0-AddedOffRampNode','gneJ8','1039767895','1039690553']
#        origin_list_2=list(set(origin_list))   
#        destination_list_2=list(set(destination_list))        
        route=[]
        route_dir={}
        edge_route={}
        edge_routeIDs={}
        
        for edge in G.edges:
            edge_route[G[edge[0]][edge[1]]['id']]=[]
            edge_routeIDs[G[edge[0]][edge[1]]['id']]=[]
            print(G[edge[0]][edge[1]]['id'])
        
        route_n=0
        O_D_route_IDs={}
        D_route_IDs={}
        for origin in origin_list:
            D_route_IDs={}
            for destination in destination_list:
                if origin!=destination:
                    try:
                        path_node=nx.dijkstra_path(G,origin,destination,weight='length')
                    except :
                        continue
                    
                    route=[]                    
                    for i in range(0,len(path_node)-1):
                        node_start=path_node[i]
                        node_end=path_node[i+1]
                        
                        node_to_edge=G[node_start][node_end]
                                                             
                        
                        route.append(node_to_edge['id'])
                        
                  
                    correct_flag=1
                                                             ##此处一定要check 是否有的路径是不合法的
                                                             ## 万一生出来的路径不合法，某一些交叉口禁左怎么办？  
                    
                    for i in range(0,len(route)-1):
                        edge_A=route[i]
                        edge_B=route[i+1]
                        try:
                            connect_two_egde[edge_A][edge_B]
                        except KeyError:
                            correct_flag=0
#                            print(route)                   ## 完美
                            
                                         
                    if  correct_flag==0:
                        continue
                                        
                    route_ID='route'+str(route_n)    
                    route_dir[route_ID]=route
                    for edge in route:                        
                        edge_route[edge].append(route)
                        edge_routeIDs[edge].append(route_ID)
                        
                        
                    route_n=route_n+1
                    
                    D_route_IDs[destination]=route_ID
            O_D_route_IDs[origin]=D_route_IDs   
            
        cls.origin_list=origin_list
        cls.destination_list=destination_list
        cls.O_D_route_IDs=O_D_route_IDs
        
        
        cls.network=G
        cls.route_dir=route_dir
        cls.edge_route=edge_route
        cls.edge_routeIDs=edge_routeIDs

       
    @staticmethod
    def draw_network_node_ids(A,node_list):     #A.draw_network_node_ids(A,A.origin_list+A.destination_list)
        G=A.network        
        plt.figure(2,figsize=(18*0.393701, 18*0.393701), dpi=200, facecolor='w', edgecolor='k')
        
        for edge in G.edges:
            node_o=edge[0]
            node_d=edge[1]
         
            plt.plot([G.node[node_o]['x'],G.node[node_d]['x']],[G.node[node_o]['y'],G.node[node_d]['y']],color='g',linewidth=1)        
        for node in node_list:

            plt.plot(G.node[node]['x'],G.node[node]['y'],color='r',marker=".", markersize=10)
            text_x=G.node[node]['x']
            text_y=G.node[node]['y']
            

            node_id= G.node[node]['id']
            plt.text(text_x,text_y,node_id,fontsize=4)
            
        plt.xticks([])
        plt.yticks([])
        csfont = {'fontname':'Times New Roman'} 
        plt.title('OD nodes',**csfont)            
    @staticmethod
    def draw_OD_table_map(A):                 #A.draw_OD_table_map(A)
        
#        cls.origin_list=origin_list
#        cls.destination_list=destination_list
#        cls.O_D_route_IDs=O_D_route_IDs        
#        
        data=[]
        
        node_list=A.origin_list+A.destination_list
        node_list=list(set(node_list))
        for origin in node_list:
            data_list=[]
            for dest in node_list:
                
                try:
                    route_ID=A.O_D_route_IDs[origin][dest]
                    value=A.route_flow_list[route_ID]
                except KeyError:
                    value=0
                data_list.append(value)
            data.append(data_list)

        import numpy as np; 
        import seaborn as sns; 
        import matplotlib.pyplot as plt

        ax = sns.heatmap(data,yticklabels=node_list,xticklabels=node_list,cmap="Greens")
        plt.xticks(rotation=90) 
        plt.xlabel('Origin node IDs')
        plt.ylabel('Destination node IDs')
        plt.show()
    @staticmethod
    def opt_route_flow(G,edge_routeIDs,route_dir,edge_flow):    
        
        edge_list=list(edge_routeIDs.keys())
        route_list=list(route_dir.keys())

        ## generate edge_flow
        edge_flow={}
        for edge in edge_list:
            edge_flow[edge]=random.randint(100,300)

        
        
        route_edge_dataframe=pd.DataFrame(0,columns =edge_list,index=route_list)
        
        for edge in edge_list: ## 或许edge_flow.keys() is ok
            for route in edge_routeIDs[edge]:
                
                route_edge_dataframe[edge][route]=1
        #build empty matix        
        M_matix=route_edge_dataframe.to_dict('index')    
        
        m = pyomo.ConcreteModel()
        ##create_vars
        m.x = pyomo.Var(route_list, domain=pyomo.NonNegativeReals)
        m.err = pyomo.Var(edge_list, domain=pyomo.Reals)
        
        # objective
        total_err = sum(m.err[edge]*m.err[edge] for edge in edge_list) 
        m.obj= pyomo.Objective(expr = total_err, sense=pyomo.minimize)
                                        
        # constraints
        m.cons = pyomo.ConstraintList()
        for edge in edge_list:
            m.cons.add(sum(m.x[route]*M_matix[route][edge] for route in route_list)+ m.err[edge] == edge_flow[edge])
            
        # solve
        solver = pyomo.SolverFactory('ipopt') #cbc
        solver.solve(m)
        
        for edge in edge_list:
            print("edge_err:"+edge+' '+str(m.err[edge]()))
        
        route_flow_list={}
        
        for route in route_list:
            
            print("route_flow:"+route+' '+str(m.x[route]()))
            route_flow_list[route]=round(m.x[route]())
            
        
        
        edge_cal_flow={}
        for edge in edge_routeIDs:
            edge_cal_flow[edge]=0
            paths_set=edge_routeIDs[edge]
            for route in paths_set:
                edge_cal_flow[edge]=edge_cal_flow[edge]+route_flow_list[route]
     
        return route_flow_list,edge_cal_flow

    @classmethod
    def write_routes(cls,sumo_config_file_path,sumo_rou_name):
        
        tree = xml.etree.ElementTree.ElementTree()
        
        root = xml.etree.ElementTree.Element("routes")
        root.attrib['xmlns:xsi'] ="http://www.w3.org/2001/XMLSchema-instance"
        root.attrib['xsi:noNamespaceSchemaLocation']="http://sumo.dlr.de/xsd/routes_file.xsd"
        root.tail='\n    ' 
        root.text='\n    '  

#        edge_flow={}
#        detect_current=cls.detector_data.index.tolist()
#        
#        for detect_lane in detect_current:
#             edge=detect_lane.split('_')[0]
#             try:
#                edge_flow[edge]=edge_flow[edge]+cls.detector_data['traffic flow'][detect_lane]
#             except KeyError:
#                edge_flow[edge]=cls.detector_data['traffic flow'][detect_lane]
                  
        for route_ID in cls.route_dir.keys():
            
            new_element = xml.etree.ElementTree.SubElement(root,'route')
            new_element.attrib['edges'] =' '.join(cls.route_dir[route_ID]) 
            new_element.attrib['color'] = 'green'
            new_element.attrib['id']= route_ID
            new_element.tail='\n    '
        
        
        tree._setroot(root)
        
        tree.write(sumo_config_file_path+sumo_rou_name,encoding='utf-8', xml_declaration=True)                
        cls.new_rou_name=sumo_rou_name
        

          
    @classmethod
    def write_route_flow_detector_and_optimization(cls,sumo_config_file_path,sumo_rou_name):
        
        tree = xml.etree.ElementTree.ElementTree()
        
        root = xml.etree.ElementTree.Element("routes")
        root.attrib['xmlns:xsi'] ="http://www.w3.org/2001/XMLSchema-instance"
        root.attrib['xsi:noNamespaceSchemaLocation']="http://sumo.dlr.de/xsd/routes_file.xsd"
        root.tail='\n    ' 
        root.text='\n    '  

#        edge_flow={}
#        detect_current=cls.detector_data.index.tolist()
#        
#        for detect_lane in detect_current:
#             edge=detect_lane.split('_')[0]
#             try:
#                edge_flow[edge]=edge_flow[edge]+cls.detector_data['traffic flow'][detect_lane]
#             except KeyError:
#                edge_flow[edge]=cls.detector_data['traffic flow'][detect_lane]
                  
        edge_flow=cls.edge_flow
        route_flow_list={}    
        for route_ID in cls.route_dir.keys():
            
            new_element = xml.etree.ElementTree.SubElement(root,'route')
            new_element.attrib['edges'] =' '.join(cls.route_dir[route_ID]) 
            new_element.attrib['color'] = 'green'
            new_element.attrib['id']= route_ID
            new_element.tail='\n    '
        
            route_flow_list[route_ID]=[]
                   

        route_flow_list,edge_cal_flow=cls.opt_route_flow(cls.network,cls.edge_routeIDs,cls.route_dir,edge_flow)
        
        cls.route_flow_list=route_flow_list
        cls.edge_cal_flow=edge_cal_flow
        for route_ID in route_flow_list.keys():
            if route_flow_list[route_ID]<=0:
                route_flow_aver='10'
            else:
                route_flow_aver=str(route_flow_list[route_ID])
            
            
            new_element = xml.etree.ElementTree.SubElement(root,'flow')
            new_element.attrib['id']= 'flow'+route_ID   
            new_element.attrib['begin'] ="0.00" 
            
#            new_element.attrib['route'] =route_ID                           # flow 既可以只设置OD点 也可以设置 路径
                                                                            #设置路径的话可能遇到复杂交叉口没有实现，比如禁左
                                                                            #建议设置O点和D点
            new_element.attrib['from'] =cls.route_dir[route_ID][0]
            route_len=len(cls.route_dir[route_ID])
            new_element.attrib['to'] =cls.route_dir[route_ID][route_len-1]
            
            
            new_element.attrib['end'] ="3600.00"
            new_element.attrib['vehsPerHour'] =route_flow_aver
            new_element.attrib['departLane']="best"
            new_element.tail='\n    '
        
        tree._setroot(root)
        
        tree.write(sumo_config_file_path+sumo_rou_name,encoding='utf-8', xml_declaration=True)                
        cls.new_rou_name=sumo_rou_name
        
    @classmethod
    
    def random_edge_flow(cls):
        for edge in cls.edge_flow.keys():
            cls.edge_flow[edge]=random.randint(100,500)
 

    @classmethod
    def veh_generation_by_optimization(cls,sumo_config_file_path,sumo_rou_name,start_time,end_time):
        
                
        edge_flow=cls.edge_flow
        route_flow_list,edge_cal_flow=cls.opt_route_flow(cls.network,cls.edge_routeIDs,cls.route_dir,edge_flow)
        
        cls.route_flow_list=route_flow_list
        cls.edge_cal_flow=edge_cal_flow


        flag=1
        for time in range(start_time,end_time+1):            
            cls.veh_dir[time]=[]
                
        for route_ID in route_flow_list.keys():
            
            route_flow_aver=route_flow_list[route_ID]
            
            if route_flow_aver==0:
                    continue
                
#            max_veh_number=int((end_time-start_time)/5)  
#            veh_num=min(max_veh_number,route_flow_aver)              
            veh_num=route_flow_aver    
            for depart in np.linspace(start_time+(random.randint(0,50)), end_time-(random.randint(0,50)), num=veh_num):
                    
                    depart=int(depart)
                    vehicle_id= 'vehicle_'+route_ID+'_'+str(flag)+'_'+str(depart)  
                    depart_time=str(depart)
                    cls.veh_dir[depart].append(vehicle(vehicle_id,depart_time,route_ID))                    
            flag=flag+1    
        
        #------------write into rou.xml
        et = xml.etree.ElementTree.parse(sumo_config_file_path+sumo_rou_name)
        
        for veh_time in range(start_time,end_time):

            for veh in cls.veh_dir[veh_time]:
                
                new_element = xml.etree.ElementTree.SubElement(et.getroot(),'vehicle')
                new_element.attrib['id']= veh.veh_id 
                new_element.attrib['depart'] =str(veh.depart) 
                new_element.attrib['route'] =veh.route
                new_element.attrib['departLane']=veh.departLane
                new_element.tail='\n    '
                new_element.text='\n        '       
                
        et.write(sumo_config_file_path+sumo_rou_name)   
        
    @classmethod
    def write_configuration(cls,sumo_config_file_path,sumo_config_name,sumo_net_name,sumo_add_name,sumo_rou_name):


        tree = xml.etree.ElementTree.ElementTree()
        configuration = xml.etree.ElementTree.Element("configuration")
        configuration.attrib['xmlns:xsi'] ="http://www.w3.org/2001/XMLSchema-instance"
        configuration.attrib['xsi:noNamespaceSchemaLocation']="http://sumo.dlr.de/xsd/sumoConfiguration.xsd"
        configuration.tail='\n    ' 
        configuration.text='\n'  
#        
#        configuration=tree.getroot()
        
        input_element = xml.etree.ElementTree.SubElement(configuration,'input')
        
        net_file_element=xml.etree.ElementTree.SubElement(input_element,'net-file')
        route_files_element=xml.etree.ElementTree.SubElement(input_element,'route-files')
        additional_files_element=xml.etree.ElementTree.SubElement(input_element,'additional-files')
        
        net_file_element.attrib['value']="osm.net.xml" 
        route_files_element.attrib['value']=sumo_rou_name
        additional_files_element.attrib['value']=sumo_add_name
        
        net_file_element.tail='\n'
        route_files_element.tail='\n'
        additional_files_element.tail='\n'

#        net_file_element.text='\n    '
#        route_files_element.text='\n    '
#        additional_files_element.text='\n    '
#        
        input_element.text='\n'
        input_element.tail='\n'
        
        new_element = xml.etree.ElementTree.Element('processing')
        new_element.text='\n    '
        new_element.tail='\n'
             
        processing_config=xml.etree.ElementTree.SubElement(new_element,'ignore-route-errors')
        processing_config.attrib['value']="true"
        processing_config.tail='\n'
             
        configuration.append(new_element)  
        
        
        new_element = xml.etree.ElementTree.Element('routing')
        new_element.tail='\n'
             
        routing_config=xml.etree.ElementTree.SubElement(new_element,'device.rerouting.adaptation-steps')
        routing_config.attrib['value']="180"
        routing_config.tail='\n'
             
             
        report_config=xml.etree.ElementTree.SubElement(new_element,'verbose')
        report_config.attrib['value']="true"
        report_config.tail='\n'

        duration_report_config=xml.etree.ElementTree.SubElement(new_element,'duration-log.statistics')
        duration_report_config.attrib['value']="true"
        duration_report_config.tail='\n'

        step_report_config=xml.etree.ElementTree.SubElement(new_element,'no-step-log')
        step_report_config.attrib['value']="true"
        step_report_config.tail='\n'
             
        configuration.append(new_element) 
        tree._setroot(configuration)
        
        tree.write(sumo_config_file_path+sumo_config_name)
        
class  simulation():
    def __init__(self,simulation_time,simulation_interval):
        self.simulation_time=simulation_time
        self.simulation_interval=simulation_interval
    def simulation_process_Real_time_gengerated_Vehs_by_detector_data(self,traci,demand_gen,sumo_config_file_path,sumo_rou_name,sumo_add_name,sumo_config_name):
        time=0
        start_time=0
        end_time=self.simulation_interval
        
        
        while time < self.simulation_time:
           time += self.simulation_interval

           end_time=time
           start_time=time-self.simulation_interval
           
           demand_gen.random_edge_flow()
           demand_gen.veh_generation_by_optimization(sumo_config_file_path,sumo_rou_name,start_time,end_time)
           
           for veh_time in range(start_time,end_time):
               for veh in demand_gen.veh_dir[veh_time]:
                   traci.vehicle.add(veh.veh_id,veh.route,depart=veh.depart,departLane=veh.departLane)
           traci.simulationStep(time)
        traci.close()           
    
    def simulation_process_by_fun(self,traci,fun,*fun_input):  # 如果的多个输入，写成tuple (input1,input2)
        time=0
        
        while time < self.simulation_time:
           time += self.simulation_interval
           traci.simulationStep(time)
           fun(*fun_input)
        traci.close()

