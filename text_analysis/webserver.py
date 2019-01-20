import sys

from flask import Flask, render_template, request, redirect, Response
import random, json
import text_analysis

app = Flask(__name__)

#Sets up a path (page of website)
@app.route("/")
def output():
    text_analysis.main()
    return "complete"

if __name__ == "__main__":
    app.run()

