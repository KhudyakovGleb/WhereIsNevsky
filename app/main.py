from fastapi import FastAPI, HTTPException, status
import pandas as pd
from fastapi.responses import HTMLResponse
from app.geocoder.geocoder import Geocoder
from shapely.wkt import dumps
import psycopg2
from .schemas import ItemRequest, ItemResponse

app = FastAPI()

conn = psycopg2.connect(dbname="nevskiy_db", user="user", password="password", host="postgres", port="5432")
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS nevskiy_db (
  id SERIAL PRIMARY KEY,
  text VARCHAR(255) NOT NULL,
  location VARCHAR(255),
  geometry VARCHAR(255)
);
''')

conn.commit()

@app.get('/')
def root():
    return {'message': 'Hello! Give me any text with geo subject and i will tell you where is it'}

@app.get('/items/all', response_model=ItemResponse)
def get_all_items():
    cur.execute('SELECT * FROM nevskiy_db')
    rows = cur.fetchall()
    if not rows:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No items found')
    return HTMLResponse(pd.DataFrame(rows, columns=['id', 'text', 'location', 'geometry']).to_html(), status_code=200)

@app.get('/items', response_model=ItemResponse)
def get_item(item_id: int):
    cur.execute('SELECT * FROM nevskiy_db WHERE id = %s', (item_id,))
    row = cur.fetchone()
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No item found')
    return HTMLResponse(pd.DataFrame([row], columns=['id', 'text', 'location', 'geometry']).to_html(), status_code=200)

@app.post('/items', response_model=ItemResponse)
def find_Nevsky(text_ent: str):
    global ids
    data = pd.DataFrame({
        'text': [text_ent],
    }) 
    
    osm_id = 337422  # Saint Petersburg
    geocoder = Geocoder(data, osm_id=osm_id, city_tags={'place': ['state']}, text_column_name='text')
    result = geocoder.run(group_column=None)
    
    if result.empty:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Geo not found')
    
    location = str(result.iloc[0]['Location'])
    geometry = result.iloc[0]['geometry']
    geometry = dumps(geometry)
    cur.execute('''
        INSERT INTO nevskiy_db (text, location, geometry)
        VALUES (%s, %s, %s)
        RETURNING id
    ''', (text_ent, location, geometry))
    conn.commit()
    new_item_id = cur.fetchone()[0]
    
    return {'id': new_item_id, 'text': text_ent, 'location': location, 'geometry': geometry}

@app.delete('/delete/items', response_model=ItemResponse)
def delete_items(item_id: int):
    cur.execute('SELECT * FROM nevskiy_db WHERE id = %s', (item_id,))
    row = cur.fetchone()
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')
    
    cur.execute('DELETE FROM nevskiy_db WHERE id = %s', (item_id,))
    conn.commit()
    
    return {'message': f'Item with id {item_id} deleted successfully'}
