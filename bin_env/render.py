import plotly.io as pio
import plotly.graph_objects as go
from dataclasses import asdict


def getBoxPlotDef(start, dimensions, color, width, height):
    # 8 vertices of a cube
    x = [start["x"], start["x"], start["x"] +
         dimensions["width"], start["x"] + dimensions["width"], ]
    y = [height - start["y"], height - (start["y"] + dimensions["height"]),
         height - (start["y"] + dimensions["height"]), height-start["y"]]

    boxDef = go.Scatter(
        x=x,
        y=y,
        fillcolor=color,
        # i, j and k give the vertices of triangles
        fill="toself",
        mode='markers'
    )

    return boxDef


def renderContainer2DData(Container2DData, renderer="vscode"):
    data = []

    pio.renderers.default = renderer

    x = [0, 0, Container2DData["dimensions"]["width"],
         Container2DData["dimensions"]["width"], 0]
    y = [0, Container2DData["dimensions"]["height"],
         Container2DData["dimensions"]["height"], 0, 0]

    boxDef = go.Scatter(
        x=x,
        y=y,
        mode='lines'
    )
    data.append(boxDef)

    cnt = 1
    colorCode = 165498
    for boxData in Container2DData["boxes"]:
        box = boxData.boxInfo
        #location = boxData["location"]
        color = f"#{colorCode}"
        #''.join([random.choice('0123456789ABCDEF') for j in range(6)])

        location = {
            "y": boxData.y,
            "x": boxData.x
        }

        data.append(getBoxPlotDef(location, asdict(
            box), color, Container2DData["dimensions"]["width"], Container2DData["dimensions"]["height"]))
        cnt = cnt + 1

        colorCode += box.width

    fig = go.Figure(data=data)

    # camera = dict(
    #     up=dict(x=0, y=1, z=0),
    #     center=dict(x=0, y=0, z=0),
    #     eye=dict(x=-2, y=1, z=-2)
    # )

    fig['layout'].update(
        title="XY Plane"
    )

    fig.show()
