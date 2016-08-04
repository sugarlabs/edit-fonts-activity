Sugar Edit Fonts Contributing Guidelines
========================================

To develop the Activity, your changes must conform to the [PEP8 style guide](https://www.python.org/dev/peps/pep-0008/). 
We use Travis CI to enforce this; the following command is run on every pull request and it must run without outputting any errors:

    flake8 --statistics  --ignore=E402 --exclude=defcon,\
    extractor,fontTools,fontmake,robofab,ufo2ft,ufoLib,\
    snippets,docs,compreffor,booleanOperations .

The `--statistics` argument prints a list at the end showing the total count of each error category at the end. 

To eliminate all errors, it is helpful to see the total number of errors for each file:

    flake8 --ignore=E402 \
    --exclude=defcon,extractor,fontTools,fontmake,robofab,\
    ufo2ft,ufoLib,snippets,localIcon  . \
    | cut -d: -f1 | sort | uniq -c | sort;

To eliminate a specific error, it is helpful to filter the output using grep:

    flake8 --ignore=E402 \
    --exclude=defcon,extractor,fontTools,fontmake,robofab,\
    ufo2ft,ufoLib,snippets,localIcon  . \
    | grep W291; # trailing whitespace

The [autopep8](https://pypi.python.org/pypi/autopep8) tool can be used to automatically format code to comply with this standard.
