# Documentation Cleanup Plan

## Identified Issues

After reviewing the current documentation, we've identified several issues:

1. **Redundant Files**: Multiple files covering the same components with duplicated content
2. **Inconsistent Table Formatting**: File inventory tables aren't consistently formatted
3. **Navigation Challenges**: Limited ability to quickly navigate within large documentation files
4. **Content Organization**: Difficulty finding specific information within documentation

## Implemented Solutions

We've implemented the following improvements:

1. **Navigation Menu**: Added a horizontal navigation menu to jump directly to sections
2. **Collapsible Sections**: Created collapsible sections for better content organization
3. **Template System**: Established a consistent documentation template with proper formatting
4. **Proper Table Formatting**: Fixed Markdown table formatting for better readability

## Files to Consolidate

The following redundant files should be removed once their content is consolidated into the main module documentation:

| Remove | Consolidate Into |
|--------|------------------|
| src-web-files.md | src-web.md |
| src-software-files.md | src-software.md |
| src-config-files.md | src-config.md |
| src-power-files.md | src-power.md |
| src-web-middleware-files.md | src-web-middleware.md |
| src-web-static-css.md + src-web-static-js.md | src-web-static.md |
| root-files.md | root.md |
| deployment-files.md | deployment.md |

## Implementation Steps

1. For each module documentation file:
   - Apply the template structure from `templates/document-template.md`
   - Ensure proper Markdown table formatting
   - Include the navigation menu with `{% include navigation.html %}`
   - Add collapsible sections using the `<details>` element
   - Cross-reference related modules

2. For each redundant "*-files.md" file:
   - Move any unique content to the corresponding main module documentation
   - Once verified, remove the redundant file

3. Update all internal links:
   - Ensure all documentation cross-references point to the correct files
   - Add anchor links to specific sections (e.g., `#file-inventory`)

## Example Implementation

We've implemented the new format for `src-web.md` as a demonstration. This file now features:

- A clear overview section
- Collapsible detailed sections
- Proper table formatting
- A horizontal navigation menu
- Cross-references to related modules

## Technical Details

### Navigation Menu

The navigation menu is implemented in `_includes/navigation.html` and can be included at the top of each documentation file:

```
{% include navigation.html %}
```

### Collapsible Sections

Collapsible sections use HTML `<details>` and `<summary>` tags:

```html
<details id="section-id">
<summary><h2>Section Title</h2></summary>
<div markdown="1">
Content goes here...
</div>
</details>
```

### Proper Table Formatting

Use this Markdown format for tables:

```markdown
| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Cell 1   | Cell 2   | Cell 3   |
| Cell 4   | Cell 5   | Cell 6   |
```

## Benefits of the New Structure

1. **Reduced Redundancy**: Eliminates duplicated content across multiple files
2. **Improved Navigation**: Makes it easier to find specific information
3. **Better Organization**: Groups related information logically
4. **Consistent Formatting**: Ensures a uniform look and feel across all documentation
5. **Focused Viewing**: Allows users to focus on just the sections they need

## Next Steps

1. Apply the new template to all module documentation files
2. Remove redundant files once content is consolidated
3. Update the README.md with the complete navigation structure
4. Verify all cross-references and links
