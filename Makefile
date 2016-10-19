run:
	python reason.py && sfdp -x -Tpng -Goverlap=prism stategraph.dot > data.png

clean:
	rm *.png *.dot *.svg
