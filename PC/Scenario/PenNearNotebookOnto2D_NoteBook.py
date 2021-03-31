#!/usr/bin/env python
# coding: utf-8

# # Ontology diagram
# 
# ![diagram](../Ontology/PenNearNotebook.jpg)

# # Loading
# 
# Made in "load" method in [PenNearNotebookOnto2D.py at line 27](PenNearNotebookOnto2D.py#L27).
# 
# ```
# def LoadOnto(self, file):
# 
#     self.onto = owl.get_ontology(file)
#     self.onto.load()
# ```
# 
# For the following demonstrations, a scenario is loaded.

# In[1]:


from PenNearNotebookOnto2D import PenNearNotebookOnto2D

scenario = PenNearNotebookOnto2D()
scenario.LoadOnto("../Ontology/PenNearNotebook.owl")


# After these steps, the onto attributes represent the ontology and classes or objects inside could be called. There is 2 way : attribute or hashmap.

# In[2]:


# attribute way
scenario.onto.Pen


# In[4]:


# hashmap way
scenario.onto["Pen"]


# # Link between object detection and ontology
# 
# As detected objects are identified by a string, classes should be called with hashmap method. Moreover, if requested class is not in the ontology, it returns *None*.
# 
# So, assuming that *detected* is a dict containing detected objects, you could check those belonging to the ontology :

# In[5]:


detected = {
    "Pen" : [0,0],
    "Notebook" : [0,0],
    "Pencil" : [0,0]
}

for object_name, object_position in detected.items():
    
    if scenario.onto[object_name] != None:
        print(object_name, "is in ontology")
    else:
        print(object_name, "is not in ontology")
        


# # Properties
# 
# In the ontology, Pen and Notebook have a property called "nextTo" indicating wich objects could be placed near. A property is readable like an attribute and return an array containing classes.

# In[11]:


scenario.onto["Pen"].nextTo


# In[12]:


scenario.onto["Notebook"].nextTo


# In natural language, these results means :
# 
# * A pen could be next to a notebook
# 
# * A notebook could be next to a pen
# 
# *Note : you could parse the classes you get in arrays using **name** attribute*

# # Automatisation of process
# 
# To summarize what we seen :
# 
# * If a class is requested to an ontology, it is returned otherwise *None* is returned.
# 
# * Properties of classes are like attributes and return array of other classes.
# 
# The goal is to test check if known objects are near each other. For that, here is likely approach :
# 
# ```
# for each detected object
#     if this object is inside the ontology then
#         for each class in property nextTo
#             if this class is inside the ontology
#                 check distance between object and class 
# ```
# 
# This is what is implemented in Action method in [PenNearNotebookOnto2D.py at line 35](PenNearNotebookOnto2D.py#L35).
# 
