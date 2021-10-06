#!/usr/bin/env python
# coding: utf-8

# <h2>customers.xlsx</h2>

# In[3]:


#!python --version


import pandas as pd


#Lectura del Data Frame
df =pd.read_csv("C:/Memoria/clientes.csv", sep=';')


#Cambio de nombre a las columnas (sólo a las que aplique) y borrar columnas sobrantes
customers_renombrado = df.rename(columns={'fecha_nacimiento':'birth_date','fecha_vencimiento':'due_date',
                                          'deuda':'due_balance','direccion':'address'})

customers = customers_renombrado.drop(['altura', 'peso', 'correo','estatus_contacto','prioridad','telefono'], axis=1)


#Pasar todos los datos de cada columna a su tipo de dato correcto
customers = customers.astype({'fiscal_id': 'string', 'first_name': 'string', 'last_name': 'string'
                             , 'gender': 'string', 'address': 'string'})

customers['birth_date'] = pd.to_datetime(customers['birth_date'], errors='coerce')
customers['due_date'] = pd.to_datetime(customers['due_date'], errors='coerce')


#customers.dtypes


#Los datos que no existen, limpiarlos y pasar en mayúsculas los strings
customers = customers.fillna({"fiscal_id":"NAN","first_name":"NAN","last_name":"NAN","gender":"NAN"
                                    ,"birth_date":"NaN","due_date":"NaN","due_balance":0,"address":"NAN"})

customers["fiscal_id"] = customers["fiscal_id"].str.upper()
customers["first_name"] = customers["first_name"].str.upper()
customers["last_name"] = customers["last_name"].str.upper()
customers["gender"] = customers["gender"].str.upper()
customers["address"] = customers["address"].str.upper()


#Nueva columna "age"
customers["birth_date"] = pd.to_datetime(customers["birth_date"],format="%Y-%m-%d")
today = pd.datetime.now()
customers["age"] = (today - customers["birth_date"]).dt.days/365
customers = customers.astype({'age': 'int'})


#Nueva columna "age_group"
def age_group(fila):
    x = fila["age"]
    if x <= 20:
        y=1
        return y
    elif x > 20 and x <= 30:
        y=2
        return y
    elif x > 30 and x <= 40:    
        y=3
        return y
    elif x > 40 and x <= 50:    
        y=4
        return y 
    elif x > 50 and x <= 60:    
        y=5
        return y
    else:
        y=6
        return y

customers["age_group"] = customers.apply(age_group, axis=1)


#Nueva columna "delinquency"
customers["due_date"] = pd.to_datetime(customers["due_date"],format="%Y-%m-%d")
today = pd.datetime.now()
customers["delinquency"] = (today - customers["due_date"]).dt.days


#Generación de la tabla customers
customers=customers[["fiscal_id","first_name","last_name","gender","birth_date","age","age_group","due_date",
                     "delinquency","due_balance","address"]]


# <h2>emails.xlsx</h2>

# In[5]:


#Cambio de nombre a las columnas (sólo a las que aplique) y borrar columnas sobrantes
emails_renombrado = df.rename(columns={'correo':'email','estatus_contacto':'status',
                                          'prioridad':'priority'})

emails = emails_renombrado.drop(['first_name', 'last_name', 'gender','fecha_nacimiento','deuda','direccion',
                                'altura','peso','telefono','fecha_vencimiento'], axis=1)


#Pasar todos los datos de cada columna a su tipo de dato correcto
emails = emails.fillna({"priority":0.0}) #no se podía cambiar los datos de la col 'priority' a int porque había datos vacios

emails = emails.astype({'fiscal_id': 'string','email': 'string','status': 'string','priority': 'int'})


#emails.dtypes


#Los datos que no existen, limpiarlos y pasar en mayúsculas los strings
emails = emails.fillna({"fiscal_id":"NAN","email":"NAN","status":"NAN"})

emails["fiscal_id"] = emails["fiscal_id"].str.upper()
emails["email"] = emails["email"].str.upper()
emails["status"] = emails["status"].str.upper()


# <h2>phones.xlsx</h2>

# In[7]:


#Cambio de nombre a las columnas (sólo a las que aplique) y borrar columnas sobrantes
phones_renombrado = df.rename(columns={'telefono':'phone','estatus_contacto':'status',
                                          'prioridad':'priority'})

phones = phones_renombrado.drop(['first_name', 'last_name', 'gender','fecha_nacimiento','fecha_vencimiento','deuda',
                                'altura','peso','correo','direccion'], axis=1)

#Pasar todos los datos de cada columna a su tipo de dato correcto
phones = phones.fillna({"priority":0.0}) #no se podía cambiar los datos de la col 'priority' a int porque había datos vacios

phones = phones.astype({'fiscal_id': 'string','phone': 'string','status': 'string','priority': 'int'})


#phones.dtypes


#Los datos que no existen, limpiarlos y pasar en mayúsculas los strings
phones = phones.fillna({"fiscal_id":"NAN","phone":"NAN","status":"NAN"})

phones["fiscal_id"] = phones["fiscal_id"].str.upper()
phones["phone"] = phones["phone"].str.upper()
phones["status"] = phones["status"].str.upper()



#Generación de la tabla phones
phones=phones[["fiscal_id","phone","status","priority"]]


# <h2>Base de datos sqlitle</h2>

# In[12]:


from sqlalchemy import create_engine
engine = create_engine('sqlite://', echo=False)
customers.to_sql('customers', con=engine)
emails.to_sql('emails', con=engine)
phones.to_sql('phones', con=engine)
customersxlsx = engine.execute("SELECT * FROM customers").fetchall()
emailsxlsx = engine.execute("SELECT * FROM emails").fetchall()
phonesxlsx = engine.execute("SELECT * FROM phones").fetchall()

