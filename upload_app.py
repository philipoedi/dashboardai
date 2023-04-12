import dash
import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__)
app.layout = html.Div(
    [
        dcc.Upload(
            id="upload-data",
            children=html.Div(["Drag and Drop or ", html.A("Select Files")]),
            style={
                "width": "50%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px",
            },
            multiple=True,
        ),
        html.Div(id="output-data-upload"),
    ]
)


@app.callback(
    Output("output-data-upload", "children"),
    Input("upload-data", "contents"),
    State("upload-data", "filename"),
)
def update_output(contents, filename):
    if contents is None:
        return html.Div(["No file selected"])
    else:
        import pdb

        pdb.set_trace()
    data = pd.read_csv(contents)
    return html.Div(
        [
            html.H5(filename),
            html.Br(),
            html.Table(
                [
                    html.Thead(html.Tr([html.Th(col) for col in data.columns])),
                    html.Tbody(
                        [
                            html.Tr(
                                [html.Td(data.iloc[i][col]) for col in data.columns]
                            )
                            for i in range(len(data))
                        ]
                    ),
                ]
            ),
        ]
    )


if __name__ == "__main__":
    app.run_server(debug=True)
