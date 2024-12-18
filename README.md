# SpTRSV Tester

A general script for testing sptrsv.

## What should we do before run it?

Just modify the `config.ini`!

## How to run it?

Just run:

```bash
python run_all.py
```

You will get the result from folder `YYYY-MM-DD`.

## How to add and modify test cases?

1. You can add your custom test cases in `run_config.py`. Add the class which should have:

```python
class ClassName:
    def get_run_command(self, matrix_path):
        # Execute command of program
        return "./bin/tilesptrsv -d $CUDA_VISIBLE_DEVICES " + matrix_path
    def get_extract_re(self):
        # RE for extract the time
        return [r'CUDA TileSpTRSV runtime\s*([\d.]+)\sms', r'YYRuntime: \s*([\d.]+)\sms']
    def get_name(self):
        # Output of the name of result
        return ["TileSpTRSV", "YYSpTRSV"]
```

Note: You can get multiple results by add regular expressions and name to the list.

2. You can change the test cases order or enables in `run_all.py`:

```python
  projects = [rc.MixSpTRSVWithGraph(), rc.MixSpTRSVWithLevelSet()]
```
