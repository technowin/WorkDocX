import json

class GenericObject(dict):
    """
    A dict subclass that provides access to its members as if they were
    attributes.
    Note that an attribute that has the same name as one of dict's existing
    method (``keys``, ``items``, etc.) will not be accessible as an attribute.
    """
    @classmethod
    def from_json(cls, json_string):
        """
        Parses the given json_string, returning GenericObject instances instead
        of dicts.
        """
        return json.loads(json_string, object_hook=cls)

    def __setattr__(self, prop, val):
        if prop[0] == '_' or prop in self.__dict__:
            return super(GenericObject, self).__setattr__(prop, val)
        else:
            self[prop] = val

    def __getattr__(self, prop):
        """
        Provides access to the members of the dict as attributes.
        """
        if prop in self:
            return self[prop]
        else:
            raise AttributeError
    
    def __delitem__(self, prop):
        # on delete, setting value to None
        if prop in self:
            self[prop] = None
    '''
    def __repr__(self):
        ident_parts = [type(self).__name__]
        if isinstance(self, dict):
            ident_parts.append('id=%s' % (self.get('id'),))
        elif isinstance(self.get('id'), dict):
            sid = self.get('id').get('id')
            ident_parts.append('id=%s' % (sid,))
        elif isinstance(self.get('id'), basestring):
            ident_parts.append('id=%s' % (self.get('id'),))
        unicode_repr = '<%s at %s> : %s' % (
            ' '.join(ident_parts), hex(id(self)), str(self))
        if sys.version_info[0] < 3:
            return unicode_repr.encode('utf-8')
        else:
            return unicode_repr
    '''
    def __str__(self):
        if isinstance(self.get('id'), dict):
            self = self.get('id')
        data = self.copy()
        return json.dumps(data, sort_keys=True, indent=2)

def list_of_dict_to_list_to_obj(list_of_dict):
    list_of_obj = []
    for data in list_of_dict:
        list_of_obj.append(GenericObject(data))
    return list_of_obj

def make_chuncks_of_number_of_elements(element_per_chunk, data_list):
    return [data_list[i:i + element_per_chunk] for i in range(0, len(data_list), element_per_chunk)]