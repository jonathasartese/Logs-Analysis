#!/usr/bin/env python3

import psycopg2

DBNAME = "news"

def execute_query(query):

    conn = psycopg2.connect(dbname=DBNAME)
    cursor = conn.cursor()
    print("\n Connected!\n")
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

def question1():
    query = "SELECT articles.title, COUNT(*) AS num "\
            "FROM articles "\
            "INNER JOIN log ON log.path like CONCAT('%', articles.slug) "\
            "GROUP BY articles.title ORDER BY num DESC limit 3;" 
    results =execute_query(query);
    
    print('The most popular articles of all time are:')
    for result in results:
        print("   ", result[0] ," - ", result[1], " views ")

def question2():
    query = "SELECT authors.name, COUNT(*) AS num "\
            "FROM articles "\
            "INNER JOIN authors ON authors.id = articles.author "\
            "INNER JOIN log ON log.path like CONCAT('%', articles.slug) "\
            "GROUP BY authors.name ORDER BY num DESC;"
    results =execute_query(query);
    
    print('The most popular article authors of all time are')
    for result in results:
        print("   ", result[0] ," - ", result[1], " views ")

def question3():
    query = "SELECT * FROM "\
            "(SELECT date(time), round(100.0*sum(case log.status WHEN '200 OK' THEN 0 ELSE 1 END)/count(log.status), 2) "\
            "as error FROM log GROUP BY date(time) ORDER BY error DESC) as subq where error > 1;"
    results =execute_query(query);
    
    print('On which days did more than 1% of requests lead to errors?')
    for result in results:
        print("   ", result[0] ," - ", result[1], "% errors ")


if __name__ == "__main__":
    question1();
    question2();
    question3();

