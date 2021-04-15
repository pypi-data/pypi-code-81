#from geopy.distance import geodesic
from   scipy.spatial.distance       import cdist
    
def find_nearest(coords,path_coords):
    distance_matrix=cdist(coords,path_coords)
    return distance_matrix


def path_segmenting(coords,path_coords):
    distance_matrix=find_nearest(coords,path_coords)
    index=[distance_row.argmin() for distance_row in distance_matrix]
    index_pairs=tuple(zip(index,index[1:]))
    #print(path_coords)
    paths=[path_coords[pair[0]:pair[1]+1] for pair in index_pairs]
    return paths[0]



if __name__ == '__main__':

    lat_path=[0,0.1,0.5,1,1.5,2,3]
    long_path=list(lat_path)
    path_coords=list(zip(lat_path,long_path))
    lat=[0,1]
    long=list(lat)
    coords=list(zip(lat,long))
    distance_matrix=find_nearest(coords,path_coords)
    result=path_segmenting(coords,path_coords)
    #print(result)
    
