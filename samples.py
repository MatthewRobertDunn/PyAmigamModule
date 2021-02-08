from struct import unpack_from

class Sample:
    def __str__(self):
        return str(self.__dict__)
        
def get_sample(buffer, sample_number):
    print(f"loading sample {sample_number}")
    sample = Sample()
    sample.id = sample_number
    offset = 20 + sample_number * 30
    sample.sample_name = b''.join(unpack_from('s'*22,buffer,offset)).strip(b'\x00')
    offset+=22
    instrument_data = unpack_from('>HBBHH',buffer, offset)
    sample.length = instrument_data[0] * 2 #Sample length in bytes
    sample.fine_tune = instrument_data[1]  #Lower four bits are the finetune value, stored as a signed, TEDIOUS :(
    sample.volume = instrument_data[2]  #Volume for sample 1. Range is $00-$40, or 0-64 decimal.
    sample.repeat_point = instrument_data[3] * 2 #Repeat point for sample . Stored as number of words offset
    assert(sample.repeat_point <= sample.length)
    sample.repeat_length = instrument_data[4] * 2 #Repeat Length for sample. Stored as number of words in loop
    assert(sample.repeat_length == 2 or sample.repeat_length <= sample.length)
    return sample


def get_pcm_data_for_samples(buffer,samples, patterns_count):
    offset = 1084 + (patterns_count * 1024)
    for sample in filter(lambda x: x.length > 0, samples):
        print(f"loading pcm data for sample {sample.id}")
        raw_data = buffer[offset:offset+sample.length]
        sample.pcm_data = [to8bitsigned(x) / 128.0 for x in raw_data]
        assert(len(sample.pcm_data) == sample.length)
        offset = offset + sample.length

def to8bitsigned(byte):
    if byte > 127:
        return (256-byte) * (-1)
    else:
        return byte
