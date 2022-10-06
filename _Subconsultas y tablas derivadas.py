#!/usr/bin/env python
# coding: utf-8

# ## Subconsultas y tablas derivadas
# 
# 
# 

# Las subconsultas, también, denominadas consultas internas o consultas anidadas, son consultas que están incrustadas en el contexto de otra consulta. Se pueden utilizar en las cláusulas SELECT, WHERE y FROM. Cuando se usan en cláusulas FROM, se crea lo que se denominan tablas derivadas. Empleamos operadores IN, NOT IN, EXISTS y NOT EXISTS.
# 
# Las subconsultas son útiles, para aislar cada parte lógica de una declaración de consultas largas y complicadas. Se ejecutan más rápido que las uniones y a veces son más legibles que las uniones. Las subconsultas deben estar entre paréntesis y tienen un par de reglas que las uniones no:
# 
# - Las frases ORDER BY no se pueden usar en subconsultas (aunque las frases ORDER BY todavía se pueden usar en consultas externas que contienen subconsultas).
# - Las subconsultas en cláusulas SELECT o WHERE que devuelven más de una fila deben usarse en combinación con operadores que están diseñados explícitamente para manejar múltiples valores, como el operador IN. De lo contrario, las subconsultas en las declaraciones SELECT o WHERE no pueden generar más de 1 fila.
# 

# In[2]:


get_ipython().run_line_magic('load_ext', 'sql')


# In[3]:


get_ipython().run_line_magic('sql', 'mysql://studentuser:studentpw@localhost/dognitiondb')


# In[4]:


get_ipython().run_line_magic('sql', 'USE dognitiondb')


# Uno de los usos principales de las subconsultas es calcular valores a medida que los necesitamos. Esto nos permite utilizar un cálculo de resumen en su consulta sin tener que ingresar el valor generado por el cálculo de forma explícita. Una situación en la que esta capacidad sería útil es si quisiera ver todos los registros que eran mayores que el valor promedio de un subconjunto de sus datos.
# 
# Por ejemplo, escribimos una consulta para ver sólo los datos de las filas cuyas duraciones fueron mayores que el promedio, para poder determinar si hay características que parecen correlacionarse con los perros que tardan más tiempo en terminar sus pruebas. Usamos una subconsulta para calcular la duración promedio y luego indicar en las cláusulas SELECT y WHERE que sólo  recupere las filas cuyas duraciones fueran mayores que el promedio. 

# In[5]:


get_ipython().run_cell_magic('sql', '', 'SELECT *\nFROM exam_answers \nWHERE TIMESTAMPDIFF(minute,start_time,end_time) > (SELECT AVG(TIMESTAMPDIFF(minute,start_time,end_time)) AS AvgDuration\n       FROM exam_answers\n       WHERE TIMESTAMPDIFF(minute,start_time,end_time)>0)\nLIMIT 10;')


# Podemos verificar el resultado de esta consulta, otbeniendo primero el promedio e incorporandolo a la consulta: 

# In[11]:


get_ipython().run_cell_magic('sql', '', 'SELECT AVG(TIMESTAMPDIFF(minute,start_time,end_time)) AS AvgDuration\nFROM exam_answers\nWHERE TIMESTAMPDIFF(minute,start_time,end_time)>0;')


# In[12]:


get_ipython().run_cell_magic('sql', '', 'SELECT *\nFROM exam_answers \nWHERE TIMESTAMPDIFF(minute,start_time,end_time) > 11233.0951\nLIMIT 10;')


# Este ejemplo, muestra cómo las subconsultas le permiten recuperar información de forma dinámica, en lugar de tener que codificar números o nombres específicos. Esta capacidad es particularmente útil cuando se necesita generar el resultado de sus consultas en informes o tableros que se supone que deben mostrar información en tiempo real.

# Las subconsultas también pueden ser útiles para evaluar si los grupos de filas son miembros de otros grupos de filas. Para usarlas en esta capacidad, necesitamos los operadores IN, NOT IN, EXISTS y NOT EXISTS.
# 
# Escribimos una consulta  para seleccionar a todos los usuarios que viven en el estado de Carolina del Norte (abreviado "NC") o Nueva York (abreviado "NY"). Podemos emplear el operador IN en una cláusula WHERE para decir cómo deseamos que los resultados se relacionen con una lista de valores múltiples, que es básicamente una forma condensada de escribir una secuencia de sentencias OR. 
# 
# 
# Observe las comillas alrededor de los miembros de la lista a la que se refiere la instrucción IN. Estas comillas son obligatorias ya que los nombres de los estados son cadenas de texto.

# In[15]:


get_ipython().run_cell_magic('sql', '', "SELECT COUNT(user_guid)\nFROM users\nWHERE state IN ('NC','NY');")


# In[16]:


get_ipython().run_cell_magic('sql', '', "SELECT COUNT(*)\nFROM users\nWHERE state ='NC' OR state ='NY';")


# Una consulta que seleccionaría a todos los usuarios que NO viven en el estado de Carolina del Norte o Nueva York sería:

# In[18]:


get_ipython().run_cell_magic('sql', '', "SELECT COUNT(*) \nFROM users\nWHERE state NOT IN ('NC','NY');")


# EXISTS y NOT EXISTS realizan funciones similares a IN y NOT IN, pero EXISTS y NOT EXISTS solo se pueden usar en subconsultas. La sintaxis de las sentencias EXISTS y NOT EXISTS es un poco diferente a la de las sentencias IN porque EXISTS no va precedida de un nombre de columna ni de ninguna otra expresión. Sin embargo, la diferencia más importante entre las declaraciones EXISTS/NOT EXISTS y IN/NOT IN es que, a diferencia de las declaraciones IN/NOT IN, EXISTS/NOT EXISTS son declaraciones lógicas. En lugar de devolver datos sin procesar, las declaraciones EXISTS/NOT EXISTS devuelven un valor de VERDADERO o FALSO. Como consecuencia práctica, las declaraciones EXISTS a menudo se escriben usando un asterisco después de la cláusula SELECT en lugar de nombres de columna explícitos. El asterisco es más rápido de escribir, y dado que el resultado será un verdadero/falso lógico de cualquier manera, no importa si usa un asterisco o nombres de columna explícitos.
# 
# Recuperamos una lista de todos los usuarios en la tabla de users que también estaban en la tabla de dogs, usamos EXISTS:

# In[7]:


get_ipython().run_cell_magic('sql', '', 'SELECT COUNT(DISTINCT u.user_guid) AS NumbuUserID\nFROM users u\nWHERE EXISTS (SELECT d.user_guid\n              FROM dogs d \n              WHERE u.user_guid =d.user_guid);')


# In[8]:


get_ipython().run_cell_magic('sql', '', 'SELECT COUNT(DISTINCT u.user_guid) AS NumbuUserID\nFROM users u\nWHERE EXISTS (SELECT *\n              FROM dogs d \n              WHERE u.user_guid =d.user_guid);')


# Usamos una cláusula NOT EXISTS para examinar todos los usuarios en la tabla de dogs que no están en la tabla de users.

# In[6]:


get_ipython().run_cell_magic('sql', ' ', 'SELECT d.user_guid AS dUserID, d.dog_guid AS dDogID\nFROM dogs d  \nWHERE NOT EXISTS(SELECT DISTINCT u.user_guid  \n                 FROM users u  \n                 WHERE d.user_guid=u.user_guid);')


# Una tercera situación en la que las subconsultas pueden ser útiles es cuando simplemente representan la lógica de lo que desea mejor que las uniones.

# Esta misma consulta general sin la función COUNT se podría haber utilizado para generar una lista completa de todos los distintos usuarios en la tabla de usuarios, sus perros y la información sobre la raza de sus perros. Sin embargo, el método que usamos para llegar a esto no fue muy bonito o lógicamente satisfactorio. En lugar de unir muchas filas duplicadas y corregir los resultados más tarde con la cláusula GROUP BY, sería mucho más elegante si pudiéramos simplemente unir los distintos ID de usuario en primer lugar. No hay forma de hacer eso con la sintaxis de unión, por sí sola. Sin embargo, puede usar subconsultas en combinación con uniones para lograr este objetivo.
# 
# Para completar la unión SOLO en ID de usuario distintos de la tabla de usuarios, podríamos escribir:

# Queremos obtener la cantidad de usuarios en la tabla de users y en la tabla dogs y los id de los perros asociados.

# In[5]:


get_ipython().run_cell_magic('sql', '', 'SELECT COUNT(u.user_guid) AS NumbuUserID, COUNT(d.user_guid) AS NumbdUserID, COUNT(d.dog_guid) AS NumbdDogID\nFROM users u LEFT JOIN dogs d\n    ON u.user_guid=d.user_guid;')


# Dada la cantidad de filas duplicadas, escribimos una consulta de seguimiento para evaluar cuántas filas se generan por ID_usuario cuando salimos de la tabla de users y empleamos la tabla de dogs:

# In[6]:


get_ipython().run_cell_magic('sql', '', 'SELECT u.user_guid AS uUserID, d.user_guid AS dUserID, count(*) AS numrows\nFROM users u LEFT JOIN dogs d\n   ON u.user_guid=d.user_guid\nGROUP BY u.user_guid\nORDER BY numrows DESC\nLIMIT 5;')

