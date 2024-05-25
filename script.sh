output=$(python3 driver.py)
if [ "$output" = "1" ]; then
    cd projects/expense-tracker
    python3 csv-getter.py
    jupyter nbconvert --execute --inplace stats.ipynb
    jupyter nbconvert --to html stats.ipynb --output index.html
    code stats.ipynb
    git add --all
    git commit -m "."
    git remote set-url origin https://MBUYt0n:$GITHUB_TOKEN@github.com/MBUYt0n/expense-tracker.git
    git push
fi