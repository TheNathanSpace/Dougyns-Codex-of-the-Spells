cd ..
cd fork

FOR /L %%y IN (1, 1, 73) DO (
    git push -d origin patch-%%y
)

cd ..