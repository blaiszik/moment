#! /bin/bash

# Run the extractions
echo 'Running Extract'
cd extract
sh ./run_extract.sh
cd ..

# Run the render
echo 'Running Render'
cd render
sh ./run_render.sh
cp index.html ../
cd ..
