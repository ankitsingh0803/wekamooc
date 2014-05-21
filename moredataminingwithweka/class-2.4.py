# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# More Data Mining with Weka - Class 2.4
# Copyright (C) 2014 Fracpete (fracpete at gmail dot com)

# TODO
# wherever your datasets are located
data_dir = "/some/where/data"

import os
import weka.core.jvm as jvm
from weka.core.converters import Loader
from weka.classifiers import Classifier, FilteredClassifier, Evaluation, PredictionOutput
from weka.filters import Filter
import weka.plot.graph as plg

jvm.start()

# load simpletext-train
fname = data_dir + os.sep + "simpletext-train.arff"
print("\nLoading dataset: " + fname + "\n")
loader = Loader(classname="weka.core.converters.ArffLoader")
data = loader.load_file(fname)
data.set_class_index(data.num_attributes() - 1)

# 1a filter data
print("Filtering data...")
fltr = Filter("weka.filters.unsupervised.attribute.StringToWordVector")
fltr.set_inputformat(data)
filtered = fltr.filter(data)
filtered.set_class_index(0)

# 1b build classifier
print("Building/evaluating classifier...")
cls = Classifier(classname="weka.classifiers.trees.J48")
cls.build_classifier(filtered)
evl = Evaluation(filtered)
evl.test_model(cls, filtered)
print(evl.to_summary())
print(str(cls))
plg.plot_dot_graph(cls.graph())

# 2. filtered classifier
fname = data_dir + os.sep + "simpletext-test.arff"
print("\nLoading dataset: " + fname + "\n")
loader = Loader(classname="weka.core.converters.ArffLoader")
test = loader.load_file(fname)
test.set_class_index(test.num_attributes() - 1)
print("Building/evaluating filtered classifier...")
cls = FilteredClassifier()
cls.set_classifier(Classifier(classname="weka.classifiers.trees.J48"))
cls.set_filter(Filter(classname="weka.filters.unsupervised.attribute.StringToWordVector"))
cls.build_classifier(data)
pout = PredictionOutput(classname="weka.classifiers.evaluation.output.prediction.PlainText")
pout.set_header(test)
evl = Evaluation(data)
evl.test_model(cls, test, pout)
print(str(pout))
print(str(cls))

# load ReutersCorn-train
fname = data_dir + os.sep + "ReutersCorn-train.arff"
print("\nLoading dataset: " + fname + "\n")
loader = Loader(classname="weka.core.converters.ArffLoader")
data = loader.load_file(fname)
data.set_class_index(data.num_attributes() - 1)

# load ReutersCorn-test
fname = data_dir + os.sep + "ReutersCorn-test.arff"
print("\nLoading dataset: " + fname + "\n")
loader = Loader(classname="weka.core.converters.ArffLoader")
test = loader.load_file(fname)
test.set_class_index(test.num_attributes() - 1)

# build/evaluate classifier
cls = FilteredClassifier()
cls.set_classifier(Classifier(classname="weka.classifiers.trees.J48"))
cls.set_filter(Filter(classname="weka.filters.unsupervised.attribute.StringToWordVector"))
cls.build_classifier(data)
evl = Evaluation(data)
evl.test_model(cls, test)
print(evl.to_summary())
print(str(cls))

jvm.stop()