import requests
import pandas as pd
import json
from pandas import json_normalize

#obtengo categorias
url_data ='https://api.mercadolibre.com/sites/MLA/categories'
response = requests.get(url_data)
response.encoding = 'utf-8'
r = response.json()
df_categoria = pd.json_normalize(r)
id_categorias = df_categoria
id_product = df_categoria['id']
name_product = df_categoria['name']

#busco produtos con esos id    
list_item = []
cantidad_productos = []
for id_item in id_product.tolist():
    cantidad_productos = []
    for pagina in range(21):
        offset = str(50 + pagina) 
        response = requests.get("https://api.mercadolibre.com/sites/MLA/search?category=" + id_item + "&limit=50&offset=" + offset)
        response.encoding = 'utf-8'
        r = response.json()['results']
        cantidad_productos.append(r)
    list_item.append(cantidad_productos)


listData = pd.DataFrame()

for i  in range (32):
  for j in range(21):
    listData= listData.append(pd.json_normalize(list_item[i][j]), ignore_index=True)

df_item_list = listData
id_product = df_item_list["id"]

list_item = []
for id_item in id_product.tolist():
    response = requests.get("https://api.mercadolibre.com/items/" + id_item)
    response.encoding = 'utf-8'
    r = response.json()
    list_item.append(r)
   
df_detail_list = pd.json_normalize(list_item)
id_product = df_detail_list["category_id"]
print(len(id_product))

list_item_category = []
list_item_subcategory = []

# obtengo las categorias y subcategorias
for id_item in id_product.tolist():
    response = requests.get("https://api.mercadolibre.com/categories/" + id_item)
    response.encoding = 'utf-8'
    r = response.json()['name']
    list_item_subcategory.append(r)
    r = response.json()['path_from_root'][0]['name']
    list_item_category.append(r)


#construyo el dataset final    
df_subcategory_list = pd.DataFrame({'subcategory':list_item_subcategory})
df_category_list = pd.DataFrame({'category':list_item_category})
df_subcategory_list.head()
print(len(df_category_list))

dataset_meli = pd.concat([df_item_list,df_detail_list], axis=1)
print (len(dataset_meli))

dataset_meli['subcategory'] = df_subcategory_list
dataset_meli['category'] = df_category_list
dataset_meli.insert(0, 'subcategory', dataset_meli.pop("subcategory"))
dataset_meli.insert(0, 'category', dataset_meli.pop("category"))

## Save dataset
dataset_meli.to_csv('dataset_meli.csv', index = False)