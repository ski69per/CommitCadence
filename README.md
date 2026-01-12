
# CommitCadence

CommitCadence is a simple tool for creating custom patterns on your GitHub contribution graph. It lets you design pixel-style artwork using a visual grid and apply it to your profile by generating backdated commits.

## Demo

The grid editor allows you to select commit intensity per day and preview how the pattern will appear on your GitHub contribution calendar.

![CommitCadence Demo](docs/demo.gif)

![CommitCadence Grid Reference](docs/grid.png)

## Features

- Visual grid editor matching GitHub's contribution calendar
- Adjustable commit intensity (0–4 commits per day)
- Automated setup and commit generation
- Works with new or existing repositories

## Requirements

- Java (JRE 8+)
- Git
- Bash shell
- GitHub account with a verified email

## Quick Start

```bash
git clone https://github.com/ski69per/CommitCadence.git
cd CommitCadence

# For Mac/Linux users:
bash automate.sh

# For Windows users (or if you prefer Python):
python automate.py
```

Follow the prompts to enter your GitHub email, repository details, and a Sunday start date. Design your pattern in the grid editor and let the script handle the rest.

## Important

**Email Verification:** The email you enter must be verified in your GitHub account settings at https://github.com/settings/emails. Commits will only appear on YOUR contribution graph if the email matches YOUR GitHub account.

## Notes

- Start dates must be Sundays to align with GitHub's calendar
- Contributions appear on your public profile
- Remove the design by deleting or privatizing the repository
- Each person should use their own verified GitHub email to see commits on their profile
