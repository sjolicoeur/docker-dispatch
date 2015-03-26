import re

class DockValidator(object):
    def __init__(self, data):
        self.dirty_data = data
        self.clean_data = {}
        self.errors = []
        self.clean()

    def clean(self):
        for key in self.dirty_data.keys():
            func = getattr(self, "clean_"+key, None)
            if func:
                func(self.dirty_data[key])

    def clean_type(self, data):
        if data in ['www', 'wwwp', 'wwws']:
            self.clean_data['type'] = data
        else:
            self.errors.append('Invalid type selected')    

    def clean_port(self, data):
        try:
            result = int(data)
            self.clean_data['port'] = result
        except ValueError:
            self.errors.append("Port is missing or is not an INT")

    def clean_title(self, data):
        try:
            cleaned = re.match(r'^(?P<title>[a-zA-Z0-9|\-]*)$', data)
            if cleaned:
                result = cleaned.groupdict()['title']
                self.clean_data['title'] = result
            else:
                raise ValueError
        except ValueError:
            self.errors.append("title is invalid or unsafe")


    def clean_image_name(self, data):
        # u'sdasd', 
        try:
            cleaned = re.match(r'^(?P<image>[a-zA-Z0-9|\-|\_|\.|/]*)$', data)
            if cleaned:
                result = cleaned.groupdict()['image']
                self.clean_data['image_name'] = result
            else:
                raise ValueError
        except ValueError:
            self.errors.append("image_name is invalid or unsafe")


    def clean_instances(self, data):
        # u'1', 
        try:
            result = int(data)
            if  0 <= result < 10:
                self.clean_data['instances'] = result
            else:
                raise ValueError
        except ValueError:
            self.errors.append("instances is missing or is not an INT or is out of range")

    def clean_tag_name(self, data):
        # u'latest', 
        try:
            cleaned = re.match(r'^(?P<tag>[a-zA-Z0-9|\-|\_|\.]*)$', data)
            if cleaned:
                result = cleaned.groupdict()['tag']
                self.clean_data['tag_name'] = result
            else:
                raise ValueError
        except ValueError:
            self.errors.append("tag_name is invalid or unsafe")


    def clean_memory(self, data):
        # u'16', 
        try:
            result = int(data)
            if  15 < result < 520:
                self.clean_data['memory'] = result
            else:
                raise ValueError
        except ValueError:
            self.errors.append("memory is missing or is not an INT or is out of range")

    def clean_cpu(self, data):
        # u'0.1'
        try:
            result = float(data)
            if  0.0 < result < 11.0:
                self.clean_data['cpu'] = result
            else:
                raise ValueError
        except ValueError:
            self.errors.append("CPU is missing or is not an Float or is out of range")

    def clean_env_vars(self, data):
        try:
            self.clean_data['env_vars'] = []
            for entry in data:
                cleaned_name = re.match(
                    r'^(?P<name>[a-zA-Z0-9|\-|\_]*)$', entry['name'])
                cleaned_value = cleaned = re.match(
                    r'^(?P<value>[a-zA-Z0-9|\-|\_|\.|/]*)$', entry['value'])
                if cleaned_value and cleaned_name:
                    self.clean_data['env_vars'].append([
                            cleaned_name.groupdict()['name'],
                            cleaned_value.groupdict()['value']
                        ])
                else:
                    raise ValueError
        except ValueError:
            self.errors.append('Invalid Data')
    
    def is_valid(self):
        return len(self.errors) == 0


