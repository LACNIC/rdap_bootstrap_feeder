# rdap_bootstrap_feeder
Set of scripts that provide the RDAP Bootstrap server with up-to-date Internet Number Resources information regarding RIRs and NIRs.

## Tests
```
python tests/tests.py
```

## Configs
The main configuration file is `resources/objects.json`, containing information regarding _where_ to find the resource file, its content's _kind_ of information (AUTNUM | NETWORK), and its _precedence_. Lower precedence means this object will be dropped when encountered with the same object with higher precedence. Lower precedence also means that by encountering a higher-precedence but smaller object, where the smaller object is contained within the bigger object, the smaller object will split the bigger object.
```
{
  "objects": [
    {
      "filename": "resources/rir.asn.json",
      "precedence": 2,
      "kind": "autnum",
      "python_object": {}
    },
    {
      "filename": "resources/nirs.asn.json",
      "precedence": 3,
      "kind": "autnum",
      "python_object": {}
    }
  ]
}
``
## Running the script
```
python get_files.py
```