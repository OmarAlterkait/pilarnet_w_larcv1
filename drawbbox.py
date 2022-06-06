import os,sys

class DrawBBox:
    def __init__(self, meta3d, draw_voxels=False ):

        if draw_voxels:
            self.tpc = [[0,meta3d.num_voxel_x()],
                        [0,meta3d.num_voxel_y()],
                        [0,meta3d.num_voxel_z()]]
        else:
            self.tpc = [[meta3d.min_x(),meta3d.max_x()],
                        [meta3d.min_y(),meta3d.max_y()],
                        [meta3d.min_z(),meta3d.max_z()]]
            

        self.top_pts  = [ [self.tpc[0][0],self.tpc[1][1], self.tpc[2][0]],
                          [self.tpc[0][1],self.tpc[1][1], self.tpc[2][0]],
                          [self.tpc[0][1],self.tpc[1][1], self.tpc[2][1]],
                          [self.tpc[0][0],self.tpc[1][1], self.tpc[2][1]],
                          [self.tpc[0][0],self.tpc[1][1], self.tpc[2][0]] ]
        self.bot_pts  = [ [self.tpc[0][0],self.tpc[1][0], self.tpc[2][0]],
                          [self.tpc[0][1],self.tpc[1][0], self.tpc[2][0]],
                          [self.tpc[0][1],self.tpc[1][0], self.tpc[2][1]],
                          [self.tpc[0][0],self.tpc[1][0], self.tpc[2][1]],
                          [self.tpc[0][0],self.tpc[1][0], self.tpc[2][0]] ]
        self.up_pts   = [ [self.tpc[0][0],self.tpc[1][0], self.tpc[2][0]],
                          [self.tpc[0][1],self.tpc[1][0], self.tpc[2][0]],
                          [self.tpc[0][1],self.tpc[1][1], self.tpc[2][0]],
                          [self.tpc[0][0],self.tpc[1][1], self.tpc[2][0]],
                          [self.tpc[0][0],self.tpc[1][0], self.tpc[2][0]] ]
        self.down_pts = [ [self.tpc[0][0],self.tpc[1][0], self.tpc[2][1]],
                          [self.tpc[0][1],self.tpc[1][0], self.tpc[2][1]],
                          [self.tpc[0][1],self.tpc[1][1], self.tpc[2][1]],
                          [self.tpc[0][0],self.tpc[1][1], self.tpc[2][1]],
                          [self.tpc[0][0],self.tpc[1][0], self.tpc[2][1]] ]
                
    def getlines(self,color=(255,255,255)):

        # top boundary
        Xe = []
        Ye = []
        Ze = []

        for boundary in [self.top_pts, self.bot_pts, self.up_pts, self.down_pts]:
            for ipt, pt in enumerate(boundary):
                Xe.append( pt[0] )
                Ye.append( pt[1] )
                Ze.append( pt[2] )
            Xe.append(None)
            Ye.append(None)
            Ze.append(None)
        
        
        # define the lines to be plotted
        lines = {
            "type": "scatter3d",
            "x": Xe,
            "y": Ye,
            "z": Ze,
            "mode": "lines",
            "name": "",
            "line": {"color": "rgb(%d,%d,%d)"%color, "width": 5},
        }
        
        return [lines]

                
