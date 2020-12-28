cd ..
cd fork
git checkout tasha-updated
git push --set-upstream origin tasha-updated

FOR /L %%y IN (59, 1, 73) DO (
	git pull origin patch-%%y
	git commit -m "Merge patch-%%y"
	git push
)

cd ..