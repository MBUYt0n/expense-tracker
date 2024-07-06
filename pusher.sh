export GITHUB_TOKEN=$(cat /home/shusrith/key.txt)
git remote set-url origin https://MBUYt0n:$GITHUB_TOKEN@github.com/MBUYt0n/expense-tracker.git
git push