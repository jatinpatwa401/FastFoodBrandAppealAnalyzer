# For printing
from __future__ import print_function

# For creating a DataFrame in spark
from pyspark.ml import Pipeline

# For Naive Bayes classifier to generate model
from pyspark.ml.classification import NaiveBayes, NaiveBayesModel, LogisticRegression
from pyspark.ml.evaluation import MulticlassClassificationEvaluator, BinaryClassificationEvaluator

# For generating tf-idf for use with Naive Bayes classifier
from pyspark.ml.feature import HashingTF, IDF, Tokenizer, RegexTokenizer, NGram, StringIndexer, IndexToString

# For getting pyspark context
from pyspark import SparkContext
from pyspark.sql import SparkSession

from pyspark.sql.functions import *
import shutil
import sys
import string
import re

sc = SparkSession.builder.appName("sarcasmModel").getOrCreate()
sc.sparkContext.setLogLevel("Error")
dataset = sc.read.csv('./train-balanced-sarcasm.csv', header=False, inferSchema=True)

dataset = dataset.select(col("_c0").alias("original"), col("_c1").alias("text"))
dataset.show(30)

dataset = dataset.where(dataset.text.isNotNull())
dateset = dataset.where(dataset.original.isNotNull())

(trainSet, valSet, testSet) = dataset.randomSplit([0.90, 0.05, 0.05])

#tokenizer = Tokenizer(inputCol="text", outputCol="words")
tokenizer = RegexTokenizer(inputCol="text", outputCol="words", pattern="\\w+", gaps=False)
ngrams = NGram(n=1, inputCol="words", outputCol="ngrams")
hashtf = HashingTF(numFeatures=2**16, inputCol="ngrams", outputCol="tf")
idf = IDF(inputCol="tf", outputCol="features", minDocFreq=5)
labels = StringIndexer(inputCol="original", outputCol = "label")
lines = Pipeline(stages=[tokenizer,ngrams,hashtf,idf,labels])


linesFit = lines.fit(trainSet)
trainModel = linesFit.transform(trainSet)
validationModel = linesFit.transform(valSet)


lr = LogisticRegression(maxIter=100)
model = lr.fit(trainModel)
predictions = model.transform(validationModel)
evaluator = BinaryClassificationEvaluator(rawPredictionCol="rawPrediction")
predictions.show(30)


converter = IndexToString(inputCol="label", outputCol="label meaning")
converted = converter.transform(predictions.select("label").distinct())
converted.select("label", "label meaning").distinct().show()


truePositive = predictions[(predictions.label == 0) & (predictions.prediction == 0)].count()
trueNegative = predictions[(predictions.label == 1) & (predictions.prediction == 1)].count()
falsePositive = predictions[(predictions.label == 1) & (predictions.prediction == 0)].count()
falseNegative = predictions[(predictions.label == 0) & (predictions.prediction == 1)].count()
recall = float(truePositive) / (truePositive + falseNegative)
precision = float(truePositive) / (truePositive + falsePositive)

print("True Positive", truePositive)
print("True Negative", trueNegative)
print("False Positive", falsePositive)
print("False Negative", falseNegative)
print("recall", recall)
print("precision", precision)
print("accuracy", evaluator.evaluate(predictions))


# Save the model
output_directory = "./logisticRegressionSarcasm"
shutil.rmtree(output_directory, ignore_errors=True)
model.save(output_directory)

sc.stop()
