import os,json

resFolder = os.path.join('res')

def test_json():
    jsonFiles = [f for f in os.listdir(resFolder) if f.rsplit('.',1)[-1] == 'txt']
    print(jsonFiles)
    for j in jsonFiles:
        try:
            with open(os.path.join(resFolder,j)) as r:
                try: 
                    a = json.load(r)
                except json.decoder.JSONDecodeError as err:
                    print(f"Incorrect JSON {err}")
                    a = None
                
                assert isinstance(a,dict)
        except FileNotFoundError as err:
            print(f"file not found: {err}")