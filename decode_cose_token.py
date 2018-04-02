#!/usr/bin/env python
import argparse, json, cbor, pprint, datetime

def parseJsonFromFile(input_path):
    with open(input_path, "r") as f:
        data = json.load(f)
    return data

class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)                
                
def coseToCborDict(coseIn):
    cborOut = []
    tmp = cbor.loads(coseIn)
    cborOut.append(cbor.loads(tmp[0]))
    for key in tmp[1]:
        tmp[1][key] = cbor.loads(tmp[1][key])
    cborOut.append(tmp[1])
    
    for key in tmp[2]:
        tmp[2][key] = cbor.loads(tmp[2][key])
    cborOut.append(tmp[2])
    
    return cborOut;
    
class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return super(DatetimeEncoder, obj).default(obj)
        except TypeError:
            return str(obj)

def convertCborToJson(in_file):
    out_file = in_file + ".json"
    jsonIn = parseJsonFromFile(in_file);
    if u'data' in jsonIn:
        base64Item = jsonIn[u'data']
        coseItem = base64Item.decode('base64')
        cborDict = coseToCborDict(coseItem)
        with open(out_file, 'w+') as fo:
            json.dump(cborDict, fo, cls=CJsonEncoder, encoding='latin1', indent=2)
        return
    print("Cannot process invalid data input\n");

def print_cbor(args):
    convertCborToJson(args.input_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="decode T payload as json")
    parser.add_argument('-in', '--input_file',  dest='input_path', help='input file path', required=True)
    args = parser.parse_args()
    print_cbor(args)
