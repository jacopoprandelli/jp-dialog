from flask import render_template, request, redirect, url_for, session, make_response, flash
from .forms import *
from . import app

from config import Config
from .utils.logger import get_logger

logger = get_logger(__name__)



@app.route('/')
def index():
    return render_template('index.html')