# GitHub Pages Setup Instructions

## Quick Setup Steps

1. **Go to Repository Settings**
   - Visit: https://github.com/aculich/pasifika-database/settings

2. **Enable Pages**
   - Click "Pages" in the left sidebar
   - Under "Source", select "GitHub Actions"
   - Save the settings

3. **Check Actions**
   - Go to: https://github.com/aculich/pasifika-database/actions
   - You should see the deployment workflow running

4. **Access Your Site**
   - Once deployed: https://aculich.github.io/pasifika-database/

## Alternative: Manual Pages Setup

If GitHub Actions doesn't work, you can use the legacy Pages setup:

1. Go to Settings > Pages
2. Under "Source", select "Deploy from a branch"
3. Select "main" branch and "/ (root)" folder
4. Click "Save"

## Troubleshooting

- **If you get "Not Found" errors**: Make sure Pages is enabled in repository settings
- **If Actions fail**: Check that the repository has Actions enabled
- **If site doesn't load**: Wait 5-10 minutes for DNS propagation

## Repository Permissions

Make sure your repository has:
- ✅ Pages enabled
- ✅ Actions enabled  
- ✅ Public repository (or GitHub Pro/Team for private repos with Pages)
