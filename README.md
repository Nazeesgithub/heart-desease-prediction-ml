Project: Heart disease prediction (Streamlit app + notebooks)

Quick run (from the `app/` folder):


Dataset: https://www.kaggle.com/ (not included)cd "D:\University NIBM\coding 2nd year\NLP\heart disease -2"
git init
git add .
git commit -m "Initial commit - heart disease project (without dataset)"

## Git

This repository should include all project files except the dataset `heart.csv`.

To push this project to GitHub from PowerShell (recommended):

1. Initialize git, add files and commit:

```powershell
cd "D:\\heart disease -2"
git init
git add .
git commit -m "Initial commit - heart disease project (without dataset)"
```

2. Create a GitHub repo and push.

Option A — using GitHub CLI (`gh`):

```powershell
gh repo create <Nazeesgithub>/<repo-name> --public --source=. --remote=origin --push
```

Option B — manually create a repo on GitHub, then add remote and push:

```powershell
git remote add origin https://github.com/<your-github-username>/<repo-name>.git
git branch -M main
git push -u origin main
```


## License / notes

Keep `heart.csv` out of the repo to avoid sharing sensitive data. The trained model files are included under `app/models/` and `notebooks/models/`.

