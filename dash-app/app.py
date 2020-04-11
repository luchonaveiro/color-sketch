import base64
import io
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_reusable_components as drc
from dash.dependencies import Input, Output, State
import json
import numpy as np
import datetime
import requests
from PIL import Image
import numpy as np


group_colors = {"control": "light blue", "reference": "red"}

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server

# App Layout
app.layout = html.Div(
    children=[
        # Top Banner
        html.Div(
            className="study-browser-banner row",
            children=[
                html.H2(className="h2-title", children="AI PAINTING"),
                html.Div(
                    className="div-logo",
                    children=html.Img(
                        #className="logo", src=app.get_asset_url("iunigo_blanco.png")
                    ),
                ),
                html.H2(className="h2-title-mobile", children="AI PAINTING"),
            ],
        ),
        # Body of the App
        html.Div(
            className="row app-body",
            children=[
                # User Controls
                html.Div(
                    className="six columns card",
                    children=[
                        html.Div(
                            className="bg-white user-control",
                            children=[
                                html.Div(
                                    className="padding-top-bot",
                                    children=[
                                        html.H4('Select Black and White Sketch to paint:'),
                                        html.Br(),
                                        dcc.Upload(html.Button('Upload Image', id='upload_image'), id='image_path'),
                                        html.Br(),
                                        html.Img(id='image')
                                    ],
                                ),
                            ],
                        )
                    ],
                ),
                # Resultados
                html.Div(
                    className="six columns card-left",
                    children=[
                        html.Div(
                            className="bg-white",
                            children=[
                                html.H4("Image Painted"),
                                html.Br(),
                                html.Br(),
                                html.Br(),
                                html.Br(),
                                dcc.Loading(id="loading-1", children=[html.Img(id='image_painted')], type="default"),
                            ],
                        )
                    ],
                ),
            ],
        ),
    ]
)

# Callbacks
@app.callback(
    Output(component_id='image', component_property='src'),
    [Input('image_path', 'contents')],
    state=[State(component_id='image_path', component_property='contents')]
)
def update_image(content, input_1):
    if content != None:
        string = input_1.split(';base64,')[-1]
        im_pil = drc.b64_to_pil(string)
        im_pil = im_pil.resize((300, 300), Image.ANTIALIAS)
        enc_img = drc.pil_to_b64(im_pil)
        
        return 'data:image/png;base64, ' + enc_img


@app.callback(
    Output(component_id='image_painted', component_property='src'),
    [Input('image_path', 'contents')],
    state=[State(component_id='image_path', component_property='contents')]
)
def update_image(contents, input_1):
    if contents != None:
        string = input_1.split(';base64,')[-1]
        im_pil = drc.b64_to_pil(string)
        im_pil = im_pil.resize((128, 128), Image.ANTIALIAS)
        if im_pil.mode != "RGB":
            im_pil = im_pil.convert("RGB")

        # Convert image to numpy array
        img_array = np.asarray(im_pil)
        img_array = (img_array - 127.5) / 127.5
        img2 = img_array
        #img2 = np.zeros((img_array.shape[0],img_array.shape[1],3))
        #img2[:,:,0] = img_array
        #img2[:,:,1] = img_array
        #img2[:,:,2] = img_array

        # Create payload
        payload = {'instances': [img2.tolist()]}

        # Predict image
        #res = requests.post('http://localhost:8080/v1/models/color_sketch_model:predict', json=payload)
        res = requests.post('http://color-sketch_model-development_1:8080/v1/models/color_sketch_model:predict', json=payload)
        res = res.json()
        res = res['predictions'][0]
        res = ((np.array(res) + 1)/2.0)*255.0

        # Encode prediction
        pred_pil = Image.fromarray(np.uint8(res))
        pred_pil = pred_pil.resize((300, 300), Image.ANTIALIAS)
        enc_pred = drc.pil_to_b64(pred_pil)
        
        return 'data:image/png;base64, ' + enc_pred


if __name__ == "__main__":
    app.run_server(debug=False, host='0.0.0.0', port=8050)