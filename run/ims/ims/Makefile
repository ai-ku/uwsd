JAVAC = javac
JAVAFLAGS = -O -d bin -encoding utf-8
CLASSPATH = lib/liblinear-1.33-with-deps.jar:lib/jwnl.jar:lib/commons-logging.jar:lib/jdom.jar:lib/trove.jar:lib/maxent-2.4.0.jar:lib/opennlp-tools-1.3.0.jar:lib/weka-3.2.3.jar:lib/libsvm.jar
all:
	mkdir -p bin
	$(JAVAC) -classpath $(CLASSPATH) $(JAVAFLAGS) src/sg/edu/nus/comp/nlp/ims/*/*.java
	cd bin;	pwd; jar cvf ../ims-`date +%Y-%m-%d`.jar sg; cd ..
	cp ims-`date +%Y-%m-%d`.jar ims.jar
