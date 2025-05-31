from flask import Flask, render_template, session, redirect, url_for
from auth import auth

@app.route("/")
def start():
    return "🚗 Schülerakte ist online!"
