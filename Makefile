pdf:
	python reason.py && sfdp -x -Tpdf -Goverlap=prism stategraph.dot > stategraph.pdf && echo "Plot: stategraph.pdf"
run:
	python reason.py && sfdp -x -Tpng -Goverlap=prism stategraph.dot > stategraph.png && echo "Plot: stategraph.png"

clean:
	rm *.png *.dot *.svg
