# pyreadr_wheels5
Wheels for Pyreadr based on cibuildwheel

This repo is used to build Python wheels for Pyreadr for 
linux, mac and windows. 

The file controlling the workflow is in .github/workflows/wheels.yml.

The configuration file is cibuildwheel.toml. Scripts special for windows are in the folder scripts.

Wheels for windows are compiled using mingw64 and remediated to grab the necessary dlls. 
Currently dlls are also kept in the pyreadr folder as it is needed for compilation and also
to be able to compile with conda (not used here,but needed for conda packages).

Wheels are uploaded as artifacts to github and also to [anaconda](https://anaconda.org/ofajardo/pyreadr),
where they are publicly available. 

Later wheels are uploaded manually to Pypi. This is to allow anaconda to be a source for testing wheels before releasing. 
