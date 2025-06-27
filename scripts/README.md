# Startup Script Refactoring

## Overview

The startup script has been decoupled from `compute.tf` to improve maintainability and readability.

## Changes Made

### 1. Created `scripts/startup.sh`

- Extracted the entire startup script from the `compute.tf` file
- Used template variables (e.g., `${APP_PY_CONTENT}`) for dynamic content
- Maintains all original functionality

### 2. Updated `compute.tf`

- Replaced inline script with `templatefile()` function
- Uses `templatefile("${path.module}/scripts/startup.sh", {...})` to render the script
- All necessary variables are passed through the template variables map

## Benefits

### Improved Maintainability

- **Separation of Concerns**: Infrastructure definition (compute.tf) is now separate from deployment logic (startup.sh)
- **Easier Editing**: Startup script can be edited with proper shell syntax highlighting
- **Version Control**: Changes to startup script are easier to track and review
- **Reduced File Size**: compute.tf is now significantly shorter and more focused

### Better Developer Experience

- **Syntax Highlighting**: Shell script gets proper syntax highlighting in editors
- **Debugging**: Easier to test and debug the startup script independently
- **Reusability**: Startup script can potentially be reused in other contexts

## File Structure

```
3-tier-application/
├── compute.tf              # Infrastructure definitions (shorter, cleaner)
├── scripts/
│   └── startup.sh          # Application deployment script
└── app/                    # Application files (unchanged)
    ├── app.py
    ├── requirements.txt
    ├── test_db.py
    └── templates/
        ├── base.html
        ├── index.html
        ├── browse.html
        └── authors.html
```

## Template Variables

The following variables are passed from Terraform to the startup script:

- `APP_PY_CONTENT`: Content of the Flask application
- `TEST_DB_CONTENT`: Database test script content
- `REQUIREMENTS_CONTENT`: Python dependencies
- `BASE_TEMPLATE_CONTENT`: Base HTML template
- `INDEX_TEMPLATE_CONTENT`: Index page template
- `BROWSE_TEMPLATE_CONTENT`: Browse page template
- `AUTHORS_TEMPLATE_CONTENT`: Authors page template
- `CONNECTION_NAME`: Cloud SQL connection string
- `DB_USER`: Database username
- `DB_PASS`: Database password
- `DB_NAME`: Database name

## Usage

No changes to the deployment process are required. Run Terraform commands as usual:

```bash
terraform init
terraform plan
terraform apply
```

The startup script will be automatically rendered with the correct values during the Terraform execution.
