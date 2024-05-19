output=$(python3 driver.py)
if [ "$output" = "1" ]; then
    python3 csv-getter.py
    jupyter nbconvert --execute --inplace stats.ipynb
    code stats.ipynb
    git add --all
    git commit -m "."
    git push
fi