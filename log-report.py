#!/usr/bin/env python3
import psycopg2

DBNAME = "news"

# query strings

popular_articles_query = """
    select title,count(title) as article_views
    from articles,log
    where log.path = concat('/article/',articles.slug)
    group by articles.title
    order by article_views desc
    limit 3 ;
    """
popular_authors_query = """
    select authors.name , count(author) as author_views
    from articles , log , authors
    where log.path = concat('/article/',articles.slug)
    and articles.author = authors.id
    group by authors.name
    order by author_views desc;
    """
error_perentage_query = """
    select * from errors_percentage
    where  E_percentage > 1 ;
    """

# fuunction to execute "select" queries


def get_results(query):
    db = psycopg2.connect(database=DBNAME)
    conn = db.cursor()
    conn.execute(query)
    result = conn.fetchall()
    db.close()
    return result

# functions to print each query


def print_popular_articles(results):
    print("\n")
    print("1- The three most popular articles of all time are:\n")
    for i in range(len(results)):
        title = results[i][0]
        article_views = results[i][1]
        print("article :   " + "%s has %d" % (title, article_views) + " views")
    print("\n")


def print_popular_authors(results):
    print("\n")
    print("2- The most popular authors of all time are:\n")
    for i in range(len(results)):
        name = results[i][0]
        article_views = results[i][1]
        print("author :   " + "%s has %d" % (name, article_views) + " views")
    print("\n")


def print_error_perentage(results):
    print("3- days which have more than 1" + "%" +
          " of requests lead to errors are:\n")
    for i in range(len(results)):
        daylog = results[i][0]
        E_perentage = str(results[i][1])
        print("the day of :  " + "%s has error perentage of %s" %
              (daylog, E_perentage) + "%")
    print("\n")

# Execute queries


popular_articles = get_results(popular_articles_query)
popular_authors = get_results(popular_authors_query)
error_rate = get_results(error_perentage_query)

# print result

print_popular_articles(popular_articles)
print_popular_authors(popular_authors)
print_error_perentage(error_rate)
