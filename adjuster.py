def adjust_axes(val, adj_x=1, adj_y=1):
    x, y = adj_x, adj_y
    if x == 0:
        if val == 0:
            return 0
        if val > 0:
            return y
        if val < 0:
            return -y
    if x == 1:
        if val == -1:
            return -1
        if val == 1:
            return 1
        if val > -x and val < x:
            return y*val
    if y == 0:
        if val >= -1 and val < -x:
            return 1/(1-x)*val+x/(1-x)
        if val >= -x and val <= x:
            return 0
        if val > x and val <= 1:
            return 1/(1-x)*val-x/(1-x)
    if y == 1:
        if val >= -1 and val < -x:
            return -1
        if val >= -x and val <= x:
            return y/x*val
        if val > x and val <= 1:
            return 1
    else:
        if val >= -1 and val < -x:
            return (y-1)/(x-1)*val-(x-y)/(x-1)
        if val >= -x and val <= x:
            return y/x*val
        if val > x and val <= 1:
            return (y-1)/(x-1)*val+(x-y)/(x-1)

    
def steer_val(val, center_y=1, peak_y=-1):
    if center_y == peak_y:
        return center_y
    else:
        px = (1-center_y)/(center_y-peak_y)
        if val <-1 or val >1:
            print("steer_val error")
            return None
        elif val < px and val > -1:
            return center_y+val*(center_y-peak_y)
        elif val == -1:
            return -1
        else:
            return 1
        
def steer2_val(val, adj_x=0.2, peak_y1=1, peak_y2=-1):
    if val > adj_x and val <=1:
        return peak_y1
    elif val>=-adj_x and val <= adj_x:
        return 1
    elif val<-adj_x and val >=-1:
        return peak_y2

def steer_trans1(axesX, axesY):
    if axesX == 0:
        trans_set_1 = trans_set_2 = axesY
    elif axesX < 0:
        if axesY == 0:
            trans_set_1 = axesX
            trans_set_2 = -axesX
        elif axesY > 0:
            trans_set_1 = axesX
            trans_set_2 = axesY - 1
        elif axesY < 0:
            trans_set_1 = axesY + 1
            trans_set_2 = -axesX
    elif axesX >0:
        if axesY == 0:
            trans_set_1 = -axesX
            trans_set_2 = axesX
        elif axesY > 0:
            trans_set_1 = axesY - 1
            trans_set_2 = axesX
        elif axesY < 0:
            trans_set_1 = -axesX
            trans_set_2 = axesY + 1
    return trans_set_1, trans_set_2

def steer_trans2(axesX, axesY):
    if axesX == 0:
        trans_set_1 = trans_set_2 = axesY
    elif axesX < 0:
        if axesY == 0:
            trans_set_1 = 1
            trans_set_2 = -1
        elif axesY > 0:
            trans_set_1 = 1
            trans_set_2 = axesY - 1
        elif axesY < 0:
            trans_set_1 = axesY + 1
            trans_set_2 = -1
    elif axesX >0:
        if axesY == 0:
            trans_set_1 = -1
            trans_set_2 = 1
        elif axesY > 0:
            trans_set_1 = axesY - 1
            trans_set_2 = 1
        elif axesY < 0:
            trans_set_1 = -1
            trans_set_2 = axesY + 1
    return trans_set_1, trans_set_2

def steer_trans(axesX, axesY):
    return move_coordinate(point=(axesX, axesY), move_index=(0,0), turn_degree=45)