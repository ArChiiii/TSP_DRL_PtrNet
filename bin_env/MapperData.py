

from dataclasses import dataclass
from typing import List
from enum import Enum


class IterationResult(Enum):
    Success = 1
    Failure = 2
    BiggerThanBestContainer = 3
    SmallerThanCombinedImages = 4



@dataclass
class ContainerStats():
    rectangleAddAttempts: int
    nbrCellsGenerated: int
    lowestFreeHeightDeficit: int



@dataclass(order=True)
class BoxInfo():
    height: int
    width: int

@dataclass
class MappedBoxInfo():
    x: int
    y: int
    boxInfo: BoxInfo

@dataclass
class IterationStats():
    result: IterationResult
    maxContainerWidth: int
    maxContainerHeight: int
    intermediateSpriteWidth: int
    intermediateSpriteHeight: int
    boxDetails: List[MappedBoxInfo]
