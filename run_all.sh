#! /bin/bash

# Run the extractions
cd extract
sh ./run_extract.sh
cd ..

# Run the render
cd render
sh ./run_render.sh
cp index.html ../
cd ..
