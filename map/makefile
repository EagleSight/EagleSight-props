
pack:
	gzip -9 -k -f ./**/*.asc

unpack:
	gzip -d -f -k ./**/*.asc.gz

obj:
	python map_maker.py ${map}

objs:
	for dir in `ls -d */` ; do \
        python map_maker.py $$dir ; \
    done

clean:
	rm ./**/*.asc
	rm ./**/*.obj

prepare: decompress_all objs
