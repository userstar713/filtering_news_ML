# Startup news scraping and classification

This is the source code of MonkeyLearn's series of posts related to analyzing startup news using machine learning models.

### Code organization

The project itself is a Scrapy project that is used to gather data from different sites like TechCrunch and VentureBeat. Besides, there are a series of Python scripts and Jupyter notebooks that implement other logic like data processing and communication with the MonkeyLearn API.

### [Filtering startup news with Machine Learning](https://blog.monkeylearn.com/filtering-startup-news-machine-learning/)

The TechCrunch, VentureBeat, and Recode spiders (startup_news/spiders) are used to gather data to train a topic classifier in MonkeyLearn. Article title, subtitle (if exists), text, and tags are used as sample text. A subsample of the whole dataset has to be tagged by a human in order to train a model.

To crawl from these sites use
```sh
scrapy crawl techcrunch -o itemsTechCrunch.csv
scrapy crawl venturebeat -o itemsVentureBeat.csv
scrapy crawl recode -o itemsRecode.csv
```
The untagged training set used in the post is available as `training_set.csv`


### [Creating machine learning models to analyze startup news](https://blog.monkeylearn.com/creating-machine-learning-models-to-analyze-startup-news/)

`Try out the events and history classifier.ipynb` is a notebook that does exactly what its name says, both with and without a pipeline. Feel free to try out both versions and see which one performs better.
