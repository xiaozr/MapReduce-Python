from pyspark import SparkContext
import sys

input_path = sys.argv[1]
output_path = sys.argv[2]

sc = SparkContext(appName="WordCountJob")
text = sc.textFile(input_path)
counts = text.flatMap(lambda x: x.split()) \
             .map(lambda word: (word, 1)) \
             .reduceByKey(lambda a, b: a + b)
counts.saveAsTextFile(output_path)
