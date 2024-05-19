output=$(python3 driver.py)
if [ "$output" = "1" ]; then
    python3 csv-getter.py
    jupyter nbconvert --execute --inplace stats.ipynb
    jupyter nbconvert --to html stats.ipynb --output index.html
    code stats.ipynb
    git remote set-url origin https://MBUYt0n:$GITHUB_TOKEN@github.com/MBUYt0n/expense-tracker.git
    git add --all
    git commit -m "."
    git push
fi