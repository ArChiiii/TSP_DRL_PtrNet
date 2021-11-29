

from DynamicTwoDimensionalArray import DynamicTwoDimensionalArray
from MapperData import ContainerStats
from ContainerCell import ContainerCell


class Container ():
    def __init__(self):
        self.width =0
        self.heigh =0
        self.nbrRectangleAddAttempts = 0
        self.nbrCellsGenerated = 0
        self.lowestFreeHeightDeficitSinceLastRedim = 999999

    def setCanvasDimensions (self, width, height):
        initialCapacityX = 25
        initialCapacityY = 25


        self.containerCells = DynamicTwoDimensionalArray(initialCapacityX,initialCapacityY, width, height,ContainerCell(False))

        self.width =width
        self.height =height
    
    def addRectangle (self, rectangleWidth,rectangleHeight):
        
        rectangleXOffset,rectangleYOffset = 0,0
        lowestFreeHeightDeficit = 9999999

        requiredWidth = rectangleWidth
        requiredHeight = rectangleHeight

        self.nbrRectangleAddAttempts+=1

        x ,y, offsetX, offsetY= 0 ,0,0,0
        rectangleWasPlaced = False
        nbrRows = self.containerCells.nbrRows


        while(True):

            while y< nbrRows and self.containerCells.item(x,y) is not None and self.containerCells.item(x,y).occupied:
                offsetY += self.containerCells.rowHeight(y)
                y += 1
            
            #found an unoccupied cell , see if can place a rectangle 
            freeHeightDeficit = self.freeHeightDeficit(self.height,offsetY,requiredHeight)
            if y< nbrRows and freeHeightDeficit<=0:
                isAvailable, nbrRequiredCellsHorizontally, nbrRequiredCellsVertically, leftOverWidth, leftOverHeight = self.isAvailable(x,y,requiredWidth,requiredHeight)
                if (isAvailable):
                    self.placeRectangle(x,y,nbrRequiredCellsHorizontally, nbrRequiredCellsVertically, leftOverWidth, leftOverHeight)

                    rectangleXOffset = offsetX
                    rectangleYOffset = offsetY
                    rectangleWasPlaced = True

                    break
            
                offsetY += self.containerCells.rowHeight(y)
                y += 1

            if freeHeightDeficit > 0:
                offsetY = 0
                y = 0
                offsetX += self.containerCells.columnWidth(x)
                x += 1

                '''if the rectangle could not be placed at this column
                    // because of insufficient horizontal space, than this update should not be made
                    

                    checking for sufficient horizontal width takes a lot of CPU ticks

                    this far outstrips the gains through having fewer failed sprite generations
                    
                '''

                if self.lowestFreeHeightDeficitSinceLastRedim > freeHeightDeficit:
                    self.lowestFreeHeightDeficitSinceLastRedim = freeHeightDeficit

            if self.width - offsetX < requiredWidth:
                rectangleWasPlaced = False
                break
                
        lowestFreeHeightDeficit = self.lowestFreeHeightDeficitSinceLastRedim

        return rectangleWasPlaced, rectangleXOffset, rectangleYOffset, lowestFreeHeightDeficit


    def freeHeightDeficit (self, containerHeight, offsetY, requiredHeight):
        spaceLeftVertically = containerHeight - offsetY
        freeHeightDeficit = requiredHeight - spaceLeftVertically
        return freeHeightDeficit

    def isAvailable (self, x,y, requiredWidth,requiredHeight):
    
        foundWidth = 0
        foundHeight = 0
        trialX = x
        trialY = y

        #Check all cells that need to be unoccupied for there to be room for the rectangle.

        while (foundHeight < requiredHeight):
            trialX = x
            foundWidth = 0

            while (foundWidth < requiredWidth):
            
                if (self.containerCells.item(trialX, trialY) is not None and self.containerCells.item(trialX, trialY).occupied):
                    return False, None, None, None, None
        
                foundWidth += self.containerCells.columnWidth(trialX)
                trialX+=1
            
            foundHeight += self.containerCells.rowHeight(trialY)
            trialY+=1

        '''
        
        Visited all cells that we'll need to place the rectangle,
        and none were occupied. So the space is available here.
        '''

        nbrRequiredCellsHorizontally = trialX - x
        nbrRequiredCellsVertically = trialY - y

        leftOverWidth = (foundWidth - requiredWidth)
        leftOverHeight = (foundHeight - requiredHeight)


        return True, nbrRequiredCellsHorizontally, nbrRequiredCellsVertically, leftOverWidth, leftOverHeight


    def placeRectangle(self, x,y, nbrRequiredCellsHorizontally, nbrRequiredCellsVertically, leftOverWidth, leftOverHeight):
        if leftOverWidth > 0:
            self.nbrCellsGenerated += self.containerCells.nbrRows

            xFarRightColumn = x + nbrRequiredCellsHorizontally - 1
            self.containerCells.insertColumn(xFarRightColumn, leftOverWidth)
            

        if leftOverHeight > 0:
            self.nbrCellsGenerated += self.containerCells.nbrColumns
            yFarBottomColumn = y + nbrRequiredCellsVertically - 1
            self.containerCells.insertRow(yFarBottomColumn, leftOverHeight)

        for i in reversed(range(x, x + nbrRequiredCellsHorizontally)):
            for j in reversed(range(y, y + nbrRequiredCellsVertically)):
                self.containerCells.setitem(i, j, ContainerCell(True))

    def getStatistics(self):
        return ContainerStats(self.nbrCellsGenerated, self.nbrRectangleAddAttempts, self.lowestFreeHeightDeficitSinceLastRedim)