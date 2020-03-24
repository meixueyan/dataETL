import pandas as pd
import datetime
from flaskr import utilities
import numpy as np
import json
from flask_bootstrap import Bootstrap
from flask import *
from flask_apscheduler import APScheduler


app = Flask(__name__)
Bootstrap(app)


def method_test():
    print("The binary is runnung at:%s" % (datetime.datetime.now()))


@app.route("/",methods=['GET','POST'])
def show_tables():
    search_keywords = request.form.get('keywords','Rate')
    df_trends = utilities.getGoogleTrends(search_keywords)
    trends_snapshot = utilities.showSnapshot(df_trends)
    try:
        data_news= utilities.getNewsKeyword(search_keywords)
        df_news = utilities.getSnapshot(data_news)
        
        trendsData = np.squeeze(df_trends.values[1:])
        trendsTime = df_trends.index[1:]
        return render_template('view.html',tables=[df_news.to_html(classes='news'), trends_snapshot.to_html(classes='trends')],
        titles = ['na', 'Top News', 'Google Trends'], trendsData =json.dumps(trendsData.tolist()),
        trendsTime = json.dumps(trendsTime.tolist()))
    except:
        return redirect(url_for('show_tables'))

#Another potential way:
#     except Exception as e:
#         return str(e)


@app.route("/trends",methods=['GET','POST'])
def show_trends():
    search_keywords = request.form.get('keywords','Trump')
    df_trends = utilities.getGoogleTrends(search_keywords)
    trendsData = np.squeeze(df_trends.values[1:])
    trendsTime = df_trends.index[1:]
    return render_template('view.html', trendsData =json.dumps(trendsData.tolist()),
    trendsTime = json.dumps(trendsTime.tolist()))

if __name__ == "__main__":
    print(__name__)
    scheduler=APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    app.run(debug=True, host='0.0.0.0', port=5000)


