# %%
from render import renderContainer2DData
#from PolicyHandler import PolicyHandler
import numpy as np
from MapperData import BoxInfo, MappedBoxInfo
import random
import copy
import sys
#import matplotlib.pyplot as plt
# sys.path.append("../")


class Container2D:
    def __init__(self, remainingBoxes, height, width):
        self.height = height
        self.width = width
        self.array2D = np.zeros((height, width), dtype=bool)
        self.recLocations = []
        self.remainingBoxes = remainingBoxes
        self.noActions = []

        self.Container2DData = {}
        self.Container2DData["dimensions"] = {}
        self.Container2DData["dimensions"]["width"] = width
        self.Container2DData["dimensions"]["height"] = height

        self.nextEmptySpace = {"x": 0, "y": 0}
        self.nextBaseSpace = {"x": width, "y": 0}
        self.nextNeighborSpaces = {"right": None, "top": None, "only": None}

    def placeRectangle(self, x, y, box):

        self.array2D[y:y+box.height, x:x+box.width] = True
        self.recLocations.append(MappedBoxInfo(x, y, box))

        self.Container2DData["boxes"] = self.recLocations

        #print(f"Placed box(h:{box.height}, w:{box.width}) at ({x},{y})")

    def placeRectangle_seq(box):
        isAdded = False

        return isAdded

    def isAvailable(self, x, y, recHeight, recWidth):
        for i in range(x, x+recWidth):
            for j in range(y, y+recHeight):
                if self.array2D[j, i]:
                    return False

        return True

    def getRemainingBoxes(self):
        return self.remainingBoxes

    def getLegalMoves(self, box):
        actions = []
        requiredWidth = box.width
        requiredHeight = box.height

        if requiredHeight > self.height or requiredWidth > self.width:
            return []

        legalMoveArray = copy.deepcopy(self.array2D)
        #plt.imshow(legalMoveArray, cmap=plt.get_cmap('gray'))

        for placedBox in self.recLocations:

            boxInfo = placedBox.boxInfo
            locX = placedBox.x
            locY = placedBox.y

            locXw = locX + boxInfo.width
            locYh = locY + boxInfo.height

            padding_locX = locX - requiredWidth + 1 if locX - requiredWidth + 1 >= 0 else 0
            padding_locY = locY - requiredHeight + 1 if locY - requiredHeight + 1 >= 0 else 0

            legalMoveArray[padding_locY:locYh, padding_locX:locXw] = True

        # handle the edge
        legalMoveArray[0:self.height, self.width -
                       requiredWidth+1:self.width] = True
        legalMoveArray[self.height-requiredHeight +
                       1:self.height, 0:self.width] = True

        #plt.imshow(legalMoveArray, cmap=plt.get_cmap('gray'))

        actions = np.argwhere(legalMoveArray == False).tolist()

        # for ix,iy in np.ndindex(self.array2D.shape):

        #     if self.array2D[ix,iy]:
        #         continue
        #     if iy+box.height >=  self.height or ix+box.width >= self.width:
        #         continue
        #     if (self.array2D[iy:iy+box.height,ix:ix+box.width] == 1).sum() >0:
        #         continue

        #     actions.append((ix,iy))

        return actions

    def isOver(self):
        random.shuffle(self.remainingBoxes)
        for box in self.remainingBoxes:
            if len(self.getLegalMoves(box)) > 0:
                return False

        self.Container2DData["boxes"] = self.recLocations
        renderContainer2DData(self.Container2DData)

        return True

    def appendNoAction(self, box):
        self.noActions.append(box)

    def removeBox(self, box):
        self.remainingBoxes.remove(box)

    def evaluate(self):
        return len(self.recLocations)


if __name__ == "__main__":
    boxlist = [BoxInfo(20, 30), BoxInfo(25, 35), BoxInfo(10, 50), BoxInfo(
        20, 5), BoxInfo(20, 30), BoxInfo(5, 30), BoxInfo(5, 35), BoxInfo(36, 39), BoxInfo(56, 23), BoxInfo(11, 36), BoxInfo(36, 11), BoxInfo(26, 27), BoxInfo(9, 27)]

    c = Container2D(boxlist, 100, 100)
    boxes = c.getRemainingBoxes()

    actionlist = []

    for b in boxes:
        action = c.getLegalMoves(b)
        # actionlist.append(action)

    #p = PolicyHandler()
    #box, (y, x) = p.pick(c)
        (y, x) = action[0]
        c.placeRectangle(x, y, b)

    # for b in boxes:
        #action = c.getLegalMoves(b)
        # print(action)

        renderContainer2DData(c.Container2DData)

# %%
