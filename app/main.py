from fastapi import FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse
from app.geocoder.geocoder import Geocoder
import pandas as pd
from .schemas import ItemRequest, ItemResponse

app = FastAPI()
data_df = pd.DataFrame(columns=['id', 'text', 'Location', 'geometry'])
ids = 0

@app.get('/')
def root():
    return {'message': 'Hello! Give me any text with geo subject and i will tell you where is it'}

@app.get('/items/all', response_model=ItemResponse)
def get_all_items():
    if data_df.empty:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No items found')
    return HTMLResponse(data_df.to_html(), status_code=200)

@app.get('/items', response_model=ItemResponse)
def get_item(item_id: int):
    try:
        result = data_df[(data_df['id'] == item_id)]
        return HTMLResponse(result.to_html(), status_code=200)
    except IndexError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No item found')
    
@app.post('/items', response_model=ItemRequest)
def find_Nevsky(text_ent: str):
    global data_df, ids
    data = pd.DataFrame({
        'id': ids,
        'text': text_ent,
    }, index=[0]) 
    osm_id = 337422 # Saint Petersburg
    geocoder = Geocoder(data, osm_id=osm_id, city_tags={'place':['state']}, text_column_name='text')
    result = geocoder.run(group_column=None)
    if  result.empty:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Geo not found')
    data_df = pd.concat([data_df, result[['id', 'text', 'Location', 'geometry']].head(1)], ignore_index=True)
    ids += 1
    return HTMLResponse(result.to_html(), status_code=200)

@app.delete('/delete/items', response_model=ItemResponse)
def delete_items(item_id: int):
    global data_df
    if data_df.empty or item_id not in data_df['id'].values:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')
    data_df = data_df[data_df['id'] != item_id].reset_index(drop=True)
    return {'message': f'Item with id {item_id} deleted successfully'}
