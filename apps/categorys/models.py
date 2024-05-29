from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.utils.text import slugify

class CategoryType(models.Model):
    '''
        Class for the main category_types of the categories
    '''
    name = models.TextField(unique=True)
    def save(self, *args, **kwargs):
        '''
            Saves the category type with its name in lowercase
        '''
        self.name=self.name.lower()
        return super(CategoryType,self).save(*args,**kwargs)
    def __str__(self):
        '''
            Method used for the representation as a string
        '''
        return self.name

class Category(models.Model):
    '''
        Model for the main categories
    '''
    name = models.TextField(unique=True)
    description = models.TextField(default='Null description')
    category_types=models.ManyToManyField(CategoryType)
    slug = models.SlugField(unique=True, max_length=400)
    def save(self, *args, **kwargs):
        '''
            Save method updating or saving fields.
            Doing the right slug
        '''
        self.name=self.name.lower()
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)
    def set_category_types(self,types):
        '''
            Update correctly the category_types for a Category
        '''
        for category_type_name in types:
            category_types=CategoryType.objects.filter(name=category_type_name.lower())
            # category_type_name is being used 
            if len(category_types)!=0:
                category_type=category_types[0]
                # Add the category only when it's not already added
                if not (category_type in self.category_types):
                    self.category_types.add(category_type)
            # Category type unused error returned
            else:
                return False,f'Category type {category_type_name} does not exist'
        self.save()
        return True,'Category saved and types updated successfully'
    def __str__(self):
        '''
            Representation as a string for an instance of Category
        '''
        return self.name