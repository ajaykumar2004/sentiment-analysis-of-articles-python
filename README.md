﻿# sentiment-analysis-of-articles-python
Run in virtual env to avoid collision with system library version and required versions


# Step 1: Install virtualenv if not already installed
pip install virtualenv

# Step 2: Create a virtual environment
virtualenv myprojectenv

# Step 3: Activate the virtual environment
# On Windows
myprojectenv\Scripts\activate
# On macOS/Linux
source myprojectenv/bin/activate

# Step 4: Install required libraries
pip install pandas requests beautifulsoup4 nltk syllapy

# Step 5: When done, deactivate the virtual environment
deactivate
