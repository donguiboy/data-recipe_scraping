# pylint: disable=missing-docstring,line-too-long
import sys
from os import path
import requests
from bs4 import BeautifulSoup
import csv

def parse(html):
    ''' return a list of dict {name, difficulty, prep_time} '''
    soup = BeautifulSoup(html,"html.parser")
    recipes=[]
    for article in soup.find_all("div",class_="p-2 recipe-details"):
        recipes.append(parse_recipe(article))
    return recipes

def parse_recipe(article):
    ''' return a dict {name, difficulty, prep_time} modelising a recipe'''
    name = article.find("p",class_="recipe-name").string.strip()
    difficulty = article.find("span",class_="recipe-difficulty").string
    prep_time = article.find("span",class_="recipe-cooktime").string
    return {"name": name,"difficulty":difficulty,"prep_time":prep_time}

def write_csv(ingredient, recipes):
    ''' dump recipes to a CSV file `recipes/INGREDIENT.csv` '''
    with open(f'recipes/{ingredient}.csv',"w") as csv_file:
        keys = recipes[0].keys()
        writer = csv.DictWriter(csv_file, fieldnames=keys)
        writer.writeheader()
        writer.writerow(recipes)

SEARCH_URL = "https://recipes.lewagon.com/"
PAGES_TO_SCRAPE = 3
def scrape_from_internet(ingredient, start=1):
    ''' Use `requests` to get the HTML page of search results for given ingredients. '''
    requests.get(SEARCH_URL,params={'search[query]': ingredient, 'page': start})

def scrape_from_file(ingredient):
    file = f"pages/{ingredient}.html"
    if path.exists(file):
        return open(file)
    print("Please, run the following command first:")
    print(f'curl -g "https://recipes.lewagon.com/?search[query]={ingredient}" > pages/{ingredient}.html')
    sys.exit(1)


def main():
    if len(sys.argv) > 2:
        ingredient = sys.argv[1]
        # TODO: Replace scrape_from_file with scrape_from_internet and implement pagination (more than 2 pages needed)
        recipes = parse(scrape_from_internet(ingredient))
        write_csv(ingredient, recipes)
        print(f"Wrote recipes to recipes/{ingredient}.csv")
    else:
        print('Usage: python recipe.py INGREDIENT')
        sys.exit(0)

if __name__ == '__main__':
    main()
