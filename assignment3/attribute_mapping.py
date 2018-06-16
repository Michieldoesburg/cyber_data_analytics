class AttMap(object):
    # Implement attribute mapping M_i, i = 0...k as explained in section IV of the paper.
    def __init__(self):
        self.attrmap = dict()
        self.space_size = 0

    def get_space_size(self):
        space_size = 1
        for f in self.attrmap.keys():
            space_size = space_size * len(list(self.attrmap.keys()))
        return space_size

    def add_packet(self, p):
        for f in p.keys():
            x = p[f]
            self.add_attribute(x, f)

    def add_attribute(self, x, feature):
        # If feature not in attribute mapping, make a new map for it.
        if not feature in self.attrmap:
            new_dict = dict()
            new_dict[x] = 0
            self.attrmap[feature] = new_dict
        else:
            # If it is, make a new mapping for it if the value is new.
            feature_dict = self.attrmap[feature]
            if not x in feature_dict:
                mapped_value = len(list(feature_dict.keys()))
                feature_dict[x] = mapped_value
                self.attrmap[feature] = feature_dict

    def encode_full_netflow(self, packets, features):
        # Calculate it now to cache result.
        space_size = self.get_space_size()
        self.space_size = space_size
        results = list()
        for p in packets:
            code = self.encode_netflow(p, features)
            results.append(code)
        return results


    def encode_netflow(self, p, features):
        # define spaceSize
        spaceSize = self.space_size
        code = 0
        for f in features:
            mapping = self.attrmap[f]
            code += (mapping[p[f]] * int(float(spaceSize) / float(len(mapping.keys()))))
            spaceSize = int(float(spaceSize) / float(len(mapping.keys())))
        return code