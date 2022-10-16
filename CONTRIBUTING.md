Conventions

Python 3
- Formatting
    - Indentation use 4 space characters
    - Docstring quotation marks are on their own line
    - Type annotation may be dropped if obvious
    - Separate unrelated variable declarations with a line break
    - Separate class and function definitions with 2 line breaks
- Naming
    - Class names are in pascal case
    - Variable and Function names are in snake case
    - Constants are in CAPS
    - Class instance variables must be first declared in `__init__()`
- Punctuation
    - String quotation (single vs double quote) should be scope-consistent
- Import
    - Import order: Builtin module -> External module -> User module
        - Separate each category with a line break

Setting up your repository
1) Fork the repository
2) Add the original main branch as an upstream remote for fetching latest updates  
    `git remote add -t main upstream https://github.com/notBaekjun/tc-validator.git`
3) Keep your main branch up to date  
    `git switch main`  
    `git pull -r upstream`
4) Develop on a separate branch  
    `git branch <mybranch1>`  
    `git switch <mybranch1>`
5) Submit pull request