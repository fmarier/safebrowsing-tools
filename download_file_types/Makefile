download_file_types_pb2.py: download_file_types.proto
	protoc -I=. --python_out=. $<

download_file_types.proto:
	curl https://chromium.googlesource.com/chromium/src/+/master/chrome/common/safe_browsing/download_file_types.proto?format=TEXT | base64 --decode > $@

clean:
	rm -f download_file_types_pb2.py
