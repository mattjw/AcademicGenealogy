# AcademicGenealogy

Please visit [this blog post](http://www.mattjw.net/2014/01/academic-genealogy/) for more 
information.

Walkthrough for the Alan Turing example:

1. Generate the dot file: `python genealogy_miner.py config_turing.py turing.dot`
2. Use GraphViz to do a rough rendering to PNG: `dot -T png turing.dot > turing.png`
3. Import the dot file into graphic design software; e.g., OmniGraffle.


### Dependencies

Python packages:

* networkx  
Required by .


System packages:

* graphviz  
Optional. Used for rendering dot files.


### Author
By Matt Williams. Website: http://www.mattjw.net/

### Acknowledgements
David Alber's Geneagrapher: http://www.davidalber.net/geneagrapher/