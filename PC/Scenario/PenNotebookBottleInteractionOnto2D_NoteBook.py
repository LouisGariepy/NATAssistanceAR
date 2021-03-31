#!/usr/bin/env python
# coding: utf-8

# # **/!\ Before to read /!\**
# 
# You should read [PenNearNotebookOnto2D.ipynb](PenNearNotebookOnto2D.ipynb) before this one.
# 
# # Ontology diagram
# 
# ![diagram](../Ontology/PenNotebookBottleInteraction.jpg)
# 
# # Loading

# In[1]:


from PenNotebookBottleInteractionOnto2D import PenNotebookBottleInteractionOnto2D

scenario = PenNotebookBottleInteractionOnto2D()
scenario.LoadOnto("../Ontology/PenNotebookBottleInteraction.owl")


# # Use of inheritance and *is_a* property
# 
# By default, a child class own the *is_a* property wich return the list of mother classes.

# In[2]:


class_list = ["Pen", "Notebook", "Bottle"]

for class_name in class_list:
    
    mother_classes = scenario.onto[class_name].is_a
    print(class_name, "inherits from", mother_classes)


# This property is usefull because it helps to define compatibilities between objects. For example, if we want to know if Pen and Notebook are compatible (only first inheritance is compared here) :

# In[3]:


scenario.onto["Pen"].is_a[0] == scenario.onto["Notebook"].is_a[0]


# In[4]:


scenario.onto["Pen"].is_a[0] == scenario.onto["Bottle"].is_a[0]


# # Automatisation of process
# 
# As now we could know from wich classes inherits a class, the goal is to check compatibility for detected objects near each other. To do that here is the new approach :
# 
# ```
# for each detected object inside the ontology
#     for each one of other detected objects inside the ontology
#         if objects are near each other
#             use is_a property to check mother class
#             indicate good compatibility if equals
#             else indicate bad compatibility
# ```
# 
# This is what is implemented in Action method in [PenNotebookBottleInteractionOnto2D.py at line 39](PenNearNotebookOnto2D.py#L39).
# 
