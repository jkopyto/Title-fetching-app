import requests
from bs4 import BeautifulSoup
from flask import Flask, redirect, url_for, render_template


def get_url(num):
    return f"http://www.gornik.tbg.net.pl/news.htm?page={num}"


def fetch_data(num):
    r = requests.get(url=get_url(num), params={})
    soup = BeautifulSoup(r.text, "html.parser")
    headers_list = soup.find_all("span", class_="cont_header")

    return list(map(lambda title: title.get_text(), headers_list))


app = Flask(__name__)


@app.route("/")
def index():
    return redirect(url_for("titles", page_num=1))


@app.route("/titles/<int:page_num>")
def titles(page_num):
    article_titles = fetch_data(page_num)
    return render_template("index.html", len=(len(article_titles)), Titles=article_titles, pg_num=page_num)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("5000"), debug=True)
