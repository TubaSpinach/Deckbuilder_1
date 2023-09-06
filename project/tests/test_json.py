import os,json

resFolder = os.path.join('project','res')

def test_json():
    jsonFiles = [f for f in os.listdir(resFolder) if f.rsplit('.',1)[-1] == 'txt']

    for j in jsonFiles:
        with open(os.path.join(resFolder,j)) as r:
            try: 
                a = json.load(r)
            except json.decoder.JSONDecodeError as err:
                print(f"Incorrect JSON {err}")
                a = None
            
            assert isinstance(a,dict)