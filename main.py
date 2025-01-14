from fastapi import FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse
from geocoder.geocoder import Geocoder
from IPython.core.display import HTML
import pandas as pd

app = FastAPI()
data_df = pd.DataFrame(columns=['id', 'text', 'Location', 'geometry'])
ids = 0

@app.get('/')
def root():
    return {'message': 'Hello! Give me any text with geo subject and i will tell you where is it'}

@app.get('/items')
def get_item(item_id: int):
    try:
        map_html = data_df.iloc[item_id].explore(tiles='cartodbdark_matter', marker_kwds={'radius': 10})._repr_html_()
        return HTMLResponse(content=map_html, status_code=200)
    except IndexError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='no item found')
    
@app.post('/items')
def find_Nevsky(text_ent: str):
    global data_df, ids
    data = pd.DataFrame({
        'id': ids,
        'text': text_ent,
    }, index=[0]) 
    osm_id = 337422 # Saint Petersburg
    geocoder = Geocoder(data, osm_id=osm_id, city_tags={'place':['state']}, text_column_name='text')
    result = geocoder.run(group_column=None)
    data_df = pd.concat([data_df, result[['id', 'text', 'Location', 'geometry']].head(1)], ignore_index=True)
    ids += 1
    map_html = result.explore(tiles='cartodbdark_matter', marker_kwds={'radius': 10})._repr_html_()
    return HTMLResponse(content=map_html, status_code=200)