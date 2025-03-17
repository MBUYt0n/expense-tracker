# Expense tracker

A tracker using a flask server to record all expenses and run them in a jupyter notebook for viewing visualisations.

Runs on a docker container hosted on [Render](https://render.com/)

Cant sync a database from Render so if it crashes, my tracked expenses are lost. This is why I had to make the painstaking decision of storing it in a csv. 

I didnt want to build a website, so the easiest way is to run an ipynb and convert to HTML.

/api/input takes input clicking on Done executes the jupyter notebook which generates the HTML file and commits expenses and the changed HTML back to github.

Github workflows hosts the index.html file on github pages. 
