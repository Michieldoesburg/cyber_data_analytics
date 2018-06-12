from pandas import datetime

class packet(object):

    def __init__(self, _start_time, _durat, _protocol, _src, _dst, _flags, _tos, _packets, _bytes, _flows, _label):
        self.dateformat = '%Y-%m-%d %H:%M:%S.%f'
        self.start = datetime.strptime(_start_time, self.dateformat)
        self.duration = float(_durat)
        self.protocol = _protocol
        self.src = _src
        self.dst = _dst
        self.flags = _flags
        self.tos = int(_tos)
        self.packets = int(_packets)
        self.bytes = int(_bytes)
        self.flows = int(_flows)
        self.label = _label

    def __str__(self):
        res = '[Packet, start_time = %s, duration = %f, protocol = %s, source = %s, destination = %s, flags = %s, TOS = %i, packets = %i, ' \
              'bytes = %i, flows = %i, label = %s]' % (datetime.strftime(self.start, self.dateformat), self.duration, self.protocol, self.src, self.dst, self.flags,
                                                       self.tos, self.packets, self.bytes, self.flows, self.label)
        return res
