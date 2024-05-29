def are_keys_in_dict(dict,*keys):
    '''
        Checks if all the keys are in dict 
    '''
    message='all keys in dict'
    for index,key in enumerate(keys):
        if not key in dict:
            if index==0 or index==len(keys)-1:
                if index==0:
                    message=f'{key}, '
                if index==len(keys)-1:
                    message+=f'and {key} keys are requires'
            else:
                message+=f'{key}, '
    return message=='all keys in dict',message