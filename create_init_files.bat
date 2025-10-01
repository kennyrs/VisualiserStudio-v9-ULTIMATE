@echo off
echo Creating __init__.py files...
type nul > models\__init__.py
type nul > views\__init__.py
type nul > views\panels\__init__.py
type nul > elements\__init__.py
type nul > core\__init__.py
type nul > utils\__init__.py
echo Done!
pause