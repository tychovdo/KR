pdf:
	python gen_graph.py && sfdp -x -Tpdf -Goverlap=prism stategraph.dot > stategraph.pdf && echo "Plot:             stategraph.pdf"
run:
	python gen_graph.py && sfdp -x -Tpng -Goverlap=prism stategraph.dot > stategraph.png && echo "Plot:             stategraph.png"

clean:
	rm -rf *.png *.dot *.svg *.pdf
