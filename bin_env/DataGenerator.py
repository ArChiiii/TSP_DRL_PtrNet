

from dataclasses import asdict
import datetime
import json
from MapperData import BoxInfo
import numpy as np
import random
import math
import sys
sys.path.append("../")


def convertDict(box):
    returnDict = {}
    returnDict["height"] = int(box.height)
    returnDict["width"] = int(box.width)

    return returnDict


class RandomSizeGenerator():

    def __init__(self, minWidth,  maxWidth, maxAspectRatioDeviationPercentage, amount):
        self.minWidth = minWidth
        self.maxWidth = maxWidth
        # If this is 70, than Height will be 30% to 170% of Width
        self.maxAspectRatioDeviationPercentage = maxAspectRatioDeviationPercentage
        self.amount = amount
        pass

    def generate(self, save=False):
        boxes = np.random.randint(
            low=self.minWidth, high=self.maxWidth, size=self.amount)
        boxesDictArray = []
        for box in boxes:

            width = box
            height = random.randint(math.floor(width*(100-self.maxAspectRatioDeviationPercentage)/100),
                                    math.ceil(width*(100+self.maxAspectRatioDeviationPercentage)/100))
            box = BoxInfo(height, width)
            boxesDictArray.append(box)

        print("Init boxes:")
        print(boxesDictArray)

        if save:
            info = {}
            info["minWidth"] = self.minWidth
            info["maxWidth"] = self.maxWidth
            info["maxAspectRatioDeviationPercentage"] = self.maxAspectRatioDeviationPercentage
            info["amount"] = self.amount
            info["boxes"] = list(map(convertDict, boxesDictArray))

            jsonString = json.dumps(info)
            datetimestr = datetime.datetime.now().strftime("%Y-%m-%d-%H%M")
            with open(f"../boxData/{datetimestr}.json", "w") as f:
                f.write(jsonString)

        return boxesDictArray


class PartitionGenerator():
    def __init__(self, minWidth,  maxWidth, maxAspectRatioDeviationPercentage, containerheight=100, containerwidth=100):
        self.minWidth = minWidth
        self.maxWidth = maxWidth
        # If this is 70, than Height will be 30% to 170% of Width
        self.minHeight = minWidth * (1-maxAspectRatioDeviationPercentage/100)
        self.maxHeight = maxWidth * (1+maxAspectRatioDeviationPercentage/100)
        self.containerheight = containerheight
        self.containerwidth = containerwidth
        self.hratio = containerheight / 100
        self.wratio = containerheight / 100

        self.array2D = np.zeros((containerheight, containerwidth), dtype=bool)

        self.nextEmptySpace = {"x": 0, "y": 0}

    def generate(self, save=False):

        boxesDictArray = []

        lastbox = None

        while self.max_x < 100 or self.max_y < 100:
            width = random.randint(self.minWidth, self.maxWidth)
            height = random.randint(self.minHeight, self.maxHeight)
            box = BoxInfo(height, width)

            if lastbox is None:
                boxesDictArray.append(box)
                self.max_x = width
                self.max_y = height

                lastbox = box

            elif self.max_x + width < 100:
                boxesDictArray.append(box)
                self.max_x = self.max_x + width

        return boxesDictArray


if __name__ == "__main__":
    r = RandomSizeGenerator(10, 50, 60, 20)
    result = r.generate()
    print(result)
